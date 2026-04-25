"""Estado basal del canal de memoria institucional."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class BrainState:
    """Describe el estado inicial del subsistema de memoria."""

    collection: str = "global_knowledge"
    memory: Any | None = None
    status: str = "dormant"


brain = BrainState()
