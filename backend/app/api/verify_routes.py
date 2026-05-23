from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.database import VerificationJob, ExtractedClaim, EvidenceSource
from app.services.claim_extractor import claim_extractor
from app.services.retrieval_service import retrieval_service
from app.services.verification_service import verification_service
from app.services.scoring_service import scoring_service
from app.services.ollama_service import ollama_service

router = APIRouter()

class VerifyRequest(BaseModel):
    text: str

class EvidenceDetail(BaseModel):
    text: str
    source: str
    url: Optional[str] = None
    type: str
    verdict: str
    confidence: float

class ClaimResult(BaseModel):
    claim: str
    status: str
    risk_score: float
    confidence: float
    start: int
    end: int
    explanation: Optional[str] = None
    reasoning: Optional[str] = None
    consensus_stats: Dict[str, int]
    evidence_details: List[EvidenceDetail]

import time
from app.utils.logger import logger

class VerifyResponse(BaseModel):
    job_id: int
    text: str
    claims: List[ClaimResult]
    overall_risk: float
    metadata: Optional[dict] = None

@router.post("/verify", response_model=VerifyResponse)
async def verify_text(request: VerifyRequest, db: Session = Depends(get_db)):
    start_time = time.time()
    
    # Create a new verification job in the DB
    job = VerificationJob(text=request.text, status="Processing")
    db.add(job)
    db.commit()
    db.refresh(job)
    
    # 1. Extract Claims
    extract_start = time.time()
    extracted_claims_data = claim_extractor.extract_claims(request.text)
    extract_time = time.time() - extract_start
    
    results = []
    retrieval_time = 0
    verification_time = 0
    explanation_time = 0
    
    for claim_data in extracted_claims_data:
        claim_text = claim_data["text"]
        
        # 2. Retrieve Evidence (Hybrid: Local + Web)
        # For clinical consensus, we want more results
        r_start = time.time()
        retrieval_candidates = retrieval_service.retrieve_hybrid(claim_text, context=request.text, n_results=5)
        retrieval_time += (time.time() - r_start)
        
        # 3. Semantic Verification across candidates with Consensus
        v_start = time.time()
        consensus_res = verification_service.verify_against_sources(claim_text, retrieval_candidates)
        verification_time += (time.time() - v_start)
        
        # 4. Generate Explanation (Async-style with Ollama)
        e_start = time.time()
        # Use the best evidence snippet for explanation
        best_evidence = consensus_res["evidence_details"][0]["text"] if consensus_res["evidence_details"] else ""
        explanation = ollama_service.generate_explanation(
            claim_text, 
            best_evidence, 
            consensus_res["status"]
        )
        explanation_time += (time.time() - e_start)
        
        # Save claim to DB
        claim_obj = ExtractedClaim(
            job_id=job.id,
            claim_text=claim_text,
            status=consensus_res["status"],
            risk_score=consensus_res["risk_score"],
            confidence=consensus_res["confidence"],
            consensus_stats=consensus_res["consensus_stats"],
            reasoning=consensus_res["reasoning"],
            start_char=claim_data["start"],
            end_char=claim_data["end"]
        )
        db.add(claim_obj)
        db.commit()
        db.refresh(claim_obj)
        
        # Save evidence sources to DB
        for ev in consensus_res["evidence_details"]:
            ev_obj = EvidenceSource(
                claim_id=claim_obj.id,
                text=ev["text"],
                source_name=ev["source"],
                url=ev["url"],
                source_type=ev["type"],
                individual_verdict=ev["verdict"],
                verdict_confidence=ev["confidence"]
            )
            db.add(ev_obj)
        
        db.commit()
        
        results.append({
            "claim": claim_text,
            "status": consensus_res["status"],
            "risk_score": consensus_res["risk_score"],
            "confidence": consensus_res["confidence"],
            "start": claim_data["start"],
            "end": claim_data["end"],
            "explanation": explanation,
            "reasoning": consensus_res["reasoning"],
            "consensus_stats": consensus_res["consensus_stats"],
            "evidence_details": consensus_res["evidence_details"]
        })
    
    # 5. Final Scoring
    summary = scoring_service.calculate_final_score(results)
    
    # Update job status
    job.overall_risk = summary["overall_risk"]
    job.status = "Completed"
    db.commit()
    
    total_time = time.time() - start_time
    
    return {
        "job_id": job.id,
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
