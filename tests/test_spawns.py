from card_builder.context import RenderContext, RenderOptions
from card_builder.spawns import render_spawn, spawn_block

_CTX = RenderContext({"#mod:is_forest": "Forest"}, RenderOptions())


def test_render_spawn_combines_biome_and_time():
    spawn = {"bucket": "common", "level": "5-10",
             "condition": {"biomes": ["#mod:is_forest"], "timeRange": "night"}}
    assert render_spawn(spawn, _CTX) == "- [common] Forest, de noite — nível 5-10"


def test_render_spawn_without_conditions():
    spawn = {"bucket": "rare", "level": 20, "condition": {}}
    assert render_spawn(spawn, _CTX) == "- [rare] condições variadas — nível 20"


def test_render_spawn_needed_blocks_and_sky():
    spawn = {"bucket": "common", "level": 5,
             "condition": {"canSeeSky": False, "neededNearbyBlocks": ["minecraft:lava"]}}
    assert render_spawn(spawn, _CTX) == "- [common] sem ver o céu, perto de Lava — nível 5"


def test_spawn_block_dedupes_identical_lines():
    spawn = {"bucket": "common", "level": 5, "condition": {"biomes": ["#mod:is_forest"]}}
    index = {"poke": [spawn, dict(spawn)]}  # two identical entries
    block = spawn_block("poke", index, _CTX)
    assert block == "- [common] Forest — nível 5"
    assert block.count("\n") == 0  # collapsed to one line


def test_spawn_block_truncates_to_max_lines():
    index = {"poke": [
        {"bucket": "a", "level": 1, "condition": {}},
        {"bucket": "b", "level": 2, "condition": {}},
        {"bucket": "c", "level": 3, "condition": {}},
    ]}
    ctx = RenderContext({}, RenderOptions(full=False, max_spawn_lines=2))
    block = spawn_block("poke", index, ctx)
    assert "+1 condições" in block
    assert block.count("- [") == 2  # only 2 spawn lines kept; extra note has no bucket


def test_spawn_block_none_when_no_spawns():
    assert spawn_block("missing", {}, _CTX) is None
