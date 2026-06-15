"""Retrieval recall report: does the real index surface the answer passage?

Run it after touching the retriever, the index, or the chunking:

    python -m evals.retrieval_eval [--index content/index]

For every dataset case with an `expected_passage`, it embeds the question
against the persisted index and checks whether the substring shows up in any
retrieved passage. Cases flagged `rag_recall_known_bad` are reported apart and
do NOT fail the run — they document a known retriever miss (handled today by a
dedicated gate). The exit code is nonzero only when an expected-good case
regresses, so this doubles as a manual/CI guard.

Heavy: loads the embedding model + index, hence a script and not a unit test.
"""

import argparse
import sys

from evals.dataset import CASES, EvalCase
from modpack_bot.retrieval import ContextRetriever, LlamaIndexRetriever


def _recall_hit(retriever: ContextRetriever, case: EvalCase) -> bool:
    """True when some retrieved passage contains the case's expected substring."""
    assert case.expected_passage is not None
    needle = case.expected_passage.lower()
    return any(needle in passage.lower() for passage in retriever.retrieve(case.question))


def _report(retriever: ContextRetriever) -> int:
    """Print a per-case table and return the count of expected-good regressions."""
    cases = [c for c in CASES if c.expected_passage is not None]
    regressions = 0
    for case in cases:
        hit = _recall_hit(retriever, case)
        regressions += _print_row(case, hit)
    _print_summary(cases, regressions)
    return regressions


def _print_row(case: EvalCase, hit: bool) -> int:
    """Print one result line; return 1 if it is an expected-good miss."""
    if case.rag_recall_known_bad:
        mark = "ok (still bad)" if not hit else "FIXED -> clear the flag"
        print(f"[known-bad] {mark:<22} {case.question}")
        return 0
    print(f"[{'PASS' if hit else 'FAIL':<4}] {'':<22} {case.question}")
    return 0 if hit else 1


def _print_summary(cases: list[EvalCase], regressions: int) -> None:
    good = [c for c in cases if not c.rag_recall_known_bad]
    passed = len(good) - regressions
    print(f"\nrecall (expected-good): {passed}/{len(good)}")
    if regressions:
        print(f"REGRESSIONS: {regressions} — a case that should be retrievable is not")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index", default="content/index", help="persisted index dir")
    args = parser.parse_args()
    sys.exit(1 if _report(LlamaIndexRetriever(args.index)) else 0)


if __name__ == "__main__":
    main()
