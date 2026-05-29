from card_builder.card import build_card
from card_builder.context import BuildContext, RenderContext, RenderOptions

_SPECIES = {
    "name": "Pikachu",
    "nationalPokedexNumber": 25,
    "primaryType": "electric",
    "baseStats": {"hp": 35, "attack": 55, "defence": 40,
                  "special_attack": 50, "special_defence": 50, "speed": 90},
    "abilities": ["static", "h:lightning_rod"],
    "catchRate": 190,
    "evYield": {"speed": 2},
    "eggGroups": ["field", "fairy"],
    "drops": {"entries": [{"item": "cobblemon:thunder_stone", "percentage": 5}]},
    "evolutions": [{"variant": "item_interact",
                    "requiredContext": "cobblemon:thunder_stone", "result": "raichu"}],
    "forms": [],
}


def _build(spawn_index=None, pre_evolutions=None):
    ctx = BuildContext(RenderContext({}, RenderOptions()), spawn_index or {}, pre_evolutions or {})
    return build_card(_SPECIES, "pikachu", ctx)


def test_header_with_pokedex_and_type():
    assert _build().startswith("# Pikachu  (#25 · Elétrico)")


def test_stats_line_present():
    assert "Stats base: HP 35 / Atk 55 / Def 40 / SpA 50 / SpD 50 / Spd 90" in _build()


def test_weakness_line():
    assert "Fraco contra: 2x Terra" in _build()


def test_abilities_mark_hidden():
    assert "Habilidades: Static, Lightning Rod (oculta)" in _build()


def test_meta_and_drops():
    card = _build()
    assert "Catch rate: 190 · EV yield: 2 Spd · Egg groups: Field, Fairy" in card
    assert "Drops: Thunder Stone (5%)" in card


def test_spawn_section_falls_back_when_no_spawns():
    assert "## Spawn\n- Não nasce naturalmente" in _build()


def test_forward_evolution_section():
    assert "## Evolui em\n- Raichu — usar Thunder Stone" in _build()


def test_pre_evolution_section_when_indexed():
    card = _build(pre_evolutions={"pikachu": [("Pichu", "subir de nível (amizade ≥160)")]})
    assert "## Evolui de\n- Pichu — subir de nível (amizade ≥160)" in card


def test_detail_footer():
    assert _build().endswith("_Mais detalhes (golpes, TMs, EVs completos): `/pwiki pikachu`._")
