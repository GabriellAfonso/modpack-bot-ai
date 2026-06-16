"""Pick the stat-ranking slice of stats.md a player's message asks about.

stats.md (card_builder.rankings) holds one '## <stat>' top-N section per base
stat plus the BST total. The stats gate (intent.stats_intent) routes a
superlative stat question here — "qual o pokémon mais forte", "qual o mais
rápido" — and this returns ONLY the matching section, so the answer model sees a
tiny exact ranking instead of the whole file.
"""

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
     "strong", "strongest", "powerful", "bst", "total"}
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


def select_stats_ranking(message: str, stats_md: str) -> str | None:
    """The '## <stat>' section of stats.md the message asks about, or None.

    None when the message targets no stat (the gate should not have routed here)
    or the section is absent from stats.md (e.g. it was never built).
    """
    heading = stat_section_for(message)
    if heading is None:
        return None
    return _section(stats_md, heading)


def _section(stats_md: str, heading: str) -> str | None:
    """The block from '## heading' up to the next '## ' (or EOF), trimmed."""
    marker = f"\n## {heading}\n"
    if marker not in stats_md:
        return None
    after = stats_md.split(marker, 1)[1]
    body = after.split("\n## ", 1)[0]
    return f"## {heading}\n{body}".strip()
