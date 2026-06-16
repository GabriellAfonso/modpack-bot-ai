"""Orchestrates a player message into a final answer string.

This is the heart of the runtime. Deterministic gates run first for precision
at zero Groq tokens (admins -> Pokémon card -> facts), and semantic retrieval
(RAG) is the general fallback (plan.md §4). It returns plain text, so the
Discord layer only has to reply with it and the whole flow is testable end to
end with fakes (no Discord, no Groq, no embedding model).
"""

import functools
from collections.abc import Callable

from card_builder.card import NO_NATURAL_SPAWN

from modpack_bot.admins import AdminResolver, admins_message
from modpack_bot.conversation import ConversationStore, Turn
from modpack_bot.facts_index import facts_counts_header, matched_facts_lines
from modpack_bot.guides import CardRepository, GuideRepository
from modpack_bot.intent import detect_language, looks_like_followup
from modpack_bot.llm import ANSWER_MODELS, CONDENSE_MODELS, ModelCompleter
from modpack_bot.pokemon_filter import build_pokemon_filter, filter_tool_spec, make_dispatch
from modpack_bot.prompts import (
    build_system_prompt,
    claim_instruction,
    condense_system_prompt,
    facts_filter_instruction,
    facts_listing_message,
    fallback_message,
    pokemon_instruction,
    pokemon_obtain_instruction,
    spawn_help_message,
    usage_suffix,
)
from modpack_bot.retrieval import ContextRetriever
from modpack_bot.routing import Route, classify_route
from modpack_bot.text import collapse_blank_lines, wants_full_list

_FACTS_GUIDE = "facts.md"

# Flan land-protection docs injected verbatim by the claim gate instead of going
# through RAG: multilingual-e5 ranks them below generic FAQ/rules chunks for
# player phrasing ("como impedir de roubarem meu baú?"), so they never reach the
# top-k and the question falls to the fallback. Curated subset (5 of 14 files) to
# keep the prompt well under Groq's TPM/413 ceiling — the deep-dive docs
# (permissoes, subclaims, 3d, menus, comandos) are left to RAG.
_CLAIM_GUIDES = [
    "Flan/visao-geral.md",
    "Flan/ferramentas-de-claim.md",
    "Flan/como-criar-e-gerenciar-claims.md",
    "Flan/blocos-de-claim.md",
    "Flan/grupos-e-jogadores.md",
]

# Each remembered answer is truncated to this many characters when fed back into
# the condense step — enough to resolve references, cheap on tokens.
_CONDENSE_ANSWER_CAP = 300

# How many passages each obtain-path query contributes after merging. Keeps the
# summon ritual (mechanic query) on top while guaranteeing the structure/location
# passage (location query) is included, without doubling the passage count.
_OBTAIN_MECHANIC_K = 4
_OBTAIN_LOCATION_K = 3


