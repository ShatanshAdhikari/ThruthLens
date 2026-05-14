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

    def extract_claims(self, text: str) -> List[str]:
        """
        Extract factual claims from the given text.
        For now, it performs basic sentence segmentation.
        """
        if not text:
            return []
            
        doc = self.nlp(text)
        claims = [sent.text.strip() for sent in doc.sents if len(sent.text.strip()) > 5]
        
        # Further refinement: split on 'and' if it connects two independent clauses
        # (Simplified for now: just return sentences)
        return claims

# Singleton instance
claim_extractor = ClaimExtractor()
