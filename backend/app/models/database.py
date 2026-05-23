from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base
import datetime

class VerificationJob(Base):
    __tablename__ = "verification_jobs"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    overall_risk = Column(Float, default=0.0)
    status = Column(String, default="Pending")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    claims = relationship("ExtractedClaim", back_populates="job")

class ExtractedClaim(Base):
    __tablename__ = "extracted_claims"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("verification_jobs.id"))
    claim_text = Column(Text, nullable=False)
    status = Column(String) # Supported, Contradicted, Inconclusive
    risk_score = Column(Float)
    confidence = Column(Float)
    consensus_stats = Column(JSON) # e.g., {"supported": 3, "contradicted": 1, "neutral": 2}
    reasoning = Column(Text) # Clinical reasoning from Judge Agent
    start_char = Column(Integer)
    end_char = Column(Integer)
    
    job = relationship("VerificationJob", back_populates="claims")
    evidence = relationship("EvidenceSource", back_populates="claim")

class EvidenceSource(Base):
    __tablename__ = "evidence_sources"

    id = Column(Integer, primary_key=True, index=True)
    claim_id = Column(Integer, ForeignKey("extracted_claims.id"))
    text = Column(Text, nullable=False)
    source_name = Column(String)
    url = Column(String)
    source_type = Column(String) # news, fact_check, web_search, local
    individual_verdict = Column(String) # individual NLI result against this source
    verdict_confidence = Column(Float)
    
    claim = relationship("ExtractedClaim", back_populates="evidence")
