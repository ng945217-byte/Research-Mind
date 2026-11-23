# ResearchMind AI

An intelligent multi-agent research and document intelligence platform. ResearchMind orchestrates autonomous agents to search, verify, summarize, and generate structured analysis reports from web sources and uploaded documents.

---

## Architecture Overview

```
+-----------------------------------------------------------+
|                    Client Layer                           |
|       React + TypeScript + Tailwind (Vite) / Streamlit    |
+-----------------------------+-----------------------------+
                              | REST / SSE
                              v
+-----------------------------------------------------------+
|                    FastAPI Backend                        |
|   /api/research  |  /api/documents  |  /api/reports       |
+-----------------------------+-----------------------------+
                              |
                              v
+-----------------------------------------------------------+
|                 Research Engine & Agents                  |
|    LangGraph Workflow | Fact-Checking | Vector Search     |
+-----------------------------+-----------------------------+
                              |
              +---------------+---------------+
              |                               |
              v                               v
       Primary LLM (Gemini)           Fallback LLM (Groq)
```

---

## Core Capabilities

- **Autonomous Agent Workflows**: Coordinated search, filtering, and cross-source synthesis using LangGraph.
- **Dual Engine Search**: Combines internet search results with structured knowledge queries.
- **Document RAG System**: Upload PDFs, DOCX, or CSVs for vector retrieval using ChromaDB and sentence transformers.
- **Fact Verification**: Evaluates statements against gathered evidence with confidence scoring.
- **Multi-Format Export**: Generates reports in Markdown, PDF, or text format.
- **Interactive UI & Streamlit Option**: Full React dashboard alongside an alternative Streamlit interface.

---

## Directory Layout

```
.
|-- .github/               # Workflows and templates
|-- backend/               # FastAPI application
|   |-- agents/            # Multi-agent worker definitions
|   |-- api/routes/        # REST route handlers
|   |-- data/              # Storage for ChromaDB, uploads, reports
|   |-- graphs/            # LangGraph workflow configurations
|   |-- memory/            # Conversation & research history
|   |-- models/            # Pydantic schemas & SQLAlchemy models
|   |-- parsers/           # Document extraction utilities
|   |-- rag/               # Vector store & retriever
|   |-- reporting/         # Export generators
|   |-- tests/             # Automated test suite
|   |-- main.py            # Server entrypoint
|   |-- requirements.txt   # Python dependencies
|-- frontend/              # React + TypeScript frontend
|   |-- src/               # Application source code
|   |-- package.json       # Node package configuration
|-- streamlit_app.py       # Streamlit application
|-- docker-compose.yml     # Multi-container orchestration
`-- README.md              # Project documentation
```

---

## Quick Setup

### 1. Prerequisites
- Python 3.10 or higher
- Node.js 18 or higher
- Git

### 2. Backend Installation

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
```

Add your API keys to `backend/.env`:
- `GEMINI_API_KEY`
- `GROQ_API_KEY`
- `TAVILY_API_KEY`

Start the server:
```bash
uvicorn main:app --port 8001 --reload
```

### 3. Frontend Installation

```bash
cd frontend
npm install
npm run dev
```

The React interface will run at `http://localhost:5173`.

### 4. Running with Docker

```bash
docker compose up --build
```

---

## API Summary

- `GET /health` - System health check
- `POST /api/research/start` - Trigger research session
- `GET /api/research/status/{id}` - Monitor research task status
- `POST /api/documents/upload` - Process document for RAG
- `POST /api/reports/generate` - Produce exportable reports

---

## Reference Guide

Additional notes and presentation guidelines are provided in [README_Hinglish.md](README_Hinglish.md).
