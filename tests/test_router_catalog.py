"""router_catalog: outline parsing and catalog assembly from guide headings."""

from modpack_bot.router_catalog import build_catalog, catalog_entry, guide_outline


def test_guide_outline_takes_title_and_level_two_headings_only():
    text = "# The Title\n\nintro\n\n## Alpha\n\ntext\n\n### nested\n\n## Beta\n"
    assert guide_outline(text) == ("The Title", ["Alpha", "Beta"])


def test_guide_outline_handles_no_headings():
    assert guide_outline("just prose, no headings") == ("", [])


def test_catalog_entry_joins_title_and_sections():
    entry = catalog_entry("market.md", "# Market\n\n## Comandos\n\n## Como Vender\n")
    assert entry == "- **market.md** — Market. Seções: Comandos; Como Vender."


def test_build_catalog_keeps_file_order():
    guides = {
        "a.md": "# A\n\n## One\n",
        "b.md": "# B\n\n## Two\n",
    }
    out = build_catalog(("a.md", "b.md"), guides.__getitem__)
    assert out == (
        "- **a.md** — A. Seções: One.\n"
        "- **b.md** — B. Seções: Two."
    )
