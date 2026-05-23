from app.models.verifier_model import verifier_model
from app.services.ollama_service import ollama_service
from typing import Dict, Any, List
import numpy as np

class VerificationService:
    def __init__(self):
        # NLI labels for cross-encoder/nli-deberta-v3-small:
        # 0: contradiction, 1: entailment, 2: neutral
        self.labels = ["Contradicted", "Supported", "Insufficient Evidence"]

    def _softmax(self, x):
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum()

    def verify_against_sources(self, claim: str, sources: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Verify a claim against multiple sources and calculate consensus using a Judge Agent.
        """
        if not sources:
            return {
                "status": "Insufficient Evidence",
                "risk_score": 0.0,
                "confidence": 0.0,
                "consensus_stats": {"Supported": 0, "Contradicted": 0, "Insufficient Evidence": 0},
                "evidence_details": [],
                "reasoning": "No evidence found on the web."
            }
            
        evidence_details = []
        stats = {"Supported": 0, "Contradicted": 0, "Insufficient Evidence": 0}
        
        # 1. Individual NLI checks (Clinical Audit Trail)
        for source in sources:
            v_res = self.verify_claim(claim, source["text"])
            source_name = source.get("source") or source.get("metadata", {}).get("source", "Unknown")
            
            detail = {
                "text": source["text"],
                "source": source_name,
                "url": source.get("url") or source.get("metadata", {}).get("url"),
                "type": source.get("type") or source.get("metadata", {}).get("type", "web_search"),
                "verdict": v_res["status"],
                "confidence": v_res["confidence"]
            }
            evidence_details.append(detail)
            stats[v_res["status"]] += 1
            
        # 2. Judge Agent Synthesis (Deep Reasoning)
        judge_res = ollama_service.judge_consensus(claim, evidence_details)
        
        # 3. Final Synthesis: Combine NLI stats with Judge Reasoning
        # If Judge and NLI strongly disagree, we lean towards the Judge but flag uncertainty
        return {
            "status": judge_res.get("status", "Inconclusive"),
            "risk_score": float(judge_res.get("risk_score", 0.5)),
            "confidence": float(judge_res.get("confidence", 0.0)),
            "consensus_stats": stats,
            "evidence_details": evidence_details,
            "reasoning": judge_res.get("reasoning", "The judge agent provided no reasoning.")
        }

    def verify_claim(self, claim: str, evidence: str, confidence_threshold: float = 0.5) -> Dict[str, Any]:
        """
        Determine the relationship between a claim and evidence with a confidence threshold.
        """
        if not evidence or not claim:
            return {
                "status": "Insufficient Evidence",
                "risk_score": 0.0,
                "confidence": 0.0,
                "reason": "Missing evidence or claim text"
            }
            
        # Standard NLI: (Premise, Hypothesis) -> (Evidence, Claim)
        logits = verifier_model.verify(evidence, claim)
        probs = self._softmax(logits)
        
        # Find the index of the highest probability
        label_idx = np.argmax(probs)
        confidence = float(probs[label_idx])
        
        # Apply confidence threshold
        if confidence < confidence_threshold:
            status = "Insufficient Evidence"
        else:
            status = self.labels[label_idx]
        
        # Risk score is the probability of contradiction (index 0)
        risk_score = float(probs[0])
        
        return {
            "status": status,
            "risk_score": risk_score,
            "confidence": confidence,
            "label_probs": {
                "contradiction": float(probs[0]),
                "entailment": float(probs[1]),
                "neutral": float(probs[2])
            }
        }

# Singleton instance
verification_service = VerificationService()