class Responder:
    """Turns a message into the text the player should receive."""

    def __init__(
        self,
        retriever: ContextRetriever,
        completer: ModelCompleter,
        guides: GuideRepository,
        cards: CardRepository,
        admins: AdminResolver | None = None,
        show_usage: bool = False,
        conversations: ConversationStore | None = None,
    ) -> None:
        self._retriever = retriever
        self._completer = completer
        self._guides = guides
        self._cards = cards
        self._admins = admins
        self._show_usage = show_usage
        self._conversations = conversations
        self._pokemon_names = cards.pokemon_names()

    def set_show_usage(self, enabled: bool) -> None:
        """Toggle the per-message token-cost footer at runtime (the !token command)."""
        self._show_usage = enabled

    def answer(self, message: str, session_key: str | None = None) -> str:
        """Full pipeline; returns the player-facing text (or the fallback).

        When a session_key is given and the store holds prior turns, the message
        is first condensed into a standalone question so follow-ups ("e onde ele
        spawna?") reach the right gate. The exchange is then remembered for the
        next turn. Without a key (or store) the bot is fully stateless, as before.

        Token usage is reset up front and read at the end so the optional footer
        reflects every model call this one message made (condense + answer + tools).
        """
        self._completer.reset_usage()
        resolved = self._resolve_followup(message, session_key)
        answer = self._gate_and_answer(resolved)
        self._remember(session_key, message, answer)
        return self._with_usage(answer)

    def _resolve_followup(self, message: str, session_key: str | None) -> str:
        """Rewrite a follow-up into a standalone question using recent turns.

        Returns the message untouched on the first turn (no history), when no
        session is tracked, or when the message already stands on its own
        (looks_like_followup is False) — so a fresh question never pays for a
        condense call nor risks the model narrowing it against the last answer.
        """
        if self._conversations is None or session_key is None:
            return message
        history = self._conversations.history(session_key)
        if not history or not looks_like_followup(message):
            return message
        return self._condense(message, history)

    def _condense(self, message: str, history: list[Turn]) -> str:
        """One cheap model call that resolves references; falls back to the raw
        message if the model returns nothing usable."""
        transcript = _format_transcript(history)
        resolved = self._completer.complete(
            messages=[
                {"role": "system", "content": condense_system_prompt(transcript, detect_language(message))},
                {"role": "user", "content": message},
            ],
            models=CONDENSE_MODELS,
            max_tokens=120,
            temperature=0.0,
        )
        return resolved.strip() or message

    def _remember(self, session_key: str | None, question: str, answer: str) -> None:
        """Store the original question and the answer for follow-up resolution."""
        if self._conversations is None or session_key is None:
            return
        self._conversations.record(session_key, Turn(question, answer))

    def _gate_and_answer(self, message: str) -> str:
        """Route the message to a gate (pure, 0 tokens), then build that answer.

        Routing lives in routing.classify_route so it can be evaluated in
        isolation (eval/); the order rationale (claim before admins so "mas e o
        mod flan?" dodges the bare-"mod" match; spawn-help before RAG so a
        nameless spawn question dodges the gacha docs) is documented there and in
        the intent predicates.
        """
        language = detect_language(message)
        load_facts = self._facts_loader()  # read at most once, only if a gate needs it
        decision = classify_route(message, self._pokemon_names, load_facts)
        if decision.route is Route.CLAIM:
            return self._answer_claim(message, language)
        if decision.route is Route.ADMINS:
            return self._answer_admins(language)
        if decision.route is Route.POKEMON:
            assert decision.pokemon is not None  # set whenever route is POKEMON
            return self._answer_pokemon(message, decision.pokemon, language)
        if decision.route is Route.SPAWN_HELP:
            return spawn_help_message(language)
        if decision.route is Route.FACTS:
            return self._answer_facts(message, load_facts(), language)
        return self._answer_from_rag(message, language)

    def _facts_loader(self) -> Callable[[], str]:
        """A memoizing thunk for facts.md: keeps the disk read off the claim/
        admins/Pokémon paths (which never reach the facts gate), yet reuses the
        text across the classify + answer calls on the facts path itself."""
        return functools.cache(lambda: self._guides.load_guide(_FACTS_GUIDE))

    def _with_usage(self, text: str) -> str:
        """Append the token-cost footer when the runtime enabled it."""
        if not self._show_usage:
            return text
        return text + usage_suffix(self._completer.usage)

    def _answer_pokemon(self, message: str, pokemon: str, language: str) -> str:
        """Inject the detected Pokémon's card and answer (the wiki gate, §4.2).

        Falls back to RAG only if the card vanished from disk — detect_pokemon
        already guarantees the name exists in the card set. When the card has no
        natural spawn, the answer is augmented with RAG so a mod-based summon
        method (e.g. Legendary Monuments pedestals) can surface.
        """
        card = self._cards.load_card(pokemon, wants_full_list(message))
        if card is None:
            return self._answer_from_rag(message, language)
        if NO_NATURAL_SPAWN in card:
            return self._answer_pokemon_obtain(message, pokemon, card, language)
        return self._answer_from_guide(message, card, pokemon_instruction(pokemon, language), language)

    def _answer_pokemon_obtain(
        self, message: str, pokemon: str, card: str, language: str
    ) -> str:
        """No-natural-spawn card: append RAG passages so the summon/obtain method
        (which lives in the mod docs, not the card) reaches the answer model."""
        passages = self._retrieve_obtain_passages(message, pokemon)
        guide = "\n\n".join([card, *passages]) if passages else card
        return self._answer_from_guide(
            message, guide, pokemon_obtain_instruction(pokemon, language), language
        )

    def _retrieve_obtain_passages(self, message: str, pokemon: str) -> list[str]:
        """Summon-mechanic passages PLUS the structure-location passage.

        The player's phrasing ("como acho um zekrom?") retrieves the summon ritual
        but never the Arc Phone / monument passage that names WHERE the pedestals
        are — it is worded differently, so it stays out of the top-k and the
        answer can't name the structure (the recurring zekrom complaint). A second
        query seeded with location terms surfaces it; the two lists are merged and
        de-duped, capped to stay under Groq's TPM ceiling.
        """
        mechanic = self._retriever.retrieve(message)
        location = self._retriever.retrieve(_obtain_location_query(pokemon))
        return _merge_passages(mechanic, location)

    def _answer_claim(self, message: str, language: str) -> str:
        """Answer land/chest-protection questions from the curated Flan guide,
        bypassing RAG (which can't surface these docs for player phrasing, §4.4)."""
        guide = self._guides.load_guides(_CLAIM_GUIDES)
        return self._answer_from_guide(message, guide, claim_instruction(language), language)

    def _answer_from_rag(self, message: str, language: str) -> str:
        """Fallback: retrieve top-k passages locally and answer from them, or the
        fallback message when nothing relevant is found (§4.4)."""
        passages = self._retriever.retrieve(message)
        if not passages:
            return fallback_message(language)
        return self._answer_from_guide(message, "\n\n".join(passages), "", language)

    def _answer_from_guide(
        self, message: str, guide: str, instruction: str, language: str
    ) -> str:
        """Plain answer-model call over a context blob (card / RAG passages)."""
        answer = self._completer.complete(
            messages=[
                {"role": "system", "content": build_system_prompt(guide, instruction, language)},
                {"role": "user", "content": message},
            ],
            models=ANSWER_MODELS,
            max_tokens=500,
            temperature=0.4,
            frequency_penalty=0.6,
            presence_penalty=0.3,
        )
        # The model is inconsistent about blank lines between paragraphs — force one.
        return collapse_blank_lines(answer)

    def _answer_facts(self, message: str, facts: str, language: str) -> str:
        """facts.md: deterministic full list if asked, else the tool-backed model."""
        listing = self._answer_facts_listing(message, facts, language)
        if listing is not None:
            return listing
        return self._answer_with_filter(message, facts, language)

    def _answer_with_filter(self, message: str, facts: str, language: str) -> str:
        """Answer facts questions with the `filtrar_pokemon` tool available.

        The guide is only the small counts header — the per-type/category name
        lists are NOT inlined (that bloated the prompt to thousands of tokens and
        made the model paraphrase instead of list). Names come from the tool,
        which is built from the full facts.md.
        """
        guide = facts_counts_header(facts)
        answer = self._completer.complete_with_tools(
            messages=[
                {
                    "role": "system",
                    "content": build_system_prompt(guide, facts_filter_instruction(language), language),
                },
                {"role": "user", "content": message},
            ],
            models=ANSWER_MODELS,
            tools=[filter_tool_spec()],
            dispatch=make_dispatch(build_pokemon_filter(facts)),
            max_tokens=500,
            temperature=0.4,
        )
        return collapse_blank_lines(answer)

    def _answer_admins(self, language: str) -> str:
        """Resolve the admin role to mentions, returned verbatim (no LLM, so the
        `<@id>` mentions are not mangled). No resolver wired -> plain fallback."""
        if self._admins is None:
            return fallback_message(language)
        return admins_message(self._admins.mentions(), language)

    def _answer_facts_listing(self, message: str, facts: str, language: str) -> str | None:
        """Deterministic big-list answer (no LLM), or None to fall back to the model.

        Only when the player asks for a full list AND it maps to exactly ONE
        facts.md line — then Python sends that line verbatim, never truncated by
        the answer model's token cap nor reworded. A request that touches two or
        more axes ("quais lendários do tipo elétrico") returns None so the tool
        path can intersect them, instead of dumping both full lists concatenated.
        """
        if not wants_full_list(message):
            return None
        lines = matched_facts_lines(message, facts)
        if len(lines) != 1:
            return None
        return facts_listing_message(lines, language)


