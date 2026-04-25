"""Orquestador controlado de la Unidad 1.

Este modulo solo describe el plan de ejecucion. No dispara ingesta ni
recalcula artefactos de datos.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys

if __package__ in {None, ""}:
    sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.core.config import settings


@dataclass(frozen=True, slots=True)
class MasterBuildStep:
    """Define un paso declarativo del master build."""

    label: str
    script: Path
    purpose: str


def build_master_plan() -> list[MasterBuildStep]:
    """Construye el plan canonico sin ejecutar ningun paso."""
    tasks_dir = settings.root_path / "src" / "tasks"
    return [
        MasterBuildStep(
            label="T01",
            script=tasks_dir / "T01-U1-APE-Homicidios_Ecuador.py",
            purpose="Construccion de la base raw de homicidios y controles",
        ),
        MasterBuildStep(
            label="T02",
            script=tasks_dir / "T02-U1-ACD-Consolidado_Equipo.py",
            purpose="Consolidacion de variables normalizadas del equipo",
        ),
        MasterBuildStep(
            label="T03",
            script=tasks_dir / "T03-U1-AA-Panel_Ambiental_Latam.py",
            purpose="Panel ambiental LATAM y controles estructurales",
        ),
        MasterBuildStep(
            label="T04",
            script=tasks_dir / "T04-U1-ACD-SEM_Homicidios.py",
            purpose="SEM de homicidios y diagnostico de variables",
        ),
        MasterBuildStep(
            label="T05",
            script=tasks_dir / "T05-Report_Engine.py",
            purpose="Renderizado controlado de la capa de reporteo",
        ),
    ]


def main() -> int:
    """Imprime el plan controlado de la Unidad 1."""
    print(f"Plan controlado para {settings.project_name}")
    for step in build_master_plan():
        print(
            f"{step.label}: {step.script.relative_to(settings.root_path)} - {step.purpose}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
