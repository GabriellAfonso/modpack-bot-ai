"""Thin entrypoint shim — keeps `python build_index.py` working.

The generator lives in the index_builder package; this just delegates to it.
Run either `python build_index.py` or `python -m index_builder`. Run it after
build_cards.py whenever the cards or any content/*.md changes (plan.md §14).
"""

from index_builder.__main__ import main

if __name__ == "__main__":
    main()
