"""Cobblemon `labels` surfaced as player-facing Pokémon categories.

Single source of truth shared by the build side (facts.py renders these lines
into facts.md) and the runtime side (facts_index.py matches a player's question
to the right category line). Keyed by the label string exactly as it appears in
each species file's `labels` array.
"""

from typing import NamedTuple


class Category(NamedTuple):
    """A surfaced label: its PT display name and the words players use for it.

    `synonyms` are already accent-stripped/lowercased to match normalize_tokens
    output, so a question token compares against them directly.
    """

    pt_name: str
    synonyms: frozenset[str]


CATEGORIES: dict[str, Category] = {
    "legendary": Category(
        "Lendários",
        frozenset({"lendario", "lendarios", "lendaria", "lendarias", "legendary", "legendaries"}),
    ),
    "mythical": Category(
        "Míticos",
        frozenset({"mitico", "miticos", "mitica", "miticas", "mythical", "mythicals", "mythic"}),
    ),
}
