from fastapi.testclient import TestClient

from localllm.api.main import app


def test_health_includes_basic_config() -> None:
    client = TestClient(app)
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("status") == "ok"
    assert "llm_provider" in data
    assert "qdrant_collection" in data
    assert "embedding_model" in data

