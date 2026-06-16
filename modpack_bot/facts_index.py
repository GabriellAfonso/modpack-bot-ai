"""Select only the relevant slice of facts.md for a player message.

facts.md holds the full per-type and per-item lists (~10k tokens). Sending it
whole busts Groq's free-tier request cap (12k TPM -> HTTP 413), and swapping
models can't help because every model shares that cap. This gate keeps the small
counts header (always tiny) and appends only the line(s) the player actually
asked about, so the request stays small no matter how big the modpack grows.
"""

from card_builder.categories import CATEGORIES
from card_builder.type_chart import TYPE_PT
from modpack_bot.text import normalize_tokens

_TYPE_HEADING = "## Pokémon por tipo"
_ITEM_HEADING = "## Pokémon por item dropado"
_CATEGORY_HEADING = "## Pokémon por categoria"

# Subjects of a modpack-wide total ("quantos pokémons/biomas/tipos tem?"). These
# counts live in the facts.md header verbatim, so a count question naming one is
# answered from the header rather than a per-axis line.
_TOTAL_SUBJECTS = frozenset(
    {
        "pokemon", "pokemons", "pokemom", "mon", "mons", "bicho", "bichos",
        "bichinho", "bichinhos", "bioma", "biomas", "tipo", "tipos",
    }
)


def asks_modpack_total(message: str) -> bool:
    """True when a question is about a modpack-wide total (how many Pokémon,
    biomes or types in total), as opposed to a specific type/item/category axis.

    Pure on the message — the totals it points at are fixed lines in the facts.md
    counts header (facts_counts_header), so the caller answers from there.

    Example:
        >>> asks_modpack_total("quantos pokemons tem no servidor?")
        True
        >>> asks_modpack_total("quantos comandos tem o market?")
        False
    """
    return bool(set(normalize_tokens(message)) & _TOTAL_SUBJECTS)


def matched_facts_lines(message: str, facts: str) -> list[str]:
    """The facts.md list lines the message asks about (type lines, then item lines).

    Empty for a general counts question. Used both to trim the guide and, when the
    player explicitly wants a full list, to answer deterministically without the LLM.

    Example:
        >>> facts = "# H\\n\\n## Pokémon por tipo\\n\\n- Fogo (1): X\\n" \
"\\n## Pokémon por item dropado\\n\\n- Bone (1): Y\\n"
        >>> matched_facts_lines("tipo fogo", facts)
        ['- Fogo (1): X']
    """
    sections = _split_sections(facts)
    if sections is None:
        return []
    _, type_lines, item_lines, category_lines = sections
    tokens = normalize_tokens(message)
    normalized = " ".join(tokens)
    return (
        _match_types(tokens, type_lines)
        + _match_items(normalized, item_lines)
        + _match_categories(tokens, category_lines)
    )


def select_facts(message: str, facts: str) -> str:
    """Trim facts.md to exactly the slice the message asks about.

    A general counts question ("quantos pokemon tem?") matches no type or item,
    so it gets the counts header. A specific question ("quantos do tipo água?")
    gets ONLY the matched type/item line(s) and NOT the header — otherwise the
    answer model sees the global totals (e.g. "spawn natural: 890") and tacks
    them onto a reply that should only state the asked-about count.

    Example:
        >>> facts = "# H\\n- total: 1\\n\\n## Pokémon por tipo\\n\\n- Fogo (1): X\\n"
        >>> select_facts("tipo fogo", facts)
        '- Fogo (1): X'
    """
    sections = _split_sections(facts)
    if sections is None:  # no list sections -> already small enough to send whole
        return facts
    picked = matched_facts_lines(message, facts)
    if not picked:
        return sections[0]
    return "\n".join(picked)


def facts_counts_header(facts: str) -> str:
    """The small counts header of facts.md (totals + per-type summary line).

    Used as the guide for the tool-backed answer path: the big per-type/category
    lists are NOT inlined (the `filtrar_pokemon` tool fetches names on demand), so
    the prompt stays tiny instead of dumping hundreds of names. Falls back to the
    whole text when facts has no list sections.
    """
    sections = _split_sections(facts)
    return sections[0] if sections else facts


def _split_sections(
    facts: str,
) -> tuple[str, dict[str, str], dict[str, str], dict[str, str]] | None:
    """(counts_header, {type_label: line}, {item_label: line}, {category_label: line}),
    or None if facts lacks the list sections (then there is nothing to trim)."""
    headings = (_TYPE_HEADING, _ITEM_HEADING, _CATEGORY_HEADING)
    if any("\n" + heading not in facts for heading in headings):
        return None
    header, rest = facts.split("\n" + _TYPE_HEADING, 1)
    type_block, rest = rest.split("\n" + _ITEM_HEADING, 1)
    item_block, category_block = rest.split("\n" + _CATEGORY_HEADING, 1)
    return (
        header.rstrip(),
        _index_lines(type_block),
        _index_lines(item_block),
        _index_lines(category_block),
    )


def _index_lines(block: str) -> dict[str, str]:
    """{normalized_label: full_line} for every '- Label (n): …' line in a block."""
    indexed: dict[str, str] = {}
    for line in block.splitlines():
        if line.startswith("- ") and " (" in line:
            label = line[2 : line.index(" (")]
            indexed[" ".join(normalize_tokens(label))] = line
    return indexed


def _match_types(tokens: list[str], type_lines: dict[str, str]) -> list[str]:
    """Lines for every type named in the message, by PT label or English id."""
    matched = []
    for english, pt_name in TYPE_PT.items():
        label = " ".join(normalize_tokens(pt_name))
        if (label in tokens or english in tokens) and label in type_lines:
            matched.append(type_lines[label])
    return matched


def _match_items(normalized: str, item_lines: dict[str, str]) -> list[str]:
    """Lines for every item whose label appears verbatim in the message."""
    return [line for label, line in item_lines.items() if label and label in normalized]


def _match_categories(tokens: list[str], category_lines: dict[str, str]) -> list[str]:
    """Lines for every category a synonym in the message points at (legendary, mythical)."""
    matched = []
    token_set = set(tokens)
    for category in CATEGORIES.values():
        label = " ".join(normalize_tokens(category.pt_name))
        if label in category_lines and category.synonyms & token_set:
            matched.append(category_lines[label])
    return matched
