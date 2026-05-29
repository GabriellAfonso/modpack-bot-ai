"""Orchestrates a player message into a final answer string.

This is the heart of the runtime: route → pick guide (or swap in a Pokémon
card) → build the prompt → ask the answer model. It returns plain text, so the
Discord layer only has to reply with it and the whole flow is testable end to
end with fakes (no Discord, no Groq, no filesystem).
"""

from modpack_bot.guides import CardRepository, GuideRepository
from modpack_bot.llm import ANSWER_MODELS, ModelCompleter
from modpack_bot.pokemon import detect_pokemon
from modpack_bot.prompts import (
    build_system_prompt,
    fallback_message,
    non_pokemon_instruction,
    pokemon_instruction,
)
from modpack_bot.router import Router
from modpack_bot.text import wants_full_list

_WIKI_GUIDE = "wiki.md"


class Responder:
    """Turns a message into the text the player should receive."""

    def __init__(
        self,
        router: Router,
        completer: ModelCompleter,
        guides: GuideRepository,
        cards: CardRepository,
    ) -> None:
        self._router = router
        self._completer = completer
        self._guides = guides
        self._cards = cards
        self._pokemon_names = cards.pokemon_names()

    def answer(self, message: str) -> str:
        """Full pipeline; returns the player-facing text (or the fallback)."""
        guide_file, language = self._router.route(message)
        if guide_file is None:
            return fallback_message(language)

        guide = self._guides.load_guide(guide_file)
        if guide_file == _WIKI_GUIDE:
            guide, instruction = self._apply_wiki_gate(message, guide, language)
        else:
            instruction = ""

        return self._completer.complete(
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
