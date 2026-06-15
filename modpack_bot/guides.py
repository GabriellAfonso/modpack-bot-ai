"""Filesystem repositories for the text guides and the Pokémon cards.

These are the only runtime modules that read from disk. The Responder depends
on them by their public methods, so tests substitute in-memory fakes.
"""

import os


class GuideRepository:
    """Reads a guide file at runtime.

    Since the RAG migration only facts.md is read directly (for the facts gate);
    the other guides reach the answer model through the retrieved index instead.
    Read fresh on each call so editing a guide needs no restart.
    """

    def __init__(self, content_dir: str) -> None:
        self._content_dir = content_dir

    def load_guide(self, name: str) -> str:
        """Read a guide file by name (e.g. facts.md for the facts gate)."""
        with open(os.path.join(self._content_dir, name), "r", encoding="utf-8") as file:
            return file.read()

    def load_guides(self, names: list[str]) -> str:
        """Concatenate several guide files in order (e.g. the Flan claim set).

        Lets a gate inject a curated multi-file guide as one context blob; the
        caller picks which files (and keeps the list short enough for the prompt).
        """
        return "\n\n".join(self.load_guide(name) for name in names)


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
