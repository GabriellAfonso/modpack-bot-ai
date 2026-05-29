from modpack_bot.facts_index import facts_counts_header, matched_facts_lines, select_facts

_FACTS = (
    "# Números do Modpack\n"
    "\n"
    "- Total de Pokémon no modpack: 3\n"
    "\n"
    "## Pokémon por tipo\n"
    "\n"
    "Cada Pokémon aparece em todos os seus tipos.\n"
    "\n"
    "- Água (2): Psyduck, Squirtle\n"
    "- Fogo (1): Charizard\n"
    "\n"
    "## Pokémon por item dropado\n"
    "\n"
    "Quem dropa cada item.\n"
    "\n"
    "- Blaze Powder (1): Ponyta\n"
    "- Leather (2): Ponyta, Rapidash\n"
    "\n"
    "## Pokémon por categoria\n"
    "\n"
    "- Lendários (1): Mewtwo\n"
    "- Míticos (1): Mew\n"
)


def test_counts_header_drops_every_name_list():
    header = facts_counts_header(_FACTS)
    assert "Total de Pokémon no modpack: 3" in header
    # none of the per-type/item/category name lists leak into the header.
    assert "Charizard" not in header
    assert "Leather" not in header
    assert "Mewtwo" not in header


def test_counts_header_returns_whole_text_without_sections():
    assert facts_counts_header("# só um header\n") == "# só um header\n"


def test_general_question_keeps_only_the_counts_header():
    result = select_facts("quantos pokemon tem?", _FACTS)
    assert "Total de Pokémon no modpack: 3" in result
    assert "Fogo (1)" not in result
    assert "Leather" not in result


def test_type_question_adds_only_that_type_line():
    result = select_facts("lista todos os pokemons tipo fogo", _FACTS)
    assert "- Fogo (1): Charizard" in result
    assert "Água (2)" not in result
    # global totals are dropped on a specific question so the model can't cite them.
    assert "Total de Pokémon no modpack: 3" not in result


def test_type_question_matches_english_type_id():
    result = select_facts("list every water pokemon", _FACTS)
    assert "- Água (2): Psyduck, Squirtle" in result
    assert "Fogo (1)" not in result


def test_item_question_adds_only_that_item_line():
    result = select_facts("who drops leather?", _FACTS)
    assert "- Leather (2): Ponyta, Rapidash" in result
    assert "Blaze Powder" not in result


def test_multiword_item_label_matches():
    result = select_facts("quem dropa blaze powder?", _FACTS)
    assert "- Blaze Powder (1): Ponyta" in result


def test_trimmed_output_is_far_smaller_than_the_whole_file():
    result = select_facts("tipo fogo", _FACTS)
    assert len(result) < len(_FACTS)


def test_matched_lines_returns_type_then_item_lines():
    lines = matched_facts_lines("fogo e leather", _FACTS)
    assert lines == ["- Fogo (1): Charizard", "- Leather (2): Ponyta, Rapidash"]


def test_matched_lines_empty_for_general_count_question():
    assert matched_facts_lines("quantos pokemon tem?", _FACTS) == []


def test_legendary_question_adds_only_the_legendary_line():
    result = select_facts("quais pokemons lendarios tem?", _FACTS)
    assert result == "- Lendários (1): Mewtwo"


def test_mythical_question_matches_english_synonym():
    result = select_facts("list the mythical pokemon", _FACTS)
    assert result == "- Míticos (1): Mew"


def test_category_and_type_questions_do_not_cross_match():
    assert "Lendários" not in select_facts("tipo fogo", _FACTS)
    assert "Fogo" not in select_facts("quais lendarios", _FACTS)
