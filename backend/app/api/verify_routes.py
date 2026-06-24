import asyncio
import json
import time
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
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
from app.utils.logger import logger

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


class VerifyResponse(BaseModel):
    job_id: int
    text: str
    claims: List[ClaimResult]
    overall_risk: float
    metadata: Optional[dict] = None


async def _process_single_claim(claim_data: dict, context: str) -> dict:
    """Run retrieval + verification + explanation for one claim in the thread pool."""
    claim_text = claim_data["text"]

    candidates = await asyncio.to_thread(
        retrieval_service.retrieve_hybrid, claim_text, context, 5
    )
    consensus = await asyncio.to_thread(
        verification_service.verify_against_sources, claim_text, candidates
    )
    best_evidence = consensus["evidence_details"][0]["text"] if consensus["evidence_details"] else ""
    explanation = await asyncio.to_thread(
        ollama_service.generate_explanation, claim_text, best_evidence, consensus["status"]
    )

    return {
        "claim": claim_text,
        "status": consensus["status"],
        "risk_score": consensus["risk_score"],
        "confidence": consensus["confidence"],
        "start": claim_data["start"],
        "end": claim_data["end"],
        "explanation": explanation,
        "reasoning": consensus["reasoning"],
        "consensus_stats": consensus["consensus_stats"],
        "evidence_details": consensus["evidence_details"],
    }


def _persist_results(db: Session, text: str, results: list, overall_risk: float) -> int:
    """Write a completed job + all claims + evidence to the DB and return job_id."""
    job = VerificationJob(text=text, status="Completed", overall_risk=overall_risk)
    db.add(job)
    db.flush()

    for res in results:
        claim_obj = ExtractedClaim(
            job_id=job.id,
            claim_text=res["claim"],
            status=res["status"],
            risk_score=res["risk_score"],
            confidence=res["confidence"],
            consensus_stats=res["consensus_stats"],
            reasoning=res["reasoning"],
            start_char=res["start"],
            end_char=res["end"],
        )
        db.add(claim_obj)
        db.flush()

        for ev in res["evidence_details"]:
            db.add(EvidenceSource(
                claim_id=claim_obj.id,
                text=ev["text"],
                source_name=ev["source"],
                url=ev["url"],
                source_type=ev["type"],
                individual_verdict=ev["verdict"],
                verdict_confidence=ev["confidence"],
            ))

    db.commit()
    return job.id


@router.post("/verify", response_model=VerifyResponse)
async def verify_text(request: VerifyRequest, db: Session = Depends(get_db)):
    if not request.text or not request.text.strip():
        return {"job_id": 0, "text": "", "claims": [], "overall_risk": 0.0, "metadata": None}

    start_time = time.time()

    extract_start = time.time()
    extracted = await asyncio.to_thread(claim_extractor.extract_claims, request.text)
    extract_ms = int((time.time() - extract_start) * 1000)

    process_start = time.time()
    results = list(await asyncio.gather(*[
        _process_single_claim(cd, request.text) for cd in extracted
    ]))
    process_ms = int((time.time() - process_start) * 1000)

    summary = scoring_service.calculate_final_score(results)
    job_id = _persist_results(db, request.text, results, summary["overall_risk"])

    return {
        "job_id": job_id,
        "text": request.text,
        "claims": results,
        "overall_risk": summary["overall_risk"],
        "metadata": {
            "total_time_ms": int((time.time() - start_time) * 1000),
            "extraction_time_ms": extract_ms,
            "processing_time_ms": process_ms,
            "claim_count": len(results),
        },
    }


@router.post("/verify/stream")
async def verify_text_stream(request: VerifyRequest, db: Session = Depends(get_db)):
    """SSE endpoint — emits one JSON event per claim as it completes."""

    async def event_stream():
        if not request.text or not request.text.strip():
            yield f"data: {json.dumps({'type': 'error', 'message': 'Empty input'})}\n\n"
            return

        try:
            start_time = time.time()

            extracted = await asyncio.to_thread(claim_extractor.extract_claims, request.text)
            yield f"data: {json.dumps({'type': 'start', 'claim_count': len(extracted)})}\n\n"

            results = []
            for i, claim_data in enumerate(extracted):
                claim_result = await _process_single_claim(claim_data, request.text)
                results.append(claim_result)
                yield f"data: {json.dumps({'type': 'claim', 'index': i, 'data': claim_result})}\n\n"

            summary = scoring_service.calculate_final_score(results)
            job_id = _persist_results(db, request.text, results, summary["overall_risk"])

            yield f"data: {json.dumps({'type': 'complete', 'job_id': job_id, 'overall_risk': summary['overall_risk'], 'total_time_ms': int((time.time() - start_time) * 1000)})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
