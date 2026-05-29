from modpack_bot.text import collapse_blank_lines, normalize_tokens, wants_full_list


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


def test_collapse_blank_lines_reduces_runs_to_one_blank():
    assert collapse_blank_lines("154 do tipo Água.\n\n\n\nExistem 890.") == (
        "154 do tipo Água.\n\nExistem 890."
    )


def test_collapse_blank_lines_handles_whitespace_only_lines():
    assert collapse_blank_lines("a\n  \n\t\nb") == "a\n\nb"


def test_collapse_blank_lines_keeps_single_newline_and_trims():
    assert collapse_blank_lines("  a\nb  ") == "a\nb"
