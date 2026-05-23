# TruthLens - System Design & Documentation

TruthLens is a high-integrity, clinically rigorous AI Hallucination Detection & Verification Platform. It uses a multi-agent **Consensus-Audit-Reasoning (CAR)** architecture to verify factual claims against live web evidence.

---

## 1. System Architecture (CAR Pipeline)

The system is designed as a multi-stage verification pipeline where every stage is logged for transparency.

### **Stage 1: Deep Claim Deconstruction**
- **Service:** `ClaimExtractor` + `OllamaService` (Llama3)
- **Action:** Breaks input text into atomic claims.
- **Innovation:** Resolves coreferences (pronouns) and maintains context. "The Moon... It is..." becomes "The Moon... The Moon is...".
- **Mapping:** Uses NLP sentence matching to map deconstructed claims back to original text offsets for UI highlighting.

### **Stage 2: Multi-Perspective Search**
- **Service:** `SearchService` + `OllamaService`
- **Action:** Generates 3 unique search queries for every claim:
    1.  **Direct:** Supporting evidence search.
    2.  **Contradictory:** Search for "debunked" or "conflicting" info.
    3.  **Contextual:** Subject-focused property search.
- **Sources:** Tavily (RAG-optimized), Google Fact Check Tools, DuckDuckGo.

### **Stage 3: Consensus-Audit-Reasoning (CAR) Engine**
- **Service:** `VerificationService`
- **NLI Check:** Every retrieved source is checked against the claim using a DeBERTa NLI cross-encoder.
- **Judge Agent:** An LLM "Judge" reviews the raw snippets and NLI verdicts. It weighs source reliability (e.g., NASA > Blog) and resolves contradictions.
- **Output:** A final status (**Supported**, **Contradicted**, **Inconclusive**) with a deep "Clinical Reasoning" chain.

### **Stage 4: Relational Audit Trail**
- **Database:** SQLAlchemy (SQLite/PostgreSQL)
- **Logging:** Every verification job stores:
    - Raw input and metadata.
    - Every extracted claim and its consensus stats.
    - **Every individual evidence source** found, its URL, and its individual NLI verdict.
    - The Judge Agent's full reasoning notes.

---

## 2. Technical Stack

### **Backend**
- **Framework:** FastAPI
- **AI Models:** 
    - Llama3 (Ollama) for reasoning/deconstruction.
    - DeBERTa-v3-small (Transformers) for NLI.
    - all-MiniLM-L6-v2 for optional vector search.
- **Database:** SQLAlchemy (Relational) + ChromaDB (Vector/Cache).
- **Search APIs:** Tavily, Google Fact Check.

### **Frontend**
- **Framework:** React + Vite
- **Styling:** Tailwind CSS
- **Visualization:** 
    - **Recharts:** Risk distribution charts.
    - **Custom Heatmap:** Sentence-level risk highlighting with clinical tooltips.
    - **Evidence Panel:** A dedicated audit trail viewer.

---

## 3. Clinical Verification Logic

### **Status Mapping**
- **Supported:** High consensus across multiple reputable sources with low contradiction ratio.
- **Contradicted:** Direct contradiction found in fact-check sources or >30% contradiction ratio among web sources.
- **Inconclusive:** Mixed evidence, low source count, or weak model confidence.

### **Risk Scoring**
Risk is not a simple average. It is weighted by **Match Quality**:
- `Risk = (Contradiction Probability) * (Source Reliability + Model Confidence) / 2`
- High-confidence contradictions yield 90%+ risk.
- Uncertain or inconclusive claims default to 50-70% risk to ensure user caution.

---

## 4. API Endpoints

### **POST `/api/verify`**
- **Request:** `{ "text": "..." }`
- **Response:**
    ```json
    {
      "job_id": 123,
      "claims": [
        {
          "claim": "...",
          "status": "Supported",
          "risk_score": 0.05,
          "reasoning": "...",
          "evidence_details": [...]
        }
      ],
      "overall_risk": 0.12
    }
    ```

---

## 5. Visual Guide

- **Consensus Bar:** Shows the ratio of agreement vs disagreement among web sources.
- **Clinical Audit Reasoning:** Prominent block showing the "Judge Agent's" logical chain of thought.
- **Evidence Audit Trail:** Global list of every URL and source consulted during the "Clinical Test".