def _obtain_location_query(pokemon: str) -> str:
    """A location-seeded query for the obtain path: biases retrieval toward the
    passage that names WHERE the summon happens (the structure/monument and how
    to locate it with the Arc Phone), which the player's own phrasing misses.

    Portuguese on purpose: the mod docs are written in Portuguese, so a PT query
    embeds closest to them regardless of the player's language."""
    return f"em qual estrutura ou monumento se invoca {pokemon} e como localizar pelo Arc Phone"


def _merge_passages(mechanic: list[str], location: list[str]) -> list[str]:
    """Interleave the two passage lists: the top summon-mechanic passages first,
    then the top location passages not already present (de-duped, order kept)."""
    merged = list(mechanic[:_OBTAIN_MECHANIC_K])
    for passage in location[:_OBTAIN_LOCATION_K]:
        if passage not in merged:
            merged.append(passage)
    return merged


def _format_transcript(history: list[Turn]) -> str:
    """Render recent turns as a compact "Jogador/Bot" transcript for condensing.

    Answers are capped (_CONDENSE_ANSWER_CAP) so a long reply can't blow up the
    condense prompt — only enough of it is needed to resolve a reference.
    """
    return "\n".join(
        f"Jogador: {turn.question}\nBot: {turn.answer[:_CONDENSE_ANSWER_CAP]}" for turn in history
    )
