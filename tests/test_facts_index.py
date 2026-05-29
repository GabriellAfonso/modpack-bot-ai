from modpack_bot.facts_index import matched_facts_lines, select_facts

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
)


def test_general_question_keeps_only_the_counts_header():
    result = select_facts("quantos pokemon tem?", _FACTS)
    assert "Total de Pokémon no modpack: 3" in result
    assert "Fogo (1)" not in result
    assert "Leather" not in result


def test_type_question_adds_only_that_type_line():
    result = select_facts("lista todos os pokemons tipo fogo", _FACTS)
    assert "- Fogo (1): Charizard" in result
    assert "Água (2)" not in result
    assert "Total de Pokémon no modpack: 3" in result  # header always kept


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
