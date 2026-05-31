import os

from modpack_bot.indexing import (
    Chunk,
    card_pokemon,
    chunk_card,
    chunk_guide,
    discover_cards,
    discover_guides,
    guide_source,
)

_GUIDE = (
    "# GTS / Market\n"
    "\n"
    "Documento de referência.\n"
    "\n"
    "## Comandos\n"
    "\n"
    "- `/market` abre a GUI.\n"
    "\n"
    "## Taxas\n"
    "\n"
    "Sem taxa de listagem.\n"
)


def test_chunk_guide_splits_one_chunk_per_h2_section():
    sections = [chunk.section for chunk in chunk_guide(_GUIDE, "market.md")]
    assert sections == ["# GTS / Market", "## Comandos", "## Taxas"]


def test_chunk_guide_keeps_heading_inside_each_chunk_text():
    chunks = chunk_guide(_GUIDE, "market.md")
    taxas = next(chunk for chunk in chunks if chunk.section == "## Taxas")
    assert taxas.text == "## Taxas\n\nSem taxa de listagem."
    assert taxas.source == "market.md"
    assert taxas.pokemon is None


def test_chunk_guide_handles_text_with_no_sections():
    chunks = chunk_guide("# Só título\n\nUma linha.\n", "faq.md")
    assert len(chunks) == 1
    assert chunks[0].section == "# Só título"


def test_chunk_guide_returns_empty_for_blank_text():
    assert chunk_guide("   \n", "faq.md") == []


def test_chunk_card_is_a_single_card_sourced_chunk():
    chunk = chunk_card("# Pikachu  (#25 · Elétrico)\nStats…", "Pikachu")
    assert chunk == Chunk(
        text="# Pikachu  (#25 · Elétrico)\nStats…",
        source="card",
        section=None,
        pokemon="Pikachu",
    )


def test_discover_guides_is_recursive_and_excludes_db_and_core(tmp_path):
    (tmp_path / "market.md").write_text("x", encoding="utf-8")
    (tmp_path / "core.md").write_text("x", encoding="utf-8")
    mod = tmp_path / "cobbled_gacha"
    mod.mkdir()
    (mod / "capsulas.md").write_text("x", encoding="utf-8")
    db = tmp_path / "pokemons-db" / "species_cards"
    db.mkdir(parents=True)
    (db / "pikachu.md").write_text("x", encoding="utf-8")

    found = {os.path.relpath(path, tmp_path) for path in discover_guides(str(tmp_path))}
    assert found == {"market.md", os.path.join("cobbled_gacha", "capsulas.md")}


def test_discover_cards_only_picks_species_cards(tmp_path):
    cards = tmp_path / "pokemons-db" / "species_cards"
    cards.mkdir(parents=True)
    (cards / "abra.md").write_text("x", encoding="utf-8")
    (cards / "pikachu.md").write_text("x", encoding="utf-8")
    full = tmp_path / "pokemons-db" / "species_cards_full"
    full.mkdir()
    (full / "pikachu.md").write_text("x", encoding="utf-8")

    found = [os.path.basename(path) for path in discover_cards(str(tmp_path))]
    assert found == ["abra.md", "pikachu.md"]


def test_guide_source_is_relative_with_forward_slashes():
    path = os.path.join("content", "cobbled_gacha", "capsulas.md")
    assert guide_source(path, "content") == "cobbled_gacha/capsulas.md"


def test_card_pokemon_is_the_file_stem():
    path = os.path.join("content", "pokemons-db", "species_cards", "pikachu.md")
    assert card_pokemon(path) == "pikachu"
