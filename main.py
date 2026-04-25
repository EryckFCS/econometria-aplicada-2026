from __future__ import annotations
from typing import Any

def build_status(config: Any | None = None, brain: Any | None = None) -> dict[str, Any]:
    if config is None:
        from src.core.config import settings as config
    if brain is None:
        from src.core.brain import brain as brain

    return {
        "project_root": str(config.root_path),
        "project_name": config.project_name,
        "rag_collection": getattr(brain, "collection", "applied_econometrics"),
        "rag_available": getattr(brain, "memory", None) is not None,
    }

def main() -> int:
    status = build_status()
    print(f"📊 {status['project_name']} 2026")
    print(f"Root: {status['project_root']}")
    print(f"RAG collection: {status['rag_collection']}")
    print(f"RAG disponible: {'sí' if status['rag_available'] else 'no'}")
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
