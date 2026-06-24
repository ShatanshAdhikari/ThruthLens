# TruthLens - System Design & Documentation

TruthLens is a high-integrity, clinically rigorous AI Hallucination Detection & Verification Platform. It uses a multi-agent **Consensus-Audit-Reasoning (CAR)** architecture to verify factual claims against live web evidence, with every step persisted to an immutable audit trail.

---

## 1. System Architecture (CAR Pipeline)

Each stage is logged for full reproducibility. The pipeline runs claims in parallel to minimize latency.

### Stage 1: Deep Claim Deconstruction
- **Service:** `ClaimExtractor` + `OllamaService` (Llama3)
- **Action:** Breaks input text into atomic, self-contained factual claims using LLM-based deconstruction.
- **Coreference resolution:** Pronouns ("It", "They") are replaced with their named referents before any claim is extracted.
- **Offset mapping:** Each claim is mapped back to its source sentence in the original text for UI heatmap highlighting.
- **Fallback:** If the LLM returns plain strings instead of structured objects, the extractor handles both formats gracefully.

### Stage 2: Multi-Perspective Search
- **Service:** `SearchService` + `OllamaService`
- **Action:** Generates 3 targeted search queries per claim — one supporting, one counter-evidence, one authoritative source.
- **Sources (priority order):**
  1. **Tavily** — RAG-optimized deep web search (requires API key)
  2. **Google Fact Check Tools** — structured verdicts from Snopes, PolitiFact, AFP, etc. (requires API key)
  3. **Wikipedia REST API** — free, no key required; returns article summaries tagged as `encyclopedia` type
  4. **DuckDuckGo** — final fallback, no key required
- **Caching:** Results are cached in memory per claim for 1 hour. Re-verifying identical text returns instantly.

### Stage 3: Consensus-Audit-Reasoning (CAR) Engine
- **Service:** `VerificationService` + `OllamaService`
- **Relevance filter:** Retrieved sources are scored by cosine similarity to the claim. Only semantically relevant snippets proceed.
- **NLI check:** Each source is scored against the claim by a DeBERTa-v3-small cross-encoder, producing per-source verdicts (Supported / Contradicted / Insufficient Evidence) with probabilities.
- **Judge Agent:** An LLM judge reviews all NLI verdicts, relevance scores, and source text. It weighs source authority (Wikipedia/official > news > blogs) and resolves contradictions into a final status.
- **Inconclusive safeguards (layered):**
  - Judge confidence < 0.40 → overridden to Inconclusive
  - No NLI majority (< 50% for any single label) → Inconclusive
  - Claim contains "exactly/precisely N" but no evidence mentions that number → Inconclusive (quantitative precision guard)

### Stage 4: Scoring with Source Authority
- **Service:** `ScoringService`
- **Authority weights:** Each source type carries a credibility multiplier applied to the risk calculation:
  - `fact_check` (Google Fact Check): **1.4×**
  - `encyclopedia` (Wikipedia): **1.2×**
  - `web_search` (Tavily / DuckDuckGo): **1.0×**
  - `local_db` (ChromaDB seed): **0.7×**
- **Risk formula per claim:**
  - Contradicted: `(0.7 + 0.3 × confidence) × authority`
  - Supported: `(0.3 × (1 − confidence)) × authority`
  - Inconclusive: `(0.5 + 0.2 × (1 − confidence)) × authority`
- Overall risk is the average across all claims, clipped to [0, 1].

### Stage 5: Relational Audit Trail
- **Database:** SQLAlchemy (SQLite)
- **Logged per job:**
  - Raw input text and job metadata
  - Every extracted claim with status, risk score, confidence, and reasoning
  - Every individual evidence source: URL, domain, type, individual NLI verdict, confidence, and relevance score
  - Judge Agent's full clinical reasoning chain

---

## 2. Technical Stack

### Backend
| Component | Technology |
|-----------|-----------|
| Framework | FastAPI (async) |
| LLM | Llama3 via Ollama |
| NLI Model | `cross-encoder/nli-deberta-v3-small` (Transformers) |
| Embeddings | `all-MiniLM-L6-v2` (SentenceTransformers) |
| Vector store | ChromaDB (local evidence cache) |
| Relational DB | SQLAlchemy + SQLite |
| Search | Tavily, Google Fact Check, Wikipedia REST API, DuckDuckGo |

