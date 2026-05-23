import ollama
import time
from typing import List, Optional

class OllamaService:
    def __init__(self, model: str = "llama3"):
        self.model = model

    def generate_explanation(self, claim: str, evidence: str, status: str) -> str:
        """
        Generate a natural language explanation for why a claim is supported or contradicted.
        """
        prompt = f"""
        Analyze the relationship between the following Claim and Evidence.
        Claim: {claim}
        Evidence: {evidence}
        Status: {status}
        
        Provide a concise, professional one-sentence explanation for this status.
        If Supported, explain how the evidence confirms it.
        If Contradicted, explain the specific factual discrepancy.
        If Insufficient Evidence, explain what is missing.
        """
        
        try:
            response = ollama.generate(model=self.model, prompt=prompt)
            return response['response'].strip()
        except Exception as e:
            return f"Reasoning: Evidence is {status.lower()} relative to the claim."

    def extract_atomic_claims(self, text: str) -> List[dict]:
        """
        Use LLM to extract granular atomic claims with full coreference resolution.
        Ensures 'It', 'They', etc. are replaced with their actual subjects.
        """
        prompt = f"""
        Deconstruct the following text into atomic factual claims.
        
        CRITICAL REQUIREMENTS:
        1. COREFERENCE RESOLUTION: Replace all pronouns (it, they, he, she, this, these) with the actual subject they refer to.
        2. ATOMICITY: Each claim must be a single, standalone factual statement.
        3. CONTEXT: If a claim depends on a previous sentence for meaning, re-incorporate that context.
        
        Text: {text}
        
        Output format:
        Return ONLY a JSON list of objects, each with:
        - "claim": The self-contained, resolved claim string.
        - "reasoning": Brief explanation of how the context was resolved.
        
        Example Input: "The Moon is Earth's satellite. It is small."
        Example Output: [{{"claim": "The Moon is Earth's satellite", "reasoning": "Direct claim"}}, {{"claim": "The Moon is small", "reasoning": "Resolved 'It' to 'The Moon'"}}]
        """
        
        try:
            response = ollama.generate(model=self.model, prompt=prompt, format="json")
            import json
            claims_data = json.loads(response['response'])
            # Support both list of dicts or nested dict
            if isinstance(claims_data, dict) and "claims" in claims_data:
                claims_data = claims_data["claims"]
            return claims_data
        except Exception as e:
            print(f"LLM Extraction Error: {e}")
            # Fallback to simple split if LLM fails
            return [{"claim": s.strip(), "reasoning": "Fallback split"} for s in text.split('.') if len(s.strip()) > 5]

    def generate_search_queries(self, claim: str, context: Optional[str] = None) -> List[str]:
        """
        Generate multiple targeted search queries to verify a claim from different angles.
        """
        prompt = f"""
        Generate exactly 3 targeted search queries to verify the following factual claim.
        
        Claim: {claim}
        Overall Context: {context if context else "None provided"}
        
        Requirements:
        1. Query 1 (Direct): A query to find supporting evidence.
        2. Query 2 (Contradictory): A query to find potential debunking or conflicting info.
        3. Query 3 (Subject-focused): A query focused on the main subject's properties related to the claim.
        
        Output format:
        Return ONLY a JSON list of 3 strings.
        """
        
        try:
            response = ollama.generate(model=self.model, prompt=prompt, format="json")
            import json
            queries = json.loads(response['response'])
            if isinstance(queries, dict) and "queries" in queries:
                queries = queries["queries"]
            return queries[:3]
        except Exception:
            # Fallback
            return [claim, f"is {claim} true?", f"{claim} debunked"]

    def judge_consensus(self, claim: str, evidence_list: List[dict]) -> dict:
        """
        Act as a clinical auditor to synthesize evidence and provide a final verdict.
        """
        evidence_summary = "\n".join([f"- [{e['source']}]: {e['text']}" for e in evidence_list[:10]])
        
        prompt = f"""
        VERDICT AUDIT TASK:
        Analyze the following factual claim against the provided web evidence.
        
        Claim: {claim}
        
        Evidence Found:
        {evidence_summary}
        
        INSTRUCTIONS:
        1. Weigh the reliability of sources (Official > News > Blogs).
        2. Resolve contradictions. If sources disagree, identify which is more recent or authoritative.
        3. Determine the final status: Supported, Contradicted, or Inconclusive.
        4. Provide a "Clinical Reasoning" explaining your decision.
        
        Output format:
        Return ONLY a JSON object:
        {{
            "status": "Supported" | "Contradicted" | "Inconclusive",
            "reasoning": "Deep logical chain of thought...",
            "confidence": 0.0 to 1.0,
            "risk_score": 0.0 to 1.0
        }}
        """

        
        try:
            response = ollama.generate(model=self.model, prompt=prompt, format="json")
            import json
            return json.loads(response['response'])
        except Exception as e:
            print(f"Judge Agent Error: {e}")
            return {
                "status": "Inconclusive",
                "reasoning": "The judge agent failed to reach a decision.",
                "confidence": 0.0,
                "risk_score": 0.5
            }

# Singleton instance
ollama_service = OllamaService()
