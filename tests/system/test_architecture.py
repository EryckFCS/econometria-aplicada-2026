import re
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

def test_root_structure():
    """Validates that the root directory follows Blueprint v8.0.0."""
    required_dirs = [
        "bibliography/raw",
        "bibliography/processed",
        "bibliography/markdown",
        "bibliography/sanitized",
        "config",
        "data",
        "docs/vaults",
        "docs/management",
        "docs/readings",
        "docs/syllabus",
        "reports",
        "scratch",
        "scripts",
        "src/core",
        "tests/governance",
        "tests/system",
    ]

    for d in required_dirs:
        assert (REPO_ROOT / d).is_dir(), f"Missing required directory: {d}"


def test_evidence_naming_convention():
    """Ensures evidence units follow the [unit]-[cat]-[seq]-[slug] convention."""
    vaults_path = REPO_ROOT / "docs" / "vaults"
    if not vaults_path.exists():
        pytest.skip("No evidence folder found.")
        
    pattern = re.compile(r"^u\d-(aa|ape|acd)-\d{2}-[\w-]+$")

    for item in vaults_path.iterdir():
        if item.is_dir() and not item.name.startswith("."):
            assert item.name == item.name.lower(), f"Vault '{item.name}' must be lowercase."
            assert pattern.match(item.name), (
                f"Vault '{item.name}' does not follow convention [unit]-[cat]-[seq]-[slug]."
            )


def test_evidence_autonomy():
    """Validates that each research evidence unit has the required internal structure."""
    vaults_path = REPO_ROOT / "docs" / "vaults"
    if not vaults_path.exists():
        pytest.skip("No evidence folder found.")
        
    required_internal = ["assets", "logs", "chapters", "index.qmd"]

    for vault in vaults_path.iterdir():
        if vault.is_dir() and not vault.name.startswith("."):
            for req in required_internal:
                assert (vault / req).exists(), (
                    f"Vault '{vault.name}' is missing '{req}' for autonomy."
                )


def test_zero_floating_root():
    """Ensures no unauthorized research files are floating in the root."""
    prohibited_extensions = [".ipynb", ".csv", ".xlsx", ".pdf", ".do"]
    
    for item in REPO_ROOT.iterdir():
        if item.is_file() and item.suffix in prohibited_extensions:
            pytest.fail(f"Floating file detected in root: {item.name}. Move it to a vault.")
            
def test_canonical_docs_v8():
    """Ensures core governance and management files exist."""
    required_files = [
        "AGENTS.md",
        "docs/management/ARCHITECTURE.md",
        "docs/management/ROADMAP.md",
        "docs/management/CHANGELOG.md",
        "docs/management/SESSION_REPORT.md",
        "docs/management/status/RAG_CURATED_BOOKS_CONSUMPTION.md",
        "bibliography/bibliography_index.json",
        "bibliography/rag_status.json"
    ]
    for f in required_files:
        assert (REPO_ROOT / f).is_file(), f"Missing required governance file: {f}"