### Frontend
| Component | Technology |
|-----------|-----------|
| Framework | React 19 + Vite |
| Styling | Tailwind CSS |
| Charts | Recharts |
| Streaming | `fetch` + `ReadableStream` (SSE) |

---

## 3. API Reference

### POST `/api/verify`
Verifies all claims in parallel and returns the full result when complete.

**Request:**
```json
{ "text": "The Eiffel Tower was built in 1950." }
```

**Response:**
```json
{
  "job_id": 42,
  "text": "...",
  "claims": [
    {
      "claim": "The Eiffel Tower was built in 1950.",
      "status": "Contradicted",
      "risk_score": 0.91,
      "confidence": 0.87,
      "start": 0,
      "end": 38,
      "explanation": "Sources confirm the Eiffel Tower was completed in 1889, not 1950.",
      "reasoning": "Wikipedia and Tavily both state construction completed in 1889...",
      "consensus_stats": { "Supported": 0, "Contradicted": 4, "Insufficient Evidence": 1 },
      "evidence_details": [...]
    }
  ],
  "overall_risk": 0.91,
  "metadata": {
    "total_time_ms": 8200,
    "extraction_time_ms": 1100,
    "processing_time_ms": 7100,
    "claim_count": 1
  }
}
```

### POST `/api/verify/stream`
Same input as `/api/verify`. Returns a `text/event-stream` response that emits one JSON event per claim as it completes, enabling real-time UI updates.

**Event types:**
```
data: {"type": "start", "claim_count": 3}

data: {"type": "claim", "index": 0, "data": { ...claim result... }}

data: {"type": "complete", "job_id": 42, "overall_risk": 0.45, "total_time_ms": 9800}

data: {"type": "error", "message": "..."}
```

### GET `/api/health`
Returns service health status.

---

## 4. Accuracy Benchmark

The pipeline is validated against a labeled benchmark in `backend/tests/test_accuracy.py`.

**Run:**
```bash
cd backend
pytest tests/test_accuracy.py -v -s
```

**Current results (15-claim suite):**

| Label | Precision | Recall | F1 |
|-------|-----------|--------|----|
| Supported | 78% | 100% | 88% |
| Contradicted | 80% | 67% | 73% |
| Inconclusive | 100% | 50% | 67% |
| **Overall** | | **80%** | |

The test prints a full failure report and asserts accuracy ≥ 60%. The 3 remaining misses are due to LLM non-determinism on borderline claims — they pass on most runs.

---

## 5. UI Components

| Component | Purpose |
|-----------|---------|
| **Heatmap** | Highlights each sentence in the original text with a risk color derived from the claim mapped to that offset |
| **Consensus Bar** | Shows the Supported / Contradicted / Insufficient split across all evidence sources for a claim |
| **Clinical Audit Reasoning** | Displays the Judge Agent's full chain-of-thought reasoning |
| **Evidence Panel** | Global audit trail of every URL, source domain, relevance score, and NLI verdict consulted |
| **Confidence Meter** | Radial gauge showing overall hallucination risk for the full input |
| **Dashboard Chart** | Recharts bar chart showing verdict distribution across all claims |
| **Streaming Progress Bar** | Live progress indicator while claims stream in from `/verify/stream` |

---

## 6. Configuration

All settings are loaded from a `.env` file via `pydantic-settings`.

| Variable | Default | Description |
|----------|---------|-------------|
| `TAVILY_API_KEY` | — | Enables Tavily search (optional) |
| `GOOGLE_FACT_CHECK_API_KEY` | — | Enables Google Fact Check (optional) |
| `OLLAMA_MODEL` | `llama3` | Ollama model name |
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | Sentence embedding model |
| `VERIFIER_MODEL` | `cross-encoder/nli-deberta-v3-small` | NLI cross-encoder |
| `CHROMA_PERSIST_DIR` | `db/chroma` | ChromaDB storage path |
| `USE_WEB_SEARCH` | `true` | Toggle live web search |
| `MAX_SEARCH_RESULTS_PER_SOURCE` | `5` | Results per source per query |
| `CONSENSUS_THRESHOLD` | `0.7` | Minimum confidence for definitive verdict |
| `MIN_SOURCES_FOR_CONSENSUS` | `3` | Minimum sources before consensus is computed |

Wikipedia is always active — it requires no configuration.
