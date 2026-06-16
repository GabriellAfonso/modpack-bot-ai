from card_builder.context import Json
from card_builder.rankings import build_rankings

# Three full species + one missing a stat. Arceus has the highest total and the
# highest single stats; Ninjask is fastest; the malformed entry must be skipped.
_SPECIES: list[tuple[str, Json]] = [
    ("arceus", {"name": "Arceus", "baseStats": {
        "hp": 120, "attack": 120, "defence": 120,
        "special_attack": 120, "special_defence": 120, "speed": 120}}),
    ("ninjask", {"name": "Ninjask", "baseStats": {
        "hp": 61, "attack": 90, "defence": 45,
        "special_attack": 50, "special_defence": 50, "speed": 160}}),
    ("snorlax", {"name": "Snorlax", "baseStats": {
        "hp": 160, "attack": 110, "defence": 65,
        "special_attack": 65, "special_defence": 110, "speed": 30}}),
    ("broken", {"name": "Broken", "baseStats": {"hp": 1}}),
]


def _section(markdown: str, heading: str) -> list[str]:
    """The entry lines under '## heading' (up to the next blank line)."""
    block = markdown.split(f"## {heading}\n\n", 1)[1].split("\n\n", 1)[0]
    return block.splitlines()


def test_total_section_ranks_by_bst_descending():
    markdown = build_rankings(_SPECIES)
    first = _section(markdown, "Total (BST)")[0]
    assert first.startswith("1. Arceus — 720")


def test_total_entries_include_the_full_stat_breakdown():
    markdown = build_rankings(_SPECIES)
    first = _section(markdown, "Total (BST)")[0]
    assert "(HP 120 / Atk 120 / Def 120 / SpA 120 / SpD 120 / Spd 120)" in first


def test_speed_section_puts_the_fastest_first():
    markdown = build_rankings(_SPECIES)
    first = _section(markdown, "Velocidade")[0]
    assert first == "1. Ninjask — 160"


def test_hp_section_puts_the_bulkiest_first():
    markdown = build_rankings(_SPECIES)
    assert _section(markdown, "HP")[0] == "1. Snorlax — 160"


def test_species_missing_a_base_stat_is_skipped():
    markdown = build_rankings(_SPECIES)
    assert "Broken" not in markdown


def test_every_stat_section_is_rendered():
    markdown = build_rankings(_SPECIES)
    for heading in ("Total (BST)", "HP", "Ataque", "Defesa",
                    "Ataque Especial", "Defesa Especial", "Velocidade"):
        assert f"## {heading}\n" in markdown


def test_ranking_is_capped_to_top_fifteen():
    many: list[tuple[str, Json]] = [
        (f"m{i}", {"name": f"M{i}", "baseStats": {
            "hp": i, "attack": i, "defence": i,
            "special_attack": i, "special_defence": i, "speed": i}})
        for i in range(40)
    ]
    assert len(_section(build_rankings(many), "Total (BST)")) == 15
