from app.services.ollama_service import ollama_service
from typing import List

class ClaimExtractor:
    def __init__(self):
        # We still keep spaCy for character offset mapping if needed, 
        # but the primary deconstruction is now LLM-based.
        try:
            import spacy
            self.nlp = spacy.load("en_core_web_sm")
        except:
            self.nlp = None

    def extract_claims(self, text: str) -> List[dict]:
        """
        Extract factual claims using deep LLM deconstruction.
        Resolves coreferences and maps claims back to original text offsets.
        """
        if not text:
            return []
            
        # 1. Split original text into sentences for offset mapping
        sentences = []
        if self.nlp:
            doc = self.nlp(text)
            sentences = [{"text": s.text, "start": s.start_char, "end": s.end_char} for s in doc.sents]
        else:
            # Fallback split
            sentences = [{"text": s.strip(), "start": 0, "end": len(text)} for s in text.split('.') if s.strip()]

        # 2. LLM-based Deconstruction
        llm_claims = ollama_service.extract_atomic_claims(text)
        
        # 3. Map back to original text offsets
        processed_claims = []
        for item in llm_claims:
            # Handle both {"claim": "...", "reasoning": "..."} and plain strings
            if isinstance(item, str):
                claim_text = item.strip()
            elif isinstance(item, dict):
                claim_text = item.get("claim", "").strip()
            else:
                continue
            if not claim_text:
                continue
                
            # Find the sentence with the highest overlap or similarity
            # Simple heuristic: find the sentence that contains the most keywords from the claim
            best_sent = sentences[0] if sentences else {"start": 0, "end": len(text)}
            max_overlap = -1
            
            claim_words = set(claim_text.lower().split())
            for sent in sentences:
                sent_words = set(sent["text"].lower().split())
                overlap = len(claim_words.intersection(sent_words))
                if overlap > max_overlap:
                    max_overlap = overlap
                    best_sent = sent
            
            processed_claims.append({
                "text": claim_text,
                "reasoning": item.get("reasoning", ""),
                "start": best_sent["start"],
                "end": best_sent["end"]
            })
            
        return processed_claims

# Singleton instance
claim_extractor = ClaimExtractor()
