"""The single place that configures the local embedding model.

The offline index builder and the runtime retriever MUST embed with the same
model and the same e5 prefixes, or query vectors land in a different space than
the indexed passages and retrieval silently degrades. Centralizing the factory
here keeps that contract in one tested spot.
"""

# intfloat/multilingual-e5-small is asymmetric: it expects every query prefixed
# with "query: " and every indexed passage with "passage: ". HuggingFaceEmbedding
# prepends these instructions for us (query_instruction / text_instruction).
DEFAULT_EMBED_MODEL = "intfloat/multilingual-e5-small"
_QUERY_PREFIX = "query: "
_PASSAGE_PREFIX = "passage: "


def build_embed_model(model_name: str = DEFAULT_EMBED_MODEL) -> "HuggingFaceEmbedding":
    """The e5 embedding model wired with the required query/passage prefixes.

    HuggingFaceEmbedding (and its torch dependency, ~hundreds of MB) is imported
    lazily here so that merely importing this module — or the retriever Protocol
    that the Responder type-hints against — stays cheap and torch-free.

    Example:
        >>> # build_embed_model().query_instruction == "query: "
    """
    from llama_index.embeddings.huggingface import HuggingFaceEmbedding

    return HuggingFaceEmbedding(
        model_name=model_name,
        query_instruction=_QUERY_PREFIX,
        text_instruction=_PASSAGE_PREFIX,
    )
