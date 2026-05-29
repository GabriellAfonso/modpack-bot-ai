"""Pure text helpers shared by detection and routing."""

import re
import unicodedata

# Explicit request for a full list (e.g. "lista todos os biomas", "completo").
_FULL_LIST_PATTERN = re.compile(
    r"\b(todos|todas|complet[oa]s?|lista(r|\b)|liste|list all|all of them|every|inteir)",
    re.IGNORECASE,
)


def normalize_tokens(text: str) -> list[str]:
    """Lowercase, accent-stripped, alphanumeric chunks only.

    Example:
        >>> normalize_tokens("Mr. Mime é Psíquico")
        ['mr', 'mime', 'e', 'psiquico']
    """
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.findall(r"[a-z0-9]+", text.lower())


def wants_full_list(message: str) -> bool:
    """True when the user explicitly asks for a complete/full listing.

    Example:
        >>> wants_full_list("lista todos os biomas")
        True
    """
    return bool(_FULL_LIST_PATTERN.search(message))
