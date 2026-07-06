"""Web-layer tests using FastAPI's TestClient."""
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_measure_accepts_valid_payload():
    # duration=0 is invalid; use a tiny duration so the background job finishes fast.
    resp = client.post(
        "/measure",
        json={"url": "https://example.com", "frequency": 1, "duration": 0.01},
    )
    assert resp.status_code == 202
    body = resp.json()
    assert body["status"] == "started"
    assert body["url"] == "https://example.com/"
    assert "job_id" in body


def test_measure_rejects_bad_payload():
    resp = client.post(
        "/measure", json={"url": "not-a-url", "frequency": -5}
    )
    assert resp.status_code == 422
