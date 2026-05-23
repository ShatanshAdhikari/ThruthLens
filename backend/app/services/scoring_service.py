from typing import List, Dict, Any
import numpy as np

class ScoringService:
    def calculate_final_score(self, verification_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Aggregate scores with weighted adjustments based on consensus and confidence.
        """
        if not verification_results:
            return {"overall_risk": 0.0, "status": "No data"}
            
        weighted_risks = []
        for res in verification_results:
            confidence = res.get("confidence", 0.5)
            
            if res["status"] == "Contradicted":
                # High risk: at least 0.7, scaled by confidence
                base_risk = 0.7
                adjusted_risk = base_risk + (0.3 * confidence)
            elif res["status"] == "Supported":
                # Low risk: at most 0.3, inverted by confidence
                base_risk = 0.3
                adjusted_risk = base_risk * (1.0 - confidence)
            else:
                # Inconclusive/Insufficient Evidence
                # Moderate risk with uncertainty
                adjusted_risk = 0.5 + (0.2 * (1.0 - confidence))
                
            weighted_risks.append(np.clip(adjusted_risk, 0, 1))
            
        avg_risk = sum(weighted_risks) / len(weighted_risks)
        
        return {
            "overall_risk": float(avg_risk),
            "claim_count": len(verification_results),
            "status": "Verified"
        }

# Singleton instance
scoring_service = ScoringService()
