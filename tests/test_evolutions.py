import json

from card_builder.context import RenderContext, RenderOptions
from card_builder.evolutions import (
    index_pre_evolutions,
    render_evolution,
    render_method,
    render_requirement,
)

_CTX = RenderContext({"#mod:is_forest": "Forest"}, RenderOptions())


def test_requirement_level():
    assert render_requirement({"variant": "level", "minLevel": 16}, _CTX) == "nível 16+"


def test_requirement_friendship():
    assert render_requirement({"variant": "friendship", "amount": 160}, _CTX) == "amizade ≥160"


def test_requirement_static_phrase():
    assert render_requirement({"variant": "weather"}, _CTX) == "com tempo específico"


def test_requirement_biome_uses_map():
    assert render_requirement({"variant": "biome", "biomeCondition": "#mod:is_forest"}, _CTX) == "em Forest"


def test_method_item_interact():
    evo = {"variant": "item_interact", "requiredContext": "cobblemon:water_stone"}
    assert render_method(evo, _CTX) == "usar Water Stone"


def test_method_level_up_with_requirements():
    evo = {"variant": "level_up", "requirements": [{"variant": "level", "minLevel": 36}]}
    assert render_method(evo, _CTX) == "subir de nível (nível 36+)"


def test_render_evolution_line():
    evo = {"variant": "trade", "result": "alakazam"}
    assert render_evolution(evo, _CTX) == "- Alakazam — trocar"


def test_index_pre_evolutions_reverses_links(tmp_path):
    species_dir = tmp_path / "species"
    species_dir.mkdir()
    eevee = {"name": "Eevee", "evolutions": [
        {"variant": "item_interact", "requiredContext": "cobblemon:water_stone", "result": "vaporeon"}]}
    (species_dir / "eevee.json").write_text(json.dumps(eevee), encoding="utf-8")
    (species_dir / "vaporeon.json").write_text(json.dumps({"name": "Vaporeon"}), encoding="utf-8")

    pre = index_pre_evolutions(str(species_dir), {"eevee", "vaporeon"}, _CTX)
    assert pre["vaporeon"] == [("Eevee", "usar Water Stone")]
