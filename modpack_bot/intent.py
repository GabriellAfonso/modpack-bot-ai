"""Deterministic intent gates that run before the RAG fallback (plan.md §4, §8).

No LLM: language is a stopword heuristic, the admin and facts gates are token /
index matches. Keeps the common path at one Groq call (the answer) instead of
two (the old router + answer).
"""

from card_builder.type_chart import TYPE_PT
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

# Bare "mod"/"mods" were dropped: in a MODPACK bot "mod" overwhelmingly means a
# game mod ("me da um resumo do mod cobble safari"), not a moderator, so the
# marker false-routed every mod-name question to the staff redirect — and a
# follow-up's condense step inherited the word and re-tripped it. The moderator
# sense is still covered by the explicit "moderador"/"moderator" forms.
_ADMIN_MARKERS = frozenset(
    {
        "admin", "admins", "adm", "staff", "moderacao", "moderador",
        "moderadores", "moderator", "moderators",
    }
)

# Counting words; the listing words ("quais", "todos", "lista", "which"...) are
# already covered by wants_full_list, so they are not duplicated here.
_COUNT_MARKERS = frozenset({"quantos", "quantas", "quanto", "qtos", "qto", "total", "numero"})

# Generic "where does a Pokémon spawn / how to find one" cues. A NAMED Pokémon is
# answered earlier from its card (which has a Spawn section); these only fire for
# the nameless version ("como descubro onde um pokemon spawna"), which otherwise
# falls to RAG and collides with the gacha spawn-machine docs (term "spawn").
_SPAWN_VERBS = frozenset(
    {
        "spawn", "spawna", "spawnam", "spawnar", "nasce", "nascem", "encontro",
        "encontrar", "acho", "achar", "acha", "pego", "pegar", "spawns", "find",
    }
)
_POKEMON_WORDS = frozenset({"pokemon", "pokemons", "pokemom", "mon", "bicho", "bichinho"})

# Drop verbs. Item names in facts.md are English ("Bone", "Slime Ball"), so a PT
# query ("quais dropam osso") never matches an item line verbatim. These cues let
# a drop question reach the facts tool path, where the model translates the item
# before calling `filtrar_pokemon` — instead of falling to RAG and dumping the
# whole item-drop section (~5k tokens -> HTTP 413).
_DROP_MARKERS = frozenset(
    {
        "dropa", "dropam", "dropar", "drop", "drops", "dropado", "dropada",
        "dropados", "dropadas", "larga", "largam", "solta", "soltam",
    }
)

# Gacha/casino prize terms. A "drop" question that names one of these is about
# what a gacha MACHINE hands out as a prize, not which Pokémon drops an item on
# death — it belongs to RAG over the gacha guides, not the facts drop tool (the
# tool only knows Pokémon item drops, so it answers "nenhum Pokémon corresponde").
_PRIZE_SOURCE_MARKERS = frozenset(
    {
        "gacha", "cassino", "casino", "capsula", "capsulas", "capsule",
        "maquina", "maquinas", "giro", "giros", "girar", "premio", "premios",
    }
)

# Land/chest-protection cues. These questions ("como impeço de roubarem meu baú?",
# "mas e o mod flan?") must reach the Flan claim guide directly: multilingual-e5
# ranks the Flan docs below generic FAQ/rules chunks for this phrasing, so RAG
# alone returns the fallback (see responder._CLAIM_GUIDES). "flan" is listed so
# "mas e o mod flan?" routes here instead of tripping the bare-"mod" admin gate.
_CLAIM_MARKERS = frozenset(
    {
        "flan", "claim", "claims", "clamar", "bau", "baus", "roubar", "roubam",
        "roubaram", "roubo", "roubado", "grief", "griefar", "terreno", "enxada",
    }
)

# Referential cues that only resolve against a previous turn (pronouns and
# leading connectives). A message carrying one is a follow-up whose reference
# must be expanded before it can reach a gate; a message WITHOUT any already
# stands on its own. We condense ONLY the former: condensing a self-contained
# question (e.g. the same question asked twice) just lets the model fold the
# previous answer back in and narrow/corrupt it — the repeated-question
# regression in the Slime-drop log.
_FOLLOWUP_MARKERS = frozenset(
    {
        "ele", "ela", "eles", "elas", "dele", "dela", "deles", "delas",
        "nele", "nela", "neles", "nelas", "isso", "isto", "esse", "essa",
        "esses", "essas", "este", "esta", "aquele", "aquela", "aquilo", "ai",
        "it", "they", "them", "its", "their", "that", "those", "these",
    }
)
_FOLLOWUP_LEADERS = frozenset({"e", "and", "mas", "but"})

