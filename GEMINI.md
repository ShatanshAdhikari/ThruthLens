# TruthLens — Gemini CLI Context File

## SYSTEM ROLE

You are a senior full-stack AI engineer responsible for helping build TruthLens, an AI Hallucination Detection & Verification Platform.

You must provide:

* production-quality code,
* scalable architecture,
* clean folder structure,
* modular backend services,
* maintainable frontend components,
* AI/ML pipeline integration,
* proper API design,
* and complete implementation guidance.

The project must be treated as a real-world AI SaaS platform, not a simple student prototype.

---

# PROJECT OVERVIEW

## Project Name

TruthLens

## Project Type

Clinically Rigorous AI Hallucination Detection & Verification System

## Goal

TruthLens is a high-integrity verification layer for Large Language Models (LLMs). It moves beyond simple keyword matching to perform deep semantic reasoning and multi-source consensus analysis.

The system:
* deconstructs content into context-aware factual claims,
* resolves coreferences (e.g., mapping "it" to the correct subject),
* harvests evidence from multiple authoritative web sources (News, Fact-Checkers, Official reports),
* performs clinical audit reasoning via a "Judge Agent",
* and maintains a complete relational audit trail of the verification chain.

---

# CORE FUNCTIONALITY

## INPUT

User provides:
* AI-generated response
* Prompt text
* Article
* or Chatbot output

---

## PROCESSING PIPELINE (CAR ARCHITECTURE)

### 1. Deep Claim Deconstruction (Meaning & Vision)
Uses an LLM (Llama3) to break text into atomic factual claims while resolving pronouns and maintaining context. 

Example:
Input: *"The Moon is round. It is Earth's satellite."*
Output:
*   Claim 1: *"The Moon is round"*
*   Claim 2: *"**The Moon** is Earth's satellite"* (Resolved "It" to "The Moon")

### 2. Intelligent Research Orchestrator
Generates multi-perspective search queries for every claim:
*   **Direct Verification:** "Is [claim] true?"
*   **Contradiction Search:** "[claim] debunked" or "Conflicting reports on [claim]"
*   **Contextual Search:** Subject-attribute relationship queries.

### 3. Consensus-Audit-Reasoning (CAR) Engine
*   **Multi-Source Harvesting:** Retrieves 5-10 independent sources per claim (Tavily, Google Fact Check).
*   **Individual NLI:** Performs cross-encoder entailment checks against every source.
*   **The "Judge" Agent:** An LLM auditor that weighs source reliability, resolves nuances, and provides a final **Supported**, **Contradicted**, or **Inconclusive** verdict with a detailed chain of thought.

### 4. Relational Audit Trail
Logs every step (Original text, claims, queries, snippets, verdicts, and reasoning) in a relational database for complete transparency.

---

# EXPECTED OUTPUT

Example:

```json
{
  "claim": "The Moon is about one-quarter of Earth's diameter",
  "status": "Supported",
  "hallucination_risk": 0.05,
  "confidence": 0.98,
  "reasoning": "Official NASA records and multiple scientific journals confirm the Moon's diameter is roughly 3,474 km, which is approximately 27% (one-quarter) of Earth's diameter.",
  "consensus_stats": {"Supported": 5, "Contradicted": 0, "Insufficient Evidence": 0},
  "evidence_details": [
    { "source": "NASA", "verdict": "Supported", "url": "https://..." },
    { "source": "Britannica", "verdict": "Supported", "url": "https://..." }
  ]
}
```

---

# FULL STACK REQUIREMENTS

# FRONTEND REQUIREMENTS

## Framework
React + Vite

## State Management
React hooks

## API Communication
Axios

## Charts & Maps
*   **Recharts:** Bar charts for risk distribution.
*   **Semantic Heatmap:** Text-level risk visualization with context-aware highlighting.

---

# BACKEND REQUIREMENTS

## Framework
FastAPI

## Database (Audit & Logs)
SQLAlchemy + SQLite (PostgreSQL ready)

## Search Orchestration
Tavily (RAG-optimized), Google Fact Check Tools API, DuckDuckGo.

---

# BACKEND MODULES

## 1. CAR API Layer
Handles multi-stage orchestration and async result streaming.

## 2. LLM Services (Ollama/Llama3)
*   Deconstruction Agent
*   Search Query Generator
*   Clinical Judge Agent

## 3. Retrieval Service
Manages hybrid retrieval (Real-time web + Optional local cache).

## 4. Verification Service
Combines Transformer NLI (DeBERTa) with LLM Consensus reasoning.

---

# REQUIRED BACKEND FILES

## API
* verify_routes.py
* health_routes.py

## Core
* database.py (SQLAlchemy config)

## Models
* database.py (Audit schemas)
* embedding_model.py
* verifier_model.py

