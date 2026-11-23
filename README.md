<div align="center">

# ResearchMind AI

### Autonomous Multi-Agent Research, Document Intelligence & Knowledge Synthesis Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.10%20%7C%203.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19.2-61DAFB?logo=react&logoColor=black)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-6.0-3178C6?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Vite](https://img.shields.io/badge/Vite-8.1-646CFF?logo=vite&logoColor=white)](https://vitejs.dev/)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-4.3-38B2AC?logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.2.55-FF6F00)](https://langchain-ai.github.io/langgraph/)
[![Docker](https://img.shields.io/badge/Docker-Supported-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)

<p align="center">
  <b>ResearchMind AI</b> is an enterprise-grade autonomous research platform. It leverages a stateful multi-agent LangGraph architecture to conduct automated web searches, cross-examine evidence, ingest multi-format enterprise documents, fact-check claims, and assemble publication-ready research reports.
</p>

</div>

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Problem Statement vs. ResearchMind Solution](#problem-statement-vs-researchmind-solution)
3. [System Architecture](#system-architecture)
4. [Multi-Agent Orchestration Flow](#multi-agent-orchestration-flow)
5. [Core Features & Capabilities](#core-features--capabilities)
6. [Technology Stack](#technology-stack)
7. [Directory Structure](#directory-structure)
8. [Installation & Local Setup](#installation--local-setup)
   - [Prerequisites](#prerequisites)
   - [Backend Configuration](#backend-configuration)
   - [Frontend Configuration](#frontend-configuration)
   - [Streamlit Alternative Interface](#streamlit-alternative-interface)
9. [Running with Docker Compose](#running-with-docker-compose)
10. [Environment Variables Reference](#environment-variables-reference)
11. [API Endpoints Reference](#api-endpoints-reference)
12. [Testing & Quality Assurance](#testing--quality-assurance)
13. [Contributing & Development Guidelines](#contributing--development-guidelines)
14. [License & Acknowledgments](#license--acknowledgments)

---

## System Overview

Manual online research is fragmented, labor-intensive, and prone to hallucinations. Researchers and analysts typically juggle dozens of browser tabs, independently verify source authority, synthesize dense text, and manually format reports.

**ResearchMind AI** solves this by automating the end-to-end research lifecycle through specialized autonomous agents:
- **Web Agent & Wikipedia Agent**: Aggregates multi-source information in real time across the open web and curated reference datasets.
- **Fact-Checker Agent**: Validates claims across corroborating sources, calculating an objective confidence score.
- **RAG & Document Agent**: Vectorizes user-uploaded files (`.pdf`, `.docx`, `.pptx`, `.csv`, `.txt`) using local embeddings and ChromaDB.
- **Synthesis & Report Agent**: Consolidates gathered intelligence into structured formats with technical summaries, beginner-friendly explanations, historical timelines, and exportable deliverables (`.pdf`, `.md`, `.txt`).

---

## Problem Statement vs. ResearchMind Solution

| Challenge in Traditional Research | ResearchMind AI Automated Approach |
| :--- | :--- |
| **Information Overload**: 30+ browser tabs needed to understand complex topics. | **Automated Synthesis**: Aggregates, cleans, and ranks sources into a unified dossier. |
| **Unverified Hallucinations**: Standard LLMs often produce unsourced or outdated claims. | **Multi-Step Fact Verification**: Cross-references claims against live web sources with confidence metrics. |
| **Siloed Document Analysis**: Internal PDFs and slides cannot interact with live web data. | **Hybrid RAG Pipeline**: Queries private enterprise files concurrently with real-time web retrieval. |
| **Manual Formatting Overhead**: Hours spent designing reports and summaries. | **Instant Automated Export**: Generates styled PDFs via ReportLab and formatted Markdown with one click. |
| **Vendor Lock-in**: Hardcoded to a single proprietary AI model. | **Dual LLM Provider System**: Supports Google Gemini 1.5 Pro and Groq Llama 3.3 with dynamic fallback. |

---

## System Architecture

```
                                  +-----------------------------+
                                  |   Web Browser / Client UI   |
                                  |  (React 19 / Streamlit App) |
                                  +--------------+--------------+
                                                 |
                                     REST API / SSE Streams
                                                 v
+---------------------------------------------------------------------------------------------------+
|                                      FastAPI Backend Engine                                        |
|                                                                                                   |
|  +--------------------+   +-----------------------+   +-------------------+   +----------------+  |
|  |  /api/research     |   |  /api/documents       |   |  /api/reports     |   |  /api/features |  |
|  +---------+----------+   +-----------+-----------+   +---------+---------+   +--------+-------+  |
|            |                          |                         |                      |          |
|            +--------------------------+------------+------------+----------------------+          |
|                                                    v                                              |
|                                      Research Engine (Core)                                        |
+----------------------------------------------------+----------------------------------------------+
                                                     |
                                                     v
+---------------------------------------------------------------------------------------------------+
|                                    LangGraph Multi-Agent Team                                      |
|                                                                                                   |
|   +-------------------+      +---------------------+      +------------------+                    |
|   |   Search Agent    | ---> | Fact-Checker Agent  | ---> |  Summary Agent   |                    |
|   | (DuckDuckGo/Tavily|      | (Claim Corroboration|      |  (Multi-level    |                    |
|   |  + Wikipedia API) |      |   & Confidence)     |      |   Synthesis)     |                    |
|   +-------------------+      +---------------------+      +------------------+                    |
+----------------------------------------------------+----------------------------------------------+
                                                     |
                     +-------------------------------+-------------------------------+
                     |                                                               |
                     v                                                               v
      +-----------------------------+                                 +-----------------------------+
      |      LLM Inference Layer    |                                 |    Storage & Vector Store   |
      | - Google Gemini 1.5 Pro     |                                 | - ChromaDB (Embeddings)     |
      | - Groq Llama 3.3 (Fallback) |                                 | - SQLite (Async Sessions)   |
      +-----------------------------+                                 | - File System (PDF/Reports) |
                                                                      +-----------------------------+
```

---

## Multi-Agent Orchestration Flow

ResearchMind uses **LangGraph** to coordinate discrete agents through a state machine:

1. **Query Parsing & Decomposition**: The system evaluates input complexity and determines depth (`quick` vs. `deep`).
2. **Parallel Retrieval**:
   - `SearchAgent` queries search engines for news, articles, and whitepapers.
   - `WikipediaAgent` pulls structured encyclopedic background.
   - `Retriever` fetches semantic matches from uploaded user documents via ChromaDB.
3. **Fact Checking & Deduplication**:
   - `FactCheckerAgent` strips conflicting claims, correlates assertions across independent URLs, and scores evidence strength.
4. **Multi-Perspective Synthesis**:
   - Technical breakdown for engineers and domain experts.
   - Simplified beginner summary for introductory onboarding.
   - Milestone timeline highlighting historical and future events.
5. **Persistence & Delivery**:
   - Session metadata is written to SQLite via async SQLAlchemy.
   - Complete dossier is served back to the React UI or compiled into PDF format.

---

## Core Features & Capabilities

### 1. Autonomous Research Modes
- **Quick Mode**: Rapid 1-2 minute synthesis optimized for fast answers and headline briefings.
- **Deep Research Mode**: Multi-step recursive search exploring subtopics, technical nuances, and opposing perspectives.

### 2. Multi-Format Document Ingestion (RAG)
Supports enterprise files up to 50MB:
- **PDF Documents**: Extracted via PyMuPDF with text layout preservation.
- **Word Files (`.docx`)**: Structured table and paragraph extraction via python-docx.
- **PowerPoint (`.pptx`)**: Slide-by-slide parsing via python-pptx.
- **Tabular Data (`.csv`)**: Data preview and columnar statistics via pandas.

### 3. Verification & Confidence Engine
Every research result includes:
- Source citations with direct external hyperlinks.
- Calculated confidence metric based on corroborating citations.
- Key industry keywords and tags automatically generated from corpus text.

### 4. Enterprise Report Compilation
- Instant export to clean Markdown format (`.md`).
- Formatted Plain Text (`.txt`).
- Downloadable PDF documents built using custom ReportLab styling rules.

### 5. Dual UI Options
- **Modern React Dashboard**: Built on React 19, TypeScript, Tailwind CSS, Lucide icons, and Recharts.
- **Streamlit Rapid App**: Standalone lightweight UI for quick local workflows and demonstrations.

---

## Technology Stack

| Layer | Technologies | Purpose |
| :--- | :--- | :--- |
| **Frontend Framework** | React 19, TypeScript, Vite | Fast, type-safe reactive web interface |
| **Styling & Animation** | Tailwind CSS 4, Framer Motion | Modern responsive UI and smooth transitions |
| **Icons & Charts** | Lucide React, Recharts | Visual indicators and data visualizations |
| **Backend Framework** | FastAPI, Uvicorn, Pydantic | High-performance asynchronous REST API |
| **Agent Framework** | LangGraph, LangChain Core | Multi-agent coordination and state graphs |
| **LLM Providers** | Google Gemini (1.5 Pro), Groq (Llama 3.3 70B) | Primary and fallback natural language synthesis |
| **Search Tools** | DuckDuckGo Search, Tavily API, Wikipedia API | Live internet discovery and structured knowledge |
| **Vector Database** | ChromaDB, Sentence-Transformers | Local embedding store for semantic document search |
| **Relational Database**| SQLite 3, SQLAlchemy 2.0 (aiosqlite) | Async persistence for research sessions and logs |
| **Document Parsers** | PyMuPDF, python-docx, python-pptx, pandas | Multi-format text and table extraction |
| **PDF Generation** | ReportLab | Production-ready PDF report compilation |
| **Containerization** | Docker, Docker Compose | Consistent multi-service production deployment |

---

## Directory Structure

```
Research-Mind/
|-- .github/
|   |-- ISSUE_TEMPLATE/
|   |   |-- bug_report.yml         # GitHub issue form for bugs
|   |   |-- config.yml             # Issue configuration
|   |   `-- feature_request.yml    # GitHub issue form for enhancements
|   |-- pull_request_template.md   # Standard pull request checklist
|   `-- workflows/
|       `-- ci.yml                 # Automated CI verification workflow
|-- .streamlit/
|   `-- config.toml                # Streamlit UI theme configuration
|-- backend/
|   |-- agents/                    # Multi-agent workers
|   |   |-- base_agent.py          # Abstract base agent interface
|   |   |-- fact_checker_agent.py  # Evidence verification worker
|   |   |-- search_agent.py        # Web search retrieval worker
|   |   |-- summary_agent.py       # Synthesis & summary worker
|   |   `-- wikipedia_agent.py     # Wikipedia knowledge retrieval
|   |-- api/
|   |   `-- routes/
|   |       |-- documents.py       # Upload & document ingestion endpoints
|   |       |-- features.py        # Fact check, compare, timeline routes
|   |       |-- reports.py         # PDF and Markdown export routes
|   |       `-- research.py        # Research session lifecycle routes
|   |-- data/                      # Data storage (git-ignored)
|   |   |-- chroma/                # Local ChromaDB vector storage
|   |   |-- reports/               # Compiled downloadable reports
|   |   `-- uploads/               # Processed user document uploads
|   |-- graphs/
|   |   `-- research_graph.py      # LangGraph state machine definition
|   |-- memory/
|   |   `-- persistent_memory.py   # Research history and memory store
|   |-- models/
|   |   |-- document.py            # Document Pydantic models
|   |   |-- report.py              # Report generation models
|   |   `-- research.py            # Research request/response schemas
|   |-- parsers/
|   |   |-- docx_parser.py         # DOCX document extractor
|   |   |-- pdf_parser.py          # PDF PyMuPDF extractor
|   |   |-- pptx_parser.py         # Presentation extractor
|   |   `-- txt_csv_parser.py      # Plaintext and CSV extractor
|   |-- rag/
|   |   |-- indexer.py             # Document chunking & indexing
|   |   |-- retriever.py           # Similarity search & BM25 retrieval
|   |   `-- vector_store.py        # ChromaDB client wrapper
|   |-- reporting/
|   |   `-- report_generator.py    # ReportLab PDF & Markdown generator
|   |-- tests/
|   |   |-- __init__.py
|   |   `-- test_api.py            # Automated API endpoint tests
|   |-- tools/
|   |   |-- tavily_tool.py         # Tavily search API integration
|   |   `-- wikipedia_tool.py      # Wikipedia API integration
|   |-- utils/
|   |   |-- helpers.py             # String, date, and formatting utilities
|   |   |-- llm_factory.py         # Dynamic model instantiation (Gemini/Groq)
|   |   `-- logger.py              # Structured logging configuration
|   |-- .env.example               # Backend environment variables template
|   |-- config.py                  # Pydantic Settings application config
|   |-- database.py                # SQLAlchemy async SQLite models & setup
|   |-- Dockerfile                 # Backend container definition
|   |-- main.py                    # FastAPI server entrypoint
|   |-- requirements.txt           # Python dependency specifications
|   `-- research_engine.py         # Main engine coordinating agents & tools
|-- frontend/
|   |-- public/                    # Static icons and assets
|   |-- src/
|   |   |-- assets/                # Images and illustrations
|   |   |-- App.css                # Custom styling rules
|   |   |-- App.tsx                # Primary React application container
|   |   |-- index.css              # Tailwind and typography foundation
|   |   `-- main.tsx               # React DOM bootstrap
|   |-- Dockerfile                 # Multi-stage frontend container
|   |-- package.json               # Node dependencies and scripts
|   |-- tsconfig.json              # TypeScript compilation rules
|   `-- vite.config.ts             # Vite build configuration
|-- .dockerignore                  # Docker build exclusions
|-- .env.example                   # Root environment template
|-- .gitignore                     # Git tracking exclusions
|-- CONTRIBUTING.md                # Open-source contribution guidelines
|-- docker-compose.yml             # Multi-service composition
|-- README.md                      # Primary project documentation
|-- README_Hinglish.md             # Secondary reference and guide
|-- run_app.bat                    # One-click Windows launch script
|-- run_streamlit.bat              # Streamlit launch script
|-- SECURITY.md                    # Vulnerability reporting policy
`-- streamlit_app.py               # Standalone Streamlit application
```

---

## Installation & Local Setup

### Prerequisites
- **Python**: Version `3.10` or `3.11`
- **Node.js**: Version `18.x` or `20.x` with `npm`
- **Git**: For cloning the repository

---

### Backend Configuration

1. Open your terminal and navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a Python virtual environment:
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # Linux / macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install all required dependencies:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. Create your local environment configuration:
   ```bash
   cp .env.example .env
   ```

5. Open `.env` and fill in your API credentials:
   ```ini
   GEMINI_API_KEY=your_gemini_api_key
   GROQ_API_KEY=your_groq_api_key
   TAVILY_API_KEY=your_tavily_api_key  # Optional: DuckDuckGo is used by default
   ```

6. Launch the FastAPI server:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8001 --reload
   ```
   The interactive Swagger documentation will be available at: `http://localhost:8001/docs`.

---

### Frontend Configuration

1. In a separate terminal window, navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node dependencies:
   ```bash
   npm install
   ```

3. Start the Vite development server:
   ```bash
   npm run dev
   ```

4. Access the React interface in your browser:
   ```
   http://localhost:5173
   ```

---

### Streamlit Alternative Interface

If you prefer using the single-file Streamlit interface:
```bash
# Ensure your virtual environment is active in the project root
pip install streamlit
streamlit run streamlit_app.py
```
Or execute the bundled Windows batch launcher:
```cmd
run_streamlit.bat
```

---

## Running with Docker Compose

To deploy both the backend and frontend simultaneously in isolated containers:

```bash
# Build images and start services
docker compose up --build -d
```

- **Frontend Application**: `http://localhost:5173`
- **Backend API**: `http://localhost:8001`
- **Swagger Documentation**: `http://localhost:8001/docs`

To stop the containers:
```bash
docker compose down
```

---

## Environment Variables Reference

| Variable Name | Default Value | Required | Description |
| :--- | :--- | :---: | :--- |
| `GEMINI_API_KEY` | `""` | Yes | Google AI Studio key for Gemini 1.5 Pro |
| `GROQ_API_KEY` | `""` | Optional | Groq API key used for Llama 3.3 high-speed fallback |
| `TAVILY_API_KEY` | `""` | Optional | Tavily Search key for advanced search filtering |
| `DEFAULT_LLM` | `gemini` | No | Primary LLM selection (`gemini` or `groq`) |
| `GEMINI_MODEL` | `gemini-1.5-pro` | No | Gemini model tier identifier |
| `GROQ_MODEL` | `llama-3.3-70b-versatile` | No | Groq model identifier |
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | No | Local sentence-transformers embedding model |
| `SQLITE_DB_PATH` | `./data/researchmind.db` | No | SQLite database storage path |
| `CHROMA_PERSIST_DIR` | `./data/chroma` | No | Local directory for ChromaDB vector embeddings |
| `UPLOAD_DIR` | `./data/uploads` | No | Storage directory for uploaded research files |
| `REPORTS_DIR` | `./data/reports` | No | Storage directory for compiled export documents |
| `MAX_RESEARCH_DEPTH` | `5` | No | Maximum recursive search steps in deep mode |
| `MAX_SEARCH_RESULTS` | `10` | No | Maximum web links retrieved per query |
| `BACKEND_PORT` | `8001` | No | Port on which FastAPI listens |
| `CORS_ORIGINS` | `http://localhost:5173` | No | Allowed frontend cross-origin requests |

---

## API Endpoints Reference

### Health & System
- `GET /health`: Returns operational status and current engine configuration.
- `GET /`: Welcome check confirming API availability.

### Research Engine
- `POST /api/research/start`: Accepts research query, mode (`quick` or `deep`), and optional uploaded context. Initiates async research execution.
- `GET /api/research/status/{session_id}`: Retrieves execution state, active agent step, and real-time progress.
- `GET /api/research/result/{session_id}`: Returns complete research dossier including summary, confidence score, sources, keywords, and timeline.

### Documents & RAG
- `POST /api/documents/upload`: Ingests and indexes `.pdf`, `.docx`, `.pptx`, `.csv`, or `.txt` into the ChromaDB vector store.
- `GET /api/documents/list`: Returns list of indexed files with metadata and token sizes.

### Fact-Checking & Analysis
- `POST /api/features/fact-check`: Evaluates an isolated claim against web and Wikipedia knowledge.
- `POST /api/features/timeline`: Builds a chronological sequence of events related to the topic.
- `POST /api/features/compare`: Analyzes and compares two distinct topics side by side.

### Reports & Export
- `POST /api/reports/generate`: Generates `.pdf`, `.md`, or `.txt` document for a given research session.
- `GET /api/reports/download/{filename}`: Downloads the compiled report file.

---

## Testing & Quality Assurance

ResearchMind includes automated test suites to ensure endpoint stability and response contracts.

Run backend tests via `pytest`:
```bash
cd backend
pytest -v tests/test_api.py
```

Run frontend production build verification:
```bash
cd frontend
npm run build
```

---

## Contributing & Development Guidelines

Contributions are welcome! Please adhere to the following steps:

1. **Fork the Repository**: Create your personal branch from `main`.
2. **Follow Coding Standards**: Keep Python functions documented and maintain TypeScript types without using `any`.
3. **Verify Locally**: Ensure both `pytest` and `npm run build` pass without errors.
4. **Submit a Pull Request**: Use the provided [Pull Request Template](.github/pull_request_template.md).

For security reports, please review our [Security Policy](SECURITY.md).

---

## License & Acknowledgments

- **License**: Released under the [MIT License](https://opensource.org/licenses/MIT).
- **Core Integrations**: Built with [LangGraph](https://github.com/langchain-ai/langgraph), [FastAPI](https://fastapi.tiangolo.com/), [React](https://react.dev/), [Vite](https://vitejs.dev/), [ChromaDB](https://www.trychroma.com/), [Google Gemini](https://ai.google.dev/), and [Groq](https://groq.com/).
