"""Pure gate routing: which path a message belongs to (no LLM, no I/O).

Extracted from the Responder so the routing decision can be evaluated in
isolation (see eval/) and unit-tested without building an answer. The order
mirrors Responder._gate_and_answer exactly — precision gates first, RAG last —
so the eval measures the real runtime routing, not a copy that can drift.
"""

from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum

from modpack_bot.intent import (
    admins_intent,
    claim_intent,
    facts_intent,
    spawn_help_intent,
    stats_intent,
)
from modpack_bot.pokemon import detect_pokemon


class Route(Enum):
    """The gate a message resolves to (the branch Responder will take)."""

    CLAIM = "claim"
    ADMINS = "admins"
    POKEMON = "pokemon"
    STATS = "stats"
    SPAWN_HELP = "spawn_help"
    FACTS = "facts"
    RAG = "rag"


@dataclass(frozen=True)
class RouteDecision:
    """The chosen route plus the detected Pokémon name (only for Route.POKEMON)."""

    route: Route
    pokemon: str | None = None


def classify_route(
    message: str,
    pokemon_names: frozenset[str],
    load_facts: Callable[[], str],
) -> RouteDecision:
    """Pick the gate for a message; pure given its inputs, zero tokens.

    `load_facts` is a thunk, not the text, so facts.md is read only when the
    earlier gates miss — preserving the Responder's lazy load on the claim/
    admins/Pokémon paths.

    Example:
        >>> classify_route("como falo com um admin?", frozenset(), lambda: "").route
        <Route.ADMINS: 'admins'>
    """
    if claim_intent(message):
        return RouteDecision(Route.CLAIM)
    if admins_intent(message):
        return RouteDecision(Route.ADMINS)
    pokemon = detect_pokemon(message, pokemon_names)
    if pokemon:
        return RouteDecision(Route.POKEMON, pokemon)
    if stats_intent(message):
        return RouteDecision(Route.STATS)
    if spawn_help_intent(message):
        return RouteDecision(Route.SPAWN_HELP)
    if facts_intent(message, load_facts()):
        return RouteDecision(Route.FACTS)
    return RouteDecision(Route.RAG)
