"""Configuracion canonica del nodo Applied Econometrics 2026."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


def _project_root() -> Path:
    """Resuelve la raiz canonica del repositorio."""
    return Path(__file__).resolve().parents[2]


@dataclass(frozen=True, slots=True)
class ProjectSettings:
    """Metadatos y rutas canonicas del proyecto."""

    root_path: Path
    project_name: str = "Applied Econometrics"
    rag_collection: str = "global_knowledge"

    def path(self, *parts: str) -> Path:
        """Construye una ruta relativa a la raiz del proyecto."""
        return self.root_path.joinpath(*parts)

    @property
    def data_path(self) -> Path:
        """Ruta al directorio de datos del nodo."""
        return self.root_path / "data"

    @property
    def docs_path(self) -> Path:
        """Ruta al vault documental del nodo."""
        return self.root_path / "docs"

    @property
    def evidence_path(self) -> Path:
        """Ruta al vault de evidencia."""
        return self.docs_path / "evidence"

    @property
    def readings_path(self) -> Path:
        """Ruta al vault de lecturas, reservado como placeholder."""
        return self.docs_path / "readings"

    @property
    def syllabus_path(self) -> Path:
        """Ruta al vault del syllabus institucional."""
        return self.docs_path / "syllabus"

    @property
    def manuals_path(self) -> Path:
        """Ruta al vault de manuales operativos."""
        return self.docs_path / "manuals"

    @property
    def bibliography_path(self) -> Path:
        """Ruta al vault bibliografico local."""
        return self.docs_path / "bibliography"

    @property
    def writing_path(self) -> Path:
        """Ruta a la capa de redaccion y reporteo."""
        return self.root_path / "writing"

    @property
    def logs_path(self) -> Path:
        """Ruta a los logs del nodo."""
        return self.root_path / "logs"

    @property
    def metadata_path(self) -> Path:
        """Ruta a los metadatos y catalogos del nodo."""
        return self.data_path / "metadata"

    @property
    def curation_path(self) -> Path:
        """Ruta a la curacion local de datos."""
        return self.metadata_path / "curation" / "group_work"

    @property
    def standardized_path(self) -> Path:
        """Ruta a los CSV estandarizados del trabajo de grupo."""
        return self.curation_path / "standardized"


settings = ProjectSettings(root_path=_project_root())
