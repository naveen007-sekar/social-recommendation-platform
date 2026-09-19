from fastapi.testclient import TestClient
from app.main import app
def test_health_returns_a_safe_response():
    r=TestClient(app).get("/health")
    assert r.status_code == 200
    assert r.json()["status"] in {"healthy","degraded"}
