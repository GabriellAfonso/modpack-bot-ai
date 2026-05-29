from modpack_bot.router import Router, parse_route
from tests.conftest import FakeCompleter, FakeGuideRepository


def test_parse_valid_guide_and_language():
    assert parse_route("wiki.md | en") == ("wiki.md", "en")


def test_parse_unknown_guide_collapses_to_none():
    assert parse_route("nonsense|pt") == (None, "pt")


def test_parse_unknown_language_defaults_to_pt():
    assert parse_route("market.md|fr") == ("market.md", "pt")


def test_parse_no_pipe_defaults_language():
    assert parse_route("rules.md") == ("rules.md", "pt")


def test_parse_is_case_insensitive_and_trims():
    assert parse_route("  WIKI.MD | EN ") == ("wiki.md", "en")


def test_router_routes_via_completer():
    completer = FakeCompleter(route_reply="wiki.md|en")
    router = Router(completer, FakeGuideRepository(core="ROUTE PROMPT"))
    assert router.route("anything") == ("wiki.md", "en")
    # router stage must feed core as the system prompt.
    assert completer.calls[0][0][0]["content"] == "ROUTE PROMPT"
