"""Thin entrypoint shim — keeps `python build_cards.py` working.

The generator now lives in the card_builder package; this just delegates to it.
Run either `python build_cards.py` or `python -m card_builder`.
"""

from card_builder.__main__ import main

if __name__ == "__main__":
    main()
