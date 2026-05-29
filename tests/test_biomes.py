from card_builder.biomes import ANY_SURFACE_BIOME, load_biomes, resolve_biome
from card_builder.context import RenderContext, RenderOptions

_BIOME_MAP = """## #cobblemon:is_forest
- **Vanilla:** Forest, Birch Forest, Dark Forest, Flower Forest, Old Growth Birch Forest, Taiga

## #cobblemon:is_overworld
- Algo TODOS os biomas da superfície
"""


def _write_map(tmp_path):
    path = tmp_path / "biome_map.md"
    path.write_text(_BIOME_MAP, encoding="utf-8")
    return load_biomes(str(path))


def test_load_reads_vanilla_and_special(tmp_path):
    biomes = _write_map(tmp_path)
    assert biomes["#cobblemon:is_forest"].startswith("Forest, Birch Forest")
    assert biomes["#cobblemon:is_overworld"] == ANY_SURFACE_BIOME


def test_missing_file_returns_empty():
    assert load_biomes("/no/such/biome_map.md") == {}


def test_resolve_truncates_to_max_biomes(tmp_path):
    biomes = _write_map(tmp_path)
    ctx = RenderContext(biomes, RenderOptions(full=False, max_biomes=2))
    assert resolve_biome("#cobblemon:is_forest", ctx) == "Forest, Birch Forest…"


def test_resolve_full_keeps_everything(tmp_path):
    biomes = _write_map(tmp_path)
    ctx = RenderContext(biomes, RenderOptions(full=True))
    resolved = resolve_biome("#cobblemon:is_forest", ctx)
    assert resolved.endswith("Taiga") and "…" not in resolved


def test_resolve_unmapped_tag_falls_back_to_clean_name():
    ctx = RenderContext({}, RenderOptions())
    assert resolve_biome("othermod:is_lava_cave", ctx) == "lava cave"
