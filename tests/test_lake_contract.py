from pathlib import Path

from ecs_quantitative.management.lake import LakeManager

from src.core.lake import build_bibliography_manifest, write_bibliography_manifest


def test_bibliography_manifest_is_built_from_the_central_lake(tmp_path: Path) -> None:
    source_file = tmp_path / "sample_bibliography.pdf"
    source_file.write_bytes(b"%PDF-1.4\n% sample bibliography\n")

    lake = LakeManager(lake_base=tmp_path / "lake")
    registered_path = lake.register_bibliography(
        source_file, "sample_source", tags=["test"]
    )

    manifest = build_bibliography_manifest(lake_base=lake.base)

    assert manifest["library"]
    entry = manifest["library"][0]
    assert entry["id"] == "sample_source"
    assert entry["path"] == str(registered_path)
    assert entry["source_type"] == "book"
    assert entry["tags"] == ["test"]


def test_bibliography_manifest_can_be_written_to_disk(tmp_path: Path) -> None:
    source_file = tmp_path / "sample_bibliography.pdf"
    source_file.write_bytes(b"%PDF-1.4\n% sample bibliography\n")

    lake = LakeManager(lake_base=tmp_path / "lake")
    lake.register_bibliography(source_file, "sample_source", tags=["test"])

    output_path = write_bibliography_manifest(
        output_path=tmp_path / "generated_manifest.json", lake_base=lake.base
    )

    assert output_path.is_file()
    assert "sample_source" in output_path.read_text(encoding="utf-8")
