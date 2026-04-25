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
        REPO_ROOT / "docs" / "evidence",
        REPO_ROOT / "docs" / "evidence" / "U1-Applied-Econometrics",
        REPO_ROOT / "docs" / "bibliography" / "readings",
        REPO_ROOT / "docs" / "bibliography" / "syllabus",
        REPO_ROOT / "docs" / "bibliography" / "manuals",
        REPO_ROOT / "docs" / "bibliography",
        REPO_ROOT / "writing",
        REPO_ROOT / "data" / "curation" / "group_work" / "standardized",
    ]

    for path in required_paths:
        assert path.exists(), f"Falta la ruta requerida: {path}"

    expected_evidence = [
        REPO_ROOT
        / "docs"
        / "evidence"
        / "U1-Applied-Econometrics"
        / "APE1-Exploracion-Ambiental",
        REPO_ROOT
        / "docs"
        / "evidence"
        / "U1-Applied-Econometrics"
        / "ACD0-Evaluacion-Diagnostica",
        REPO_ROOT
        / "docs"
        / "evidence"
        / "U1-Applied-Econometrics"
        / "ACD1-Variables-Normalizadas",
        REPO_ROOT
        / "docs"
        / "evidence"
        / "U1-Applied-Econometrics"
        / "ACD2-SEM-Homicidios",
    ]
    for path in expected_evidence:
        assert path.is_dir(), f"Falta la sub-boveda de evidencia: {path}"

    assert (REPO_ROOT / "docs" / "bibliography" / "bibliography_index.json").is_file()
    assert (REPO_ROOT / "docs" / "bibliography" / "rag_status.json").is_file()
    assert (REPO_ROOT / "docs" / "bibliography" / "manuals" / "README.md").is_file()
    assert (REPO_ROOT / "docs" / "bibliography" / "syllabus" / "SYLLABUS.pdf").is_file()
    assert not any((REPO_ROOT / "docs" / "bibliography" / "readings").iterdir())
