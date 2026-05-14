from sentence_transformers import CrossEncoder
import torch

class VerifierModel:
    def __init__(self, model_name: str = "cross-encoder/nli-deberta-v3-small"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = CrossEncoder(model_name, device=self.device)

    def verify(self, claim: str, evidence: str):
        """
        Verify the claim against the evidence.
        Returns probabilities for [entailment, neutral, contradiction].
        """
        scores = self.model.predict([(claim, evidence)])
        return scores[0]

# Singleton instance
verifier_model = VerifierModel()
