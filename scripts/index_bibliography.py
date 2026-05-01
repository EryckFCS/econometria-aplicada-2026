import argparse
import sys
import asyncio
from pathlib import Path
from loguru import logger

# Importar desde la librería central consolidada
try:
    from ecs_quantitative.ingestion.rag import BibliographyRAG
except ImportError:
    # Si no está instalado, intentar añadir el path de las libs si estamos en el mismo workspace
    sys.path.append("/home/erick-fcs/Capital_Workstation/capital-workstation-libs/src")
    from ecs_quantitative.ingestion.rag import BibliographyRAG

PROJECT_ROOT = Path(__file__).resolve().parents[1]

sys.path.append(str(PROJECT_ROOT))

from src.core.lake import DEFAULT_BIBLIOGRAPHY_COLLECTION  # noqa: E402
from src.core.lake import write_bibliography_manifest  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Index bibliography PDFs into the Sovereign L0 Brain."
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=None,
        help=(
            "Path to the bibliographic manifest. If omitted, the manifest is built "
            "from the central Lake registry."
        ),
    )
    parser.add_argument(
        "--persist-path",
        type=Path,
        default=Path.home() / ".capital" / "brain" / "vector_store",
        help="Directory where the central vector store is persisted.",
    )
    parser.add_argument(
        "--collection",
        default=DEFAULT_BIBLIOGRAPHY_COLLECTION,
        help="ChromaDB collection name (lobe).",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional maximum number of manifest entries to index.",
    )
    return parser


async def run_indexing() -> int:
    args = build_parser().parse_args()

    manifest_path = args.manifest
    if manifest_path is None or not manifest_path.exists():
        manifest_path = write_bibliography_manifest(
            output_path=PROJECT_ROOT / "scratch" / "lake_bibliography_manifest.json"
        )
        logger.info(f"Manifest generated from the central Lake: {manifest_path}")

    logger.info(f"🧠 Iniciando indexación Soberana L0: {args.collection}")

    rag = BibliographyRAG(
        persist_path=args.persist_path,
        collection_name=args.collection,
    )

    # 1. Base Indexing (Text & Formulas) - Nivel 0 puro
    summary = rag.index_manifest(manifest_path, limit=args.limit)
    logger.success(f"✅ Consolidación L0 completada: {summary}")

    return 0


if __name__ == "__main__":
    asyncio.run(run_indexing())
