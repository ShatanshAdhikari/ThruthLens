import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_verify_endpoint_basic():
    # Note: This might be slow the first time as it loads models
    response = client.post(
        "/api/verify",
        json={"text": "Paris is the capital of France."}
    )
    assert response.status_code == 200
    assert "claims" in response.json()
    assert len(response.json()["claims"]) > 0
    assert response.json()["claims"][0]["claim"] == "Paris is the capital of France."
