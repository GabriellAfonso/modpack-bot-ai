"""Embed the content chunks and persist the LlamaIndex vector store.

Reads guides + Pokémon cards via index_builder.nodes, embeds them locally with
the shared e5 model, and persists to content/index/. The only heavy import
(the embedding model / torch) lives behind this module, not in nodes.py.
"""

import os

from llama_index.core import VectorStoreIndex
from llama_index.core.schema import TextNode

from index_builder.nodes import collect_chunks, node_metadata
from modpack_bot.embedding import build_embed_model

DEFAULT_INDEX_DIR = os.path.join("content", "index")
_DEFAULT_CONTENT_DIR = "content"


def build_index(
    content_dir: str = _DEFAULT_CONTENT_DIR, index_dir: str = DEFAULT_INDEX_DIR
) -> int:
    """Chunk every guide and card, embed locally, and persist the index.

    Returns the node count (also printed, mirroring card_builder's output).
    """
    nodes = [
        TextNode(text=chunk.text, metadata=node_metadata(chunk))
        for chunk in collect_chunks(content_dir)
    ]
    index = VectorStoreIndex(nodes, embed_model=build_embed_model())
    index.storage_context.persist(index_dir)
    print(f"Indexed {len(nodes)} nodes into {index_dir}")
    return len(nodes)
