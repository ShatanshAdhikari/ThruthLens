import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal, Base, engine
from app.models.database import VerificationJob

client = TestClient(app)

@pytest.fixture
def db():
    # Setup: Create tables
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    # Teardown: Close session
    db.close()

def test_consensus_verification_pipeline(db):
    # Test a claim that should trigger consensus
    response = client.post(
        "/api/verify",
        json={"text": "Paris is the capital of France."}
    )
    assert response.status_code == 200
    data = response.json()
    
    assert "job_id" in data
    assert "claims" in data
    assert len(data["claims"]) > 0
    
    claim = data["claims"][0]
    assert "consensus_stats" in claim
    assert "evidence_details" in claim
    assert len(claim["evidence_details"]) > 0
    
    # Check if it was saved to the DB
    job = db.query(VerificationJob).filter(VerificationJob.id == data["job_id"]).first()
    assert job is not None
    assert job.status == "Completed"

def test_contradiction_consensus(db):
    # Test a claim that is likely to be contradicted
    response = client.post(
        "/api/verify",
        json={"text": "The Eiffel Tower was built in 1920."}
    )
    assert response.status_code == 200
    data = response.json()
    
    # Even if web results are mixed, our logic should weigh fact-checks or contradictions
    # Depending on live web results, this might be Contradicted or Inconclusive
    assert data["overall_risk"] > 0
