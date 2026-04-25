from main import build_status

def test_build_status_structure():
    status = build_status()
    assert "project_root" in status
    assert "project_name" in status
    assert "rag_collection" in status
    assert "rag_available" in status

def test_project_identity():
    status = build_status()
    assert "Applied Econometrics" in status["project_name"]
