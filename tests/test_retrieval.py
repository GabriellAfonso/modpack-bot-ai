"""Retrieval tests.

The fast tests exercise only the Protocol via the conftest FakeRetriever — the
real LlamaIndexRetriever loads the model and the persisted index, so its smoke
test is marked `slow` and deselected by default (`pytest -m slow` to run it).
The heavy import lives inside the slow test so default collection stays torch-free.
"""

import os

import pytest

from tests.conftest import FakeRetriever

_INDEX_DIR = os.path.join("content", "index")


def test_fake_retriever_returns_canned_passages_and_records_query():
    retriever = FakeRetriever(["taxa de listagem"])
    assert retriever.retrieve("tem taxa?") == ["taxa de listagem"]
    assert retriever.queries == ["tem taxa?"]


@pytest.mark.slow
@pytest.mark.skipif(not os.path.isdir(_INDEX_DIR), reason="index not built")
def test_llama_index_retriever_finds_market_passage_for_market_query():
    from modpack_bot.retrieval import LlamaIndexRetriever

    passages = LlamaIndexRetriever(_INDEX_DIR).retrieve("tem taxa pra vender no market?")
    assert passages
    assert any("market" in passage.lower() for passage in passages)
