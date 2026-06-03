from modpack_bot.responder import Responder
from tests.conftest import (
    FakeAdminResolver,
    FakeCardRepository,
    FakeCompleter,
    FakeGuideRepository,
    FakeRetriever,
)


def make_responder(
    passages=None,
    answer_reply="ANSWER",
    facts=None,
    cards=None,
    admins=None,
    show_usage=False,
    tool_call=None,
):
    completer = FakeCompleter(answer_reply=answer_reply, tool_call=tool_call)
    guides = FakeGuideRepository(guides={"facts.md": facts} if facts else {})
    cards_repo = FakeCardRepository(cards=cards or {})
    retriever = FakeRetriever(passages or [])
    responder = Responder(retriever, completer, guides, cards_repo, admins, show_usage)
    return responder, completer


def test_empty_retrieval_returns_fallback_pt():
    responder, completer = make_responder(passages=[])
    assert "suporte" in responder.answer("???")
    # answer model must NOT be called when nothing is retrieved.
    assert len(completer.calls) == 0


def test_empty_retrieval_returns_fallback_en():
    responder, _ = make_responder(passages=[])
    assert "support channel" in responder.answer("what is this thing?")


def test_rag_feeds_retrieved_passages_into_prompt():
    responder, completer = make_responder(passages=["MARKET GUIDE"], answer_reply="REPLY")
    assert responder.answer("o market cobra taxa?") == "REPLY"
    assert "MARKET GUIDE" in completer.last_system_prompt
    # common path is a single Groq call now (no router) — the §4 win.
    assert len(completer.calls) == 1


def test_rag_joins_multiple_passages_into_one_context():
    responder, completer = make_responder(passages=["CHUNK A", "CHUNK B"])
    responder.answer("o que dá a cherish capsule?")
    prompt = completer.last_system_prompt
    assert "CHUNK A" in prompt
    assert "CHUNK B" in prompt


_FACTS_DOC = (
    "# Números do Modpack\n"
    "\n"
    "- Total de Pokémon no modpack: 1\n"
    "\n"
    "## Pokémon por tipo\n"
    "\n"
    "- Fogo (1): Charizard\n"
    "\n"
    "## Pokémon por item dropado\n"
    "\n"
    "- Leather (1): Ponyta\n"
    "\n"
    "## Pokémon por categoria\n"
    "\n"
    "- Lendários (1): Mewtwo\n"
)


def test_full_list_request_answers_from_python_without_answer_llm():
    responder, completer = make_responder(facts=_FACTS_DOC)
    reply = responder.answer("lista todos os pokemons tipo fogo")
    assert "Aqui está:" in reply
    assert "- Fogo (1): Charizard" in reply
    # the list is built in Python; the answer model must NOT be called.
    assert len(completer.calls) == 0


def test_count_question_uses_filter_tool_with_counts_header_only():
    responder, completer = make_responder(answer_reply="Existem 1", facts=_FACTS_DOC)
    assert responder.answer("quantos pokemons de fogo tem?") == "Existem 1"
    assert len(completer.calls) == 1  # tool-backed answer only (no router)
    prompt = completer.last_system_prompt
    # the small counts header is the guide; the big per-type list is NOT inlined
    # (it bloated the prompt and made the model paraphrase) — the tool fetches names.
    assert "Total de Pokémon no modpack: 1" in prompt
    assert "- Fogo (1): Charizard" not in prompt


def test_legendary_question_lists_from_python_without_answer_llm():
    # "quais lendários tem?" is a full-list request ("which ones are there"). It
    # must hit the deterministic listing, not the LLM — feeding the bare roster
    # line to the answer model made it ramble instead of listing the names.
    responder, completer = make_responder(answer_reply="Mewtwo", facts=_FACTS_DOC)
    reply = responder.answer("quais pokemons lendarios tem?")
    assert "Aqui está:" in reply
    assert "- Lendários (1): Mewtwo" in reply
    assert len(completer.calls) == 0


_CROSS_FACTS = (
    "# Números do Modpack\n"
    "\n"
    "- Total de Pokémon no modpack: 3\n"
    "\n"
    "## Pokémon por tipo\n"
    "\n"
    "- Elétrico (2): Pikachu, Zapdos\n"
    "\n"
    "## Pokémon por item dropado\n"
    "\n"
    "- Leather (1): Ponyta\n"
    "\n"
    "## Pokémon por categoria\n"
    "\n"
    "- Lendários (2): Mewtwo, Zapdos\n"
)


def test_cross_axis_facts_question_uses_filter_tool():
    # "lendários do tipo elétrico" crosses two axes — no precomputed line exists,
    # so the answer model is given the filter tool and the dispatch intersects.
    responder, completer = make_responder(
        answer_reply="É o Zapdos.",
        facts=_CROSS_FACTS,
        tool_call=("filtrar_pokemon", {"types": ["electric"], "categories": ["legendary"]}),
    )
    reply = responder.answer("quantos lendarios do tipo eletrico tem?")
    assert reply == "É o Zapdos."
    assert completer.tool_result == "1 Pokémon: Zapdos"  # intersection, not both lists
    assert len(completer.calls) == 1