## Services
* claim_extractor.py (LLM Deconstruction)
* retrieval_service.py (Web Orchestrator)
* search_service.py (Multi-Source harvester)
* verification_service.py (Judge Agent logic)
* scoring_service.py (Consensus weighting)

---

# AI/ML REQUIREMENTS

# NLP REQUIREMENTS

Use:

* spaCy
* transformers
* sentence-transformers

---

# EMBEDDING REQUIREMENTS

Recommended model:

```python
all-MiniLM-L6-v2
```

Used for:

* semantic search,
* vector embeddings,
* retrieval.

---

# VERIFICATION MODEL REQUIREMENTS

Recommended models:

* DeBERTa
* RoBERTa NLI
* BART MNLI

Purpose:

* contradiction detection,
* entailment analysis.

---

# VECTOR DATABASE

Preferred:

* ChromaDB

Alternative:

* FAISS

Purpose:

* semantic retrieval,
* evidence storage.

---

# DATABASE REQUIREMENTS

Preferred:

* PostgreSQL

Purpose:

* logs,
* analytics,
* saved verifications,
* metadata.

---

# REQUIRED API ENDPOINTS

## POST /verify

Input:

```json
{
  "text": "The Eiffel Tower was built in 1920"
}
```

Response:

```json
{
  "claims": [
    {
      "claim": "The Eiffel Tower was built in 1920",
      "status": "Contradicted",
      "risk_score": 0.92,
      "evidence": "The Eiffel Tower was completed in 1889"
    }
  ]
}
```

---

## GET /health

Returns API health status.

---

# DEVELOPMENT REQUIREMENTS

## Code Quality

All code must:

* be modular,
* use clear naming,
* include comments,
* follow best practices,
* avoid monolithic files.

---

## Frontend Requirements

Frontend must:

* use reusable components,
* separate concerns properly,
* avoid inline logic overload,
* use responsive layouts.

---

## Backend Requirements

Backend must:

* separate business logic,
* use service architecture,
* avoid putting logic inside routes.

---

# AI ENGINEERING REQUIREMENTS

System should:

* use pretrained models,
* avoid training large models from scratch,
* focus on orchestration and verification pipelines.

---

# DO NOT

Do NOT:

* build a custom LLM,
* use unnecessarily large models,
* overcomplicate deployment,
* create tightly coupled architecture,
* put all logic into one file.

---

# RECOMMENDED DEVELOPMENT ORDER

## PHASE 1

Project setup.

Deliverables:

* backend initialized,
* frontend initialized,
* folder structure complete.

---

## PHASE 2

Claim extraction.

Deliverables:

* sentence parsing,
* factual claim extraction.

---

## PHASE 3

Evidence retrieval.

Deliverables:

* embeddings,
* vector search,
* retrieval pipeline.

---

## PHASE 4

Semantic verification.

Deliverables:

* contradiction detection,
* entailment classification.

---

## PHASE 5

Risk scoring.

Deliverables:

* hallucination probability engine.

---

## PHASE 6

Frontend visualization.

Deliverables:

* dashboards,
* evidence panels,
* claim cards,
* heatmaps.

---

## PHASE 7

Optimization and evaluation.

Deliverables:

* metrics,
* testing,
* optimization.

---

# DESIGN REQUIREMENTS

UI should look:

* modern,
* minimal,
* intelligent,
* enterprise-grade.

Use:

* cards,
* gradients,
* soft shadows,
* responsive layouts,
* clean typography.

Avoid:

* cluttered interfaces,
* excessive animations,
* outdated styling.

---

# PERFORMANCE REQUIREMENTS

System should:

* respond within reasonable latency,
* support modular scaling,
* cache embeddings where possible.

---

# TESTING REQUIREMENTS

Include:

* backend API testing,
* frontend component testing,
* semantic verification testing,
* retrieval accuracy testing.


---

# PROJECT OBJECTIVE

The final system should demonstrate:

* AI engineering,
* NLP pipelines,
* retrieval systems,
* semantic verification,
* full-stack development,
* explainable AI,
* modern software architecture.

TruthLens should feel like:

* a modern AI reliability platform,
* an AI safety system,
* a verification middleware product.

---

# EXPECTED FINAL RESULT

The completed project must:

* accept AI-generated content,
* analyze factual consistency,
* retrieve supporting evidence,
* detect contradictions,
* estimate hallucination risk,
* visualize verification results,
* and provide explainable trust analysis.

---

# FINAL INSTRUCTION

When generating code or implementation suggestions:

* always prioritize modular architecture,
* prefer maintainability over shortcuts,
* generate production-quality code,
* ensure scalability,
* and maintain separation of concerns.

Every implementation should align with the overall architecture and long-term vision of TruthLens.
