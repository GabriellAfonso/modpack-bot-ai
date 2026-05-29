"""Deterministic Pokémon-name detection (no LLM, 0 tokens)."""

import difflib

from modpack_bot.text import normalize_tokens

_MIN_FUZZY_LEN = 4
_FUZZY_CUTOFF = 0.85


def detect_pokemon(message: str, names: frozenset[str]) -> str | None:
    """Find a Pokémon name in the message, or None if there isn't one.

    Normalizes the same way as the card file names (mrmime, hooh, tapukoko...).
    Joins adjacent word pairs ('mr mime' -> 'mrmime') and, as a last step, tries
    a conservative fuzzy match for typos ('pikachuu' -> 'pikachu').

    `names` is the canonical set (the card file stems), injected so the function
    stays pure and testable.

    Example:
        >>> detect_pokemon("onde acho pikachu?", frozenset({"pikachu"}))
        'pikachu'
    """
    tokens = normalize_tokens(message)
    bigrams = [a + b for a, b in zip(tokens, tokens[1:])]
    for candidate in bigrams + tokens:  # bigram first (longest match)
        if candidate in names:
            return candidate
    return _fuzzy_match(tokens, names)


def _fuzzy_match(tokens: list[str], names: frozenset[str]) -> str | None:
    """Conservative typo match: only longer tokens, high cutoff."""
    for token in tokens:
        if len(token) < _MIN_FUZZY_LEN:
            continue
        close = difflib.get_close_matches(token, names, n=1, cutoff=_FUZZY_CUTOFF)
        if close:
            return close[0]
    return None
