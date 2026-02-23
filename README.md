# 🧠 Developer Knowledge Copilot

A production-grade AI system that indexes technical documentation and answers developer queries with citations, confidence scores, and latency tracking.

**Stack**: FastAPI · FAISS · BGE-small embeddings · SQLite · React Native (Expo)

---

## Quick Start

### 1. Install dependencies

```bash
python -m venv venv
venv\Scripts\activate       # Windows
pip install -r requirements.txt
```

### 2. Configure environment

```bash
copy .env.example .env
# Edit .env and add your free API key from https://openrouter.ai
```

### 3. Ingest sample documents

```bash
python scripts/ingest_docs.py --source data/sample_docs
```

### 4. Start the backend

```bash
uvicorn backend.main:app --reload --port 8000
```

Visit **http://localhost:8000/docs** for interactive API documentation.

### 5. Run the mobile app

```bash
cd mobile
npx create-expo-app@latest .    # First time only
npm start
# Scan QR with Expo Go on your phone
```

---

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/health` | Liveness check + indexed vector count |
| `POST` | `/api/v1/query` | Ask a question, get answer + citations |
| `GET` | `/api/v1/documents` | List all indexed docs + stats (chunk count, tokens) |

### POST /api/v1/query

The query endpoint uses a **two-stage retrieval pipeline**:
1. **Hybrid Search**: Combines BM25 and Vector search for high recall.
2. **Re-ranking**: Uses a Cross-Encoder (`TinyBERT`) to ensure high precision.
3. **Factuality Guard**: A second-pass LLM self-check to prevent hallucinations.

```json
// Request
{
  "query": "How do I configure CORS in FastAPI?",
  "top_k": 5
}

// Response
{
  "answer": "Use CORSMiddleware from fastapi.middleware.cors...",
  "citations": [
    {
      "title": "FastAPI Getting Started",
      "source_url": null,
      "text_preview": "from fastapi.middleware.cors import CORSMiddleware..."
    }
  ],
  "confidence": "high",
  "latency_ms": 482,
  "tokens_used": 347
}
```

---

## Run Tests

```bash
# Week 1 tests
pytest backend/tests/test_week1.py -v

# Week 5 tests (Re-ranking, Scoring, Factuality)
pytest backend/tests/test_week5.py -v
```

---

## Docker

```bash
# Build
docker build -t dev-copilot:latest .

# Run
docker run -p 8000:8000 --env-file .env dev-copilot:latest
```

---

## Project Structure

```
├── backend/
│   ├── api/routes.py         ← HTTP endpoints (Query, Health, Docs)
│   ├── core/config.py        ← Settings (pydantic-settings)
│   ├── db/models.py          ← SQLite schema + Query Logs
│   ├── ingestion/
│   │   ├── chunker.py        ← Structural Code Chunking (.py, .js)
│   │   └── embedder.py       ← BGE-small-en-v1.5 embeddings
│   ├── retrieval/
│   │   ├── vector_store.py   ← FAISS IndexFlatIP
│   │   ├── hybrid.py        ← BM25 + Vector Fusion
│   │   └── reranker.py       ← Cross-Encoder Re-ranking
│   ├── scoring/
│   │   └── engine.py         ← Centralized Confidence Engine
│   ├── generation/
│   │   └── llm.py            ← LLM + Factuality Guard
│   └── main.py               ← App entry point
├── mobile/
│   ├── app/search.tsx        ← Premium Results UI
│   └── services/api.ts       ← Backend API calls
├── scripts/ingest_docs.py    ← Code-aware ingestion script
└── data/sample_docs/         ← Sample documents
```

---

---

## Roadmap

| Week | Focus |
|------|-------|
| ✅ 1 | Basic RAG — chunking, embeddings, FAISS, citations |
| ✅ 2 | Advanced Citations + Mobile UI + Code Ingestion |
| ✅ 3 | Hybrid search (BM25 + Vector) |
| ✅ 4 | Latency metrics + request logging |
| ✅ 5 | Confidence scoring + re-ranking + Factuality Guard |
| 📅 6 | Redis caching + benchmarks |
| 📅 7 | Load testing (50 concurrent users) |
| 📅 8 | Deploy to Render + Expo APK build |
