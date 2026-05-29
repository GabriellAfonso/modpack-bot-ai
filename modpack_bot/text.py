"""Pure text helpers shared by detection and routing."""

import re
import unicodedata

# Explicit request for a full list (e.g. "lista todos os biomas", "completo").
_FULL_LIST_PATTERN = re.compile(
    r"\b(todos|todas|complet[oa]s?|lista(r|\b)|liste|list all|all of them|every|inteir"
    r"|quais|which)",
    re.IGNORECASE,
)

# A run of two or more newlines (blank-only lines allowed between them).
_BLANK_LINE_RUN = re.compile(r"\n[ \t]*(?:\n[ \t]*)+")


def normalize_tokens(text: str) -> list[str]:
    """Lowercase, accent-stripped, alphanumeric chunks only.

    Example:
        >>> normalize_tokens("Mr. Mime é Psíquico")
        ['mr', 'mime', 'e', 'psiquico']
    """
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.findall(r"[a-z0-9]+", text.lower())


def collapse_blank_lines(text: str) -> str:
    """Collapse runs of blank lines into a single blank line.

    The answer model is told to separate topics with a blank line but is not
    consistent — it sometimes emits several. This forces exactly one empty line
    between paragraphs (max two consecutive newlines) and trims the edges.

    Example:
        >>> collapse_blank_lines("154 do tipo Água.\\n\\n\\n\\nExistem 890.")
        '154 do tipo Água.\\n\\nExistem 890.'
    """
    return _BLANK_LINE_RUN.sub("\n\n", text.strip())


def wants_full_list(message: str) -> bool:
    """True when the user explicitly asks for a complete/full listing.

    Example:
        >>> wants_full_list("lista todos os biomas")
        True
    """
    return bool(_FULL_LIST_PATTERN.search(message))
