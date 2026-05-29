from modpack_bot.responder import Responder
from modpack_bot.router import Router
from tests.conftest import (
    FakeAdminResolver,
    FakeCardRepository,
    FakeCompleter,
    FakeGuideRepository,
)


def make_responder(route_reply, answer_reply="ANSWER", guides=None, cards=None, admins=None):
    completer = FakeCompleter(route_reply, answer_reply)
    guide_repo = FakeGuideRepository(guides=guides or {})
    card_repo = FakeCardRepository(cards=cards or {})
    router = Router(completer, guide_repo)
    return Responder(router, completer, guide_repo, card_repo, admins), completer


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


def test_count_question_still_uses_answer_llm_with_trimmed_facts():
    responder, completer = make_responder(
        route_reply="facts.md|pt", answer_reply="Existem 1", guides={"facts.md": _FACTS_DOC}
    )
    assert responder.answer("quantos pokemons de fogo tem?") == "Existem 1"
    assert len(completer.calls) == 2  # router + answer
    assert "Total de Pokémon no modpack: 1" in completer.last_system_prompt


def test_answer_collapses_extra_blank_lines_from_model():
    responder, _ = make_responder(
        route_reply="market.md|pt",
        answer_reply="Tipo Água: 154.\n\n\n\nNo mundo: 890.",
        guides={"market.md": "GUIDE"},
    )
    assert responder.answer("quantos tipo agua") == "Tipo Água: 154.\n\nNo mundo: 890."


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
