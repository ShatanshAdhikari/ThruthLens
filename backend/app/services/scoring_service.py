from typing import List, Dict, Any
import numpy as np

# Higher weight = verdicts from these sources shift risk more decisively
_SOURCE_AUTHORITY: Dict[str, float] = {
    "fact_check": 1.4,    # Google Fact Check (Snopes, PolitiFact, etc.)
    "encyclopedia": 1.2,  # Wikipedia
    "web_search": 1.0,    # Tavily / DuckDuckGo
    "local_db": 0.7,      # ChromaDB seed data
}


class ScoringService:
    def _authority_multiplier(self, evidence_details: List[Dict[str, Any]]) -> float:
        if not evidence_details:
            return 1.0
        weights = [_SOURCE_AUTHORITY.get(ev.get("type", "web_search"), 1.0) for ev in evidence_details]
        return sum(weights) / len(weights)

    def calculate_final_score(self, verification_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not verification_results:
            return {"overall_risk": 0.0, "status": "No data"}

        weighted_risks = []
        for res in verification_results:
            confidence = res.get("confidence", 0.5)
            authority = self._authority_multiplier(res.get("evidence_details", []))

            if res["status"] == "Contradicted":
                base_risk = 0.7
                adjusted_risk = base_risk + (0.3 * confidence)
            elif res["status"] == "Supported":
                base_risk = 0.3
                adjusted_risk = base_risk * (1.0 - confidence)
            else:
                adjusted_risk = 0.5 + (0.2 * (1.0 - confidence))

            # Authority > 1 amplifies the signal; < 1 dampens low-credibility verdicts
            adjusted_risk = adjusted_risk * authority
            weighted_risks.append(np.clip(adjusted_risk, 0, 1))

        avg_risk = sum(weighted_risks) / len(weighted_risks)

        return {
            "overall_risk": float(avg_risk),
            "claim_count": len(verification_results),
            "status": "Verified",
        }


scoring_service = ScoringService()
