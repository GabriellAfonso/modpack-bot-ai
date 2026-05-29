from modpack_bot.router import Router, parse_route
from tests.conftest import FakeCompleter, FakeGuideRepository


def test_parse_valid_guide_and_language():
    assert parse_route("wikigui.md | en") == ("wikigui.md", "en")


def test_parse_unknown_guide_collapses_to_none():
    assert parse_route("nonsense|pt") == (None, "pt")


def test_parse_faq_and_facts_are_valid_guides():
    assert parse_route("faq.md|pt") == ("faq.md", "pt")
    assert parse_route("facts.md|en") == ("facts.md", "en")


def test_parse_admins_tool_label_is_routable():
    assert parse_route("tool:admins|pt") == ("tool:admins", "pt")


def test_parse_unknown_language_defaults_to_pt():
    assert parse_route("market.md|fr") == ("market.md", "pt")


def test_parse_no_pipe_defaults_language():
    assert parse_route("rules.md") == ("rules.md", "pt")


def test_parse_is_case_insensitive_and_trims():
    assert parse_route("  WIKIGUI.MD | EN ") == ("wikigui.md", "en")


def _repo_with_catalog() -> FakeGuideRepository:
    """Fake repo whose core carries the {{ARQUIVOS}} token and whose guides have
    headings, so the Router builds and injects the catalog like in production."""
    from modpack_bot.guides import ROUTABLE_GUIDES

    guides = {name: f"# {name} title\n\n## Seção de {name}\n" for name in ROUTABLE_GUIDES}
    guides["market.md"] = "# Market\n\n## Comandos\n\n## Como Vender\n"
    return FakeGuideRepository(core="ROUTE {{ARQUIVOS}} END", guides=guides)


def test_router_routes_via_completer():
    completer = FakeCompleter(route_reply="wikigui.md|en")
    router = Router(completer, _repo_with_catalog())
    assert router.route("anything") == ("wikigui.md", "en")
    # the {{ARQUIVOS}} token is replaced by the generated catalog before routing.
    prompt = completer.calls[0][0][0]["content"]
    assert "{{ARQUIVOS}}" not in prompt
    assert prompt.startswith("ROUTE ") and prompt.endswith(" END")


def test_router_prompt_lists_each_guide_section_from_its_headings():
    # regression: "quais comandos do market" hit the fallback because the curated
    # core.md summary never mentioned "Comandos"; now it comes from the heading.
    completer = FakeCompleter(route_reply="market.md|pt")
    router = Router(completer, _repo_with_catalog())
    router.route("quais comandos do market")
    prompt = completer.calls[0][0][0]["content"]
    assert "- **market.md** — Market. Seções: Comandos; Como Vender." in prompt
