import sys
sys.path.insert(0, r"C:\Users\shata\OneDrive\Desktop\TruthLens\backend")

from app.services.retrieval_service import retrieval_service, RELEVANCE_THRESHOLD, MIN_EVIDENCE_TEXT_LENGTH
from app.models.embedding_model import embedding_model
import numpy as np

claim = "The number 0 was invented by Ramanujan"

print(f"Config: MIN_LEN={MIN_EVIDENCE_TEXT_LENGTH}, THRESHOLD={RELEVANCE_THRESHOLD}")

# Call exactly what the API calls
print("\nCalling retrieve_hybrid...")
results = retrieval_service.retrieve_hybrid(claim, context=None, n_results=5)
print(f"retrieve_hybrid returned {len(results)} relevant candidates")
for r in results:
    print(f"  source={r.get('source')} relevance={r.get('relevance_score')} text={r.get('text','')[:80]}")

# Now check manually with very low threshold
print("\n--- Manual check with threshold=0.05 ---")
from app.services.search_service import search_service
from app.services.retrieval_service import _cosine_similarity

raw = search_service.search_all(claim, max_results=5)
print(f"Raw search results: {len(raw)}")
claim_emb = np.array(embedding_model.encode([claim])[0]).flatten().astype(float)
for r in raw:
    text = r.get("text", "")
    if not text:
        print(f"  EMPTY from {r.get('source')}")
        continue
    text_emb = np.array(embedding_model.encode([text])[0]).flatten().astype(float)
    sim = _cosine_similarity(claim_emb, text_emb)
    passes_len = len(text.strip()) >= MIN_EVIDENCE_TEXT_LENGTH
    print(f"  sim={sim:.3f} len={len(text)} passes_len={passes_len} source={r.get('source')}")
    print(f"    text: {text[:100]}")
