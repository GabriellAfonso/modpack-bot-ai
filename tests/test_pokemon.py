from modpack_bot.pokemon import detect_pokemon

NAMES = frozenset({"pikachu", "mrmime", "hooh", "charizard"})


def test_direct_token_match():
    assert detect_pokemon("onde acho pikachu?", NAMES) == "pikachu"


def test_bigram_match_joins_adjacent_words():
    assert detect_pokemon("como evoluo o mr mime", NAMES) == "mrmime"


def test_fuzzy_match_fixes_typo():
    assert detect_pokemon("info do pikachuu", NAMES) == "pikachu"


def test_no_match_returns_none():
    assert detect_pokemon("onde fica a vila", NAMES) is None


def test_short_token_is_not_fuzzy_matched():
    # "hoh" (len 3) must not fuzzy-match "hooh"; below the min length.
    assert detect_pokemon("hoh", NAMES) is None
