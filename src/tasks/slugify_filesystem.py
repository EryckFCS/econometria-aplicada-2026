import os
import re
import unicodedata
from pathlib import Path
from loguru import logger


def slugify(text):
    """Convierte texto a un formato seguro para sistemas de archivos (kebab-case)."""
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[-\s]+", "-", text)


class SlugificationProtocol:
    def __init__(self, root_path: Path):
        self.root = root_path
        self.config_path = root_path / "config" / "intelligence_map.json"
        self.path_map = {}  # Old -> New

    def process_directory(self, target_dir: Path):
        """Escanea y renombra archivos de forma recursiva."""
        if not target_dir.exists():
            return

        # Primero archivos, luego carpetas (de abajo hacia arriba para no perder punteros)
        for root, dirs, files in os.walk(target_dir, topdown=False):
            for name in files:
                old_path = Path(root) / name
                if old_path.suffix == ".json" and old_path.name != "intelligence_map.json":
                    continue  # Skip other jsons for now if needed

                new_name = slugify(old_path.stem) + old_path.suffix
                new_path = Path(root) / new_name

                if old_path != new_path:
                    logger.info(f"Renaming file: {old_path.name} -> {new_name}")
                    old_path.rename(new_path)
                    self.path_map[str(old_path.relative_to(self.root))] = str(
                        new_path.relative_to(self.root)
                    )

            for name in dirs:
                old_path = Path(root) / name
                new_name = slugify(name)
                new_path = Path(root) / new_name

                if old_path != new_path:
                    logger.info(f"Renaming dir: {name} -> {new_name}")
                    old_path.rename(new_path)
                    self.path_map[str(old_path.relative_to(self.root))] = str(
                        new_path.relative_to(self.root)
                    )

    def update_config(self):
        """Actualiza las referencias en el mapa de inteligencia."""
        if not self.config_path.exists():
            return

        with open(self.config_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Reemplazo simple de strings (peligroso pero efectivo si los paths son únicos)
        # Ordenamos por longitud descendente para evitar reemplazos parciales
        sorted_paths = sorted(self.path_map.items(), key=lambda x: len(x[0]), reverse=True)

        updated_count = 0
        for old, new in sorted_paths:
            if old in content:
                content = content.replace(f'"{old}"', f'"{new}"')
                updated_count += 1

        with open(self.config_path, "w", encoding="utf-8") as f:
            f.write(content)

        logger.success(f"Configuración actualizada: {updated_count} referencias cambiadas.")


if __name__ == "__main__":
    protocol = SlugificationProtocol(Path("."))

    logger.info("--- Fase I: Slugificación de Bibliografía ---")
    protocol.process_directory(Path("bibliography"))

    logger.info("--- Fase II: Slugificación de Evidencia ---")
    protocol.process_directory(Path("docs/vaults"))

    logger.info("--- Fase III: Actualización de Configuración ---")
    protocol.update_config()
