"""
RESEARCHMINDAI - New Feature API Routes
Research Papers, Planner, Debate, Knowledge Graph, Timeline, Explain, Source Verification, Export
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse, Response
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import logging
import re
import json
import io

logger = logging.getLogger(__name__)
router = APIRouter()

class TTSRequest(BaseModel):
    text: str

# ─── Request Models ───────────────────────────────────────────────────────────

class TopicRequest(BaseModel):
    topic: str

class ExplainRequest(BaseModel):
    topic: str
    mode: str = "beginner"  # beginner | expert | eli5

class DebateRequest(BaseModel):
    topic: str

class VerifyRequest(BaseModel):
    sources: List[str]
    topic: str

class ExportRequest(BaseModel):
    title: str
    summary: str
    deep_summary: Optional[str] = ""
    sources: Optional[List[Dict]] = []
    keywords: Optional[List[str]] = []
    format: str = "markdown"  # markdown | txt

# ─── Helper: Real Paper Search via Semantic Scholar (free, no key) ────────────

def _search_semantic_scholar(query: str, limit: int = 8) -> List[Dict]:
    try:
        import urllib.request
        clean = re.sub(r'[^\w\s]', '', query)[:100]
        url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={urllib.parse.quote(clean)}&limit={limit}&fields=title,authors,year,abstract,url,citationCount,venue"
        import urllib.parse
        url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={urllib.parse.quote(clean)}&limit={limit}&fields=title,authors,year,abstract,url,citationCount,venue"
        req = urllib.request.Request(url, headers={"User-Agent": "ResearchMindAI/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            papers = []
            for p in data.get("data", []):
                authors = ", ".join([a.get("name","") for a in p.get("authors",[])[:3]])
                papers.append({
                    "paperId": p.get("paperId",""),
                    "title": p.get("title","Untitled"),
                    "authors": authors or "Unknown Authors",
                    "year": p.get("year","N/A"),
                    "abstract": (p.get("abstract") or "No abstract available.")[:400] + "...",
                    "url": p.get("url") or f"https://www.semanticscholar.org/paper/{p.get('paperId','')}",
                    "citations": p.get("citationCount", 0),
                    "venue": p.get("venue","")
                })
            return papers
    except Exception as e:
        logger.warning(f"Semantic Scholar search failed: {e}")
        return []

def _search_arxiv(query: str, limit: int = 5) -> List[Dict]:
    try:
        import urllib.request, urllib.parse
        from xml.etree import ElementTree as ET
        url = f"https://export.arxiv.org/api/query?search_query=all:{urllib.parse.quote(query)}&start=0&max_results={limit}"
        req = urllib.request.Request(url, headers={"User-Agent": "ResearchMindAI/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read()
        root = ET.fromstring(content)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        papers = []
        for entry in root.findall('atom:entry', ns):
            title = entry.findtext('atom:title', '', ns).strip().replace('\n', ' ')
            abstract = entry.findtext('atom:summary', '', ns).strip().replace('\n', ' ')[:400] + "..."
            link_el = entry.find("atom:link[@rel='alternate']", ns)
            url_val = link_el.get('href','') if link_el is not None else ''
            published = entry.findtext('atom:published','',ns)[:4]
            authors_els = entry.findall('atom:author/atom:name', ns)
            authors = ", ".join([a.text for a in authors_els[:3] if a.text])
            papers.append({
                "paperId": url_val,
                "title": title,
                "authors": authors or "Unknown",
                "year": published,
                "abstract": abstract,
                "url": url_val,
                "citations": "N/A",
                "venue": "arXiv"
            })
        return papers
    except Exception as e:
        logger.warning(f"ArXiv search failed: {e}")
        return []

# ─── ENDPOINT 1: Research Papers ──────────────────────────────────────────────

@router.post("/research-papers")
async def search_research_papers(request: TopicRequest):
    """Search academic papers from Semantic Scholar + ArXiv."""
    papers = _search_semantic_scholar(request.topic, limit=6)
    if len(papers) < 3:
        arxiv_papers = _search_arxiv(request.topic, limit=5)
        papers.extend(arxiv_papers)
    return {
        "topic": request.topic,
        "papers": papers,
        "total": len(papers)
    }

# ─── ENDPOINT 2: Research Planner ─────────────────────────────────────────────

@router.post("/research-planner")
async def generate_research_plan(request: TopicRequest):
    """Generate a step-by-step research plan for a topic."""
    topic = request.topic.strip()
    keywords = [w for w in re.findall(r'\b\w{4,}\b', topic) if w.lower() not in ['what','that','this','with','from','have','been','will','your','they']][:5]
    
    plan = {
        "topic": topic,
        "overview": f"A structured research roadmap for: '{topic}'. This plan is organized into 5 phases to help you conduct thorough, systematic research.",
        "phases": [
            {
                "phase": 1,
                "title": "Background & Foundation",
                "duration": "1-2 days",
                "color": "#5E5CE6",
                "tasks": [
                    f"Read introductory articles about '{topic}'",
                    "Note key terminology and definitions",
                    "Identify main subtopics and branches",
                    "Browse Wikipedia and encyclopedia sources"
                ]
            },
            {
                "phase": 2,
                "title": "Literature Review",
                "duration": "3-5 days",
                "color": "#2CB5E8",
                "tasks": [
                    f"Search Google Scholar, ArXiv, Semantic Scholar for '{' '.join(keywords)}'",
                    "Collect 10-15 relevant academic papers",
                    "Read abstracts and select 5-8 core papers",
                    "Use citation tracking to find related work"
                ]
            },
            {
                "phase": 3,
                "title": "Deep Analysis",
                "duration": "5-7 days",
                "color": "#10B981",
                "tasks": [
                    "Read selected papers in full detail",
                    "Take structured notes per paper",
                    "Identify patterns, contradictions, and gaps",
                    f"Run deep search queries on '{topic}' variations"
                ]
            },
            {
                "phase": 4,
                "title": "Synthesis & Debate",
                "duration": "2-3 days",
                "color": "#F59E0B",
                "tasks": [
                    "Organize findings into clear themes",
                    "Note supporting vs contradicting evidence",
                    "Form your own research hypothesis",
                    "Use AI Debate mode to stress-test your ideas"
                ]
            },
            {
                "phase": 5,
                "title": "Documentation & Export",
                "duration": "1-2 days",
                "color": "#E11D48",
                "tasks": [
                    "Write a structured research summary",
                    "Generate citations for all sources",
                    "Use Export Center to download your report",
                    "Share findings with peers for review"
                ]
            }
        ],
        "tips": [
            f"Use Boolean operators: '{keywords[0] if keywords else topic} AND overview'",
            "Save papers to your Library for easy access",
            "Use the Timeline Generator to understand historical context",
            "Verify key sources using Source Verification"
        ]
    }
    return plan

# ─── ENDPOINT 3: AI Debate ────────────────────────────────────────────────────

@router.post("/debate")
async def generate_debate(request: DebateRequest):
    """Generate pro vs con debate points on a topic."""
    topic = request.topic.strip()
    
    # Fetch web context to base debate on
    pro_points = []
    con_points = []
    
    try:
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            pro_results = list(ddgs.text(f"benefits advantages of {topic}", max_results=3))
            con_results = list(ddgs.text(f"criticism disadvantages problems with {topic}", max_results=3))
        
        for r in pro_results:
            snippet = r.get("body","")[:200]
            if snippet:
                pro_points.append(snippet)
        for r in con_results:
            snippet = r.get("body","")[:200]
            if snippet:
                con_points.append(snippet)
    except Exception as e:
        logger.warning(f"Debate web search failed: {e}")
    
    # Fallback structured points if web fails
    if not pro_points:
        pro_points = [
            f"Proponents argue that {topic} significantly advances efficiency and productivity.",
            f"Research indicates that {topic} has shown measurable positive outcomes in multiple studies.",
            f"Many experts believe {topic} will drive innovation and open new possibilities.",
            f"Early adopters of {topic} have reported tangible benefits and competitive advantages."
        ]
    if not con_points:
        con_points = [
            f"Critics point out that {topic} raises important ethical and societal concerns.",
            f"Studies have shown potential risks and unintended consequences associated with {topic}.",
            f"Implementation challenges make {topic} difficult to scale effectively.",
            f"Skeptics argue that the evidence supporting {topic} remains insufficient or biased."
        ]
    
    return {
        "topic": topic,
        "pro": {
            "label": "Arguments FOR",
            "color": "#10B981",
            "points": pro_points[:4]
        },
        "con": {
            "label": "Arguments AGAINST",
            "color": "#E11D48",
            "points": con_points[:4]
        },
        "verdict": f"The debate around '{topic}' reflects genuine complexity. Both sides present valid points that require careful consideration of context, scale, and long-term impact."
    }

# ─── ENDPOINT 4: Knowledge Graph ──────────────────────────────────────────────

@router.post("/knowledge-graph")
async def generate_knowledge_graph(request: TopicRequest):
    """Generate a knowledge graph of nodes and links for a topic."""
    topic = request.topic.strip()
    words = re.findall(r'\b\w{4,}\b', topic)
    
    # Fetch related concepts
    related_terms = []
    try:
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            results = list(ddgs.text(topic, max_results=5))
        all_text = " ".join([r.get("body","") for r in results])
        # Extract potential concept words (longer, meaningful words)
        candidates = re.findall(r'\b[A-Z][a-zA-Z]{4,}\b', all_text)
        seen = set()
        for c in candidates:
            if c.lower() not in topic.lower() and c not in seen:
                related_terms.append(c)
                seen.add(c)
            if len(related_terms) >= 8:
                break
    except:
        pass
    
    if len(related_terms) < 6:
        related_terms = ["Analysis", "Research", "Theory", "Application", "Innovation", "Framework", "Model", "System"]
    
    nodes = [{"id": 0, "label": topic, "type": "center", "color": "#5E5CE6", "size": 30}]
    links = []
    for i, term in enumerate(related_terms[:8], 1):
        nodes.append({"id": i, "label": term, "type": "concept", "color": "#2CB5E8" if i % 2 == 0 else "#10B981", "size": 18})
        links.append({"source": 0, "target": i, "label": "relates to"})
        if i > 1 and i % 3 == 0:
            links.append({"source": i-1, "target": i, "label": "connects"})
    
    return {"topic": topic, "nodes": nodes, "links": links}

# ─── ENDPOINT 5: Timeline Generator ───────────────────────────────────────────

@router.post("/timeline")
async def generate_timeline(request: TopicRequest):
    """Generate a historical timeline for a topic."""
    topic = request.topic.strip()
    events = []
    
    try:
        import wikipedia
        wikipedia.set_lang("en")
        search_res = wikipedia.search(topic, results=2)
        if search_res:
            page = wikipedia.page(search_res[0], auto_suggest=True)
            text = page.content[:5000]
            # Extract year mentions
            year_pattern = re.findall(r'(?:In |by |since |until |from |after |before )?((?:1[0-9]{3}|20[0-2][0-9]))\D{0,80}', text)
            seen_years = set()
            for match in year_pattern:
                year = match.strip()
                if year not in seen_years and 1800 <= int(year) <= 2030:
                    # Find sentence containing this year
                    idx = text.find(year)
                    sentence = text[max(0,idx-20):idx+120].replace('\n',' ').strip()
                    events.append({"year": year, "event": sentence})
                    seen_years.add(year)
                if len(events) >= 8:
                    break
    except Exception as e:
        logger.warning(f"Timeline Wikipedia failed: {e}")
    
    if len(events) < 3:
        events = [
            {"year": "Early Period", "event": f"Initial concepts and foundations of {topic} were established by early pioneers."},
            {"year": "Development Phase", "event": f"Key breakthroughs advanced understanding of {topic} significantly."},
            {"year": "Modern Era", "event": f"{topic} gained widespread recognition and practical applications emerged."},
            {"year": "Present Day", "event": f"Ongoing research and development continues to expand the field of {topic}."}
        ]
    
    events.sort(key=lambda x: str(x.get("year","")))
    return {"topic": topic, "events": events}

# ─── ENDPOINT 6: Explain Mode ─────────────────────────────────────────────────

@router.post("/explain")
async def explain_topic(request: ExplainRequest):
    """Explain a topic in different modes: beginner, expert, eli5."""
    topic = request.topic.strip()
    mode = request.mode.lower()
    
    wiki_summary = ""
    try:
        import wikipedia
        wikipedia.set_lang("en")
        clean_topic = re.sub(r'[^\w\s]', '', topic)
        results = wikipedia.search(clean_topic, results=2)
        if results:
            page = wikipedia.page(results[0], auto_suggest=True)
            wiki_summary = page.content[:3000]
    except Exception as e:
        logger.warning(f"Explain Wikipedia failed: {e}")
    
    base = wiki_summary or f"{topic} is a complex and multifaceted subject with broad implications."
    sentences = [s.strip() for s in base.replace('\n','').split('.') if len(s.strip()) > 40]
    
    if mode == "eli5":
        explanation = f"Imagine you're 5 years old. Let me explain '{topic}' simply:\n\n"
        explanation += f"Think of {topic} like a puzzle 🧩. Each piece is important.\n\n"
        explanation += f"{sentences[0] if sentences else topic}.\n\n"
        explanation += "The most important thing to remember is: it helps solve big problems in the world! 🌍"
        level = "Child-Friendly (ELI5)"
        color = "#F59E0B"
    elif mode == "expert":
        explanation = f"**Technical Analysis: {topic}**\n\n"
        explanation += "**Core Mechanisms:**\n"
        for s in sentences[:3]:
            explanation += f"• {s}.\n"
        explanation += f"\n**Advanced Considerations:**\n"
        for s in sentences[3:6]:
            explanation += f"• {s}.\n"
        explanation += f"\n**Research Implications:**\nCurrent evidence suggests significant interplay between theoretical frameworks and empirical applications of {topic}."
        level = "Expert / Technical"
        color = "#E11D48"
    else:  # beginner
        explanation = f"**What is {topic}?**\n\n"
        explanation += f"{sentences[0] if sentences else f'{topic} is a fascinating topic.'}\n\n"
        explanation += "**Why does it matter?**\n"
        explanation += f"{sentences[1] if len(sentences) > 1 else 'It plays an important role in modern society.'}\n\n"
        explanation += "**Key things to know:**\n"
        for s in sentences[2:5]:
            explanation += f"• {s}.\n"
        level = "Beginner-Friendly"
        color = "#10B981"
    
    return {
        "topic": topic,
        "mode": mode,
        "level": level,
        "color": color,
        "explanation": explanation
    }

# ─── ENDPOINT 7: Source Verification ──────────────────────────────────────────

@router.post("/verify-sources")
async def verify_sources(request: VerifyRequest):
    """Verify and score source reliability."""
    topic = request.topic
    verified = []
    
    trusted_domains = {
        "wikipedia.org": 85, "britannica.com": 90, "nature.com": 95,
        "science.org": 95, "pubmed.ncbi.nlm.nih.gov": 98, "arxiv.org": 88,
        "gov": 92, "edu": 89, "reuters.com": 85, "bbc.com": 82,
        "nytimes.com": 80, "who.int": 96, "un.org": 92,
        "semanticscholar.org": 90, "scholar.google.com": 88,
        "github.com": 75, "medium.com": 55, "reddit.com": 40,
        "twitter.com": 35, "facebook.com": 30, "blogspot.com": 45
    }
    
    for source_url in request.sources[:10]:
        score = 60  # default
        domain_found = "unknown"
        
        try:
            from urllib.parse import urlparse
            parsed = urlparse(source_url)
            domain = parsed.netloc.replace("www.", "")
            domain_found = domain
            
            for trusted_domain, trust_score in trusted_domains.items():
                if trusted_domain in domain:
                    score = trust_score
                    break
            else:
                if domain.endswith(".edu"):
                    score = 88
                elif domain.endswith(".gov"):
                    score = 92
                elif domain.endswith(".org"):
                    score = 72
        except:
            pass
        
        if score >= 85:
            badge = "Highly Reliable"
            color = "#10B981"
        elif score >= 70:
            badge = "Reliable"
            color = "#2CB5E8"
        elif score >= 50:
            badge = "Moderate"
            color = "#F59E0B"
        else:
            badge = "Low Reliability"
            color = "#E11D48"
        
        verified.append({
            "url": source_url,
            "domain": domain_found,
            "score": score,
            "badge": badge,
            "color": color,
            "notes": f"Domain analysis complete. {'Academic/government source — high credibility.' if score >= 85 else 'General web source — verify with additional references.'}"
        })
    
    avg = sum(v["score"] for v in verified) / len(verified) if verified else 0
    return {
        "topic": topic,
        "verified_sources": verified,
        "average_score": round(avg, 1),
        "recommendation": "Sources appear credible." if avg >= 75 else "Consider cross-referencing with more authoritative sources."
    }

# ─── ENDPOINT 8: Export ───────────────────────────────────────────────────────

@router.post("/export")
async def export_report(request: ExportRequest):
    """Export research as Markdown or plain text."""
    lines = []
    lines.append(f"# {request.title}\n")
    lines.append(f"*Generated by ResearchMind AI*\n\n---\n")
    lines.append(f"## Summary\n{request.summary}\n")
    
    if request.deep_summary:
        lines.append(f"\n## Deep Analysis\n{request.deep_summary}\n")
    
    if request.keywords:
        lines.append(f"\n## Keywords\n{', '.join(request.keywords)}\n")
    
    if request.sources:
        lines.append(f"\n## Sources\n")
        for i, src in enumerate(request.sources, 1):
            title = src.get("title", src.get("url", "Unknown"))
            url = src.get("url", "#")
            lines.append(f"{i}. [{title}]({url})\n")
    
    content = "\n".join(lines)
    safe_title = re.sub(r'[^\w]', '_', request.title)[:40]
    filename = f"{safe_title}.md"
    
    return StreamingResponse(
        io.StringIO(content),
        media_type="text/markdown",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

# ─── ENDPOINT 9: NATURAL INDIAN FEMALE NEURAL TTS (Microsoft Edge) ────────────

@router.post("/tts")
async def generate_tts(request: TTSRequest):
    """Generate Natural Indian Female TTS using Microsoft Neural voice"""
    text = request.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text is required")

    clean = re.sub(r'[*#_\[\]`]', '', text)
    clean = re.sub(r'\s+', ' ', clean).strip()[:500]

    try:
        import edge_tts
        # en-IN-NeerjaExpressiveNeural = Most natural & expressive Indian Female Neural voice
        try:
            communicate = edge_tts.Communicate(clean, voice="en-IN-NeerjaExpressiveNeural", rate="+8%", pitch="+2Hz")
            mp3_fp = io.BytesIO()
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    mp3_fp.write(chunk["data"])
            mp3_fp.seek(0)
            audio_bytes = mp3_fp.read()
            if not audio_bytes:
                raise ValueError("No audio from expressive voice")
            return Response(content=audio_bytes, media_type="audio/mpeg")
        except Exception:
            # Fallback to standard NeerjaNeural
            communicate = edge_tts.Communicate(clean, voice="en-IN-NeerjaNeural", rate="+8%", pitch="+2Hz")
            mp3_fp = io.BytesIO()
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    mp3_fp.write(chunk["data"])
            mp3_fp.seek(0)
            audio_bytes = mp3_fp.read()
            if not audio_bytes:
                raise ValueError("No audio generated")
            return Response(content=audio_bytes, media_type="audio/mpeg")
    except Exception as e:
        logger.error(f"Edge TTS failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate audio")
