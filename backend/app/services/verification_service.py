from app.models.verifier_model import verifier_model
from typing import Dict, Any
import numpy as np

class VerificationService:
    def __init__(self):
        # NLI labels for cross-encoder/nli-deberta-v3-small:
        # 0: contradiction, 1: entailment, 2: neutral
        self.labels = ["Contradicted", "Supported", "Insufficient Evidence"]

    def _softmax(self, x):
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum()

    def verify_claim(self, claim: str, evidence: str) -> Dict[str, Any]:
        """
        Determine the relationship between a claim and evidence.
        """
        if not evidence:
            return {
                "status": "Insufficient Evidence",
                "risk_score": 0.5,
                "confidence": 0.0
            }
            
        logits = verifier_model.verify(claim, evidence)
        probs = self._softmax(logits)
        
        # Find the index of the highest probability
        label_idx = np.argmax(probs)
        status = self.labels[label_idx]
        
        # Risk score is the probability of contradiction (index 0)
        risk_score = float(probs[0])
        
        return {
            "status": status,
            "risk_score": risk_score,
            "confidence": float(probs[label_idx]),
            "label_probs": probs.tolist()
        }

# Singleton instance
verification_service = VerificationService()
