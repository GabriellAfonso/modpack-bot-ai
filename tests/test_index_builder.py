import os

from index_builder.nodes import collect_chunks, node_metadata
from modpack_bot.indexing import Chunk


def _write(path, text="x"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        file.write(text)


def test_node_metadata_keeps_only_the_set_fields():
    guide = Chunk("t", "market.md", section="## Taxas")
    card = Chunk("t", "card", pokemon="Abra")
    assert node_metadata(guide) == {"source": "market.md", "section": "## Taxas"}
    assert node_metadata(card) == {"source": "card", "pokemon": "Abra"}


def test_collect_chunks_covers_guides_and_cards(tmp_path):
    base = str(tmp_path)
    _write(os.path.join(base, "market.md"), "# Market\n\n## Taxas\n\nSem taxa.\n")
    _write(os.path.join(base, "cobbled_gacha", "capsulas.md"), "# Capsulas\n\ntexto\n")
    _write(os.path.join(base, "pokemons-db", "species_cards", "abra.md"), "# Abra\nstats")

    chunks = collect_chunks(base)
    sources = sorted({chunk.source for chunk in chunks})
    assert sources == ["card", "cobbled_gacha/capsulas.md", "market.md"]
    card = next(chunk for chunk in chunks if chunk.source == "card")
    assert card.pokemon == "abra"


def test_collect_chunks_skips_core_and_pokemons_db_guides(tmp_path):
    base = str(tmp_path)
    _write(os.path.join(base, "core.md"), "# router prompt\n")
    _write(os.path.join(base, "pokemons-db", "biome_map.md"), "# biomes\n")
    _write(os.path.join(base, "faq.md"), "# FAQ\n\ntexto\n")

    sources = {chunk.source for chunk in collect_chunks(base)}
    assert sources == {"faq.md"}
