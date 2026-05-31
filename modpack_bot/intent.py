"""Deterministic intent gates that run before the RAG fallback (plan.md §4, §8).

No LLM: language is a stopword heuristic, the admin and facts gates are token /
index matches. Keeps the common path at one Groq call (the answer) instead of
two (the old router + answer).
"""

from modpack_bot.facts_index import matched_facts_lines
from modpack_bot.text import normalize_tokens, wants_full_list

# Distinctive function words only; the ambiguous ones shared by PT and EN
# ("a", "do", "to") are left out so they don't cancel each other's signal.
_PT_MARKERS = frozenset(
    {
        "que", "qual", "quais", "como", "onde", "quanto", "quantos", "quantas",
        "tem", "pra", "para", "nao", "com", "voce", "vc", "isso", "qto", "sao",
    }
)
_EN_MARKERS = frozenset(
    {
        "the", "is", "are", "what", "which", "how", "does", "where", "can",
        "you", "your", "with", "for", "many", "much", "there", "about",
    }
)

# Includes bare "mod"/"mods" per plan.md §6 (decision confirmed during build).
_ADMIN_MARKERS = frozenset(
    {
        "admin", "admins", "adm", "staff", "moderacao", "moderador",
        "moderadores", "moderator", "moderators", "mod", "mods",
    }
)

# Counting words; the listing words ("quais", "todos", "lista", "which"...) are
# already covered by wants_full_list, so they are not duplicated here.
_COUNT_MARKERS = frozenset({"quantos", "quantas", "quanto", "qtos", "qto", "total", "numero"})

_DEFAULT_LANGUAGE = "pt"


def detect_language(message: str) -> str:
    """"pt" or "en" by counting distinctive stopwords; ties default to pt.

    Example:
        >>> detect_language("how many fire pokemon are there?")
        'en'
        >>> detect_language("quantos pokemon de fogo tem?")
        'pt'
    """
    tokens = set(normalize_tokens(message))
    english = len(tokens & _EN_MARKERS)
    portuguese = len(tokens & _PT_MARKERS)
    return "en" if english > portuguese else _DEFAULT_LANGUAGE


def admins_intent(message: str) -> bool:
    """True when the player asks how to reach an admin / staff member.

    Example:
        >>> admins_intent("como falo com um admin?")
        True
        >>> admins_intent("onde nasce o pikachu?")
        False
    """
    return bool(set(normalize_tokens(message)) & _ADMIN_MARKERS)


def facts_intent(message: str, facts: str) -> bool:
    """True when the message is a counting/listing question about a facts axis.

    BOTH conditions are required (decision confirmed during Fase 9):
    - it asks to count or list ("quantos"/"quais"/"lista"/"todos"...), and
    - it names a facts.md axis (a type, item, or category).

    The conjunction keeps two kinds of question out of the facts path:
    - "quais comandos do market" — a cue but no axis -> RAG over the guide.
    - "pokemon de fogo que nasce no deserto" — a type axis but no counting cue:
      a descriptive query the filter tool can't satisfy (it has no biome param),
      so it must fall through to RAG over the cards (plan.md §4/§7 flagship case).

    Example:
        >>> # facts_intent("quantos do tipo fogo?", facts_md) is True when
        >>> # facts_md has a "Fogo" line under "## Pokémon por tipo".
    """
    if not _asks_count_or_list(message):
        return False
    return bool(matched_facts_lines(message, facts))


def _asks_count_or_list(message: str) -> bool:
    """A counting or listing question — the only shape the facts gate claims."""
    if wants_full_list(message):
        return True
    tokens = set(normalize_tokens(message))
    if tokens & _COUNT_MARKERS:
        return True
    return "how" in tokens and "many" in tokens
