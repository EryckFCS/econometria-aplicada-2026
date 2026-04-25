"""Query the bibliography vector store from the central institutional brain."""

from __future__ import annotations

import argparse
from pathlib import Path
from ecs_quantitative.ingestion.rag import BibliographyRAG

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Query the Central Institutional Brain."
    )
    parser.add_argument(
        "query", help="Query text to search in the bibliography corpus."
    )
    parser.add_argument(
        "--persist-path",
        type=Path,
        default=Path.home() / ".capital" / "brain" / "vector_store",
        help="Directory where the central vector store is persisted.",
    )
    parser.add_argument(
        "--collection",
        default="econometria_2026_bibliografia",
        help="ChromaDB collection name (lobe).",
    )
    parser.add_argument(
        "--top-k", type=int, default=5, help="Number of hits to return."
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    rag = BibliographyRAG(
        persist_path=args.persist_path, collection_name=args.collection
    )
    results = rag.query(args.query, n_results=args.top_k)
    print(rag.format_results(results))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
