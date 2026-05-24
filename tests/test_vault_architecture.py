"""Gatekeeper for the controlled Level 5 vault structure."""

from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_level_5_vaults_exist() -> None:
    """Confirma la presencia de las bóvedas y puntos de arranque canonicos."""
    required_paths = [
        REPO_ROOT / "main.py",
        REPO_ROOT / "src" / "core",
        REPO_ROOT / "src" / "core" / "config.py",
        REPO_ROOT / "src" / "core" / "brain.py",
        REPO_ROOT / "src" / "orchestration",
        REPO_ROOT / "src" / "orchestration" / "M01-U1-APE-Master_Build.py",
        REPO_ROOT / "docs" / "vaults",
        REPO_ROOT / "docs" / "vaults" / "u1-aa-01-applied-econometrics",
        REPO_ROOT / "docs" / "writing",
        REPO_ROOT / "bibliography",
        REPO_ROOT / "bibliography" / "raw",
        REPO_ROOT / "data" / "curation" / "group_work" / "standardized",
    ]

    for path in required_paths:
        assert path.exists(), f"Falta la ruta requerida: {path}"

    expected_vaults = [
        REPO_ROOT
        / "docs"
        / "vaults"
        / "u1-aa-01-applied-econometrics"
        / "ape1-exploracion-ambiental",
        REPO_ROOT
        / "docs"
        / "vaults"
        / "u1-aa-01-applied-econometrics"
        / "acd0-evaluacion-diagnostica",
        REPO_ROOT
        / "docs"
        / "vaults"
        / "u1-aa-01-applied-econometrics"
        / "acd1-variables-normalizadas",
        REPO_ROOT
        / "docs"
        / "vaults"
        / "u1-aa-01-applied-econometrics"
        / "acd2-sem-homicidios",
    ]
    for path in expected_vaults:
        assert path.is_dir(), f"Falta la sub-boveda de evidencia: {path}"

    assert (REPO_ROOT / "bibliography" / "bibliography_index.json").is_file()
    assert (REPO_ROOT / "bibliography" / "rag_status.json").is_file()
    assert (REPO_ROOT / "bibliography" / "raw" / "manuals").is_dir()
    assert (
        REPO_ROOT
        / "bibliography"
        / "raw"
        / "manuals"
        / "inec_metodologia_enemdu.pdf"
    ).is_file()
    assert (
        REPO_ROOT
        / "bibliography"
        / "raw"
        / "manuals"
        / "iess_2024_bulletin_29.pdf"
    ).is_file()


def test_zero_floating_in_vault_units() -> None:
    """Enfuerza la Doctrina Zero Floating dentro de la raíz de cada sub-bóveda y sus sub-unidades."""
    import pytest
    vaults_path = REPO_ROOT / "docs" / "vaults"
    if not vaults_path.exists():
        return

    forbidden_ext = [".docx", ".xlsx", ".pdf", ".csv", ".dta", ".do", ".zip", ".rar"]
    allowed_names = ["index.qmd", "references.bib", "knowledge_map.json", "settings.json", "settings.toml", ".gitignore", "_quarto.yml"]

    for p in vaults_path.rglob("*"):
        if p.is_file() and not p.name.startswith("."):
            parts = p.parts
            fine_dirs = {
                "assets", "data", "scripts", "logs", "readings", "scratch",
                "notebooks", ".quarto", "chapters", "reports", "code", "graph",
                "_book", "analysis_erick_condoy", "notes", "templates"
            }
            if not any(fd in parts for fd in fine_dirs):
                is_forbidden = p.suffix in forbidden_ext or (p.suffix in [".md", ".py"] and p.name not in allowed_names)
                if is_forbidden and "template" not in p.name.lower():
                    pytest.fail(
                        f"Archivo flotante prohibido detectado en la raíz de la bóveda '{p.parent.name}': {p.name}. "
                        f"Por favor muévelo a assets/, data/, scripts/, o readings/."
                    )

