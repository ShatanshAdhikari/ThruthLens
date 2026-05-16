import spacy
from typing import List

class ClaimExtractor:
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            # Fallback if model not found (though we just installed it)
            self.nlp = spacy.blank("en")
            self.nlp.add_pipe("sentencizer")

    def extract_claims(self, text: str) -> List[dict]:
        """
        Extract factual claims with their character offsets.
        Improved version that splits complex sentences into atomic claims.
        """
        if not text:
            return []
            
        doc = self.nlp(text)
        claims = []
        
        for sent in doc.sents:
            # We look for coordinating conjunctions (CCONJ) that connect two independent clauses (ROOTs)
            # For simplicity, we split sentences longer than 15 words if they contain 'and' or 'but'
            clean_text = sent.text.strip()
            if len(clean_text) <= 5:
                continue

            # Check if sentence is complex and needs splitting
            split_points = []
            if len(sent) > 15:
                for token in sent:
                    if token.pos_ == "CCONJ" and token.text.lower() in ["and", "but"]:
                        # Heuristic: split if the conjunction is not at the start/end
                        if 0 < token.i - sent.start < len(sent) - 1:
                            split_points.append(token)

            if not split_points:
                claims.append({
                    "text": clean_text,
                    "start": sent.start_char,
                    "end": sent.end_char
                })
            else:
                # Split at the first split point for now
                sp = split_points[0]
                
                # First part
                part1_text = text[sent.start_char : sp.idx].strip()
                if len(part1_text) > 5:
                    claims.append({
                        "text": part1_text,
                        "start": sent.start_char,
                        "end": sp.idx
                    })
                
                # Second part (skipping the conjunction itself)
                next_token_idx = sp.idx + len(sp.text) + 1
                part2_text = text[next_token_idx : sent.end_char].strip()
                if len(part2_text) > 5:
                    claims.append({
                        "text": part2_text,
                        "start": next_token_idx,
                        "end": sent.end_char
                    })
        
        return claims

# Singleton instance
claim_extractor = ClaimExtractor()
