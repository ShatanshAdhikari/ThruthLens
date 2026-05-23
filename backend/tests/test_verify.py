import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_verify_endpoint_basic():
    response = client.post(
        "/api/verify",
        json={"text": "Paris is the capital of France."}
    )
    assert response.status_code == 200
    data = response.json()
    assert "claims" in data
    assert "text" in data
    assert len(data["claims"]) > 0
    assert data["claims"][0]["status"] == "Supported"
    assert "start" in data["claims"][0]
    assert "end" in data["claims"][0]

def test_verify_contradiction():
    response = client.post(
        "/api/verify",
        json={"text": "The Eiffel Tower was built in 1920."}
    )
    assert response.status_code == 200
    data = response.json()
    # Based on seed data: "The Eiffel Tower was completed in 1889"
    assert any(c["status"] == "Contradicted" for c in data["claims"])
    assert data["overall_risk"] > 0.5
    assert data["claims"][0]["start"] == 0
    assert data["claims"][0]["end"] > 0

def test_verify_insufficient_evidence():
    response = client.post(
        "/api/verify",
        json={"text": "The price of gold in 1950 was very high."}
    )
    assert response.status_code == 200
    data = response.json()
    # No seed data for gold prices
    assert any(c["status"] == "Insufficient Evidence" for c in data["claims"])

def test_empty_input():
    response = client.post(
        "/api/verify",
        json={"text": ""}
    )
    assert response.status_code == 200
    assert response.json()["claims"] == []
    assert response.json()["overall_risk"] == 0.0

def test_multiple_claims():
    text = "Paris is the capital of France. The Moon is Earth's only natural satellite. Python was created in 1991."
    response = client.post(
        "/api/verify",
        json={"text": text}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["claims"]) >= 3
    # Check if all are likely supported based on seed data
    supported_count = sum(1 for c in data["claims"] if c["status"] == "Supported")
    assert supported_count >= 2
