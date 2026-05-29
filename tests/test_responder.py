from modpack_bot.responder import Responder
from modpack_bot.router import Router
from tests.conftest import (
    FakeAdminResolver,
    FakeCardRepository,
    FakeCompleter,
    FakeGuideRepository,
)


def make_responder(
    route_reply,
    answer_reply="ANSWER",
    guides=None,
    cards=None,
    admins=None,
    show_usage=False,
    tool_call=None,
):
    completer = FakeCompleter(route_reply, answer_reply, tool_call=tool_call)
    guide_repo = FakeGuideRepository(guides=guides or {})
    card_repo = FakeCardRepository(cards=cards or {})
    router = Router(completer, guide_repo)
    responder = Responder(router, completer, guide_repo, card_repo, admins, show_usage)
    return responder, completer


def test_no_matching_guide_returns_fallback_pt():
    responder, completer = make_responder(route_reply="nonsense")
    assert "suporte" in responder.answer("???")
    # answer model must NOT be called when nothing routes.
    assert len(completer.calls) == 1


def test_no_matching_guide_returns_fallback_en():
    responder, _ = make_responder(route_reply="nonsense|en")
    assert "support channel" in responder.answer("???")


def test_regular_guide_feeds_guide_into_prompt():
    responder, completer = make_responder(
        route_reply="market.md|pt", answer_reply="REPLY", guides={"market.md": "MARKET GUIDE"}
    )
    assert responder.answer("quanto custa") == "REPLY"
    assert "MARKET GUIDE" in completer.last_system_prompt


def test_faq_routes_as_regular_guide_without_wiki_gate():
    responder, completer = make_responder(
        route_reply="faq.md|pt", answer_reply="REPLY", guides={"faq.md": "FAQ TEXT"}
    )
    assert responder.answer("qual o discord") == "REPLY"
    prompt = completer.last_system_prompt
    assert "FAQ TEXT" in prompt
    # the wiki gate is wiki.md-only: faq must not carry its /pwiki instructions.
    assert "/pwiki" not in prompt


def test_facts_routes_as_regular_guide():
    responder, completer = make_responder(
        route_reply="facts.md|pt", guides={"facts.md": "FACTS TEXT"}
    )
    responder.answer("quantos pokemon tem")
    assert "FACTS TEXT" in completer.last_system_prompt


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
    responder, completer = make_responder(
        route_reply="facts.md|pt", guides={"facts.md": _FACTS_DOC}
    )
    reply = responder.answer("lista todos os pokemons tipo fogo")
    assert "Aqui está:" in reply
    assert "- Fogo (1): Charizard" in reply
    # the list is built in Python; the answer model must NOT be called.
    assert len(completer.calls) == 1


def test_count_question_uses_filter_tool_with_counts_header_only():
    responder, completer = make_responder(
        route_reply="facts.md|pt", answer_reply="Existem 1", guides={"facts.md": _FACTS_DOC}
    )
    assert responder.answer("quantos pokemons de fogo tem?") == "Existem 1"
    assert len(completer.calls) == 2  # router + tool-backed answer
    prompt = completer.last_system_prompt
    # the small counts header is the guide; the big per-type list is NOT inlined
    # (it bloated the prompt and made the model paraphrase) — the tool fetches names.
    assert "Total de Pokémon no modpack: 1" in prompt
    assert "- Fogo (1): Charizard" not in prompt


def test_answer_collapses_extra_blank_lines_from_model():
    responder, _ = make_responder(
        route_reply="market.md|pt",
        answer_reply="Tipo Água: 154.\n\n\n\nNo mundo: 890.",
        guides={"market.md": "GUIDE"},
    )
    assert responder.answer("quantos tipo agua") == "Tipo Água: 154.\n\nNo mundo: 890."


def test_legendary_question_lists_from_python_without_answer_llm():
    # "quais lendários tem?" is a full-list request ("which ones are there"). It
    # must hit the deterministic listing, not the LLM — feeding the bare roster
    # line to the answer model made it ramble instead of listing the names.
    responder, completer = make_responder(
        route_reply="facts.md|pt", answer_reply="Mewtwo", guides={"facts.md": _FACTS_DOC}
    )
    reply = responder.answer("quais pokemons lendarios tem?")
    assert "Aqui está:" in reply
    assert "- Lendários (1): Mewtwo" in reply
    # the list is built in Python; the answer model must NOT be called.
    assert len(completer.calls) == 1


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
        route_reply="facts.md|pt",
        answer_reply="É o Zapdos.",
        guides={"facts.md": _CROSS_FACTS},
        tool_call=("filtrar_pokemon", {"types": ["electric"], "categories": ["legendary"]}),
    )
    reply = responder.answer("tem algum lendario do tipo eletrico?")
    assert reply == "É o Zapdos."
    assert completer.tool_result == "1 Pokémon: Zapdos"  # intersection, not both lists
    assert len(completer.calls) == 2  # router + tool-backed answer


def test_cross_axis_full_list_phrasing_skips_listing_for_the_tool():
    # "quais ... do tipo ..." matches both a category and a type line; the
    # deterministic listing must NOT fire (it would concatenate both full lists).
    responder, completer = make_responder(
        route_reply="facts.md|pt",
        guides={"facts.md": _CROSS_FACTS},
        tool_call=("filtrar_pokemon", {"types": ["electric"], "categories": ["legendary"]}),
    )
    responder.answer("quais lendarios do tipo eletrico?")
    assert completer.tool_result == "1 Pokémon: Zapdos"
    assert len(completer.calls) == 2  # not the 1-call deterministic listing


def test_usage_footer_appended_when_enabled():
    responder, _ = make_responder(
        route_reply="market.md|pt", answer_reply="REPLY", guides={"market.md": "G"}, show_usage=True
    )
    reply = responder.answer("quanto custa")
    # router + answer = 2 calls * TokenUsage(10, 5) = 30 total.
    assert reply.startswith("REPLY")
    assert "30 tokens (entrada 20 / saída 10)" in reply


def test_usage_footer_absent_by_default():
    responder, _ = make_responder(
        route_reply="market.md|pt", answer_reply="REPLY", guides={"market.md": "G"}
    )
    assert responder.answer("quanto custa") == "REPLY"


def test_admins_tool_returns_mentions_verbatim_without_answer_llm():
    responder, completer = make_responder(
        route_reply="tool:admins|pt", admins=FakeAdminResolver(["<@1>", "<@2>"])
    )
    reply = responder.answer("como falo com um admin")
    assert "<@1>, <@2>" in reply
    # mentions are returned verbatim; the answer model must NOT be called.
    assert len(completer.calls) == 1


def test_admins_tool_without_resolver_falls_back():
    responder, _ = make_responder(route_reply="tool:admins|pt")
    assert "suporte" in responder.answer("quem sao os admins")


def test_wiki_swaps_in_pokemon_card():
    responder, completer = make_responder(
        route_reply="wiki.md|pt",
        guides={"wiki.md": "WIKI DOC"},
        cards={"pikachu": "PIKACHU CARD"},
    )
    responder.answer("info do pikachu")
    prompt = completer.last_system_prompt
    assert "PIKACHU CARD" in prompt
    assert "/pwiki pikachu" in prompt
    assert "WIKI DOC" not in prompt


def test_wiki_without_pokemon_keeps_doc_and_forbids_pwiki():
    responder, completer = make_responder(
        route_reply="wiki.md|pt", guides={"wiki.md": "WIKI DOC"}, cards={}
    )
    responder.answer("onde fica a vila")
    prompt = completer.last_system_prompt
    assert "WIKI DOC" in prompt
    assert "Não mencione `/pwiki`" in prompt
