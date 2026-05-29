"""Filesystem repositories for the text guides and the Pokémon cards.

These are the only runtime modules that read from disk. The Responder depends
on them by their public methods, so tests substitute in-memory fakes.
"""

import os

# Ordered so the generated router catalog is deterministic; VALID_GUIDES is the
# membership check derived from it.
ROUTABLE_GUIDES = ("market.md", "rules.md", "wikigui.md", "faq.md", "facts.md")
VALID_GUIDES = frozenset(ROUTABLE_GUIDES)


class GuideRepository:
    """Reads the routed guide files (core.md plus the routable guides)."""

    def __init__(self, content_dir: str) -> None:
        self._content_dir = content_dir

    def load_core(self) -> str:
        """The router system prompt; read fresh so edits don't need a restart."""
        return self._read("core.md")

    def load_guide(self, name: str) -> str:
        """Read one routable guide (market.md / rules.md / wikigui.md)."""
        if name not in VALID_GUIDES:
            raise ValueError(f"unknown guide {name!r}, expected one of {sorted(VALID_GUIDES)}")
        return self._read(name)

    def _read(self, name: str) -> str:
        with open(os.path.join(self._content_dir, name), "r", encoding="utf-8") as file:
            return file.read()


class CardRepository:
    """Reads the pre-generated per-Pokémon cards.

    The card file stems under species_cards/ are the source of truth for what
    is (and isn't) a Pokémon — an in-memory lookup that costs 0 tokens.
    """

    def __init__(self, content_dir: str) -> None:
        base = os.path.join(content_dir, "pokemons-db")
        self._slim_dir = os.path.join(base, "species_cards")
        self._full_dir = os.path.join(base, "species_cards_full")

    def pokemon_names(self) -> frozenset[str]:
        """Canonical set of Pokémon names (the slim card file stems)."""
        return frozenset(f[:-3] for f in os.listdir(self._slim_dir) if f.endswith(".md"))

    def load_card(self, name: str, full: bool = False) -> str | None:
        """Read a Pokémon's card. full=True uses the untruncated version (on
        request); falls back to the slim one if the full is missing."""
        directories = [self._full_dir, self._slim_dir] if full else [self._slim_dir]
        for directory in directories:
            path = os.path.join(directory, name + ".md")
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as file:
                    return file.read()
        return None
