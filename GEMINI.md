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

AI Hallucination Detection & Verification System

## Goal

TruthLens is an intelligent verification layer for Large Language Models (LLMs).

The system detects whether AI-generated content contains hallucinated, fabricated, misleading, or unsupported factual claims.

The platform should:

* analyze AI responses,
* extract factual claims,
* retrieve supporting evidence,
* perform semantic verification,
* estimate hallucination probability,
* and visualize trust/risk scores.

---

# CORE FUNCTIONALITY

## INPUT

User provides:

* AI-generated response
* prompt text
* article
* paragraph
* or chatbot output

---

## PROCESSING PIPELINE

### 1. Claim Extraction

Break text into atomic factual claims.

Example:
Input:

```text
Paris is the capital of France and the Eiffel Tower was built in 1920.
```

Output:

```text
Claim 1:
Paris is the capital of France

Claim 2:
Eiffel Tower was built in 1920
```

---

### 2. Evidence Retrieval

Retrieve trusted evidence using:

* semantic search,
* vector similarity,
* retrieval pipelines.

Sources may include:

* Wikipedia,
* curated datasets,
* verified corpora.

---

### 3. Semantic Verification

Compare claim vs evidence.

Possible labels:

* Supported
* Contradicted
* Insufficient Evidence

---

### 4. Hallucination Scoring

Generate:

* risk score,
* confidence score,
* reliability estimate.

---

### 5. Explainability

System must explain WHY a claim was flagged.

Example:

```text
Evidence contradicts the provided date.
```

---

# EXPECTED OUTPUT

Example:

```json
{
  "claim": "Eiffel Tower was built in 1920",
  "status": "Contradicted",
  "hallucination_risk": 0.92,
  "confidence": "High",
  "evidence": "The Eiffel Tower was completed in 1889"
}
```

---

# FULL STACK REQUIREMENTS

# FRONTEND REQUIREMENTS

## Framework

React + Vite

## Styling

Tailwind CSS

## State Management

React hooks

## API Communication

Axios

## Charts

Recharts

## Frontend Goals

Frontend must look modern and production-ready.

The UI should resemble:

* AI SaaS platforms,
* modern dashboards,
* verification systems,
* analytics platforms.

---

# REQUIRED FRONTEND FEATURES

## 1. Landing Page

Contains:

* project branding,
* explanation,
* input area,
* CTA buttons.

---

## 2. Verification Workspace

Contains:

* prompt input box,
* AI response input,
* verification button,
* processing indicators.

---

## 3. Claim Analysis Panel

Display:

* extracted claims,
* verification status,
* confidence scores.

Claims should use:

* green = supported,
* red = contradicted,
* yellow = uncertain.

---

## 4. Evidence Viewer

Display:

* retrieved evidence,
* evidence source,
* semantic similarity score.

---

## 5. Heatmap Visualization

Show hallucination risk visually.

---

## 6. Analytics Dashboard

Display:

* verification statistics,
* risk trends,
* claim distributions,
* model performance.

---

# FRONTEND FOLDER STRUCTURE

```text
frontend/
│
├── src/
│   ├── components/
│   ├── pages/
│   ├── services/
│   ├── hooks/
│   ├── layouts/
│   ├── assets/
│   ├── styles/
│   ├── App.jsx
│   └── main.jsx
```

---

# RECOMMENDED FRONTEND COMPONENTS

```text
components/
│
├── Navbar.jsx
├── HeroSection.jsx
├── ClaimCard.jsx
├── VerificationCard.jsx
├── EvidencePanel.jsx
├── ConfidenceMeter.jsx
├── Heatmap.jsx
├── DashboardChart.jsx
├── Loader.jsx
└── Footer.jsx
```

---

# BACKEND REQUIREMENTS

## Framework

FastAPI

## Backend Goals

Backend must:

* expose REST APIs,
* orchestrate AI pipeline,
* manage retrieval,
* process verification,
* and return structured results.

---

# BACKEND MODULES

## 1. API Layer

Handles:

* request routing,
* response handling,
* validation.

---

## 2. Claim Extraction Service

Uses:

* spaCy,
* NLP parsing,
* sentence segmentation.

---

## 3. Retrieval Service

Uses:

* embeddings,
* vector search,
* semantic retrieval.

---

## 4. Verification Service

Uses:

* transformer NLI models,
* semantic similarity.

---

## 5. Hallucination Scoring Engine

Combines:

* contradiction confidence,
* retrieval confidence,
* semantic consistency.

---

# BACKEND FOLDER STRUCTURE

```text
backend/
│
├── app/
│   ├── api/
│   ├── core/
│   ├── models/
│   ├── services/
│   ├── utils/
│   ├── main.py
│   └── config.py
```

---

# REQUIRED BACKEND FILES

## API

* verify_routes.py
* health_routes.py

## Services

* claim_extractor.py
* retrieval_service.py
* verification_service.py
* scoring_service.py

## Models

* embedding_model.py
* verifier_model.py

## Utils

* preprocessing.py
* similarity.py
* logger.py

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
