"""Semantic retrieval over the persisted RAG index (plan.md §6).

The ONLY runtime module that imports LlamaIndex. The Responder depends on the
`ContextRetriever` Protocol, so tests inject a FakeRetriever and never load the
model or the index. Mirrors how the Responder depends on ModelCompleter.
"""

from typing import Protocol

from modpack_bot.embedding import DEFAULT_EMBED_MODEL, build_embed_model

# 6, not 4: a buried prize line (master_ball lives in one capsule subsection) is
# crowded out of the top 4 by gacha chunks that share the word "Master" (e.g.
# "Rocket Prize Master"). Subchunks are small, so 6 stays well under Groq's TPM cap.
_DEFAULT_TOP_K = 6

# Reciprocal-rank-fusion constant (the standard 60): score for a passage is
# sum over each ranking of 1/(k + rank). A larger k flattens the contribution of
# top ranks, so a passage must place well in BOTH retrievers to win — keeps a
# single lexical false-positive from outranking a passage e5 is confident about.
_RRF_K = 60


class ContextRetriever(Protocol):
    """Returns the passages most relevant to a player message."""

    def retrieve(self, query: str) -> list[str]: ...


class LlamaIndexRetriever:
    """ContextRetriever with hybrid search: dense e5 + lexical BM25, rank-fused.

    Two retrievers run per query and their rankings are fused (reciprocal rank):

    - dense (e5): catches paraphrase/meaning ("como protejo meu terreno").
    - lexical (BM25 over the same docstore texts): catches an EXACT named entity
      that e5 dilutes inside a list — "exp share", "master ball". Such a term
      lives in a loot/prize table whose chunk embeds as "list of items", so dense
      ranks it below 25 others; BM25 matches the literal token and pulls it back.

    Both are local: zero Groq tokens. The embed model must match build_index.py's
    (both pull it from modpack_bot.embedding). The lexical side is driven by bm25s
    directly (pure Python) over the texts already in the persisted docstore — no
    extra index file, no reindex, and no C-extension stemmer to compile (the
    llama-index BM25 wrapper pulls PyStemmer, which has no wheel on Windows/3.14).

    Example:
        >>> # LlamaIndexRetriever("content/index").retrieve("como consigo o exp share?")
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
        self._dense = index.as_retriever(similarity_top_k=top_k)
        self._lexical = _Bm25Lexical(_docstore_texts(storage))
        self._top_k = top_k

    def retrieve(self, query: str) -> list[str]:
        """The top-k passage texts for `query`, most relevant first (fused).

        Dense and lexical each return their own ranking; reciprocal-rank fusion
        merges them so the market/zekrom/master-ball cases (dense) and the
        buried-item cases (lexical) both surface, de-duped, in one list.
        """
        dense = [node.get_content() for node in self._dense.retrieve(query)]
        lexical = self._lexical.search(query, self._top_k)
        return _reciprocal_rank_fusion(dense, lexical, self._top_k)


class _Bm25Lexical:
    """A pure-Python BM25 ranking over a fixed list of passage texts (bm25s).

    The corpus is tokenized and indexed once at construction (cheap: a few
    thousand small chunks). No stemmer is configured — the high-value lexical
    hits are exact item/entity names ("Exp Share", "Master Ball") that need no
    stemming; skipping it also avoids bm25s's optional PyStemmer C dependency.
    """

    def __init__(self, texts: list[str]) -> None:
        import bm25s

        self._bm25s = bm25s
        self._texts = texts
        self._bm25 = bm25s.BM25()
        self._bm25.index(_tokenize(bm25s, texts))

    def search(self, query: str, top_k: int) -> list[str]:
        """The top-k passage texts BM25 ranks highest for `query`."""
        if not self._texts:
            return []
        tokens = _tokenize(self._bm25s, query)
        results, _ = self._bm25.retrieve(
            tokens, k=min(top_k, len(self._texts)), show_progress=False
        )
        return [self._texts[index] for index in results[0]]


def _tokenize(bm25s: object, text: "str | list[str]") -> object:
    """Tokenize for bm25s with stopword removal and stemming off (see _Bm25Lexical)."""
    return bm25s.tokenize(text, stopwords=None, show_progress=False)


def _docstore_texts(storage: object) -> list[str]:
    """Every indexed chunk's text, read from the persisted docstore (the same
    nodes the dense vectors were built from, so both retrievers see one corpus)."""
    return [node.get_content() for node in storage.docstore.docs.values()]


def _reciprocal_rank_fusion(dense: list[str], lexical: list[str], top_k: int) -> list[str]:
    """Merge two rankings by reciprocal rank, returning the top-k passage texts.

    Each passage scores sum(1/(_RRF_K + rank)) across the rankings it appears in,
    so a passage near the top of either list rises and one near the top of BOTH
    wins. De-dupes by text. First-seen order breaks score ties deterministically.

    Example:
        >>> _reciprocal_rank_fusion(["a", "b"], ["b", "c"], 3)
        ['b', 'a', 'c']
    """
    scores: dict[str, float] = {}
    order: list[str] = []
    for ranking in (dense, lexical):
        for rank, text in enumerate(ranking):
            if text not in scores:
                scores[text] = 0.0
                order.append(text)
            scores[text] += 1.0 / (_RRF_K + rank)
    order.sort(key=lambda text: scores[text], reverse=True)
    return order[:top_k]
