"""The evaluation cases: real player phrasings and where they should land.

Each case pins the expected gate (`expected_route`) and, when a question should
be answerable from the index, a substring that MUST appear in some retrieved
passage (`expected_passage`). The two are independent: a Pokémon-gated question
(zekrom) can still assert a retrieval expectation, because its answer is
augmented with RAG (responder._answer_pokemon_obtain).

`rag_recall_known_bad=True` marks a case where retrieval alone currently fails
to surface the answer — the very reason it has a dedicated gate (Flan claims,
gacha prizes). Those are the cases a future reranker / multi-query should fix:
flip the flag off when it does, and the retrieval report will hold us to it.

Keep this list phrasing-faithful to what players actually type (typos, slang,
no accents) — that is the whole point of measuring routing.
"""

from dataclasses import dataclass

from modpack_bot.routing import Route


@dataclass(frozen=True)
class EvalCase:
    """One evaluation question and its expectations."""

    question: str
    expected_route: Route
    expected_passage: str | None = None
    rag_recall_known_bad: bool = False


CASES: tuple[EvalCase, ...] = (
    # --- Pokémon card gate -------------------------------------------------
    EvalCase("onde o pikachu spawna?", Route.POKEMON),
    EvalCase("quais os stats do charizard?", Route.POKEMON),
    # No natural spawn: the card gate still fires, but the answer is augmented
    # with RAG, so the summon doc must be retrievable (the zekrom bug, fixed).
    EvalCase("como acho um zekrom?", Route.POKEMON, expected_passage="Pedra Escura"),
    EvalCase("como invoco o reshiram?", Route.POKEMON, expected_passage="Pedra Clara"),
    # --- Claim (Flan) gate -------------------------------------------------
    # Routed to a dedicated gate precisely because RAG can't surface the Flan
    # docs for this phrasing (e5 buries them under generic FAQ chunks). The
    # known-bad retrieval expectation documents that miss: when a reranker /
    # multi-query makes it retrievable, the report says so and the gate can go.
    EvalCase(
        "como faço pra ngm roubar meu bau?",
        Route.CLAIM,
        expected_passage="proteção de terreno",
        rag_recall_known_bad=True,
    ),
    EvalCase("mas e o mod flan?", Route.CLAIM),
    EvalCase("como protejo meu terreno?", Route.CLAIM),
    # --- Admins gate -------------------------------------------------------
    EvalCase("como falo com um admin?", Route.ADMINS),
    EvalCase("tem algum staff online?", Route.ADMINS),
    # --- Facts (counting / listing) gate -----------------------------------
    EvalCase("quantos pokemon de fogo tem?", Route.FACTS),
    EvalCase("quais pokemons lendarios tem?", Route.FACTS),
    EvalCase("lista todos os pokemons tipo agua", Route.FACTS),
    # --- Generic spawn-help gate (nameless) --------------------------------
    EvalCase("como descubro onde um pokemon spawna?", Route.SPAWN_HELP),
    # --- RAG fallback (answer lives in a guide) ----------------------------
    EvalCase("tem taxa pra vender no market?", Route.RAG, expected_passage="market"),
    EvalCase("onde fica o market?", Route.RAG, expected_passage="market"),
    # Descriptive filter the facts tool can't satisfy (no biome param) -> RAG.
    EvalCase("pokemon de fogo que nasce no deserto", Route.RAG),
    # Gacha prize, NOT a Pokémon item drop -> RAG over the gacha guides (and RAG
    # does surface it, so no known-bad flag — this guards that it stays found).
    EvalCase("como pego o master ball no gacha?", Route.RAG, expected_passage="Master Ball"),
    # An item name buried in a loot/prize table: dense e5 embeds the chunk as
    # "list of items" and ranks it below 25 others, so it needs the BM25 half of
    # the hybrid retriever to surface on the literal token (the exp-share report).
    EvalCase("como consigo o exp share?", Route.RAG, expected_passage="Exp Share"),
)
