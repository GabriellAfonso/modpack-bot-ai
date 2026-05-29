from modpack_bot.text import normalize_tokens, wants_full_list


def test_normalize_strips_accents_and_lowercases():
    assert normalize_tokens("Mr. Mime é Psíquico") == ["mr", "mime", "e", "psiquico"]


def test_normalize_keeps_digits_drops_punctuation():
    assert normalize_tokens("hp-100!!") == ["hp", "100"]


def test_normalize_empty():
    assert normalize_tokens("???") == []


def test_wants_full_list_true_for_explicit_request():
    assert wants_full_list("lista todos os biomas") is True
    assert wants_full_list("list all of them") is True


def test_wants_full_list_false_for_normal_question():
    assert wants_full_list("onde acho pikachu?") is False
