"""Entrypoint: regenerate the RAG index from the content .md files (offline)."""

from index_builder.build import build_index


def main() -> None:
    build_index()


if __name__ == "__main__":
    main()
