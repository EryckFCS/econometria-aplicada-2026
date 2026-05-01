from __future__ import annotations
from ecs_quantitative.core.federation import NodeBrain
from .config import settings

# Instancia global del cerebro del nodo
brain = NodeBrain(config=settings)
