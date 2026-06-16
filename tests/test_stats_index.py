from modpack_bot.stats_index import select_stats_ranking, stat_section_for

_STATS = (
    "# Ranking de Stats\n"
    "\n"
    "## Total (BST)\n"
    "\n"
    "1. Arceus — 720 (HP 120 / Atk 120 / Def 120 / SpA 120 / SpD 120 / Spd 120)\n"
    "\n"
    "## Ataque\n"
    "\n"
    "1. Rampardos — 165\n"
    "\n"
    "## Ataque Especial\n"
    "\n"
    "1. Deoxys — 180\n"
    "\n"
    "## Velocidade\n"
    "\n"
    "1. Regieleki — 200\n"
)


def test_strongest_maps_to_the_bst_total():
    assert stat_section_for("qual o pokemon mais forte?") == "Total (BST)"


def test_highest_stats_question_maps_to_the_total():
    assert stat_section_for("qual pokemon com stats mais altos?") == "Total (BST)"


def test_fastest_maps_to_speed():
    assert stat_section_for("qual o pokemon mais rápido?") == "Velocidade"


def test_attack_maps_to_attack():
    assert stat_section_for("qual tem mais ataque?") == "Ataque"


def test_special_promotes_attack_to_special_attack():
    assert stat_section_for("maior ataque especial?") == "Ataque Especial"


def test_special_promotes_defence_to_special_defence():
    assert stat_section_for("qual a maior defesa especial?") == "Defesa Especial"


def test_question_without_a_stat_word_targets_no_section():
    assert stat_section_for("qual a melhor pokébola?") is None


def test_select_returns_only_the_matching_section():
    ranking = select_stats_ranking("qual o mais rápido?", _STATS)
    assert ranking == "## Velocidade\n\n1. Regieleki — 200"


def test_select_returns_none_when_no_stat_named():
    assert select_stats_ranking("qual a melhor base?", _STATS) is None


def test_select_returns_none_when_section_absent():
    assert select_stats_ranking("qual a maior defesa?", _STATS) is None
