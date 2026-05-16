from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.services.claim_extractor import claim_extractor
from app.services.retrieval_service import retrieval_service
from app.services.verification_service import verification_service
from app.services.scoring_service import scoring_service

from app.services.ollama_service import ollama_service

router = APIRouter()

class VerifyRequest(BaseModel):
    text: str

class ClaimResult(BaseModel):
    claim: str
    status: str
    risk_score: float
    start: int
    end: int
    evidence: Optional[str] = None
    source: Optional[str] = None
    explanation: Optional[str] = None

import time
from app.utils.logger import logger

class VerifyResponse(BaseModel):
    text: str
    claims: List[ClaimResult]
    overall_risk: float
    metadata: Optional[dict] = None

@router.post("/verify", response_model=VerifyResponse)
async def verify_text(request: VerifyRequest):
    start_time = time.time()
    
    # 1. Extract Claims
    extract_start = time.time()
    extracted_claims = claim_extractor.extract_claims(request.text)
    extract_time = time.time() - extract_start
    
    results = []
    retrieval_time = 0
    verification_time = 0
    explanation_time = 0
    
    for claim_data in extracted_claims:
        claim_text = claim_data["text"]
        
        # 2. Retrieve Evidence
        r_start = time.time()
        retrieval_results = retrieval_service.retrieve_evidence(claim_text, n_results=1)
        retrieval_time += (time.time() - r_start)
        
        best_evidence = ""
        source = "Unknown"
        if retrieval_results["documents"] and retrieval_results["documents"][0]:
            best_evidence = retrieval_results["documents"][0][0]
            source = retrieval_results["metadatas"][0][0].get("source", "Unknown")
        
        # 3. Verify Claim
        v_start = time.time()
        verification = verification_service.verify_claim(claim_text, best_evidence)
        verification_time += (time.time() - v_start)
        
        # 4. Generate Explanation (Async-style with Ollama)
        e_start = time.time()
        explanation = ollama_service.generate_explanation(
            claim_text, 
            best_evidence, 
            verification["status"]
        )
        explanation_time += (time.time() - e_start)
        
        results.append({
            "claim": claim_text,
            "status": verification["status"],
            "risk_score": verification["risk_score"],
            "start": claim_data["start"],
            "end": claim_data["end"],
            "evidence": best_evidence,
            "source": source,
            "explanation": explanation
        })
    
    # 4. Final Scoring
    summary = scoring_service.calculate_final_score(results)
    
    total_time = time.time() - start_time
    
    return {
        "text": request.text,
        "claims": results,
        "overall_risk": summary["overall_risk"],
        "metadata": {
            "total_time_ms": int(total_time * 1000),
            "extraction_time_ms": int(extract_time * 1000),
            "retrieval_time_ms": int(retrieval_time * 1000),
            "verification_time_ms": int(verification_time * 1000),
            "explanation_time_ms": int(explanation_time * 1000),
            "claim_count": len(results)
        }
    }
