"""Orchestrates a player message into a final answer string.

This is the heart of the runtime: route → pick guide (or swap in a Pokémon
card) → build the prompt → ask the answer model. It returns plain text, so the
Discord layer only has to reply with it and the whole flow is testable end to
end with fakes (no Discord, no Groq, no filesystem).
"""

from modpack_bot.admins import TOOL_ADMINS, AdminResolver, admins_message
from modpack_bot.facts_index import matched_facts_lines, select_facts
from modpack_bot.guides import CardRepository, GuideRepository
from modpack_bot.llm import ANSWER_MODELS, ModelCompleter
from modpack_bot.pokemon import detect_pokemon
from modpack_bot.prompts import (
    build_system_prompt,
    facts_listing_message,
    fallback_message,
    non_pokemon_instruction,
    pokemon_instruction,
)
from modpack_bot.router import Router
from modpack_bot.text import collapse_blank_lines, wants_full_list

_WIKI_GUIDE = "wiki.md"
_FACTS_GUIDE = "facts.md"


class Responder:
    """Turns a message into the text the player should receive."""

    def __init__(
        self,
        router: Router,
        completer: ModelCompleter,
        guides: GuideRepository,
        cards: CardRepository,
        admins: AdminResolver | None = None,
    ) -> None:
        self._router = router
        self._completer = completer
        self._guides = guides
        self._cards = cards
        self._admins = admins
        self._pokemon_names = cards.pokemon_names()

    def answer(self, message: str) -> str:
        """Full pipeline; returns the player-facing text (or the fallback)."""
        guide_file, language = self._router.route(message)
        if guide_file is None:
            return fallback_message(language)
        if guide_file == TOOL_ADMINS:
            return self._answer_admins(language)

        guide = self._guides.load_guide(guide_file)
        instruction = ""
        if guide_file == _WIKI_GUIDE:
            guide, instruction = self._apply_wiki_gate(message, guide, language)
        elif guide_file == _FACTS_GUIDE:
            listing = self._answer_facts_listing(message, guide, language)
            if listing is not None:
                return listing
            # Not a full-list request: inject only the asked-about slice so the
            # request stays under the model's token cap.
            guide = select_facts(message, guide)

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

    def _answer_admins(self, language: str) -> str:
        """Resolve the admin role to mentions, returned verbatim (no LLM, so the
        `<@id>` mentions are not mangled). No resolver wired -> plain fallback."""
        if self._admins is None:
            return fallback_message(language)
        return admins_message(self._admins.mentions(), language)

    def _answer_facts_listing(self, message: str, facts: str, language: str) -> str | None:
        """Deterministic big-list answer (no LLM), or None to fall back to the model.

        Only when the player explicitly asks for a full list AND it maps to facts.md
        lines — then Python sends the data verbatim, so it is never truncated by the
        answer model's token cap nor reworded.
        """
        if not wants_full_list(message):
            return None
        lines = matched_facts_lines(message, facts)
        return facts_listing_message(lines, language) if lines else None

    def _apply_wiki_gate(self, message: str, guide: str, language: str) -> tuple[str, str]:
        """Pokémon gate (wiki.md only): deterministic name detection.

        Found a Pokémon -> swap in its card (data) and instruct the model to
        point at `/pwiki` for anything missing. Found none -> keep wiki.md (the
        tool's doc) and forbid suggesting `/pwiki` for non-Pokémon (stronghold).
        """
        pokemon = detect_pokemon(message, self._pokemon_names)
        card = self._cards.load_card(pokemon, wants_full_list(message)) if pokemon else None
        if card:
            return card, pokemon_instruction(pokemon, language)
        return guide, non_pokemon_instruction(language)
