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
        REPO_ROOT / "writing",
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
        / "metodologia_enemdu_general.pdf"
    ).is_file()
    assert (
        REPO_ROOT
        / "bibliography"
        / "raw"
        / "manuals"
        / "06-statistical-bulletin-29-2024.pdf"
    ).is_file()
