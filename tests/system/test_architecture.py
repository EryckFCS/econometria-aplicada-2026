import re
from pathlib import Path
import pytest

# Localización de la raíz del repositorio relativa a este archivo (tests/system/test_architecture.py)
REPO_ROOT = Path(__file__).resolve().parents[2]

def test_root_structure():
    """Valida la estructura de directorios Blueprint v8.1.5."""
    required_dirs = [
        "config",
        "data",
        "docs/vaults",
        "docs/management",
        "docs/readings",
        "docs/syllabus",
        "reports",
        "scratch",
        "scripts",
        "src",
        "tests/system",
    ]
    
    for d in required_dirs:
        assert (REPO_ROOT / d).is_dir(), f"Directorio requerido ausente: {d}"

def test_bibliography_presence():
    """Valida que el directorio de bibliografía exista."""
    bib_dir = REPO_ROOT / "bibliography"
    assert bib_dir.is_dir(), "Directorio 'bibliography/' ausente."
    # Los subdirectorios (processed, markdown, sanitized) son opcionales 
    # debido a la centralización en el Data Lake.

def test_zero_floating_doctrine():
    """Enfuerza la Doctrina Zero Floating en la raíz."""
    forbidden_ext = [".ipynb", ".csv", ".xlsx", ".pdf", ".do", ".dta"]
    forbidden_dirs = ["writing", "deliveries", "notebooks", "vaults_legacy"]
    
    for item in REPO_ROOT.iterdir():
        if item.is_file() and item.suffix in forbidden_ext:
            # Excepción para archivos de configuración o README
            if item.name not in ["README.md", "main.py"]:
                pytest.fail(f"Archivo flotante detectado en raíz: {item.name}. Muévelo a una bóveda.")
        
        if item.is_dir() and item.name in forbidden_dirs:
            pytest.fail(f"Carpeta legada/prohibida detectada en raíz: {item.name}.")

def test_evidence_naming_convention():
    """Valida la convención de nombres de bóvedas de evidencia [unit]-[cat]-[seq]-[slug]."""
    vaults_path = REPO_ROOT / "docs" / "vaults"
    if not vaults_path.exists():
        pytest.skip("No se encontró la carpeta de evidencias.")

    # Patrón estándar: u[X]-[categoría]-[secuencia]-[slug]
    # Patrón especial: [slug] (letras minúsculas y guiones)
    standard_pattern = re.compile(r"^u\d-(aa|ape|acd)-\d{2}-[\w-]+$")
    special_pattern = re.compile(r"^[a-z][a-z0-9-_]+$")

    for item in vaults_path.iterdir():
        if item.is_dir() and not item.name.startswith("."):
            assert item.name == item.name.lower(), f"La bóveda '{item.name}' debe estar en minúsculas."
            is_valid = standard_pattern.match(item.name) or special_pattern.match(item.name)
            assert is_valid, (
                f"La bóveda '{item.name}' no sigue ninguna convención válida ([unit]-[cat]-[seq]-[slug] o slug simple)."
            )

def test_governance_files():
    """Valida la presencia de archivos críticos de gobernanza."""
    required_files = [
        "AGENTS.md",
        "pyproject.toml",
        "uv.lock"
    ]
    for f in required_files:
        assert (REPO_ROOT / f).is_file(), f"Archivo de gobernanza ausente: {f}"
