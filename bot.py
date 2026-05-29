"""Thin entrypoint shim — keeps `python bot.py` working.

The bot now lives in the modpack_bot package; this just delegates to it.
Run either `python bot.py` or `python -m modpack_bot`.
"""

from modpack_bot.__main__ import main

if __name__ == "__main__":
    main()
