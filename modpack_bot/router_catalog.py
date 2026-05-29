"""Builds the router's file catalog from each guide's own headings.

The router used to choose a guide by reading a hand-written summary in core.md.
That summary drifts from the file: a section the author forgot to mention (e.g.
market.md's "Comandos") never matched, so the question fell through to the
fallback. Deriving the catalog from the guides' `##` headings keeps routing
coverage in sync with the content — a new section is routable the moment it
exists, with no prompt edit.
"""

from typing import Callable

# Token in core.md the Router swaps for the generated catalog.
CATALOG_PLACEHOLDER = "{{ARQUIVOS}}"


def guide_outline(text: str) -> tuple[str, list[str]]:
    """(title, level-2 topics) parsed from a guide's markdown.

    Title is the first `# ` line; topics are every `## ` heading (the routable
    sections). Deeper `###` headings and the title line are left out.

    Example:
        >>> guide_outline("# Title\\n\\n## Alpha\\n\\n### sub\\n\\n## Beta\\n")
        ('Title', ['Alpha', 'Beta'])
    """
    title = ""
    topics: list[str] = []
    for line in text.splitlines():
        if line.startswith("## "):
            topics.append(line[3:].strip())
        elif not title and line.startswith("# "):
            title = line[2:].strip()
    return title, topics


def catalog_entry(file_name: str, text: str) -> str:
    """One router-catalog bullet describing a guide by its title and sections.

    Example:
        >>> catalog_entry("x.md", "# Title\\n\\n## A\\n\\n## B\\n")
        '- **x.md** — Title. Seções: A; B.'
    """
    title, topics = guide_outline(text)
    return f"- **{file_name}** — {title}. Seções: {'; '.join(topics)}."


def build_catalog(file_names: tuple[str, ...], load_guide: Callable[[str], str]) -> str:
    """The '## Arquivos disponíveis' body, one bullet per guide, in order."""
    return "\n".join(catalog_entry(name, load_guide(name)) for name in file_names)
