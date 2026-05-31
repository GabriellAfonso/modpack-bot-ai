from modpack_bot.intent import admins_intent, detect_language, facts_intent

_FACTS = (
    "# Números do Modpack\n"
    "\n"
    "- Total de Pokémon no modpack: 3\n"
    "\n"
    "## Pokémon por tipo\n"
    "\n"
    "- Água (2): Psyduck, Squirtle\n"
    "- Fogo (1): Charizard\n"
    "\n"
    "## Pokémon por item dropado\n"
    "\n"
    "- Leather (2): Ponyta, Rapidash\n"
    "\n"
    "## Pokémon por categoria\n"
    "\n"
    "- Lendários (1): Mewtwo\n"
)


def test_detect_language_reads_portuguese_questions_as_pt():
    assert detect_language("quantos pokemon de fogo tem no servidor?") == "pt"


def test_detect_language_reads_english_questions_as_en():
    assert detect_language("how many fire pokemon are there?") == "en"


def test_detect_language_defaults_to_pt_when_no_markers_match():
    assert detect_language("pikachu raichu charizard") == "pt"


def test_admins_intent_true_for_staff_question():
    assert admins_intent("como falo com um admin?") is True
    assert admins_intent("quem é a staff do servidor?") is True


def test_admins_intent_false_for_a_pokemon_question():
    assert admins_intent("onde nasce o pikachu?") is False


def test_facts_intent_true_when_a_type_axis_is_named():
    assert facts_intent("quantos do tipo fogo?", _FACTS) is True


def test_facts_intent_true_when_a_category_axis_is_named():
    assert facts_intent("quais lendários existem?", _FACTS) is True


def test_facts_intent_false_for_a_bare_list_request_without_axis():
    # "quais" is a listing cue but names no facts axis -> stays out of facts.
    assert facts_intent("quais comandos tem no market?", _FACTS) is False


def test_facts_intent_false_for_a_plain_guide_question():
    assert facts_intent("o market cobra taxa?", _FACTS) is False


def test_facts_intent_false_for_descriptive_axis_query_without_count_cue():
    # Regression (Fase 9): "fogo" matches a type axis, but this is a descriptive
    # spawn question, not a count/list — the filter tool has no biome param, so
    # it must fall through to RAG over the cards, not the facts gate.
    assert facts_intent("pokemon de fogo que nasce no deserto", _FACTS) is False
