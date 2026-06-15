"""Maps a runtime exception into a helpful, player-facing message (pt/en).

The Discord edge would otherwise reply with a bare "an error occurred"; instead
we recognise the failures a player can act on — a question too long for the
model's context window, or the AI being momentarily rate-limited — and tell them
what to do about it. Anything we don't recognise still gets a generic line.
"""

from groq import APIConnectionError, APIStatusError, BadRequestError, RateLimitError

from modpack_bot.llm import groq_error_code

# Groq signals an over-budget request either as a 400 with this code or as a
# bare 413 (Request Entity Too Large) with no dedicated exception class.
_CONTEXT_OVERFLOW_CODE = "context_length_exceeded"
_REQUEST_TOO_LARGE_STATUS = 413

_TOO_LONG = {
    "pt": (
        "Sua pergunta ficou longa demais pro meu limite. Tenta reformular de forma mais curta e "
        "específica que eu consigo responder!"
    ),
    "en": (
        "Your question is too long for my limit. Try rephrasing it shorter and more specific and "
        "I'll be able to answer!"
    ),
}
_RATE_LIMITED = {
    "pt": "Tô recebendo muita pergunta agora e bati meu limite. Espera alguns segundos e manda de novo!",
    "en": "I'm getting a lot of questions right now and hit my limit. Wait a few seconds and ask again!",
}
_UNAVAILABLE = {
    "pt": "Não consegui falar com a IA agora. Tenta de novo daqui a pouco!",
    "en": "I couldn't reach the AI right now. Please try again in a moment!",
}
_GENERIC = {
    "pt": "Ocorreu um erro, tenta de novo!",
    "en": "Something went wrong, please try again!",
}


def error_reply(error: Exception, language: str) -> str:
    """Pick the most helpful message for `error`, defaulting to the generic line.

    Example:
        >>> error_reply(ValueError("boom"), "en")
        'Something went wrong, please try again!'
    """
    catalogue = _catalogue_for(error)
    return catalogue.get(language, catalogue["pt"])


def _catalogue_for(error: Exception) -> dict[str, str]:
    """Classify the failure into one of the player-facing message catalogues."""
    if _is_context_overflow(error):
        return _TOO_LONG
    if isinstance(error, RateLimitError):
        return _RATE_LIMITED
    if isinstance(error, APIConnectionError):  # covers APITimeoutError
        return _UNAVAILABLE
    return _GENERIC


def _is_context_overflow(error: Exception) -> bool:
    """True when the request exceeded the model's token/size limit."""
    if isinstance(error, BadRequestError) and groq_error_code(error) == _CONTEXT_OVERFLOW_CODE:
        return True
    return isinstance(error, APIStatusError) and error.status_code == _REQUEST_TOO_LARGE_STATUS
