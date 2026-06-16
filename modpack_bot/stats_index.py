"""Pick the stat-ranking slice of stats.md a player's message asks about.

stats.md (card_builder.rankings) holds one '## <stat>' top-N section AND one
'## <stat> — Menor' bottom-N section per base stat plus the BST total. The
stats gate (intent.stats_intent) routes a superlative stat question here —
"qual o pokémon mais forte", "qual o mais fraco", "qual o mais rápido" — and
this returns ONLY the matching section (top or bottom), so the answer model
sees a tiny exact ranking instead of the whole file.
"""

from card_builder.rankings import BOTTOM_SUFFIX as _BOTTOM_SUFFIX
from modpack_bot.text import normalize_tokens

# The BST-total section heading, the default for a "strongest/highest stats"
# question that names no specific stat.
_TOTAL_HEADING = "Total (BST)"

# Cue tokens per stat. "especial"/"special" promotes the attack/defence cues to
# their special variant. "melhor" is deliberately NOT a cue: a bare "qual a
# melhor pokébola" names no stat and must fall through to RAG, not the ranking.
_ATTACK_CUES = frozenset({"ataque", "atk", "attack", "ataca"})
_DEFENCE_CUES = frozenset({"defesa", "def", "defense", "defence", "tanque", "tank"})
_SPEED_CUES = frozenset(
    {"velocidade", "veloz", "rapido", "rapida", "agil", "speed", "fast", "fastest"}
)
_HP_CUES = frozenset({"hp", "vida", "vidas", "life", "health"})
_TOTAL_CUES = frozenset(
    {"forte", "fortes", "poderoso", "poderosa", "stats", "stat",
     "strong", "strongest", "powerful", "bst", "total",
     # minimum direction without a specific stat → falls back to BST total
     "fraco", "fraca", "fracos", "fracas", "weak", "weakest",
     "pior", "piores", "worst"}
)

# Tokens that signal the player wants the BOTTOM of the ranking (weakest/lowest).
_WEAKEST_CUES = frozenset(
    {"fraco", "fraca", "fracos", "fracas", "weak", "weakest",
     "pior", "piores", "worst", "menor", "menores", "lowest", "least"}
)
_SPECIAL_CUES = frozenset({"especial", "special"})


def stat_section_for(message: str) -> str | None:
    """The stats.md heading a message targets, or None when it names no stat.

    Example:
        >>> stat_section_for("qual o pokemon mais forte?")
        'Total (BST)'
        >>> stat_section_for("qual o mais rápido?")
        'Velocidade'
        >>> stat_section_for("qual a melhor pokébola?") is None
        True
    """
    tokens = set(normalize_tokens(message))
    special = bool(tokens & _SPECIAL_CUES)
    if tokens & _ATTACK_CUES:
        return "Ataque Especial" if special else "Ataque"
    if tokens & _DEFENCE_CUES:
        return "Defesa Especial" if special else "Defesa"
    if tokens & _SPEED_CUES:
        return "Velocidade"
    if tokens & _HP_CUES:
        return "HP"
    if tokens & _TOTAL_CUES:
        return _TOTAL_HEADING
    return None


def is_weakest_question(message: str) -> bool:
    """True when the player asks for the lowest/weakest end of a ranking.

    Example:
        >>> is_weakest_question("qual o pokemon mais fraco?")
        True
        >>> is_weakest_question("qual o pokemon mais forte?")
        False
    """
    return bool(set(normalize_tokens(message)) & _WEAKEST_CUES)


def select_stats_ranking(message: str, stats_md: str) -> str | None:
    """The matching section of stats.md for the message, or None.

    Returns the top-N section for "strongest/highest" questions and the
    bottom-N section (heading suffixed with BOTTOM_SUFFIX) for
    "weakest/lowest" questions. None when the message targets no stat or
    the section is absent from stats.md (e.g. it was never built).
    """
    heading = stat_section_for(message)
    if heading is None:
        return None
    target = f"{heading}{_BOTTOM_SUFFIX}" if is_weakest_question(message) else heading
    return _section(stats_md, target)


def _section(stats_md: str, heading: str) -> str | None:
    """The block from '## heading' up to the next '## ' (or EOF), trimmed."""
    marker = f"\n## {heading}\n"
    if marker not in stats_md:
        return None
    after = stats_md.split(marker, 1)[1]
    body = after.split("\n## ", 1)[0]
    return f"## {heading}\n{body}".strip()
