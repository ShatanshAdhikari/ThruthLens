import chromadb
from chromadb.utils import embedding_functions
from app.models.embedding_model import embedding_model
from app.services.search_service import search_service
from app.config import settings
from typing import Optional, List, Dict, Any
import numpy as np
import os

MIN_EVIDENCE_TEXT_LENGTH = 40
RELEVANCE_THRESHOLD = 0.12


def _cosine_similarity(a, b) -> float:
    a = np.array(a).flatten().astype(float)
    b = np.array(b).flatten().astype(float)
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)


class RetrievalService:
    def __init__(self, persist_directory: str = settings.CHROMA_PERSIST_DIR):
        self.client = chromadb.PersistentClient(path=persist_directory)

        class MyEmbeddingFunction(embedding_functions.EmbeddingFunction):
            def __call__(self, input: list):
                return embedding_model.encode(input).tolist()

        self.collection = self.client.get_or_create_collection(
            name="evidence_base",
            embedding_function=MyEmbeddingFunction()
        )

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

    def filter_by_relevance(
        self,
        claim: str,
        candidates: List[Dict[str, Any]],
        threshold: float = RELEVANCE_THRESHOLD,
    ) -> List[Dict[str, Any]]:
        """
        Remove candidates that are too short or semantically unrelated to the claim.
        Adds a 'relevance_score' key to each passing candidate and returns them
        sorted highest-relevance first.
        """
        if not candidates:
            return []

        # Pre-filter: drop snippets too short to carry factual content
        length_filtered = [
            c for c in candidates
            if len(c.get("text", "").strip()) >= MIN_EVIDENCE_TEXT_LENGTH
        ]

        if not length_filtered:
            return []

        # Embed the claim once
        claim_emb = np.array(embedding_model.encode([claim])[0]).flatten()

        scored = []
        for candidate in length_filtered:
            text_emb = np.array(embedding_model.encode([candidate["text"]])[0]).flatten()
            sim = _cosine_similarity(claim_emb, text_emb)
            if sim >= threshold:
                candidate["relevance_score"] = round(sim, 3)
                scored.append((sim, candidate))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [item for _, item in scored]

    def retrieve_evidence(self, query: str, n_results: int = 5, threshold: float = 1.2):
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
                        "source": results["metadatas"][0][i].get("source", "Local DB"),
                        "url": results["metadatas"][0][i].get("url", ""),
                        "type": "local_db",
                        "metadata": results["metadatas"][0][i],
                        "distance": float(distance),
                        "score": 1.0 - (distance / 2.0),
                    })

        formatted_results.sort(key=lambda x: x["distance"])
        return formatted_results

    def retrieve_hybrid(
        self,
        query: str,
        context: Optional[str] = None,
        n_results: int = 5,
        threshold: float = 1.2,
    ) -> List[Dict[str, Any]]:
        """
        Fetch evidence from web + local DB, then filter to only topically relevant
        snippets using semantic similarity.  Returns at most n_results candidates.
        """
        # 1. Web search (primary)
        web_results = []
        if settings.USE_WEB_SEARCH:
            web_results = search_service.search_all(
                query, context=context,
                max_results=settings.MAX_SEARCH_RESULTS_PER_SOURCE
            )

        formatted_web = []
        for i, res in enumerate(web_results):
            formatted_web.append({
                "id": f"web_{i}",
                "text": res["text"],
                "source": res["source"],
                "url": res.get("url", ""),
                "type": res.get("type", "web_search"),
                "metadata": {
                    "source": res["source"],
                    "url": res.get("url", ""),
                    "type": res.get("type", "web_search"),
                },
            })

        # 2. Local DB (supplementary)
        local_results = self.retrieve_evidence(query, n_results=3, threshold=threshold)

        # 3. Merge and apply relevance filter — only keep evidence that actually
        #    discusses the claim topic; discard random/short snippets.
        combined = formatted_web + local_results
        relevant = self.filter_by_relevance(query, combined, threshold=RELEVANCE_THRESHOLD)

        return relevant[:n_results]


# Singleton instance
retrieval_service = RetrievalService()
