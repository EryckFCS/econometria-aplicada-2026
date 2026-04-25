# Catálogo de variables para APE1 (Panel de América Latina)
# Centralizado para evitar duplicación en scripts.

import tomllib
from pathlib import Path


def load_catalog(name: str) -> list[dict]:
    """Carga un catálogo de variables desde un archivo TOML en config/"""
    catalog_path = (
        Path(__file__).resolve().parents[2] / "config" / f"catalog_{name}.toml"
    )
    if catalog_path.exists():
        with catalog_path.open("rb") as f:
            data = tomllib.load(f)
            return data.get("series", [])
    raise FileNotFoundError(f"No se encontró el catálogo: {catalog_path}")


# Para retrocompatibilidad (se recomienda usar load_catalog en nuevas tareas)
try:
    SERIES_APE1 = load_catalog("ape1")
except FileNotFoundError:
    SERIES_APE1 = []

try:
    SERIES_GRUPO = load_catalog("equipo")
except FileNotFoundError:
    SERIES_GRUPO = []
