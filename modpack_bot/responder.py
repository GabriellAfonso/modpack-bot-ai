"""Orchestrates a player message into a final answer string.

This is the heart of the runtime. Deterministic gates run first for precision
at zero Groq tokens (admins -> Pokémon card -> facts), and semantic retrieval
(RAG) is the general fallback (plan.md §4). It returns plain text, so the
Discord layer only has to reply with it and the whole flow is testable end to
end with fakes (no Discord, no Groq, no embedding model).
"""

from modpack_bot.admins import AdminResolver, admins_message
from modpack_bot.facts_index import facts_counts_header, matched_facts_lines
from modpack_bot.guides import CardRepository, GuideRepository
from modpack_bot.intent import admins_intent, detect_language, facts_intent
from modpack_bot.llm import ANSWER_MODELS, ModelCompleter
from modpack_bot.pokemon import detect_pokemon
from modpack_bot.pokemon_filter import build_pokemon_filter, filter_tool_spec, make_dispatch
from modpack_bot.prompts import (
    build_system_prompt,
    facts_filter_instruction,
    facts_listing_message,
    fallback_message,
    pokemon_instruction,
    usage_suffix,
)
from modpack_bot.retrieval import ContextRetriever
from modpack_bot.text import collapse_blank_lines, wants_full_list

_FACTS_GUIDE = "facts.md"


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
    ) -> None:
        self._retriever = retriever
        self._completer = completer
        self._guides = guides
        self._cards = cards
        self._admins = admins
        self._show_usage = show_usage
        self._pokemon_names = cards.pokemon_names()

    def answer(self, message: str) -> str:
        """Full pipeline; returns the player-facing text (or the fallback).

        Token usage is reset up front and read at the end so the optional footer
        reflects every model call this one message made (answer + any tools).
        """
        self._completer.reset_usage()
        return self._with_usage(self._gate_and_answer(message))

    def _gate_and_answer(self, message: str) -> str:
        """Deterministic gates first (precision, 0 tokens), RAG as fallback (§4)."""
        language = detect_language(message)
        if admins_intent(message):
            return self._answer_admins(language)
        pokemon = detect_pokemon(message, self._pokemon_names)
        if pokemon:
            return self._answer_pokemon(message, pokemon, language)
        facts = self._guides.load_guide(_FACTS_GUIDE)
        if facts_intent(message, facts):
            return self._answer_facts(message, facts, language)
        return self._answer_from_rag(message, language)

    def _with_usage(self, text: str) -> str:
        """Append the token-cost footer when the runtime enabled it."""
        if not self._show_usage:
            return text
        return text + usage_suffix(self._completer.usage)

    def _answer_pokemon(self, message: str, pokemon: str, language: str) -> str:
        """Inject the detected Pokémon's card and answer (the wiki gate, §4.2).

        Falls back to RAG only if the card vanished from disk — detect_pokemon
        already guarantees the name exists in the card set.
        """
        card = self._cards.load_card(pokemon, wants_full_list(message))
        if card is None:
            return self._answer_from_rag(message, language)
        return self._answer_from_guide(message, card, pokemon_instruction(pokemon, language), language)

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
