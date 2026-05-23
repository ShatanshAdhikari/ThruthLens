from sentence_transformers import SentenceTransformer
import torch
import numpy as np
from functools import lru_cache

class EmbeddingModel:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = SentenceTransformer(model_name, device=self.device)
        self._cache = {}

    def encode(self, sentences: list):
        # Handle list of sentences
        results = []
        to_encode = []
        indices_to_encode = []
        
        for i, s in enumerate(sentences):
            if s in self._cache:
                results.append(self._cache[s])
            else:
                results.append(None)
                to_encode.append(s)
                indices_to_encode.append(i)
        
        if to_encode:
            encoded = self.model.encode(to_encode, convert_to_tensor=True)
            for i, idx in enumerate(indices_to_encode):
                emb = encoded[i]
                self._cache[to_encode[i]] = emb
                results[idx] = emb
        
        return torch.stack(results) if isinstance(results[0], torch.Tensor) else np.array(results)

# Singleton instance
embedding_model = EmbeddingModel()
