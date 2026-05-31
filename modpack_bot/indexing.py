"""Pure chunking and file discovery for the RAG index.

String -> Chunk transforms with no embedding model and no network, so the
offline build (build_index.py) stays a thin wrapper and this logic is unit
tested in isolation. Guides split into one chunk per `## ` section; each
Pokémon card is a single chunk (the cards are already compact).
"""

import glob
import os
from dataclasses import dataclass

_CARD_SOURCE = "card"
_HEADING_PREFIX = "## "
_SECTION_SEPARATOR = "\n## "


@dataclass(frozen=True)
class Chunk:
    """One indexable passage plus the metadata that traces it back to its file.

    `source` is the guide path relative to the content dir (e.g.
    "cobbled_gacha/capsulas.md") or "card" for a Pokémon card. Exactly one of
    `section`/`pokemon` is set, depending on which builder produced the chunk —
    used for retrieval debugging and filtering noisy card hits by `source`.

    Example:
        >>> chunk_card("# Pikachu  (#25)", "Pikachu").pokemon
        'Pikachu'
    """

    text: str
    source: str
    section: str | None = None
    pokemon: str | None = None


def chunk_guide(text: str, source: str) -> list[Chunk]:
    """Split a guide into one chunk per `## ` section, preamble kept as its own.

    Each chunk's text keeps its heading line so a retrieved passage carries its
    own context. `source` is stored verbatim as the chunk's origin metadata.

    Example:
        >>> [c.section for c in chunk_guide("# T\\nintro\\n## A\\nx", "faq.md")]
        ['# T', '## A']
    """
    return [
        Chunk(text=body, source=source, section=heading)
        for heading, body in _split_sections(text)
    ]


def chunk_card(text: str, pokemon: str) -> Chunk:
    """Wrap a whole Pokémon card as a single chunk (cards are already compact).

    Example:
        >>> chunk_card("# Pikachu  (#25)", "Pikachu").source
        'card'
    """
    return Chunk(text=text, source=_CARD_SOURCE, pokemon=pokemon)


def discover_guides(content_dir: str) -> list[str]:
    """Guide .md paths under content_dir (recursive), minus the Pokémon DB and
    core.md (the removed router prompt). Picks up future mod subfolders for free.

    Example:
        >>> # content/market.md and content/cobbled_gacha/capsulas.md, but not
        >>> # content/core.md nor anything under content/pokemons-db/.
    """
    pattern = os.path.join(content_dir, "**", "*.md")
    paths = glob.glob(pattern, recursive=True)
    return sorted(path for path in paths if _is_guide(path, content_dir))


def discover_cards(content_dir: str) -> list[str]:
    """The slim Pokémon card .md paths (species_cards/, sorted)."""
    pattern = os.path.join(content_dir, "pokemons-db", "species_cards", "*.md")
    return sorted(glob.glob(pattern))


def guide_source(path: str, content_dir: str) -> str:
    """A guide's `source` metadata: its path relative to content_dir, with
    forward slashes so the value is stable across platforms.

    Example:
        >>> guide_source("content/cobbled_gacha/x.md", "content")
        'cobbled_gacha/x.md'
    """
    return os.path.relpath(path, content_dir).replace(os.sep, "/")


def card_pokemon(path: str) -> str:
    """The Pokémon name behind a card path (its file stem).

    Example:
        >>> card_pokemon("content/pokemons-db/species_cards/pikachu.md")
        'pikachu'
    """
    return os.path.basename(path)[:-3]


def _split_sections(text: str) -> list[tuple[str, str]]:
    """[(heading_line, block_including_heading)] split at each `## ` line.

    The text before the first `## ` is kept as one block whose heading is its
    first line (the `# ` title). Empty text yields no sections.
    """
    parts = text.split(_SECTION_SEPARATOR)
    sections: list[tuple[str, str]] = []
    preamble = parts[0].strip()
    if preamble:
        sections.append((preamble.splitlines()[0], preamble))
    for part in parts[1:]:
        block = (_HEADING_PREFIX + part).strip()
        sections.append((block.splitlines()[0], block))
    return sections


def _is_guide(path: str, content_dir: str) -> bool:
    """A discovered .md is a guide unless it is core.md or under pokemons-db/."""
    relative = os.path.relpath(path, content_dir)
    if relative == "core.md":
        return False
    return not relative.startswith("pokemons-db" + os.sep)
