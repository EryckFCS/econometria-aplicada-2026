from __future__ import annotations
from ecs_quantitative.core.federation import FederatedNodeConfig


class NodeSettings(FederatedNodeConfig):
    """Configuración canonizada para el nodo applied_econometrics_2026."""

    project_name: str = "Applied Econometrics 2026"
    rag_collection: str = "applied_econometrics_2026"


settings = NodeSettings()