def test_cross_axis_full_list_phrasing_skips_listing_for_the_tool():
    # "quais ... do tipo ..." matches both a category and a type line; the
    # deterministic listing must NOT fire (it would concatenate both full lists).
    responder, completer = make_responder(
        facts=_CROSS_FACTS,
        tool_call=("filtrar_pokemon", {"types": ["electric"], "categories": ["legendary"]}),
    )
    responder.answer("quais lendarios do tipo eletrico?")
    assert completer.tool_result == "1 Pokémon: Zapdos"
    assert len(completer.calls) == 1  # tool path, not the deterministic listing


def test_answer_collapses_extra_blank_lines_from_model():
    responder, _ = make_responder(
        passages=["GUIDE"], answer_reply="Tipo Água: 154.\n\n\n\nNo mundo: 890."
    )
    assert responder.answer("quanto de agua") == "Tipo Água: 154.\n\nNo mundo: 890."


def test_usage_footer_shows_single_groq_call():
    responder, _ = make_responder(passages=["G"], answer_reply="REPLY", show_usage=True)
    reply = responder.answer("o market cobra taxa?")
    # common path is now ONE answer call * TokenUsage(10, 5) = 15 total (was 2).
    assert reply.startswith("REPLY")
    assert "15 tokens (entrada 10 / saída 5)" in reply


def test_usage_footer_absent_by_default():
    responder, _ = make_responder(passages=["G"], answer_reply="REPLY")
    assert responder.answer("o market cobra taxa?") == "REPLY"


def test_admins_gate_returns_mentions_verbatim_without_answer_llm():
    responder, completer = make_responder(admins=FakeAdminResolver(["<@1>", "<@2>"]))
    reply = responder.answer("como falo com um admin?")
    assert "<@1>, <@2>" in reply
    # mentions are returned verbatim; the answer model must NOT be called.
    assert len(completer.calls) == 0


def test_admins_gate_without_resolver_falls_back():
    responder, _ = make_responder()
    assert "suporte" in responder.answer("quem sao os admins do servidor?")


def test_pokemon_gate_swaps_in_the_card():
    responder, completer = make_responder(cards={"pikachu": "PIKACHU CARD"})
    responder.answer("info do pikachu")
    prompt = completer.last_system_prompt
    assert "PIKACHU CARD" in prompt
    assert "/pwiki pikachu" in prompt


def test_non_pokemon_question_falls_through_to_rag():
    # No card matches; the message must reach the RAG fallback, not a Pokémon gate.
    responder, completer = make_responder(passages=["WIKI DOC"], cards={"pikachu": "CARD"})
    responder.answer("onde fica a vila dos aldeoes?")
    assert "WIKI DOC" in completer.last_system_prompt


def test_generic_spawn_question_points_to_pwiki_without_llm_or_rag():
    # Nameless "how do I find where a pokemon spawns" must NOT reach RAG (it
    # collides with the gacha spawn-machine docs) — answer with the /pwiki hint.
    responder, completer = make_responder(passages=["STRANGE CRYSTALLIZED MACHINE"])
    reply = responder.answer("como descubro onde um pokemon spawna?")
    assert "/pwiki" in reply
    assert len(completer.calls) == 0  # deterministic, 0 tokens


def test_named_spawn_question_still_answers_from_the_card():
    # A species in the message is caught by the card gate first, so spawn data
    # comes from the card — the generic /pwiki hint must not hijack it.
    responder, completer = make_responder(cards={"pikachu": "PIKACHU CARD"})
    responder.answer("onde o pikachu spawna?")
    assert "PIKACHU CARD" in completer.last_system_prompt


def test_descriptive_axis_query_goes_to_rag_not_facts():
    # Regression (Fase 9): "fogo" is a type axis, but "que nasce no deserto" is a
    # descriptive spawn query the filter tool can't answer (no biome param). It
    # must reach RAG over the cards, not the facts gate.
    facts = (
        "# Números\n\n## Pokémon por tipo\n\n- Fogo (1): Charizard\n"
        "\n## Pokémon por item dropado\n\n## Pokémon por categoria\n"
    )
    completer = FakeCompleter(answer_reply="É o Camerupt.")
    guides = FakeGuideRepository(guides={"facts.md": facts})
    retriever = FakeRetriever(["# Camerupt\n## Spawn\n- Desert"])
    responder = Responder(retriever, completer, guides, FakeCardRepository(), None, False)

    responder.answer("pokemon de fogo que nasce no deserto")
    assert retriever.queries == ["pokemon de fogo que nasce no deserto"]
    assert "Camerupt" in completer.last_system_prompt
