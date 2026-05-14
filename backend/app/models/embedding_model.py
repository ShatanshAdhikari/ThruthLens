from sentence_transformers import SentenceTransformer
import torch

class EmbeddingModel:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = SentenceTransformer(model_name, device=self.device)

    def encode(self, sentences: list):
        return self.model.encode(sentences, convert_to_tensor=True)

# Singleton instance
embedding_model = EmbeddingModel()
