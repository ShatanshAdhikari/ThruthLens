import sys
sys.path.insert(0, r"C:\Users\shata\OneDrive\Desktop\TruthLens\backend")

from app.services.search_service import search_service
from app.services.retrieval_service import retrieval_service, _cosine_similarity
from app.models.embedding_model import embedding_model
from app.services.ollama_service import ollama_service
import numpy as np

claim = "The number 0 was invented by Ramanujan"

print("=== GENERATED QUERIES ===")
queries = ollama_service.generate_search_queries(claim)
for q in queries:
    print(" -", q)

print()
print("=== RAW SEARCH RESULTS ===")
results = search_service.search_all(claim, max_results=5)
print(f"Total results returned: {len(results)}")

claim_emb = np.array(embedding_model.encode([claim])[0]).flatten()

for i, r in enumerate(results[:8]):
    text = r.get("text", "")
    source = r.get("source", "?")
    if len(text) > 5:
        text_emb = np.array(embedding_model.encode([text])[0]).flatten()
        sim = _cosine_similarity(claim_emb, text_emb)
        print(f"[{i+1}] sim={sim:.3f}  len={len(text)}  source={source}")
        print(f"     {text[:150]}")
    else:
        print(f"[{i+1}] EMPTY/SHORT ({len(text)} chars) from {source}")
