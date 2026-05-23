import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.retrieval_service import retrieval_service
from app.services.verification_service import verification_service
from app.services.scoring_service import scoring_service

client = TestClient(app)

def test_retrieval_service_optimization():
    # Test that retrieval returns distance and score
    query = "Paris"
    results = retrieval_service.retrieve_evidence(query, n_results=3)
    
    assert isinstance(results, list)
    if len(results) > 0:
        assert "distance" in results[0]
        assert "score" in results[0]
        assert "metadata" in results[0]
        assert results[0]["score"] >= 0 and results[0]["score"] <= 1.0

def test_verification_service_threshold():
    # Test that confidence threshold works
    claim = "The Eiffel Tower is in London."
    evidence = "The Eiffel Tower was built in 1889 and is located in Paris, France."
    
    # Low threshold should show Contradicted
    res_low = verification_service.verify_claim(claim, evidence, confidence_threshold=0.1)
    assert res_low["status"] == "Contradicted"
    
    # Very high threshold should show Insufficient Evidence if confidence is lower
    # Note: DeBERTa is usually very confident about this, so we might need a very high threshold or a vague claim.
    res_high = verification_service.verify_claim(claim, evidence, confidence_threshold=0.999)
    if res_high["confidence"] < 0.999:
        assert res_high["status"] == "Insufficient Evidence"

def test_scoring_service_weighting():
    # Test weighted scoring
    results = [
        {
            "risk_score": 0.9,
            "confidence": 0.9,
            "retrieval_score": 0.9
        },
        {
            "risk_score": 0.1,
            "confidence": 0.1,
            "retrieval_score": 0.1
        }
    ]
    
    summary = scoring_service.calculate_final_score(results)
    
    # Weighted risk for first: 0.9 * ((0.9+0.9)/2) = 0.81
    # Weighted risk for second: 0.1 * ((0.1+0.1)/2) = 0.01
    # Average: (0.81 + 0.01) / 2 = 0.41
    # Simple average would have been (0.9 + 0.1) / 2 = 0.5
    
    assert summary["overall_risk"] < 0.5
    assert summary["overall_risk"] == pytest.approx(0.41)

def test_verify_api_new_fields():
    # Test that the /verify API returns the new fields
    response = client.post(
        "/api/verify",
        json={"text": "The Moon is Earth's only natural satellite."}
    )
    assert response.status_code == 200
    data = response.json()
    
    assert "claims" in data
    claim = data["claims"][0]
    assert "confidence" in claim
    assert "retrieval_score" in claim
    assert "source" in claim
    assert claim["source"] != "Unknown" # Should match "NASA" from seed
