import pytest

from modpack_bot.pokemon_filter import (
    FILTER_TOOL_NAME,
    PokemonFilter,
    build_pokemon_filter,
    make_dispatch,
)

_FACTS = (
    "# Números do Modpack\n"
    "\n"
    "- Total de Pokémon no modpack: 4\n"
    "\n"
    "## Pokémon por tipo\n"
    "\n"
    "- Elétrico (3): Pikachu, Raikou, Zapdos\n"
    "- Fogo (1): Charizard\n"
    "\n"
    "## Pokémon por item dropado\n"
    "\n"
    "- Bone (2): Cubone, Raikou\n"
    "\n"
    "## Pokémon por categoria\n"
    "\n"
    "- Lendários (3): Raikou, Type: Null, Zapdos\n"
)


def test_query_intersects_axes():
    pokemon_filter = build_pokemon_filter(_FACTS)
    # electric AND legendary -> only those in both lists, accent-sorted.
    assert pokemon_filter.query(["electric"], ["legendary"], []) == ["Raikou", "Zapdos"]


def test_query_accepts_pt_type_and_category_synonyms():
    pokemon_filter = build_pokemon_filter(_FACTS)
    assert pokemon_filter.query(["eletrico"], ["lendarios"], []) == ["Raikou", "Zapdos"]


def test_query_single_axis_returns_whole_list():
    pokemon_filter = build_pokemon_filter(_FACTS)
    assert pokemon_filter.query(["fire"], [], []) == ["Charizard"]


def test_query_three_axes_intersect():
    pokemon_filter = build_pokemon_filter(_FACTS)
    # electric AND legendary AND drops Bone -> only Raikou.
    assert pokemon_filter.query(["electric"], ["legendary"], ["Bone"]) == ["Raikou"]


def test_query_empty_when_no_overlap():
    pokemon_filter = build_pokemon_filter(_FACTS)
    assert pokemon_filter.query(["fire"], ["legendary"], []) == []


def test_query_no_axes_returns_empty():
    pokemon_filter = build_pokemon_filter(_FACTS)
    assert pokemon_filter.query([], [], []) == []


def test_query_keeps_multiword_names_intact():
    # "Type: Null" has a colon and must survive the comma split as one name.
    pokemon_filter = build_pokemon_filter(_FACTS)
    assert "Type: Null" in pokemon_filter.query([], ["legendary"], [])


def test_build_without_sections_yields_empty_filter():
    pokemon_filter = build_pokemon_filter("# just a header, no lists\n")
    assert pokemon_filter.query(["electric"], [], []) == []


def test_dispatch_formats_intersection():
    dispatch = make_dispatch(build_pokemon_filter(_FACTS))
    result = dispatch(FILTER_TOOL_NAME, {"types": ["electric"], "categories": ["legendary"]})
    assert result == "2 Pokémon: Raikou, Zapdos"


def test_dispatch_reports_no_match():
    dispatch = make_dispatch(build_pokemon_filter(_FACTS))
    result = dispatch(FILTER_TOOL_NAME, {"types": ["fire"], "categories": ["legendary"]})
    assert result == "Nenhum Pokémon corresponde a esses filtros."


def test_dispatch_tolerates_missing_arguments():
    dispatch = make_dispatch(build_pokemon_filter(_FACTS))
    assert dispatch(FILTER_TOOL_NAME, {"types": ["fire"]}) == "1 Pokémon: Charizard"


def test_dispatch_rejects_unknown_tool():
    dispatch = make_dispatch(build_pokemon_filter(_FACTS))
    with pytest.raises(ValueError, match="unknown tool"):
        dispatch("outra", {})


def test_filter_built_from_real_facts_md():
    # Guards against drift between facts.py's rendered lines and the parser.
    with open("content/facts.md", "r", encoding="utf-8") as file:
        facts = file.read()
    legendary_electric = build_pokemon_filter(facts).query(["electric"], ["legendary"], [])
    assert "Zapdos" in legendary_electric
    assert "Pikachu" not in legendary_electric  # electric but not legendary
