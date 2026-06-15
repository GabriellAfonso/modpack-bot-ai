import httpx
from groq import APIConnectionError, APIStatusError, BadRequestError, RateLimitError

from modpack_bot.errors import error_reply

_REQUEST = httpx.Request("POST", "https://api.groq.com/openai/v1/chat/completions")


def _status_error(cls, status: int, body: object | None):
    """Build a real Groq status error around a fake httpx response."""
    return cls("boom", response=httpx.Response(status, request=_REQUEST), body=body)


def test_context_overflow_400_asks_to_rephrase_pt():
    error = _status_error(BadRequestError, 400, {"error": {"code": "context_length_exceeded"}})
    reply = error_reply(error, "pt")
    assert "longa demais" in reply
    assert "reformular" in reply


def test_context_overflow_400_asks_to_rephrase_en():
    error = _status_error(BadRequestError, 400, {"error": {"code": "context_length_exceeded"}})
    assert "too long" in error_reply(error, "en")


def test_request_too_large_413_is_treated_as_too_long():
    # 413 carries no dedicated Groq class; we classify it by status code.
    error = _status_error(APIStatusError, 413, None)
    assert "longa demais" in error_reply(error, "pt")


def test_rate_limit_tells_player_to_wait():
    error = _status_error(RateLimitError, 429, {"error": {"code": "rate_limit_exceeded"}})
    assert "limite" in error_reply(error, "pt")
    assert "Wait" in error_reply(error, "en")


def test_connection_error_says_ai_unreachable():
    error = APIConnectionError(request=_REQUEST)
    assert "falar com a IA" in error_reply(error, "pt")
    assert "reach the AI" in error_reply(error, "en")


def test_other_400_without_overflow_code_stays_generic():
    error = _status_error(BadRequestError, 400, {"error": {"code": "tool_use_failed"}})
    assert error_reply(error, "pt") == "Ocorreu um erro, tenta de novo!"


def test_unknown_exception_falls_back_to_generic():
    assert error_reply(ValueError("nope"), "en") == "Something went wrong, please try again!"


def test_unknown_language_falls_back_to_portuguese():
    assert error_reply(ValueError("nope"), "de") == "Ocorreu um erro, tenta de novo!"
