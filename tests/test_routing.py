"""Routing tests: classify_route units + the dataset-driven routing eval.

The dataset cases (evals.dataset) double as regression tests for the gate order:
if a prompt or predicate change misroutes a known question, this fails in CI
without ever loading the model. Retrieval recall (which needs the index) is the
separate, heavy report in evals.retrieval_eval.

The pure units use small stubs; the dataset eval runs against the real card set
and facts.md, because the facts gate matches a query against the actual axis
lines — a stub can't stand in for that without quietly drifting from production.
"""

import os

import pytest

from evals.dataset import CASES
from modpack_bot.guides import CardRepository, GuideRepository
from modpack_bot.routing import Route, classify_route

# Card stems for the pure units below (the dataset eval uses the real set).
_NAMES = frozenset({"pikachu", "charizard", "zekrom", "reshiram"})

# A real-shaped facts.md slice: the gate matches axis lines under these headers.
_FACTS = (
    "## Pokémon por tipo\n- Fogo (1): Charizard\n- Água (1): Squirtle\n"
    "## Pokémon por categoria\n- Lendários (1): Zekrom\n"
)

_CONTENT_DIR = "content"
_HAS_CONTENT = os.path.isfile(os.path.join(_CONTENT_DIR, "facts.md"))
_REAL_NAMES = CardRepository(_CONTENT_DIR).pokemon_names() if _HAS_CONTENT else frozenset()
_REAL_FACTS = GuideRepository(_CONTENT_DIR).load_guide("facts.md") if _HAS_CONTENT else ""


def _route(message: str) -> Route:
    return classify_route(message, _NAMES, lambda: _FACTS).route


def test_claim_runs_before_admin_for_the_flan_mod_question():
    # "flan" is a claim cue, so the question routes to the Flan claim guide.
    assert _route("mas e o mod flan?") is Route.CLAIM


def test_mod_name_question_does_not_route_to_admins():
    # Bare "mod" is a game mod here, not a moderator: a summary request must
    # fall to RAG, not the staff redirect (regression for cobble safari).
    assert _route("me da um resumo do mod cobble safari") is Route.RAG


def test_named_pokemon_beats_generic_spawn_help():
    assert _route("onde o pikachu spawna?") is Route.POKEMON


def test_nameless_spawn_question_is_spawn_help_not_rag():
    assert _route("como descubro onde um pokemon spawna?") is Route.SPAWN_HELP


def test_unmatched_question_falls_to_rag():
    assert _route("onde fica o market?") is Route.RAG


def test_facts_thunk_is_not_read_when_an_earlier_gate_matches():
    # The claim gate fires first, so load_facts must never be called.
    def explode() -> str:
        raise AssertionError("facts.md should not be read on the claim path")

    assert classify_route("como protejo meu bau?", _NAMES, explode).route is Route.CLAIM


@pytest.mark.skipif(not _HAS_CONTENT, reason="content/ not present")
@pytest.mark.parametrize("case", CASES, ids=lambda c: c.question)
def test_dataset_routes_as_expected(case):
    decision = classify_route(case.question, _REAL_NAMES, lambda: _REAL_FACTS)
    assert decision.route is case.expected_route
