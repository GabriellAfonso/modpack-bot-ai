"""Select only the relevant slice of facts.md for a player message.

facts.md holds the full per-type and per-item lists (~10k tokens). Sending it
whole busts Groq's free-tier request cap (12k TPM -> HTTP 413), and swapping
models can't help because every model shares that cap. This gate keeps the small
counts header (always tiny) and appends only the line(s) the player actually
asked about, so the request stays small no matter how big the modpack grows.
"""

from card_builder.type_chart import TYPE_PT
from modpack_bot.text import normalize_tokens

_TYPE_HEADING = "## Pokémon por tipo"
_ITEM_HEADING = "## Pokémon por item dropado"


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
    _, type_lines, item_lines = sections
    tokens = normalize_tokens(message)
    normalized = " ".join(tokens)
    return _match_types(tokens, type_lines) + _match_items(normalized, item_lines)


def select_facts(message: str, facts: str) -> str:
    """Trim facts.md to the counts header plus the type/item lines asked about.

    A general counts question ("quantos pokemon tem?") matches no type or item,
    so it gets just the header. "lista todos os pokemons tipo fogo" adds the one
    Fogo line; "quem dropa leather?" adds the one Leather line.

    Example:
        >>> facts = "# H\\n- total: 1\\n\\n## Pokémon por tipo\\n\\n- Fogo (1): X\\n"
        >>> "Fogo (1): X" in select_facts("tipo fogo", facts)
        True
    """
    sections = _split_sections(facts)
    if sections is None:  # no list sections -> already small enough to send whole
        return facts
    picked = matched_facts_lines(message, facts)
    if not picked:
        return sections[0]
    return sections[0] + "\n\n" + "\n".join(picked)


def _split_sections(
    facts: str,
) -> tuple[str, dict[str, str], dict[str, str]] | None:
    """(counts_header, {type_label: line}, {item_label: line}), or None if facts
    has neither list section (then there is nothing to trim)."""
    if "\n" + _TYPE_HEADING not in facts or "\n" + _ITEM_HEADING not in facts:
        return None
    header, rest = facts.split("\n" + _TYPE_HEADING, 1)
    type_block, item_block = rest.split("\n" + _ITEM_HEADING, 1)
    return header.rstrip(), _index_lines(type_block), _index_lines(item_block)


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
