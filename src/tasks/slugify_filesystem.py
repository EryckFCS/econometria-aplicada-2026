from pathlib import Path
from ecs_quantitative.management.filesystem import SlugificationProtocol
from loguru import logger

if __name__ == "__main__":
    protocol = SlugificationProtocol(Path("."))
    logger.info("--- Standardizing Filesystem ---")
    protocol.process_directory(Path("bibliography"))
    protocol.process_directory(Path("docs/vaults"))
    protocol.update_config()
