"""Entrypoint: regenerate every card from the source data (offline)."""

import os

from card_builder.builder import build_all

_BASE_DIR = os.path.join("guide", "pokemons-db")


def main() -> None:
    build_all(_BASE_DIR)


if __name__ == "__main__":
    main()
