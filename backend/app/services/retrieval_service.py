import chromadb
from chromadb.utils import embedding_functions
from app.models.embedding_model import embedding_model
from app.services.search_service import search_service
from app.config import settings
import os

class RetrievalService:
    def __init__(self, persist_directory: str = settings.CHROMA_PERSIST_DIR):
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
            {"id": "5", "text": "The Great Wall of China is a series of fortifications that were built across the historical northern borders of ancient Chinese states.", "source": "History Channel"},
            {"id": "6", "text": "Vatican City is the smallest country in the world, both by area and population.", "source": "World Atlas"},
            {"id": "7", "text": "Mount Everest is Earth's highest mountain above sea level, located in the Himalayas.", "source": "National Geographic"},
            {"id": "8", "text": "The Pacific Ocean is the largest and deepest of Earth's oceanic divisions.", "source": "NOAA"},
            {"id": "9", "text": "William Shakespeare was an English playwright, poet and actor, widely regarded as the greatest writer in the English language.", "source": "Britannica"},
            {"id": "10", "text": "Photosynthesis is a process used by plants and other organisms to convert light energy into chemical energy.", "source": "Biology Online"}
        ]
        
        self.collection.add(
            documents=[item["text"] for item in evidence_items],
            metadatas=[{"source": item["source"]} for item in evidence_items],
            ids=[item["id"] for item in evidence_items]
        )

    def retrieve_evidence(self, query: str, n_results: int = 5, threshold: float = 1.5):
        """
        Retrieve evidence with a similarity threshold.
        Distance scores: 0 (identical) to 2 (completely different).
        A threshold of 1.5 is fairly inclusive for vector search.
        """
        # Targeted query optimization: clean and truncate if too long
        query = query.strip()[:500] 
        
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        formatted_results = []
        
        if results["distances"] and results["distances"][0]:
            for i, distance in enumerate(results["distances"][0]):
                if distance <= threshold:
                    formatted_results.append({
                        "id": results["ids"][0][i],
                        "text": results["documents"][0][i],
                        "metadata": results["metadatas"][0][i],
                        "distance": float(distance),
                        "score": 1.0 - (distance / 2.0)  # Normalize to 0-1 similarity score
                    })
                    
        # Sort by distance (ascending)
        formatted_results.sort(key=lambda x: x["distance"])
        return formatted_results

    def retrieve_hybrid(self, query: str, context: Optional[str] = None, n_results: int = 3, threshold: float = 1.2):
        """
        Focus on real-time web search for clinical consensus, bypassing local DB
        as the primary source of truth.
        """
        # 1. Web Search (Primary source now)
        web_results = []
        if settings.USE_WEB_SEARCH:
            web_results = search_service.search_all(query, context=context, max_results=settings.MAX_SEARCH_RESULTS_PER_SOURCE)
            
        # Format web results
        formatted_web = []
        for i, res in enumerate(web_results):
            formatted_web.append({
                "id": f"web_{i}",
                "text": res["text"],
                "metadata": {
                    "source": res["source"],
                    "url": res.get("url", ""),
                    "type": res.get("type", "web_search")
                },
                "distance": 0.5,
                "score": 0.75
            })
            
        # 2. Local Search (Optional/Fallback/Supplementary)
        # We can still check local DB for previously verified facts or context
        local_results = self.retrieve_evidence(query, n_results=2, threshold=threshold)
        
        # Combine
        combined = formatted_web + local_results
        return combined[:n_results + 2]

# Singleton instance
retrieval_service = RetrievalService()
