from modpack_bot.responder import Responder
from modpack_bot.router import Router
from tests.conftest import FakeCardRepository, FakeCompleter, FakeGuideRepository


def make_responder(route_reply, answer_reply="ANSWER", guides=None, cards=None):
    completer = FakeCompleter(route_reply, answer_reply)
    guide_repo = FakeGuideRepository(guides=guides or {})
    card_repo = FakeCardRepository(cards=cards or {})
    router = Router(completer, guide_repo)
    return Responder(router, completer, guide_repo, card_repo), completer


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
