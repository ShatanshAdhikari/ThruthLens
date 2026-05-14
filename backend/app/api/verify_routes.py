from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.services.claim_extractor import claim_extractor
from app.services.retrieval_service import retrieval_service
from app.services.verification_service import verification_service
from app.services.scoring_service import scoring_service

router = APIRouter()

class VerifyRequest(BaseModel):
    text: str

class ClaimResult(BaseModel):
    claim: str
    status: str
    risk_score: float
    evidence: Optional[str] = None
    source: Optional[str] = None

class VerifyResponse(BaseModel):
    claims: List[ClaimResult]
    overall_risk: float

@router.post("/verify", response_model=VerifyResponse)
async def verify_text(request: VerifyRequest):
    # 1. Extract Claims
    extracted_claims = claim_extractor.extract_claims(request.text)
    
    results = []
    for claim in extracted_claims:
        # 2. Retrieve Evidence
        retrieval_results = retrieval_service.retrieve_evidence(claim, n_results=1)
        
        best_evidence = ""
        source = "Unknown"
        if retrieval_results["documents"] and retrieval_results["documents"][0]:
            best_evidence = retrieval_results["documents"][0][0]
            source = retrieval_results["metadatas"][0][0].get("source", "Unknown")
        
        # 3. Verify Claim
        verification = verification_service.verify_claim(claim, best_evidence)
        
        results.append({
            "claim": claim,
            "status": verification["status"],
            "risk_score": verification["risk_score"],
            "evidence": best_evidence,
            "source": source
        })
    
    # 4. Final Scoring
    summary = scoring_service.calculate_final_score(results)
    
    return {
        "claims": results,
        "overall_risk": summary["overall_risk"]
    }
