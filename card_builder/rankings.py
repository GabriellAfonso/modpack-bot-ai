"""Computed base-stat rankings, rendered into content/stats.md.

build_rankings is pure: given the parsed species it returns the markdown the
bot's stats gate reads at runtime (modpack_bot.stats_index). The same JSON that
builds the cards builds these rankings, so the "qual o mais forte / mais rápido"
answers can never drift from the cards' Stats base line.
"""

import unicodedata

from card_builder.context import Json

# How many Pokémon each ranking lists: enough to cover ties and a "top 10"
# request while keeping every section a small, exact slice for the answer model.
_TOP_N = 15

# The six base-stat JSON keys (Cobblemon spelling), in card display order.
_STAT_KEYS = ("hp", "attack", "defence", "special_attack", "special_defence", "speed")

# (heading, stat_key) per stats.md section, in render order. stat_key is None
# for the BST total — the sum of the six base stats, i.e. "strongest" overall.
# The headings are the slice keys the runtime matches (modpack_bot.stats_index).
STAT_SECTIONS: list[tuple[str, str | None]] = [
    ("Total (BST)", None),
    ("HP", "hp"),
    ("Ataque", "attack"),
    ("Defesa", "defence"),
    ("Ataque Especial", "special_attack"),
    ("Defesa Especial", "special_defence"),
    ("Velocidade", "speed"),
]


def build_rankings(species: list[tuple[str, Json]]) -> str:
    """Render stats.md: one top-N section per base stat plus the BST total.

    Deterministic — every section is sorted by value (descending), ties broken
    by accent-insensitive name, so the output is stable across runs.
    """
    entries = _entries(species)
    lines = _header()
    for heading, stat_key in STAT_SECTIONS:
        lines.extend(_section_lines(heading, stat_key, entries))
    return "\n".join(lines) + "\n"


def _header() -> list[str]:
    """The fixed preamble lines, ending with a blank before the first section."""
    return [
        "# Ranking de Stats",
        "",
        "Top Pokémon por stat base, gerado a partir do banco de Pokémon. Não editar à mão.",
        '"Mais forte" = maior total (a soma dos seis stats base, o BST).',
        "",
    ]


def _entries(species: list[tuple[str, Json]]) -> list[tuple[str, dict[str, int]]]:
    """(display_name, base_stats) for every species that has all six base stats.

    Species missing a stat are skipped rather than crashing the build (the cards
    assume the field is present; rankings stay defensive about a malformed file).
    """
    out: list[tuple[str, dict[str, int]]] = []
    for key, data in species:
        stats = _base_stats(data)
        if stats is not None:
            out.append((data.get("name", key), stats))
    return out


def _base_stats(data: Json) -> dict[str, int] | None:
    """The six base stats as ints, or None when the species omits or malforms any."""
    raw = data.get("baseStats")
    if not isinstance(raw, dict):
        return None
    try:
        return {key: int(raw[key]) for key in _STAT_KEYS}
    except (KeyError, TypeError, ValueError):
        return None


def _section_lines(
    heading: str, stat_key: str | None, entries: list[tuple[str, dict[str, int]]]
) -> list[str]:
    """The '## heading' block: the top-N entries for one stat, then a blank line."""
    ranked = sorted(entries, key=lambda e: (-_value(e[1], stat_key), _sort_key(e[0])))
    body = [_entry_line(rank, name, stats, stat_key)
            for rank, (name, stats) in enumerate(ranked[:_TOP_N], 1)]
    return [f"## {heading}", "", *body, ""]


def _entry_line(rank: int, name: str, stats: dict[str, int], stat_key: str | None) -> str:
    """'1. Arceus — 720 (HP …)' for the BST total, '1. Regieleki — 200' per stat."""
    value = _value(stats, stat_key)
    if stat_key is None:
        return f"{rank}. {name} — {value} ({_stat_line(stats)})"
    return f"{rank}. {name} — {value}"


def _value(stats: dict[str, int], stat_key: str | None) -> int:
    """The ranking value: the named stat, or the BST total when stat_key is None."""
    return sum(stats.values()) if stat_key is None else stats[stat_key]


def _stat_line(stats: dict[str, int]) -> str:
    """The card's 'HP x / Atk y / …' breakdown (mirrors card._stats_line)."""
    return (
        f"HP {stats['hp']} / Atk {stats['attack']} / Def {stats['defence']} / "
        f"SpA {stats['special_attack']} / SpD {stats['special_defence']} / "
        f"Spd {stats['speed']}"
    )


def _sort_key(name: str) -> str:
    """Accent-insensitive tiebreak key so 'Á' sorts with 'A', not after 'Z'."""
    stripped = unicodedata.normalize("NFKD", name)
    return "".join(c for c in stripped if not unicodedata.combining(c)).lower()
