"""Offline generator that builds the RAG vector index from the content files.

Parallel to card_builder: never runs inside a request. See plan.md §14 for the
build order (build_cards.py writes the cards -> build_index.py indexes them).
"""
