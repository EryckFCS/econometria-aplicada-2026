from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ecs_quantitative.management.lake import LakeManager

from .config import settings


DEFAULT_BIBLIOGRAPHY_COLLECTION = "bibliography"


def resolve_resources() -> None:
    """Resolve the node resources declared in the canonical config."""
    settings.resolve_resources()


def get_lake_manager(lake_base: Path | None = None) -> LakeManager:
    """Return the central Lake manager used by the node."""
    return LakeManager(lake_base=lake_base)


def build_bibliography_manifest(lake_base: Path | None = None) -> dict[str, Any]:
    """Build a BibliographyRAG manifest from the central Lake registry."""
    lake = get_lake_manager(lake_base)
    entries: list[dict[str, Any]] = []

    for bibliography_id, resource in sorted(
        lake.registry.get("bibliography", {}).items()
    ):
        source_path = lake.resolve(bibliography_id, category="bibliography")
        if source_path is None or not source_path.exists():
            continue

        entries.append(
            {
                "id": bibliography_id,
                "name": resource.get("original_name")
                or resource.get("filename")
                or bibliography_id,
                "path": str(source_path),
                "source_type": resource.get("source_type", "book"),
                "tags": resource.get("tags", []),
            }
        )

    if not entries:
        raise ValueError("No bibliography resources registered in the central Lake.")

    return {"library": entries}


def write_bibliography_manifest(
    output_path: Path | None = None, lake_base: Path | None = None
) -> Path:
    """Persist a Lake-derived bibliographic manifest for the local node scripts."""
    manifest = build_bibliography_manifest(lake_base=lake_base)
    target_path = (
        output_path
        or Path(__file__).resolve().parents[2]
        / "scratch"
        / "lake_bibliography_manifest.json"
    )
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return target_path
