import ollama
import json
import time
from typing import List, Optional
from app.config import settings

class OllamaService:
    def __init__(self, model: str = settings.OLLAMA_MODEL):
        self.model = model

    def generate_explanation(self, claim: str, evidence: str, status: str) -> str:
        """
        Generate a natural language explanation for why a claim is supported or contradicted.
        """
        evidence_text = evidence.strip() if evidence else "No specific evidence was retrieved."
        prompt = f"""Write exactly one concise sentence explaining why the claim below has been marked "{status}".

Claim: {claim}
Evidence: {evidence_text}
Verdict: {status}

Rules:
- Start your sentence directly with the explanation — do NOT repeat "Status:", "Verdict:", or any label.
- If Supported: explain what in the evidence confirms the claim.
- If Contradicted: state the specific factual discrepancy (use your knowledge if evidence is empty).
- If Inconclusive: explain what is missing or ambiguous.
- One sentence only. No preamble."""

        try:
            response = ollama.generate(model=self.model, prompt=prompt)
            return response['response'].strip()
        except Exception:
            return f"The claim was marked {status} based on the available evidence."

    def extract_atomic_claims(self, text: str) -> List[dict]:
        """
        Use LLM to extract granular atomic claims with full coreference resolution.
        Ensures 'It', 'They', etc. are replaced with their actual subjects.
        """
        prompt = f"""You are a fact-extraction system. Extract ONLY the explicit factual claims stated in the text below.

STRICT RULES:
1. ONLY extract claims that are explicitly written in the text. DO NOT infer, imply, or add facts not stated.
2. COREFERENCE: Replace pronouns (it, they, he, she) with the actual named subject they refer to.
3. ATOMICITY: Each claim must assert exactly one fact.
4. DO NOT add background knowledge. If the text says "X invented Y", extract that — do not also add "X is a person".
5. Trivially obvious statements (e.g. "X is a noun/person/thing") are NOT claims — skip them.

Text: {text}

Return ONLY a valid JSON list of objects. Each object must have:
- "claim": the self-contained factual statement exactly as expressed in the text (with pronouns resolved)
- "reasoning": one sentence explaining what you resolved or kept

Example Input: "The Moon is Earth's satellite. It is small."
Example Output: [{{"claim": "The Moon is Earth's satellite", "reasoning": "Direct claim"}}, {{"claim": "The Moon is small", "reasoning": "Resolved 'It' to 'The Moon'"}}]

No text outside the JSON."""
        
        try:
            response = ollama.generate(model=self.model, prompt=prompt, format="json")
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
        Generate specific, entity-aware search queries to fact-check a claim.
        Vague queries ("is this true?") are explicitly banned.
        """
        prompt = f"""You are a professional fact-checker. Generate exactly 3 precise web search queries to verify the claim below.

CLAIM: {claim}

STRICT RULES:
- Every query MUST include the specific named entities, numbers, dates, or places from the claim.
- DO NOT generate vague queries like "is this true?" or "verify this claim".
- Query 1 (Verification): Search for the exact fact stated. Use the primary entity + the specific attribute being claimed.
- Query 2 (Counter-evidence): Search for corrections, rebuttals, or alternative data about the same fact.
- Query 3 (Authoritative source): Target an authoritative domain (Wikipedia, official government site, academic source) for the primary entity.

Example for claim "The Eiffel Tower was built in 1920":
["Eiffel Tower construction completion year", "Eiffel Tower built 1889 history", "Eiffel Tower Wikipedia construction date"]

Return ONLY a valid JSON list of exactly 3 query strings. No explanation."""

        try:
            response = ollama.generate(model=self.model, prompt=prompt, format="json")
            queries = json.loads(response['response'])
            if isinstance(queries, dict):
                queries = queries.get("queries", list(queries.values()))
            if isinstance(queries, list):
                queries = [q for q in queries if isinstance(q, str) and len(q) > 5]
            if len(queries) >= 1:
                return queries[:3]
            raise ValueError("No valid queries returned")
        except Exception:
            # Specific fallback: use claim keywords rather than generic phrases
            words = [w for w in claim.split() if len(w) > 3]
            subject = " ".join(words[:5])
            return [claim, f"{subject} fact", f"{subject} wikipedia"]

    def judge_consensus(self, claim: str, evidence_list: List[dict]) -> dict:
        """
        Clinical judge: synthesizes only relevant evidence to reach a verdict.
        Explicitly instructed to return Inconclusive when evidence is off-topic.
        """
        if not evidence_list:
            return {
                "status": "Inconclusive",
                "reasoning": "No relevant evidence was found to evaluate this claim.",
                "confidence": 0.0,
                "risk_score": 0.5,
            }

        # Count NLI votes to give the judge a pre-computed consensus signal
        nli_votes: dict = {}
        for e in evidence_list:
            v = e.get("verdict", "Insufficient Evidence")
            nli_votes[v] = nli_votes.get(v, 0) + 1
        nli_summary = ", ".join(f"{k}: {v}" for k, v in nli_votes.items())

        evidence_lines = []
        for e in evidence_list[:8]:
            nli = e.get("verdict", "?")
            conf = e.get("confidence")
            conf_str = f" conf={conf:.2f}" if conf is not None else ""
            rel = f" rel={e['relevance_score']:.2f}" if "relevance_score" in e else ""
            evidence_lines.append(
                f"- [{e['source']}] NLI={nli}{conf_str}{rel}: {e['text'][:300]}"
            )
        evidence_summary = "\n".join(evidence_lines)

        prompt = f"""You are a rigorous clinical fact-checker auditing a specific factual claim.

CLAIM: "{claim}"

NLI MODEL PRE-VOTE (cross-encoder verdicts across all sources): {nli_summary}

EVIDENCE WITH NLI VERDICTS:
{evidence_summary}

EVALUATION RULES:
1. The NLI pre-vote is a strong signal — if 3+ sources are marked "Contradicted" with confidence >0.8, default toward "Contradicted" unless you find a clear reason not to.
2. "By omission" contradiction: if authoritative sources describe what the subject IS known for, and the claimed attribute is completely absent, that IS a contradiction — not merely inconclusive.
3. Weigh source authority: Wikipedia/official > established news > blogs.
4. Do NOT use your own training knowledge to fill gaps in evidence. Reason only from what is shown.
5. If the evidence strongly suggests the claim is false (even indirectly), choose "Contradicted".

VERDICT OPTIONS:
- "Supported": Evidence directly confirms the claim. NLI majority says Supported.
- "Contradicted": Evidence refutes the claim directly OR authoritative sources describe the subject in a way that is incompatible with the claim (by omission). NLI majority says Contradicted.
- "Inconclusive": Evidence is genuinely off-topic, absent, or contradictory without resolution.

Return ONLY valid JSON — no text outside it:
{{
    "status": "Supported" | "Contradicted" | "Inconclusive",
    "reasoning": "Cite specific sources and the NLI vote. Explain whether contradictions are direct or by omission.",
    "confidence": 0.0,
    "risk_score": 0.0
}}"""

        try:
            response = ollama.generate(model=self.model, prompt=prompt, format="json")
            result = json.loads(response['response'])
            # Normalise status to known values
            valid_statuses = {"Supported", "Contradicted", "Inconclusive"}
            if result.get("status") not in valid_statuses:
                result["status"] = "Inconclusive"
            return result
        except Exception as e:
            print(f"Judge Agent Error: {e}")
            return {
                "status": "Inconclusive",
                "reasoning": "The judge agent failed to reach a decision.",
                "confidence": 0.0,
                "risk_score": 0.5,
            }

# Singleton instance
ollama_service = OllamaService()
