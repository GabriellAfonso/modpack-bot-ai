"""Semantic retrieval over the persisted RAG index (plan.md §6).

The ONLY runtime module that imports LlamaIndex. The Responder depends on the
`ContextRetriever` Protocol, so tests inject a FakeRetriever and never load the
model or the index. Mirrors how the Responder depends on ModelCompleter.
"""

from typing import Protocol

from modpack_bot.embedding import DEFAULT_EMBED_MODEL, build_embed_model

_DEFAULT_TOP_K = 4


class ContextRetriever(Protocol):
    """Returns the passages most relevant to a player message."""

    def retrieve(self, query: str) -> list[str]: ...


class LlamaIndexRetriever:
    """ContextRetriever backed by the persisted LlamaIndex vector store.

    Loads the index once at construction (model + vectors are heavy), then
    embeds each query locally and returns the top-k node texts — zero Groq
    tokens. The embed model must match the one build_index.py used, so both
    pull it from modpack_bot.embedding.

    Example:
        >>> # LlamaIndexRetriever("content/index").retrieve("tem taxa no market?")
    """

    def __init__(
        self,
        storage_dir: str,
        embed_model: str = DEFAULT_EMBED_MODEL,
        top_k: int = _DEFAULT_TOP_K,
    ) -> None:
        # Imported here, not at module top, so the Responder (which only needs
        # the ContextRetriever Protocol) never pulls in LlamaIndex/torch.
        from llama_index.core import StorageContext, load_index_from_storage

        storage = StorageContext.from_defaults(persist_dir=storage_dir)
        index = load_index_from_storage(storage, embed_model=build_embed_model(embed_model))
        self._retriever = index.as_retriever(similarity_top_k=top_k)

    def retrieve(self, query: str) -> list[str]:
        """The top-k passage texts for `query`, most relevant first."""
        return [node.get_content() for node in self._retriever.retrieve(query)]