_DEFAULT_LANGUAGE = "pt"


def looks_like_followup(message: str) -> bool:
    """True when the message depends on a prior turn (so condensing is worth it).

    A leading connective ("e onde ele spawna?") or a bare referential pronoun
    ("dropa isso?") marks a follow-up. A self-contained question matches neither
    and is returned to the caller untouched, so it never pays for condensing nor
    risks the model narrowing it against the previous answer.

    Example:
        >>> looks_like_followup("e onde ele spawna?")
        True
        >>> looks_like_followup("quais pokemons dropam slime?")
        False
    """
    tokens = normalize_tokens(message)
    if not tokens:
        return False
    if tokens[0] in _FOLLOWUP_LEADERS:
        return True
    return bool(set(tokens) & _FOLLOWUP_MARKERS)


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


def claim_intent(message: str) -> bool:
    """True when the player asks about protecting their land/chests (the Flan gate).

    Runs before the admin gate so "mas e o mod flan?" reaches the claim guide
    instead of the bare-"mod" admin match. A single protection cue is enough —
    these terms are specific to the land-claim system and don't collide with the
    Pokémon/facts gates.

    Example:
        >>> claim_intent("como faço pra ngm roubar meu bau?")
        True
        >>> claim_intent("onde nasce o pikachu?")
        False
    """
    return bool(set(normalize_tokens(message)) & _CLAIM_MARKERS)


def facts_intent(message: str, facts: str) -> bool:
    """True when the message is a counting/listing question about a facts axis.

    BOTH conditions are required (decision confirmed during Fase 9):
    - it asks to count or list ("quantos"/"quais"/"lista"/"todos"...), and
    - it names a facts.md axis (a type, item, or category).

    A drop verb ("dropa"/"larga"/...) also satisfies the axis half: the item is
    named in English in facts.md, so a PT item never matches verbatim — routing on
    the verb sends the question to the tool path, which translates the item and
    queries `filtrar_pokemon`, instead of letting it fall to RAG (plan.md §4/§7).

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
    if _asks_about_drops(message):
        return True
    return bool(matched_facts_lines(message, facts))


def _asks_about_drops(message: str) -> bool:
    """True for a drop verb (the item axis, language-agnostic), UNLESS a gacha/
    prize term is present — "dropar master ball no gacha" is a machine-prize
    question for RAG, not the Pokémon item-drop tool (which would wrongly answer
    "nenhum Pokémon corresponde")."""
    tokens = set(normalize_tokens(message))
    if tokens & _PRIZE_SOURCE_MARKERS:
        return False
    return bool(tokens & _DROP_MARKERS)


def spawn_help_intent(message: str) -> bool:
    """True for a generic 'where does a Pokémon spawn / how to find one' question.

    A spawn/find verb AND the bare word "pokemon" are required; a NAMED question
    ("onde o pikachu spawna") never reaches here — it carries the species, is
    caught by the card gate first, and answered from the card's Spawn data. A
    message that names a TYPE ("pokemon de fogo que nasce no deserto") is excluded
    too: that is a descriptive filter for RAG over the cards, not a meta question.

    Example:
        >>> spawn_help_intent("como descubro onde um pokemon spawna?")
        True
        >>> spawn_help_intent("onde fica o market?")
        False
    """
    tokens = set(normalize_tokens(message))
    if not (tokens & _SPAWN_VERBS and tokens & _POKEMON_WORDS):
        return False
    return not _names_a_type(tokens)


def _names_a_type(tokens: set[str]) -> bool:
    """True when a Pokémon type is named (PT label or English id) — a descriptive
    filter that belongs to RAG over the cards, not the generic spawn-help hint."""
    for english, pt_name in TYPE_PT.items():
        if english in tokens or " ".join(normalize_tokens(pt_name)) in tokens:
            return True
    return False


def _asks_count_or_list(message: str) -> bool:
    """A counting or listing question — the only shape the facts gate claims."""
    if wants_full_list(message):
        return True
    tokens = set(normalize_tokens(message))
    if tokens & _COUNT_MARKERS:
        return True
    return "how" in tokens and "many" in tokens
