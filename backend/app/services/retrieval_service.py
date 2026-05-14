import chromadb
from chromadb.utils import embedding_functions
from app.models.embedding_model import embedding_model
import os

class RetrievalService:
    def __init__(self, persist_directory: str = "db/chroma"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Use a custom embedding function that uses our EmbeddingModel
        # But for simplicity with ChromaDB, we can use their default or a compatible one
        # Here we'll wrap our model
        class MyEmbeddingFunction(embedding_functions.EmbeddingFunction):
            def __call__(self, input: list):
                return embedding_model.encode(input).tolist()

        self.collection = self.client.get_or_create_collection(
            name="evidence_base",
            embedding_function=MyEmbeddingFunction()
        )
        
        # Seed with some example evidence if empty
        if self.collection.count() == 0:
            self._seed_data()

    def _seed_data(self):
        evidence_items = [
            {"id": "1", "text": "The Eiffel Tower was completed in 1889 and is located in Paris, France.", "source": "Wikipedia"},
            {"id": "2", "text": "Paris is the capital and most populous city of France.", "source": "Wikipedia"},
            {"id": "3", "text": "The Moon is Earth's only natural satellite. It is about one-quarter of Earth's diameter.", "source": "NASA"},
            {"id": "4", "text": "Python was created by Guido van Rossum and first released in 1991.", "source": "Python Foundation"},
            {"id": "5", "text": "The Great Wall of China is a series of fortifications that were built across the historical northern borders of ancient Chinese states.", "source": "History Channel"}
        ]
        
        self.collection.add(
            documents=[item["text"] for item in evidence_items],
            metadatas=[{"source": item["source"]} for item in evidence_items],
            ids=[item["id"] for item in evidence_items]
        )

    def retrieve_evidence(self, query: str, n_results: int = 3):
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results

# Singleton instance
retrieval_service = RetrievalService()
