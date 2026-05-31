"""Read the content files into chunks and shape each chunk's node metadata.

Kept free of the embedding model and of LlamaIndex so the collection and
metadata logic is unit tested fast; build.py turns these chunks into embedded
nodes.
"""

from modpack_bot.indexing import (
    Chunk,
    card_pokemon,
    chunk_card,
    chunk_guide,
    discover_cards,
    discover_guides,
    guide_source,
)


def collect_chunks(content_dir: str) -> list[Chunk]:
    """Every chunk to index: one per guide `## ` section, plus one per card."""
    chunks: list[Chunk] = []
    for path in discover_guides(content_dir):
        chunks.extend(chunk_guide(_read(path), guide_source(path, content_dir)))
    for path in discover_cards(content_dir):
        chunks.append(chunk_card(_read(path), card_pokemon(path)))
    return chunks


def node_metadata(chunk: Chunk) -> dict[str, str]:
    """The origin metadata stored on a chunk's index node (only the set fields).

    Example:
        >>> node_metadata(Chunk("t", "card", pokemon="Abra"))
        {'source': 'card', 'pokemon': 'Abra'}
    """
    metadata = {"source": chunk.source}
    if chunk.section is not None:
        metadata["section"] = chunk.section
    if chunk.pokemon is not None:
        metadata["pokemon"] = chunk.pokemon
    return metadata


def _read(path: str) -> str:
    with open(path, "r", encoding="utf-8") as file:
        return file.read()
