"""Computed facts about the modpack, generated into content/facts.md.

build_facts is pure: given the parsed species, the spawn index and the biome
map it returns the markdown the bot reads at runtime. Single source of truth —
the same JSON that produces the cards produces these numbers, so they can never
drift from the cards.
"""

import unicodedata

from card_builder.context import Json
from card_builder.naming import item_name
from card_builder.type_chart import TYPE_PT


def _sort_key(name: str) -> str:
    """Accent-insensitive key so 'Água' sorts before 'Fogo', not after."""
    stripped = unicodedata.normalize("NFKD", name)
    return "".join(c for c in stripped if not unicodedata.combining(c)).lower()


def collect_types(species: list[tuple[str, Json]]) -> dict[str, int]:
    """{english_type: count} over primary + secondary of every species.

    Example:
        >>> collect_types([("a", {"primaryType": "water"})])
        {'water': 1}
    """
    counts: dict[str, int] = {}
    for _, data in species:
        for type_name in _species_types(data):
            counts[type_name] = counts.get(type_name, 0) + 1
    return counts


def _species_types(data: Json) -> list[str]:
    """Primary + optional secondary type of one species, lowercase ids."""
    secondary = [data["secondaryType"]] if data.get("secondaryType") else []
    primary = [data["primaryType"]] if data.get("primaryType") else []
    return primary + secondary


def collect_type_members(species: list[tuple[str, Json]]) -> dict[str, list[str]]:
    """{english_type: [display_name, …]} over primary + secondary of every species.

    A Pokémon with two types appears under both. Display name is the card title
    (`name`), falling back to the card key so the bot can still list species
    whose JSON omits it.

    Example:
        >>> collect_type_members([("charizard", {"name": "Charizard", \
"primaryType": "fire", "secondaryType": "flying"})])
        {'fire': ['Charizard'], 'flying': ['Charizard']}
    """
    members: dict[str, list[str]] = {}
    for key, data in species:
        display = data.get("name", key)
        for type_name in _species_types(data):
            members.setdefault(type_name, []).append(display)
    return members


def render_type_members(members: dict[str, list[str]]) -> str:
    """One line per type, PT-sorted, names sorted accent-insensitively.

    '- Fogo (2): Charizard, Charmander'. Lets the bot answer "list every Fogo
    Pokémon" from the same source that produces the counts.
    """
    pt_members = {TYPE_PT.get(t, t): names for t, names in members.items()}
    lines = []
    for pt_name in sorted(pt_members, key=_sort_key):
        names = sorted(pt_members[pt_name], key=_sort_key)
        lines.append(f"- {pt_name} ({len(names)}): {', '.join(names)}")
    return "\n".join(lines)


def _species_drops(data: Json) -> list[str]:
    """Display names of every item one species can drop, deduped, source order.

    'minecraft:leather' -> 'Leather'. Dedupe because a species may list the same
    item under several entries (different drop conditions) — we only want it once.
    """
    entries = data.get("drops", {}).get("entries", [])
    items = [item_name(entry["item"]) for entry in entries if entry.get("item")]
    return list(dict.fromkeys(items))


def collect_item_droppers(species: list[tuple[str, Json]]) -> dict[str, list[str]]:
    """{item_display_name: [pokemon_display, …]} — the reverse of each card's
    `Drops:` line, so the bot can answer "who drops Bone?" from one index.

    Display name is the card title (`name`), falling back to the card key.

    Example:
        >>> collect_item_droppers([("ponyta", {"name": "Ponyta", \
"drops": {"entries": [{"item": "minecraft:leather"}]}})])
        {'Leather': ['Ponyta']}
    """
    droppers: dict[str, list[str]] = {}
    for key, data in species:
        display = data.get("name", key)
        for item in _species_drops(data):
            droppers.setdefault(item, []).append(display)
    return droppers


def render_item_droppers(droppers: dict[str, list[str]]) -> str:
    """One line per item, items and names sorted accent-insensitively.

    '- Leather (2): Ponyta, Rapidash'.
    """
    lines = []
    for item in sorted(droppers, key=_sort_key):
        names = sorted(droppers[item], key=_sort_key)
        lines.append(f"- {item} ({len(names)}): {', '.join(names)}")
    return "\n".join(lines)


def render_types_line(type_counts: dict[str, int]) -> str:
    """'- Água (123), Fogo (98), …' in PT, sorted by PT name."""
    names = sorted((TYPE_PT.get(t, t) for t in type_counts), key=_sort_key)
    parts = [f"{name} ({_count_for(name, type_counts)})" for name in names]
    return "- " + ", ".join(parts)


def _count_for(pt_name: str, type_counts: dict[str, int]) -> int:
    """Look the count up by its PT display name (the line renders in PT)."""
    for english, count in type_counts.items():
        if TYPE_PT.get(english, english) == pt_name:
            return count
    return 0


def build_facts(
    species: list[tuple[str, Json]],
    spawn_index: dict[str, list[Json]],
    biomes: dict[str, str],
) -> str:
    """Render the facts.md markdown. Deterministic: every list is sorted."""
    type_counts = collect_types(species)
    lines = [
        "# Números do Modpack",
        "",
        "Dados gerados automaticamente a partir do banco de Pokémon. Não editar à mão.",
        "",
        f"- Total de Pokémon no modpack: {len(species)}",
        f"- Tipos existentes ({len(type_counts)}), com quantos Pokémon de cada:",
        render_types_line(type_counts),
        f"- Total de biomas mapeados: {len(biomes)}",
        f"- Pokémon com spawn natural no mundo: {len(spawn_index)}",
        "",
        "## Pokémon por tipo",
        "",
        "Cada Pokémon aparece em todos os seus tipos (primário e secundário).",
        "",
        render_type_members(collect_type_members(species)),
        "",
        "## Pokémon por item dropado",
        "",
        "Quem dropa cada item. Nomes dos itens em inglês (como aparecem no jogo).",
        "",
        render_item_droppers(collect_item_droppers(species)),
    ]
    return "\n".join(lines) + "\n"
