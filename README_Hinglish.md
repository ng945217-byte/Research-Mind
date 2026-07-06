# 🧠 ResearchMind AI — Complete Project Documentation (Hinglish)
### Professor Presentation & PPT Reference Guide

> **Iska matlab kya hai?**
> Ye ek AI-powered Research Assistant hai jo internet pe automatically search karta hai, articles padhta hai, aur aapko ek clean, organized summary deta hai — bilkul ek research analyst ki tarah.

---

## 📋 TABLE OF CONTENTS

1. [Project Ka Overview](#1-project-ka-overview)
2. [Problem Statement](#2-problem-statement)
3. [Solution Architecture](#3-solution-architecture)
4. [Technology Stack — Har Cheez Kyu Chose Ki?](#4-technology-stack)
5. [Frontend — React Application](#5-frontend)
6. [Backend — FastAPI Server](#6-backend)
7. [Research Engine — Dil Ka Hissa](#7-research-engine)
8. [Multi-Agent System — LangGraph](#8-multi-agent-system)
9. [RAG Pipeline — Vector Search](#9-rag-pipeline)
10. [Database Design — SQLite + ChromaDB](#10-database-design)
11. [API Routes — Sab Endpoints](#11-api-routes)
12. [Data Flow — Request se Response Tak](#12-data-flow)
13. [Key Features Deep Dive](#13-key-features)
14. [Folder Structure](#14-folder-structure)
15. [PPT Ke Liye Key Points](#15-ppt-key-points)
16. [Important Concepts for Professors](#16-important-concepts-for-professors)

---

## 1. PROJECT KA OVERVIEW

**ResearchMind AI** ek full-stack intelligent research platform hai. Ye student ya researcher ki jagah internet pe jaake automatically:
- **Web search karta hai** (DuckDuckGo — free, no API key)
- **Wikipedia se padhta hai**
- **LLM (AI model) se summarize karta hai** (Google Gemini / Groq Llama)
- **Results ko database mein save karta hai** (future reference ke liye)
- **Export karta hai** (Markdown/TXT format mein)

### Ek Line Mein Bolun Toh:
> *"Ye ek AI agent hai jo aapki jagah research karta hai, Wikipedia aur Web dono se data uthata hai, aur ek clean, professional report banata hai."*

---

## 2. PROBLEM STATEMENT

**Kya problem solve ho rahi hai?**

| Problem | Solution |
|---------|----------|
| Manual research mein ghante lagte hain | AI automatically search karta hai |
| 20 alag tabs khol ke padhna padta hai | Sab kuch ek jagah aggregate hota hai |
| Information reliable hai ya nahi pata nahi | Source Verification feature |
| Report banana mushkil hota hai | One-click Export (Markdown/TXT) |
| Deep analysis ke liye expert chahiye | Deep Research mode + LLM synthesis |
| Voice se search nahi hota | Voice Assistant (Indian English) |

---

## 3. SOLUTION ARCHITECTURE

```
+-----------------------------------------------------------+
|                     USER (Browser)                        |
|              React + TypeScript Frontend                   |
|         (localhost:5173 — Vite Dev Server)                |
+------------------------+---------------------------------—+
                         |  HTTP REST API calls
                         v
+-----------------------------------------------------------+
|                  FastAPI Backend Server                    |
|               (localhost:8001 — Uvicorn)                  |
|                                                           |
|  /api/research    /api/documents    /api/features         |
|       |                |                  |               |
|       +----------------+------------------+               |
|                        |                                  |
|              Research Engine (Core)                       |
|     DuckDuckGo Search + Wikipedia + LLM Summarize        |
|                        |                                  |
|         +--------------+--------------+                   |
|         v                             v                   |
|   LangGraph Agents             SQLite + ChromaDB          |
+-----------------------------------------------------------+
         |                     |
         v                     v
   Google Gemini 1.5      Groq Llama 3.3
   (Primary LLM)          (Backup LLM)
         |
         v
   DuckDuckGo (Free)  Wikipedia (Free)
   Semantic Scholar   ArXiv (Free)
```

---

## 4. TECHNOLOGY STACK

### Frontend
| Technology | Version | Kyu Use Kiya |
|-----------|---------|--------------|
| **React** | 18+ | Component-based UI, fast rendering |
| **TypeScript** | 5+ | Type safety, less bugs in large codebases |
| **Vite** | 5+ | Super fast dev server, Hot Module Replacement |
| **Recharts** | Latest | Beautiful charts — Bar, Line, Pie |
| **Lucide React** | Latest | Clean, consistent icon library |
| **Vanilla CSS** | — | Full control, no framework bloat |

### Backend
| Technology | Version | Kyu Use Kiya |
|-----------|---------|--------------|
| **FastAPI** | 0.115.0 | Python ka fastest web framework, auto Swagger docs |
| **Uvicorn** | 0.32.0 | ASGI server — async/await support |
| **SQLAlchemy** | 2.0.35 | ORM — Python objects se database tables |
| **aiosqlite** | 0.20.0 | Async SQLite — non-blocking database calls |
| **Pydantic v2** | — | Request/Response validation (auto error messages) |
| **LangChain** | 0.3.7 | LLM integration framework |
| **LangGraph** | 0.2.55 | Multi-agent orchestration (graph-based flow) |
| **ChromaDB** | 0.5.18 | Vector database for semantic search |
| **Sentence Transformers** | 3.3.1 | Text ko 384-dim vectors mein convert karta hai |

### AI / LLM
| Technology | Kyu Use Kiya |
|-----------|--------------|
| **Google Gemini 1.5 Flash** | Fast, smart, free tier available |
| **Groq Llama 3.3 70B** | Backup LLM, extremely fast inference |
| **DuckDuckGo Search** | 100% free web search, no API key required |
| **Wikipedia API** | Free encyclopedia content |
| **Semantic Scholar API** | Free academic papers search |
| **ArXiv API** | Free research preprints (physics, CS, math) |
| **Edge TTS** | Microsoft ka free neural text-to-speech |

---

## 5. FRONTEND

**Location:** `frontend/src/App.tsx` (876 lines ka single-file architecture)

### 5.1 Component Structure

```
App.tsx (Main Component)
|
+-- Sidebar (Left Navigation)
|   +-- Logo + Brand Name
|   +-- Workspace Section
|   |   +-- New Research (home page)
|   |   +-- Recents (history)
|   |   +-- Library (uploaded docs)
|   +-- Features Section
|   |   +-- Deep Search
|   |   +-- Document Analysis
|   |   +-- Data Insights (charts)
|   |   +-- Generated Reports
|   +-- Bottom Section
|       +-- Export Center
|       +-- Settings
|
+-- Voice Mode Overlay (Fullscreen listening UI)
|
+-- Main Area (Right side, content changes per tab)
    +-- Recents Tab
    +-- Library Tab
    +-- Generated Reports Tab
    +-- Export Center Tab
    +-- Research Main Area
        +-- Search Box (Textarea)
        +-- Upload Button (File Input hidden)
        +-- Voice Button (Web Speech API)
        +-- Submit Button
        +-- Suggestion Pills
        +-- Loading Spinner
        +-- Error Message
        +-- Results Display (Quick/Deep)
        +-- Data Insights Charts
```

### 5.2 State Management (useState Hooks)

```typescript
// Core research states
const [activeTab, setActiveTab] = useState('New Research');
const [query, setQuery] = useState('');
const [mode, setMode] = useState<'quick'|'deep'|'insights'>('quick');
const [isLoading, setIsLoading] = useState(false);
const [result, setResult] = useState<any>(null);
const [error, setError] = useState('');

// Data states
const [recentSessions, setRecentSessions] = useState<any[]>([]);
const [libraryDocuments, setLibraryDocuments] = useState<any[]>([]);

// Voice assistant states
const [isListening, setIsListening] = useState(false);
const [voiceSupported, setVoiceSupported] = useState(false);
const recognitionRef = useRef<any>(null);

// Feature states
const [featureQuery, setFeatureQuery] = useState('');
const [featureLoading, setFeatureLoading] = useState(false);
const [featureResult, setFeatureResult] = useState<any>(null);
const [explainMode, setExplainMode] = useState<'beginner'|'expert'|'eli5'>('beginner');
```

**Professor ke liye note:** Hum sirf React ka built-in `useState` aur `useRef` use kar rahe hain — koi Redux/Zustand nahi. Kyunki app ka scope manageable hai aur prop drilling minimal hai. Ye deliberate choice hai over-engineering se bachne ke liye.

### 5.3 Research Polling Flow (Frontend Side)

```
User types query
      |
      v
handleSubmit() called
      |
      v
POST /api/research/quick OR /deep
      |
      v
session_id milta hai (e.g., "abc-123-def-456")
      |
      v
while (!isDone):
    await 3 seconds
    GET /api/research/session/{session_id}
    if status === "done" → result save karo, stop polling
      |
      v
setResult(data) → React auto re-renders
      |
      v
Export button click → POST /api/features/export → file download
```

**Ye pattern "Async Polling" kehlaata hai.** Server pe research ka time unknown hota hai (2 sec - 30 sec). Isliye hum har 3 second mein check karte rahte hain jab tak result ready na ho jaaye.

### 5.4 Voice Assistant (Web Speech API)

```typescript
const SpeechRecognition = (window as any).SpeechRecognition
                        || (window as any).webkitSpeechRecognition;

const recognition = new SpeechRecognition();
recognition.lang = 'en-IN';          // Indian English accent
recognition.continuous = false;       // Ek baar bolo, phir ruko
recognition.interimResults = false;   // Sirf final result chahiye

recognition.onresult = (event: any) => {
    const transcript = event.results[0][0].transcript;
    setQuery(transcript);
    setIsListening(false);
    // Auto submit after 300ms
    setTimeout(() => handleSubmit(undefined, transcript, true), 300);
};
```

**Interesting Implementation Detail:** Voice se jo result aata hai, usse **automatically TTS (Text-to-Speech)** se bhi sunaya jaata hai. Matlab bola, research hua, aur jawab bhi sunai diya — fully hands-free experience.

### 5.5 Audio System (Web Audio API)

```javascript
// Ye guaranteed playback deta hai — browser autoplay block nahi karta
let audioCtx = new AudioContext();

// TTS audio receive karo
const arrayBuffer = await res.arrayBuffer();
const audioBuffer = await audioCtx.decodeAudioData(arrayBuffer);
const source = audioCtx.createBufferSource();
source.buffer = audioBuffer;
source.connect(audioCtx.destination);
source.start(0);
```

**Kyu Web Audio API, na ki <audio> tag?**
Modern browsers mein `<audio>` tag autoplay policies ke wajah se mute ho jaata hai. Web Audio API directly AudioContext se play karta hai — koi restriction nahi.

### 5.6 Data Visualization (Recharts)

Data Insights mode mein teen charts:

| Chart Type | Kya dikhata hai | Data |
|-----------|-----------------|------|
| Bar Chart | Sector growth comparison | AI vs Biotech vs Quantum |
| Pie Chart | Source distribution | Academic, News, Market, Patents |
| Line Chart | Yearly trend analysis | Multi-line trend over months |

---

## 6. BACKEND

**Location:** `backend/main.py`

### 6.1 Server Setup

```python
app = FastAPI(
    title="ResearchMind AI",
    description="Multi-agent search, fact-checking, RAG synthesis...",
    version="1.0.0",
    lifespan=lifespan  # Startup/shutdown lifecycle management
)
```

**Lifespan kya hota hai?**
```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP: Ye sab server start hone pe chalega
    settings.ensure_dirs()    # Folders create karo (uploads, reports, etc.)
    await init_db()            # SQLite tables create karo
    yield                      # Server chal raha hai...
    # SHUTDOWN: Ye server band hone pe chalega
    logger.info("Shutting down...")
```

### 6.2 CORS Configuration

```python
app.add_middleware(CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
```

**CORS kyu chahiye?**
Frontend port 5173 pe hai, Backend port 8001 pe. Same machine pe hain phir bhi alag "origins" maane jaate hain. Browser security policy ke wajah se cross-origin requests block hoti hain by default. CORS middleware us policy ko relax karta hai explicitly listed origins ke liye.

### 6.3 4 Main API Router Modules

| Router File | URL Prefix | Primary Responsibility |
|------------|-----------|----------------------|
| `research.py` | `/api/research` | Research sessions start/get karo |
| `documents.py` | `/api/documents` | File upload, library listing |
| `reports.py` | `/api/reports` | Report generation (PDF, DOCX, PPTX) |
| `features.py` | `/api/features` | TTS, Export, Verification, etc. |

---

## 7. RESEARCH ENGINE

**Location:** `backend/research_engine.py` — Ye poore project ka **dil (heart)** hai.

### 7.1 Main Function Signature

```python
async def run_real_research(
    query: str,
    mode: str,          # "quick" ya "deep"
    max_sources: int = 5
) -> Dict[str, Any]:
```

### 7.2 Complete Step-by-Step Flow

```
STEP 1: Document Check
   kya query mein "[Attached Document: filename.pdf]" hai?
   -> YES: Special document analysis return karo (hardcoded professional response)
   -> NO: Continue real research...

STEP 2: Query Cleaning (Smart Preprocessing)
   "tell me about Quantum Computing in detail"
   -> stop words remove: ["tell", "me", "about", "in", "detail"]
   -> clean query: "Quantum Computing"
   -> Ab search engine better results dega!

STEP 3: DuckDuckGo Web Search (FREE)
   _duckduckgo_search("Quantum Computing", max_results=5)
   Returns: [
     {"title": "...", "url": "...", "snippet": "...", "relevance_score": 0.85}
   ]

STEP 4: Wikipedia Search (FREE)
   _wikipedia_search("Quantum Computing", sentences=5)
   Returns Wikipedia summary + URL
   -> Wikipedia result ko sources list ki SHURUAAT mein daalo
      (highest authority source hai)

STEP 5: Deep Mode Extra Search
   if mode == "deep":
       related_query = f"{query} research applications future"
       3 aur DuckDuckGo results fetch karo

STEP 6: LLM Summarization (Smart Fallback Chain)
   _try_llm_summarize(query, combined_snippets, mode)

   Chain:
   -> Gemini Key 1 try karo
   -> Fail? Gemini Key 2 try karo
   -> Fail? Groq Key 1 try karo
   -> Fail? Groq Key 2 try karo
   -> Sab fail? Snippets se manually summary banao

STEP 7: Keyword Extraction
   Query words + Source titles se meaningful keywords nikalo
   Max 10 keywords return karo

STEP 8: Confidence Score Calculate Karo
   confidence = min(0.95, 0.60 + (len(sources) * 0.05))
   # Zyada sources = zyada confidence

STEP 9: Complete Result Dict Return Karo
{
    "query": "...",
    "mode": "quick/deep",
    "summary": "...",
    "deep_summary": "...",  # Only in deep mode
    "sources": [...],
    "keywords": [...],
    "confidence_score": 0.85,
    "technical_analysis": "",
    "conclusions": "",
    "future_predictions": "",
    "entities": [],
    "timeline": []
}
```

### 7.3 Query Cleaning — Genius Preprocessing

```python
def _clean_search_query(query: str) -> str:
    stop_words = [
        "give", "me", "tell", "about", "lines", "words", "summary",
        "research", "deep", "explain", "what", "how", "why", "who",
        "when", "where", "is", "are", "the", "a", "an", "and", "or"
    ]
    words = query.lower().split()
    cleaned = [w for w in words if w not in stop_words]
    return " ".join(cleaned) if cleaned else query
```

**Example:**
- Input: `"tell me about Machine Learning in simple words"`
- Output: `"Machine Learning simple"`
- DuckDuckGo ab much better results dega!

### 7.4 API Key Rotation System

```python
# .env mein aise store karo:
GEMINI_API_KEY=AIzaSy...key1,AIzaSy...key2,AIzaSy...key3

# Code mein:
gemini_keys = [k.strip() for k in raw.split(",") if k.strip()]

for key in gemini_keys:
    try:
        genai.configure(api_key=key)
        response = model.generate_content(prompt)
        return response.text  # SUCCESS! Return karo
    except Exception as e:
        continue  # Agle key pe jaao
```

**Practical Importance:** Gemini ka free tier sirf 15 requests/minute allow karta hai. Agar pehla key rate-limit ho jaaye, doosra key automatically use hota hai — zero downtime.

### 7.5 Confidence Score Logic

```python
"confidence_score": min(0.95, 0.60 + (len(sources) * 0.05))
```

| Sources Found | Score |
|---------------|-------|
| 0 sources | 60% |
| 1 source | 65% |
| 5 sources | 85% |
| 7 sources | 95% (MAX CAP) |

> **Note:** 95% se zyada nahi jaata — kyunki koi bhi automated system 100% certain nahi ho sakta. Ye honest engineering hai.

---

## 8. MULTI-AGENT SYSTEM (LangGraph)

**Location:** `backend/graphs/research_graph.py`

### 8.1 LangGraph Kya Hai?

```
LangChain  = LLMs ke saath kaam karne ke tools (prompt templates, chains)
LangGraph  = Multiple agents ko ek directed graph mein orchestrate karna
             (Har agent ek "node" hota hai, edges define karte hain flow)
```

**Simple analogy:** Manufacturing factory jaisa — assembly line mein har worker (agent) specific kaam karta hai, aur product (state) station se station pe move karta hai.

### 8.2 Research State — Shared Memory Object

```python
class ResearchState(TypedDict):
    # Input
    query: str               # "Explain Machine Learning"
    mode: str                # "quick" ya "deep"
    include_web: bool        # DuckDuckGo use karo?
    include_wikipedia: bool  # Wikipedia use karo?
    max_sources: int         # Kitne sources chahiye

    # Collected Data
    sources: List[Dict]      # [{title, url, snippet, relevance_score}]
    contradictions: List[Dict] # Sources mein kya contradictions mili?

    # Outputs
    confidence_score: float  # 0.0 to 1.0
    summary: str             # Quick 2-para summary
    deep_summary: str        # Comprehensive analysis
    timeline: List[Dict]     # Chronological events
    technical_analysis: str  # Technical breakdown
    beginner_explanation: str# Simple ELI5 explanation
    expert_explanation: str  # Advanced technical analysis
    future_predictions: str  # Next 3-5 years outlook
    conclusions: str         # Final takeaways
    entities: List[str]      # ["OpenAI", "Transformer", "RLHF"]
    sentiment: str           # "positive"/"negative"/"neutral"

    # System
    agent_logs: List[str]    # Har agent ka activity log
```

> **Samjho aise:** ResearchState ek **shared notebook** hai. Har agent isko padhta hai, apna kaam karta hai, aur result is notebook mein likhta hai. Agle agent ko updated notebook milti hai.

### 8.3 Graph Diagram — Visual Flow

```
[START]
   |
   v
+----------------+
| web_search     |  <- Search Agent: DuckDuckGo pe query bhejo
| Node           |     state.sources mein results add karo
+-------+--------+
        |
        v
+----------------+
| wikipedia      |  <- Wikipedia Agent: Encyclopedia se content lo
| Node           |     state.sources mein Wikipedia result add karo
+-------+--------+
        |
        v
+----------------+
| fact_checker   |  <- Fact Checker Agent: Sources mein contradictions dhundho
| Node           |     state.contradictions + state.confidence_score set karo
+-------+--------+
        |
        | [CONDITIONAL EDGE — mode check karo]
        |
   mode=="quick"?         mode=="deep"?
        |                      |
        v                      v
+----------------+    +------------------+
| quick_summary  |    | deep_writer      |
| Node           |    | Node             |
| (2-para summ.) |    | (Full analysis,  |
|                |    | timeline, predict|
+-------+--------+    | ions, entities)  |
        |             +--------+---------+
        |                      |
        +----------+-----------+
                   |
                   v
                [END]
```

### 8.4 Agent Details

#### Agent 1: Search Agent (`agents/search_agent.py`)
- DuckDuckGo ya Tavily se web search karta hai
- Results ko `state.sources` mein add karta hai
- Relevance score assign karta hai

#### Agent 2: Wikipedia Agent (`agents/wikipedia_agent.py`)
- Wikipedia API call karta hai
- Encyclopedia summary fetch karta hai
- Sources mein highest priority se add karta hai

#### Agent 3: Fact Checker Agent (`agents/fact_checker_agent.py`) — MOST INTERESTING

```python
# LLM ko sab sources ka text deta hai
# Prompt: "In sources mein contradictions dhundho, JSON mein return karo"
# LLM responds:
[
    {
        "claim_a": "COVID-19 vaccines are 95% effective",
        "claim_b": "COVID-19 vaccines show 67% efficacy in trials",
        "source_a": "CDC.gov article",
        "source_b": "Medical journal study",
        "severity": "high"
    }
]

# Confidence score calculation:
base_score = 1.0 - (len(contradictions) * 0.15)
# Har contradiction 15% penalty!
# 0 contradictions = 100% base score
# 1 contradiction = 85% base score
# 4+ contradictions = 40% (minimum floor)
```

#### Agent 4: Deep Writer Agent (`graphs/research_graph.py` - `deep_writer_node`)

```python
# System Prompt to LLM:
"You are an Elite Research Writer. Generate a JSON containing:
1. deep_summary: Multi-paragraph authoritative synthesis
2. technical_analysis: Detailed mechanisms and methodology
3. beginner_explanation: Simple ELI5 explanation
4. expert_explanation: Advanced professional analysis
5. future_predictions: Next 3-5 years outlook
6. conclusions: Final takeaways
7. entities: [list of key names/concepts]
8. sentiment: positive/negative/neutral
9. timeline: [{date, event, significance}]"

# LLM returns structured JSON
# Code parses JSON aur state mein save karta hai
```

---

## 9. RAG PIPELINE (Retrieval-Augmented Generation)

**Location:** `backend/rag/`

### 9.1 RAG Kya Hota Hai?

```
Normal LLM problem:
User: "Meri company ki Q3 2024 sales report kya thi?"
LLM: "Mujhe nahi pata — ye mere training data mein nahi tha."

RAG solution:
Step 1 - RETRIEVAL: Company ka Q3 report upload karo → ChromaDB mein store
Step 2 - AUGMENTATION: Query karo → similar chunks dhundho → LLM ko do
Step 3 - GENERATION: LLM ab document ke basis pe accurate answer deta hai!
```

**Simple analogy:** Open-book exam ki tarah. Without RAG = closed book (sirf memory). With RAG = open book (reference material available).

### 9.2 3 RAG Components

#### Component 1: Vector Store (`rag/vector_store.py`) — ChromaDB

```python
class VectorStore:
    # ChromaDB mein 3 collections:
    RESEARCH_COLLECTION = "research_results"   # Past research vectors
    DOCUMENTS_COLLECTION = "uploaded_documents" # Document chunk vectors
    MEMORY_COLLECTION = "memory_entries"        # Session memory vectors

    def add_texts(self, collection_name, texts, ids, metadatas):
        # Text documents ChromaDB mein add karo
        # ChromaDB automatically embed karta hai

    def query(self, collection_name, query_text, n_results=5):
        # query_text ke similar documents dhundho
        # Cosine similarity use hoti hai
        # Top-5 most similar chunks return karo
```

**Cosine Similarity kya hai?**
Har text ko ek vector (384 numbers ka array) mein convert karo. Phir query vector aur stored vectors ke beech ka "angle" measure karo. Angle kam = zyada similar.

#### Component 2: Indexer (`rag/indexer.py`)

```
Document Upload (PDF/DOCX/TXT)
         |
         v
Parse karo (text extract karo)
         |
         v
Chunks mein todo (e.g., 500 words each, 50 words overlap)
         |
         v
Har chunk ko embed karo (all-MiniLM-L6-v2 model)
         |
         v
ChromaDB mein save karo (with metadata: filename, page_num, etc.)
```

#### Component 3: Retriever (`rag/retriever.py`)

```
User Query aaya
         |
         v
Query bhi embed karo (same model)
         |
         v
ChromaDB mein cosine similarity search karo
         |
         v
Top-K (e.g., 5) most similar chunks
         |
         v
LLM ko do: "In documents ke basis pe answer do: [query]"
         |
         v
LLM grounded, accurate answer deta hai
```

### 9.3 Embedding Model

```python
embedding_model: str = "all-MiniLM-L6-v2"
```

| Property | Value |
|----------|-------|
| Architecture | Bi-encoder Transformer |
| Model Size | ~22MB |
| Output Dimensions | 384 floating-point numbers |
| Max Input Tokens | 256 tokens |
| Speed | Very fast (CPU pe bhi chalega) |
| Quality | Good for semantic similarity tasks |

---

## 10. DATABASE DESIGN

**Location:** `backend/database.py`

Do alag-alag databases use ho rahe hain different purposes ke liye:

```
SQLite (researchmind.db)     ChromaDB (./data/chroma/)
------------------------     -------------------------
Structured data store        Vector/Embedding store
Traditional SQL tables       Similarity search optimized
Sessions, Results, Docs      Text chunk embeddings
Relations, Queries, Joins    Cosine distance matching
```

### 10.1 SQLite — 5 Tables ka Complete Schema

#### Table 1: `research_sessions` (Master Table)
```
id           TEXT  PRIMARY KEY   UUID e.g., "3fa85f64-..."
query        TEXT  NOT NULL      "What is Machine Learning?"
mode         TEXT  NOT NULL      "quick" ya "deep"
status       TEXT  DEFAULT       "pending" -> "running" -> "done"/"error"
created_at   DATETIME            Kab shuru hua
completed_at DATETIME            Kab khatam hua (NULL agar chal raha hai)
metadata     JSON                {"include_web": true, "max_sources": 5}
```

#### Table 2: `research_results` (Results Store)
```
id                   TEXT    PRIMARY KEY
session_id           TEXT    FK -> research_sessions.id
summary              TEXT    Quick 2-paragraph summary
deep_summary         TEXT    Detailed multi-paragraph analysis
keywords             JSON    ["AI", "ML", "Neural Networks"]
sources              JSON    [{title, url, snippet, relevance_score}]
confidence_score     FLOAT   0.0 to 1.0
timeline             JSON    [{date: "2017", event: "Transformer paper"}]
technical_analysis   TEXT    Technical breakdown
beginner_explanation TEXT    Simple ELI5 explanation
expert_explanation   TEXT    Advanced analysis
future_predictions   TEXT    Next 3-5 years outlook
conclusions          TEXT    Final takeaways
contradictions       JSON    [{claim_a, claim_b, severity}]
entities             JSON    ["OpenAI", "GPT-4", "Transformer"]
sentiment            TEXT    "positive"/"negative"/"neutral"
created_at           DATETIME
```

#### Table 3: `documents` (File Library)
```
id          TEXT     PRIMARY KEY
filename    TEXT     "research_paper.pdf"
file_type   TEXT     "pdf"/"docx"/"txt"/"csv"/"xlsx"
file_path   TEXT     "./data/uploads/uuid_filename.pdf"
file_size   INTEGER  Bytes mein
ocr_applied BOOLEAN  Kya OCR use hua (scanned images ke liye)
status      TEXT     "uploaded"/"processing"/"done"
page_count  INTEGER  Total pages
word_count  INTEGER  Total words
analysis    JSON     Extracted key findings
created_at  DATETIME
```

#### Table 4: `reports` (Generated Reports)
```
id          TEXT     PRIMARY KEY
session_id  TEXT     FK -> research_sessions.id (nullable)
document_id TEXT     FK -> documents.id (nullable)
title       TEXT     "Machine Learning Research Report"
format      TEXT     "pdf"/"docx"/"pptx"/"md"
file_path   TEXT     "./data/reports/report_uuid.pdf"
created_at  DATETIME
```

#### Table 5: `memory_entries` (AI Memory)
```
id           TEXT  PRIMARY KEY
type         TEXT  "research"/"document"/"conversation"
title        TEXT  Descriptive title
content      TEXT  Actual text content
embedding_id TEXT  ChromaDB mein corresponding vector ID
metadata     JSON  Extra info
created_at   DATETIME
```

### 10.2 Dual-Layer Session Management

```python
# PRIMARY: In-Memory Store (Python Dict — RAM mein)
_session_store: Dict[str, Dict] = {}
# FAST! O(1) lookup. Server restart pe clear ho jaata hai.

# SECONDARY: SQLite Database (Disk mein)
# PERSISTENT! Server restart ke baad bhi data rahta hai.

# Strategy:
# 1. Research start -> immediately RAM mein store karo (fast response)
# 2. Background task done -> RAM update karo + DB mein save karo
# 3. GET request aaya:
#    a. Pehle RAM check karo
#    b. Nahi mila -> DB check karo
#    c. Dono nahi -> 404 error
```

**Kyu ye smart approach hai?**
- RAM lookup microseconds mein hota hai
- DB write seconds le sakti hai (async ho bhi toh)
- User ko instant response milta hai
- DB failure pe bhi system chal sakta hai

---

## 11. API ROUTES — SARE ENDPOINTS

### 11.1 Research Routes (`/api/research`)

| Method | Endpoint | Request Body | Response |
|--------|----------|-------------|---------|
| POST | `/quick` | `{query, include_web, max_sources}` | `{session_id, status}` |
| POST | `/deep` | `{query, depth, include_timeline}` | `{session_id, status}` |
| GET | `/session/{id}` | — | Full result ya "running" |
| GET | `/sessions?limit=20` | — | List of past sessions |
| GET | `/session/{id}/stream` | — | SSE stream (compatibility) |

**Async Pattern — Kyu?**
Research 2-30 seconds le sakti hai. FastAPI mein sab request handlers async hote hain. Agar synchronous banao toh ek research poore server ko block kar deti. Background tasks se baaki requests normally serve hoti rehti hain.

### 11.2 Features Routes (`/api/features`)

| Method | Endpoint | Request | Kya Return Karta Hai |
|--------|----------|---------|---------------------|
| POST | `/research-papers` | `{topic}` | Papers list from Semantic Scholar + ArXiv |
| POST | `/research-planner` | `{topic}` | 5-phase research roadmap |
| POST | `/debate` | `{topic}` | Pro vs Con analysis |
| POST | `/knowledge-graph` | `{topic}` | Nodes + Links for concept map |
| POST | `/timeline` | `{topic}` | Historical events list |
| POST | `/explain` | `{topic, mode}` | Beginner/Expert/ELI5 explanation |
| POST | `/verify-sources` | `{sources, topic}` | Reliability scores |
| POST | `/export` | `{title, summary, sources}` | Downloadable .md file |
| POST | `/tts` | `{text}` | Audio MP3 bytes |

### 11.3 Research Papers — Real API Integration

```python
def _search_semantic_scholar(query: str, limit=8) -> List[Dict]:
    # Semantic Scholar ka free API (no key required!)
    url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={query}"
    # Returns: title, authors, year, abstract, citations, venue, url

def _search_arxiv(query: str, limit=5) -> List[Dict]:
    # ArXiv ka free XML API
    url = f"https://export.arxiv.org/api/query?search_query=all:{query}"
    # XML parse karke data nikalte hain
    # Returns: title, authors, published year, abstract, link

# Combined strategy:
# Pehle Semantic Scholar try karo (better data)
# Agar 3 se kam papers mile -> ArXiv se bhi lo
papers = _search_semantic_scholar(topic, limit=6)
if len(papers) < 3:
    arxiv_papers = _search_arxiv(topic, limit=5)
    papers.extend(arxiv_papers)
```

### 11.4 TTS — Indian Neural Voice

```python
import edge_tts

# Microsoft ka en-IN-NeerjaExpressiveNeural — Best Indian Female voice
communicate = edge_tts.Communicate(
    text=clean_text,
    voice="en-IN-NeerjaExpressiveNeural",
    rate="+8%",    # Thoda tez bolta hai
    pitch="+2Hz"   # Thoda high pitch
)

# Audio stream karo BytesIO mein
mp3_fp = io.BytesIO()
async for chunk in communicate.stream():
    if chunk["type"] == "audio":
        mp3_fp.write(chunk["data"])

# MP3 bytes response mein bhejo
return Response(content=audio_bytes, media_type="audio/mpeg")
```

### 11.5 Source Verification Algorithm

```python
trusted_domains = {
    "pubmed.ncbi.nlm.nih.gov": 98,  # Medical research
    "who.int": 96,                   # World Health Org
    "nature.com": 95,                # Science journal
    "science.org": 95,               # Science journal
    "arxiv.org": 88,                 # Research preprints
    "wikipedia.org": 85,             # Good but editable
    "github.com": 75,                # Code repos
    "medium.com": 55,                # Personal blogs
    "reddit.com": 40,                # Community forum
    "twitter.com": 35,               # Social media
    "facebook.com": 30,              # Social media
}
# Special rules:
# .edu domain -> 88%
# .gov domain -> 92%
# .org domain -> 72%
# Unknown -> 60%

# Final verdict:
if score >= 85: badge = "Highly Reliable" (Green)
elif score >= 70: badge = "Reliable" (Blue)
elif score >= 50: badge = "Moderate" (Yellow)
else: badge = "Low Reliability" (Red)
```

---

## 12. DATA FLOW — REQUEST SE RESPONSE TAK

### Complete Journey — "Explain Quantum Computing" Query

```
STEP 1: User Interface
--------
User types: "Explain Quantum Computing"
Tab: New Research, Mode: Quick
Clicks: Submit button

STEP 2: Frontend (App.tsx - handleSubmit function)
--------
POST http://127.0.0.1:8001/api/research/quick
Body: {
    "query": "Explain Quantum Computing",
    "include_web": true,
    "include_wikipedia": true,
    "max_sources": 5
}

STEP 3: FastAPI Receives (research.py)
--------
1. session_id = "3fa85f64-5717-4562-b3fc-2c963f66afa6"
2. _store_session(session_id, query, "quick")
   RAM mein: { status: "running", query: "...", result: null }
3. DB mein session record save karo (async, non-blocking)
4. BackgroundTasks mein add karo: run_research_background(...)
5. IMMEDIATELY return: { "session_id": "3fa85f64...", "status": "running" }
   <- Frontend ko instantly response mil gaya!

STEP 4: Background Task Starts (Parallel)
--------
run_research_background() called:
|
+-> run_real_research("Explain Quantum Computing", "quick", 5)
    |
    +-> _clean_search_query("Explain Quantum Computing")
    |   -> "Quantum Computing" (filler words removed)
    |
    +-> _duckduckgo_search("Quantum Computing", max_results=5)
    |   [Async, runs in thread pool executor]
    |   Results: 5 web articles about Quantum Computing
    |
    +-> _wikipedia_search("Quantum Computing")
    |   [Async, runs in thread pool executor]
    |   Result: Wikipedia article summary (5 sentences)
    |   -> Insert at index 0 in sources (highest priority)
    |
    +-> _build_summary_from_sources(query, sources, "quick")
        |
        +-> _try_llm_summarize(query, combined_snippets, "quick")
            |
            +-> Gemini API call:
            |   Prompt: "Answer 'Explain Quantum Computing' in concise 2-para"
            |   Context: [Wikipedia + web snippets]
            |
            +-> Response: "Quantum Computing is a type of computation..."
            |
            -> Return summary
    |
    +-> _extract_keywords(query, sources)
    |   -> ["Quantum", "Computing", "Qubit", "Superposition", "Entanglement"]
    |
    +-> Return full result dict
    |   {
    |       "query": "Explain Quantum Computing",
    |       "mode": "quick",
    |       "summary": "Quantum Computing is...",
    |       "sources": [{title, url, snippet} x 6],
    |       "keywords": ["Quantum", "Computing", ...],
    |       "confidence_score": 0.90
    |   }
    |
    +-> _store_result(session_id, result)
        RAM update: { status: "done", result: {...} }
        DB save: research_results table mein insert

STEP 5: Frontend Polling
--------
While loop (har 3 seconds):
GET http://127.0.0.1:8001/api/research/session/3fa85f64...

Polling #1 (t=3s): status == "running" -> continue
Polling #2 (t=6s): status == "done" -> isDone = true!

setResult(statusData) called
setIsLoading(false) called
React re-renders automatically!

STEP 6: UI Update
--------
Summary displayed in card
Sources listed with links
Keywords shown as pills
Export button visible

STEP 7: Export (Optional)
--------
User clicks "Export" button
POST /api/features/export
Body: { title, summary, sources, format: "markdown" }
Response: Markdown file streamed
Browser: file download trigger -> research_report.md saved
```

---

## 13. KEY FEATURES — DEEP DIVE

### 13.1 Quick Research vs Deep Research

| Aspect | Quick Mode | Deep Mode |
|--------|-----------|-----------|
| Search Queries | 1 DuckDuckGo query | 2 queries (main + related) |
| Wikipedia | Yes | Yes |
| LLM Prompt | "Concise 2-paragraph" | "Comprehensive multi-paragraph" |
| Extra Analysis | No | Technical, Expert, Future predictions |
| Sources Count | Up to 5 | Up to 15 (depth * 5) |
| Processing Time | ~5-15 seconds | ~15-45 seconds |
| Best For | Quick answers | Academic/Professional use |

### 13.2 Document Analysis Mode

```
User clicks "Document Analysis" ya sidebar mein click karta hai
       |
       v
handleUploadClick() -> hidden file input pe click
User selects: "research_paper.pdf"
       |
       v
handleFileChange(event):
   file = event.target.files[0]
   setQuery(prev => prev + "[Attached Document: research_paper.pdf] ")
       |
       v
User submits -> handleSubmit() called
query mein "[Attached Document: ...]" hai
       |
       v
research_engine.py mein:
doc_match = re.search(r"\[Attached Document: (.*?)\]", query)
if doc_match:
    -> Special formatted response return karo
    -> Key Findings, Technical Architecture,
       Financial Impact, Conclusions, etc.
```

**Important Note:** Current implementation mein document actual mein parse nahi hota real-time mein (ye ek mock response hai). Full implementation ke liye `documents.py` route upload handle karta hai jahan PyMuPDF se PDF parse hoti hai.

### 13.3 Data Insights Mode

```python
# mode == "insights" select karo
setMode('insights')

# handleSubmit mein:
if currentMode === 'insights':
    setIsLoading(true);
    setTimeout(() => {
        setResult({ mode: 'insights', query: currentQuery });
        setIsLoading(false);
    }, 1500);  # 1.5 second fake delay (charts pre-made hain)
    return;
```

Ye mode static mock data use karta hai visualization demonstrate karne ke liye:
- Bar Chart: AI vs Biotech vs Quantum sector data
- Pie Chart: Source type distribution
- Line Chart: Monthly trend data

### 13.4 Voice Assistant — Complete Flow

```
1. User clicks mic button
2. AudioContext unlock hota hai (browser policy)
3. SpeechRecognition start karo (en-IN language)
4. Voice Mode Overlay dikhao (fullscreen red mic animation)
5. User bolata hai: "Tell me about Artificial Intelligence"
6. recognition.onresult: transcript = "Tell me about Artificial Intelligence"
7. setQuery(transcript) -> input box mein text aata hai
8. 300ms wait
9. handleSubmit(undefined, transcript, isVoiceSubmit=true)
10. Research process shuru (normal flow)
11. Result aaya + isVoiceSubmit == true
12. speakResult(result.summary) called
13. POST /api/features/tts {text: summary}
14. MP3 bytes receive
15. Web Audio API se play
16. Indian Female voice mein answer sunai deta hai!
```

---

## 14. FOLDER STRUCTURE — POORA PROJECT

```
research-agent2/
|
+-- frontend/                     # React TypeScript Application
|   +-- src/
|   |   +-- App.tsx               # MAIN FILE — complete app (876 lines)
|   |   +-- App.css               # Component-level styles
|   |   +-- index.css             # Global CSS, typography, variables
|   |   +-- main.tsx              # Entry: ReactDOM.createRoot(...)
|   |   +-- assets/               # Static assets (images, fonts)
|   +-- index.html                # HTML shell (single div#root)
|   +-- package.json              # npm dependencies + scripts
|   +-- vite.config.ts            # Vite bundler configuration
|   +-- tsconfig.json             # TypeScript configuration
|
+-- backend/
|   +-- main.py                   # FastAPI app entry point
|   +-- research_engine.py        # CORE: Search + LLM pipeline
|   +-- config.py                 # Pydantic Settings + .env loading
|   +-- database.py               # SQLAlchemy models + DB init
|   +-- requirements.txt          # All Python packages
|   +-- .env                      # API keys (NOT in git)
|   +-- .env.example              # Template for setup
|   |
|   +-- api/routes/
|   |   +-- __init__.py
|   |   +-- research.py           # /api/research/* endpoints
|   |   +-- documents.py          # /api/documents/* endpoints
|   |   +-- reports.py            # /api/reports/* endpoints
|   |   +-- features.py           # /api/features/* endpoints
|   |
|   +-- agents/
|   |   +-- base_agent.py         # BaseAgent class (LLM setup)
|   |   +-- search_agent.py       # Web search agent
|   |   +-- wikipedia_agent.py    # Wikipedia agent
|   |   +-- fact_checker_agent.py # Contradiction detector agent
|   |   +-- summary_agent.py      # Summarization agent
|   |
|   +-- graphs/
|   |   +-- research_graph.py     # LangGraph workflow definition
|   |
|   +-- rag/
|   |   +-- __init__.py
|   |   +-- vector_store.py       # ChromaDB interface class
|   |   +-- indexer.py            # Document -> vector chunks
|   |   +-- retriever.py          # Similarity search
|   |
|   +-- memory/
|   |   +-- persistent_memory.py  # DB operations (save/load sessions)
|   |
|   +-- models/
|   |   +-- research.py           # Pydantic request/response models
|   |
|   +-- tools/
|   |   +-- __init__.py
|   |   +-- tavily_tool.py        # Tavily premium search tool
|   |   +-- wikipedia_tool.py     # Wikipedia tool wrapper
|   |
|   +-- parsers/                  # PDF/DOCX/TXT parsers
|   +-- reporting/                # PDF/DOCX/PPTX generation
|   +-- utils/                    # Helper functions, LLM factory
|   +-- tests/                    # Unit tests
|   |
|   +-- data/                     # Runtime data (auto-created)
|       +-- researchmind.db       # SQLite database file
|       +-- chroma/               # ChromaDB vector store files
|       +-- uploads/              # User uploaded documents
|       +-- reports/              # Generated report files
|
+-- .streamlit/                   # Streamlit alternative UI config
+-- streamlit_app.py              # Alternative Streamlit frontend
+-- run_app.bat                   # Windows one-click startup script
+-- README_Hinglish.md            # Ye file!
```

---

## 15. PPT KE LIYE KEY POINTS

### Slide 1: Title Slide
```
ResearchMind AI
Intelligent Multi-Agent Research Platform

[Your Name] | [College Name] | [Date]
Technology: React + FastAPI + LangGraph + ChromaDB
```

---

### Slide 2: Problem Statement
**Aaj ka Problem:**
- Student ko ek topic research karna hai
- 15-20 different websites kholta hai
- Ghanton baad bhi clear picture nahi banti
- Information reliable hai ya nahi — pata nahi

**Hamara Solution:**
- Ek query type karo
- AI automatically web + Wikipedia search karta hai
- LLM se professional summary milti hai
- Sources ke saath verified report milti hai

---

### Slide 3: System Architecture (3-Tier)
```
LAYER 1 — PRESENTATION
React + TypeScript (Vite) | Port 5173
Beautiful UI, Voice input, Charts, Export

LAYER 2 — BUSINESS LOGIC
FastAPI + Python (Uvicorn) | Port 8001
LangGraph Agents, Research Engine, API Routes

LAYER 3 — DATA
SQLite (Structured) + ChromaDB (Vector)
Sessions, Documents, Embeddings, Memory
```

---

### Slide 4: Multi-Agent Architecture
```
User Query
    |
    v
[Web Search Agent] -> DuckDuckGo + Tavily
    |
    v
[Wikipedia Agent] -> Encyclopedia content
    |
    v
[Fact Checker Agent] -> Contradiction detection
    |
    v (conditional routing)
    |
Quick Mode: [Summary Agent] -> 2-para summary
Deep Mode: [Deep Writer Agent] -> Full analysis

All agents share: ResearchState (typed dict)
Orchestrated by: LangGraph (directed acyclic graph)
```

---

### Slide 5: RAG Pipeline
```
INDEXING (offline):
Document -> Parse -> Chunk -> Embed (384-dim) -> ChromaDB

RETRIEVAL (online):
Query -> Embed -> Cosine Similarity Search -> Top-5 chunks

GENERATION:
Chunks + Query -> LLM -> Grounded Answer

Why RAG over Fine-tuning?
- Dynamic: Naya doc upload = instant knowledge
- Cheap: No retraining needed
- Transparent: Sources cite hote hain
```

---

### Slide 6: Tech Stack Justification
| Component | Chosen | Why Not Alternative? |
|-----------|--------|---------------------|
| Web Framework | FastAPI | Flask se 3x faster, auto docs |
| Search | DuckDuckGo | Google = paid, DDG = free |
| LLM | Gemini + Groq | Both free tier available |
| Vector DB | ChromaDB | Simpler than Pinecone, local |
| DB | SQLite | No server setup needed |
| Frontend | React+Vite | Faster than CRA, TypeScript support |

---

### Slide 7: Key Innovations
1. **Free-First Architecture** — Core features bina kisi paid API ke kaam karte hain
2. **Multi-LLM Fallback** — Gemini fail -> Groq automatically. Zero downtime.
3. **API Key Rotation** — Multiple keys comma-separated, auto-cycle on rate limit
4. **Dual Storage** — RAM (fast) + SQLite (persistent) parallel operation
5. **Indian Voice TTS** — Microsoft Neural voice, real-time streaming audio
6. **Query Preprocessing** — Conversational text se search-optimized query automatic

---

### Slide 8: Demo Flow (Live Demonstration)
```
1. Open: http://localhost:5173
2. Type: "Explain Quantum Entanglement"
3. Click Submit -> Loading animation
4. 10-15 seconds -> Result card appears
   - Summary (2 paragraphs)
   - 6 Sources (Wikipedia + 5 web)
   - Keywords
   - Confidence Score: 85%
5. Export -> Download .md file
6. Voice mode demo:
   Click mic -> Speak -> Auto research -> Auto TTS reply
```

---

### Slide 9: Future Scope
- **Docker + Kubernetes** — Containerized deployment
- **User Authentication** — JWT-based multi-user support
- **Cloud Deployment** — AWS EC2 / Google Cloud Run
- **More LLMs** — Claude 3, GPT-4, local Ollama
- **Better RAG** — Hybrid search (BM25 + dense vectors)
- **Real-time Collaboration** — WebSocket pe multiple users
- **Mobile App** — React Native version

---

### Slide 10: Technical Metrics
| Metric | Value |
|--------|-------|
| Total Lines of Code | ~3,500+ |
| Backend Python Files | 25+ |
| API Endpoints | 13+ |
| Database Tables | 5 (SQLite) |
| Vector Collections | 3 (ChromaDB) |
| LLM Models | 2 (Gemini + Llama) |
| Free Search Sources | 4 (DDG, Wikipedia, Semantic Scholar, ArXiv) |
| Voice Language | Indian English (en-IN) |
| Export Formats | Markdown, TXT |

---

## 16. IMPORTANT CONCEPTS FOR PROFESSORS

### Q1: LangGraph vs simple LangChain kya fark hai?

**LangChain** ek toolkit hai — LLMs ke saath kaam ke liye prompt templates, memory, tools deta hai.

**LangGraph** ek orchestration framework hai jo LangChain ke upar build hua hai. Ye specifically **stateful, multi-step, conditional workflows** ke liye hai. Har step ek "node" hota hai, transitions "edges" hote hain. Ye zyada flexible hai kyunki aap branches, loops, aur parallel execution define kar sakte hain — simple sequential chains nahi.

**Hamara use case:** Fact-checker ke baad conditional routing — quick_summary ya deep_writer. Ye sirf LangGraph se possible hai, plain LangChain se nahi.

---

### Q2: RAG kyun use kiya, Fine-tuning kyun nahi?

| Aspect | Fine-Tuning | RAG |
|--------|------------|-----|
| Cost | GPU hours = expensive | Just API calls |
| Time | Days/weeks | Minutes |
| Update | Full retrain on new data | Just add to ChromaDB |
| Transparency | Black box | Sources cited |
| Hallucination | More prone | Less (grounded in docs) |
| Best for | Domain-specific tasks | Knowledge retrieval |

**Hamara project** research retrieval ke liye hai — RAG bilkul perfect choice hai.

---

### Q3: SQLite production mein use ho sakta hai?

Ye project single-user local application hai, isliye SQLite perfect hai. Scale karna ho toh:
1. SQLAlchemy ORM use kiya hai — database URL badlna hi enough hai
2. `sqlite+aiosqlite:///` -> `postgresql+asyncpg://user:pass@host/db`
3. Koi other code nahi badhegi — that's the beauty of ORM abstraction.

---

### Q4: DuckDuckGo kyun Google ke upar?

| Feature | Google Search API | DuckDuckGo |
|---------|-----------------|-----------|
| Price | $5 per 1000 queries | FREE |
| API Key | Required | Not Required |
| Rate Limit | Yes | Yes (lenient) |
| Results Quality | Better | Good |
| Privacy | Tracks users | Privacy-first |

Academic projects ke liye DuckDuckGo clearly better choice hai.

---

### Q5: Confidence Score kya accurately measure karta hai?

**Ye nahi batata:** Answer kitna "correct" hai.
**Ye batata hai:** Humne kitne reliable sources se data aggregate kiya.

```
confidence = min(0.95, 0.60 + (sources_count * 0.05))
```

Ye ek **heuristic metric** hai — exact calculation nahi. Real-world mein confidence measure karna extremely hard hai kyunki ground truth always available nahi hota. Humara approach: zyada sources = higher confidence = reasonable approximation.

---

### Q6: Async/Await aur BackgroundTasks kaise kaam karte hain?

```python
# User ki request: POST /quick
@router.post("/quick")
async def start_quick_research(
    request: QuickResearchRequest,
    background_tasks: BackgroundTasks  # FastAPI inject karta hai
):
    session_id = generate_id()

    # Sirf session store karo aur IMMEDIATELY return karo
    _store_session(session_id, request.query, "quick")

    # Research ko background mein schedule karo
    background_tasks.add_task(run_research_background, session_id, ...)

    # User ko turat response (research abhi bhi chal rahi hai)
    return {"session_id": session_id, "status": "running"}
```

`background_tasks.add_task()` ek separate Python coroutine start karta hai jo response send hone ke baad bhi chal sakta hai. FastAPI ka ASGI server (Uvicorn) event loop manage karta hai — multiple background tasks aur incoming requests simultaneously handle hoti hain.

---

### Q7: CORS kya hai aur kyu zaroori hai?

**Same-Origin Policy:** Browser security rule — Ek origin (host:port) se sirf same origin pe requests allowed hain.

**Problem:** 
- Frontend: `http://localhost:5173` (React dev server)
- Backend: `http://localhost:8001` (FastAPI server)
- Alag ports = alag origins = browser block karega!

**Solution:** Backend pe CORS middleware lagao:
```python
allow_origins = ["http://localhost:5173"]
```
Browser pehle "preflight" OPTIONS request bhejta hai. Backend "I allow this origin" respond karta hai. Phir actual request allowed hoti hai.

---

*README_Hinglish.md — ResearchMind AI Project Documentation*
*Prepared for Academic Presentation | Deep Technical Analysis*
*Language: Hinglish for clarity and accessibility*
