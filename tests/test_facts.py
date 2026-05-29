from card_builder.context import Json
from card_builder.facts import (
    build_facts,
    collect_item_droppers,
    collect_type_members,
    collect_types,
    render_item_droppers,
    render_type_members,
    render_types_line,
)

_SPECIES: list[tuple[str, Json]] = [
    ("squirtle", {"name": "Squirtle", "primaryType": "water"}),
    ("psyduck", {"name": "Psyduck", "primaryType": "water"}),
    ("charizard", {"name": "Charizard", "primaryType": "fire", "secondaryType": "flying"}),
]

_DROPPERS: list[tuple[str, Json]] = [
    ("ponyta", {"name": "Ponyta", "drops": {"entries": [
        {"item": "minecraft:leather", "quantityRange": "0-1"},
        {"item": "minecraft:blaze_powder", "percentage": 2.5},
    ]}}),
    ("rapidash", {"name": "Rapidash", "drops": {"entries": [
        {"item": "minecraft:leather", "quantityRange": "0-2"},
    ]}}),
    ("pidgey", {"name": "Pidgey"}),  # no drops key at all
]


def test_collect_types_counts_primary_and_secondary():
    assert collect_types(_SPECIES) == {"water": 2, "fire": 1, "flying": 1}


def test_collect_types_ignores_missing_secondary():
    assert collect_types([("a", {"primaryType": "grass"})]) == {"grass": 1}


def test_render_types_line_sorted_in_pt_with_counts():
    line = render_types_line({"water": 2, "fire": 1, "flying": 1})
    assert line == "- Água (2), Fogo (1), Voador (1)"


def test_collect_type_members_lists_each_type():
    members = collect_type_members(_SPECIES)
    assert members == {
        "water": ["Squirtle", "Psyduck"],
        "fire": ["Charizard"],
        "flying": ["Charizard"],
    }


def test_collect_type_members_falls_back_to_key_without_name():
    assert collect_type_members([("ditto", {"primaryType": "normal"})]) == {"normal": ["ditto"]}


def test_render_type_members_sorted_pt_and_names_with_counts():
    rendered = render_type_members({"water": ["Psyduck", "Squirtle"], "fire": ["Charizard"]})
    assert rendered == "- Água (2): Psyduck, Squirtle\n- Fogo (1): Charizard"


def test_build_facts_lists_pokemon_per_type():
    facts = build_facts(_SPECIES, {"squirtle": [{}]}, {"#tag": "Ocean"})
    assert "## Pokémon por tipo" in facts
    assert "- Fogo (1): Charizard" in facts
    assert "- Água (2): Psyduck, Squirtle" in facts


def test_build_facts_reports_totals():
    facts = build_facts(_SPECIES, {"squirtle": [{}]}, {"#tag": "Ocean", "#x": "Cave"})
    assert "Total de Pokémon no modpack: 3" in facts
    assert "Tipos existentes (3)" in facts
    assert "Água (2), Fogo (1), Voador (1)" in facts
    assert "Total de biomas mapeados: 2" in facts
    assert "Pokémon com spawn natural no mundo: 1" in facts


def test_collect_item_droppers_groups_pokemon_per_item():
    assert collect_item_droppers(_DROPPERS) == {
        "Leather": ["Ponyta", "Rapidash"],
        "Blaze Powder": ["Ponyta"],
    }


def test_collect_item_droppers_ignores_species_without_drops():
    assert collect_item_droppers([("pidgey", {"name": "Pidgey"})]) == {}


def test_collect_item_droppers_dedupes_repeated_item_per_species():
    species = [("snorlax", {"name": "Snorlax", "drops": {"entries": [
        {"item": "minecraft:apple", "percentage": 50},
        {"item": "minecraft:apple", "quantityRange": "1-3"},
    ]}})]
    assert collect_item_droppers(species) == {"Apple": ["Snorlax"]}


def test_collect_item_droppers_falls_back_to_key_without_name():
    species = [("ditto", {"drops": {"entries": [{"item": "minecraft:slime_ball"}]}})]
    assert collect_item_droppers(species) == {"Slime Ball": ["ditto"]}


def test_render_item_droppers_sorted_items_and_names_with_counts():
    rendered = render_item_droppers({"Leather": ["Rapidash", "Ponyta"], "Apple": ["Snorlax"]})
    assert rendered == "- Apple (1): Snorlax\n- Leather (2): Ponyta, Rapidash"


def test_build_facts_lists_pokemon_per_item():
    facts = build_facts(_DROPPERS, {}, {"#tag": "Ocean"})
    assert "## Pokémon por item dropado" in facts
    assert "- Leather (2): Ponyta, Rapidash" in facts
    assert "- Blaze Powder (1): Ponyta" in facts


def test_build_facts_is_deterministic():
    args = (_SPECIES, {"squirtle": [{}]}, {"#tag": "Ocean"})
    assert build_facts(*args) == build_facts(*args)
