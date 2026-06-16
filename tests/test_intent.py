from modpack_bot.intent import (
    admins_intent,
    claim_intent,
    detect_language,
    facts_intent,
    spawn_help_intent,
)

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


def test_admins_intent_false_for_a_game_mod_question():
    # "mod" means a game mod in a modpack bot, not a moderator: a mod-name
    # question must not hit the staff redirect (regression for the cobble
    # safari / zekrom follow-up failure).
    assert admins_intent("me da um resumo do mod cobble safari") is False
    assert admins_intent("o que faz o mod cobble safari?") is False


def test_claim_intent_true_for_chest_protection_questions():
    assert claim_intent("como faço pra ngm roubar meu bau?") is True
    assert claim_intent("como faço pra proteger meu baú?") is True
    assert claim_intent("mas e o mod flan?") is True


def test_claim_intent_false_for_a_pokemon_question():
    assert claim_intent("onde nasce o pikachu?") is False


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


def test_facts_intent_true_for_drop_query_with_untranslated_pt_item():
    # "osso" never matches the English "Bone" line verbatim; the drop verb routes
    # it to the tool path (which translates the item) instead of RAG.
    assert facts_intent("quais pokemons dropam osso?", _FACTS) is True


def test_facts_intent_true_for_drop_query_even_without_listing_word():
    assert facts_intent("quantos pokemon largam slime?", _FACTS) is True


def test_facts_intent_false_for_drop_verb_without_count_or_list_cue():
    # A drop verb alone is not enough — it must still be a count/list question.
    assert facts_intent("como faço pra dropar osso?", _FACTS) is False


def test_facts_intent_false_for_gacha_prize_drop_question():
    # "dropar ... no gacha" is a machine-prize question for RAG, not the Pokémon
    # item-drop tool (which would wrongly answer "nenhum Pokémon corresponde").
    assert facts_intent("quais as chances de dropar master ball no gacha?", _FACTS) is False


def test_facts_intent_false_for_capsule_drop_question():
    assert facts_intent("quais cápsulas dropam master ball?", _FACTS) is False


def test_spawn_help_intent_true_for_nameless_spawn_question():
    assert spawn_help_intent("como descubro onde um pokemon spawna?") is True
    assert spawn_help_intent("onde encontro um pokemon?") is True


def test_spawn_help_intent_false_without_pokemon_word():
    # "onde fica o market" has a location cue but is not about finding a Pokémon.
    assert spawn_help_intent("onde fica o market?") is False


def test_spawn_help_intent_false_without_a_spawn_or_find_verb():
    assert spawn_help_intent("qual o melhor pokemon do jogo?") is False
