"""Retrieval tests.

The fast tests exercise only the Protocol via the conftest FakeRetriever — the
real LlamaIndexRetriever loads the model and the persisted index, so its smoke
test is marked `slow` and deselected by default (`pytest -m slow` to run it).
The heavy import lives inside the slow test so default collection stays torch-free.
"""

import os

import pytest

from modpack_bot.retrieval import _reciprocal_rank_fusion
from tests.conftest import FakeRetriever

_INDEX_DIR = os.path.join("content", "index")


def test_fake_retriever_returns_canned_passages_and_records_query():
    retriever = FakeRetriever(["taxa de listagem"])
    assert retriever.retrieve("tem taxa?") == ["taxa de listagem"]
    assert retriever.queries == ["tem taxa?"]


def test_rrf_ranks_a_shared_passage_above_either_ranking_alone():
    # "b" is in both lists, so its fused score beats "a" and "c" (each in one).
    assert _reciprocal_rank_fusion(["a", "b"], ["b", "c"], 3) == ["b", "a", "c"]


def test_rrf_surfaces_a_lexical_only_passage_into_the_top_k():
    # The exp-share shape: a passage dense missed entirely (lexical-only) still
    # makes the fused top-k instead of being dropped.
    dense = ["x", "y"]
    lexical = ["exp share loot", "x"]
    assert "exp share loot" in _reciprocal_rank_fusion(dense, lexical, 2)


def test_rrf_dedupes_and_caps_to_top_k():
    fused = _reciprocal_rank_fusion(["a", "b", "c"], ["c", "d"], 2)
    assert len(fused) == 2
    assert fused == sorted(set(fused), key=fused.index)  # no duplicates


@pytest.mark.slow
@pytest.mark.skipif(not os.path.isdir(_INDEX_DIR), reason="index not built")
def test_llama_index_retriever_finds_market_passage_for_market_query():
    from modpack_bot.retrieval import LlamaIndexRetriever

    passages = LlamaIndexRetriever(_INDEX_DIR).retrieve("tem taxa pra vender no market?")
    assert passages
    assert any("market" in passage.lower() for passage in passages)


@pytest.mark.slow
@pytest.mark.skipif(not os.path.isdir(_INDEX_DIR), reason="index not built")
def test_hybrid_retriever_surfaces_item_buried_in_a_loot_list():
    # The exp-share report: dense e5 ranks the loot/prize chunk below 25 others
    # for this phrasing; the BM25 half matches the literal "Exp Share" so the
    # hybrid retriever pulls it back in. Guards the lexical half from regressing.
    from modpack_bot.retrieval import LlamaIndexRetriever

    passages = LlamaIndexRetriever(_INDEX_DIR).retrieve("como consigo o exp share?")
    assert any("exp share" in passage.lower() for passage in passages)
