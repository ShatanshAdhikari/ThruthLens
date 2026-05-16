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

    def extract_atomic_claims(self, text: str) -> List[str]:
        """
        Use LLM to extract granular atomic claims.
        """
        prompt = f"""
        Extract all factual, atomic claims from the following text. 
        Each claim should be a standalone sentence.
        Text: {text}
        
        Output only the claims, one per line. No numbering.
        """
        
        try:
            response = ollama.generate(model=self.model, prompt=prompt)
            claims = [c.strip() for c in response['response'].split('\n') if c.strip()]
            return claims
        except Exception:
            return []

# Singleton instance
ollama_service = OllamaService()
