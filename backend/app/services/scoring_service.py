from typing import List, Dict, Any

class ScoringService:
    def calculate_final_score(self, verification_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Aggregate scores from multiple evidence sources or claims.
        """
        if not verification_results:
            return {"overall_risk": 0.0, "status": "No data"}
            
        total_risk = sum(res["risk_score"] for res in verification_results)
        avg_risk = total_risk / len(verification_results)
        
        return {
            "overall_risk": avg_risk,
            "claim_count": len(verification_results),
            "status": "Verified"
        }

# Singleton instance
scoring_service = ScoringService()
