"""Offline evaluation of the bot's routing and retrieval.

Two orthogonal checks over one shared dataset (`evals.dataset`):

- routing: does `classify_route` send each question to the right gate? Pure and
  fast, asserted in tests/test_routing.py (runs in CI).
- retrieval recall: for questions that should reach RAG, does the real index
  return the passage that holds the answer? Heavy (loads the model), so it lives
  in `evals.retrieval_eval` as a runnable report, not a default test.

The dataset is the regression net: when we change a gate, a prompt, or the
retriever (reranker, multi-query…), rerun both and watch the numbers move.
"""
