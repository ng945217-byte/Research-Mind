"""
RESEARCHMINDAI - API Routes: Research
Complete rewrite with robust in-memory fallback for reliability
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime
import asyncio
import json
import logging
from typing import Dict, Any, List, Optional

from database import get_db, AsyncSessionLocal, ResearchSession as DBResearchSession
from models.research import (
    QuickResearchRequest, DeepResearchRequest, QuickResearchResponse,
    DeepResearchResponse, ResearchSessionSummary, Source, Contradiction,
    TimelineEvent, AgentEvent
)
from memory.persistent_memory import memory_manager
from utils.helpers import generate_id
from research_engine import run_real_research

logger = logging.getLogger(__name__)
router = APIRouter()

# ─── In-Memory Session Store (Primary, no DB dependency) ─────────────────────
# session_id -> {status, result_data, query, mode, created_at}
_session_store: Dict[str, Dict[str, Any]] = {}

def _store_session(session_id: str, query: str, mode: str):
    _session_store[session_id] = {
        "status": "running",
        "query": query,
        "mode": mode,
        "created_at": datetime.utcnow().isoformat(),
        "result": None
    }

def _store_result(session_id: str, result: Dict[str, Any]):
    if session_id in _session_store:
        _session_store[session_id]["status"] = "done"
        _session_store[session_id]["result"] = result

def _store_error(session_id: str, error: str):
    if session_id in _session_store:
        _session_store[session_id]["status"] = "error"
        _session_store[session_id]["error"] = error

# _build_mock_result removed — using real research engine now


# ─── Background Research Runner ───────────────────────────────────────────────

async def run_research_background(
    session_id: str,
    query: str,
    mode: str,
    graph_input: Dict[str, Any]
):
    """Background task: uses real DuckDuckGo + Wikipedia research engine."""
    logger.info(f"Starting research for session {session_id}: '{query}' (mode={mode})")

    try:
        max_sources = graph_input.get("max_sources", 5)
        result = await run_real_research(query, mode, max_sources)
        _store_result(session_id, result)
        logger.info(f"Research completed for session {session_id} with {len(result.get('sources', []))} sources")

        # Best-effort DB save
        try:
            async with AsyncSessionLocal() as db:
                await memory_manager.save_research_result(db, session_id, result)
                await memory_manager.update_session_status(db, session_id, "done", datetime.utcnow())
        except Exception as db_err:
            logger.warning(f"DB save failed (in-memory store has result): {db_err}")

    except Exception as e:
        logger.error(f"Research engine error for {session_id}: {e}", exc_info=True)
        # Even on total failure, return something useful
        fallback = {
            "query": query, "mode": mode,
            "summary": f"Research encountered an error for '{query}'. Please try again.",
            "deep_summary": "", "sources": [], "keywords": [],
            "confidence_score": 0.0
        }
        _store_result(session_id, fallback)


# ─── Endpoints ────────────────────────────────────────────────────────────────

@router.post("/quick", response_model=Dict[str, str])
async def start_quick_research(
    request: QuickResearchRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """Start a quick research session in the background."""
    session_id = generate_id()

    # Register in in-memory store immediately
    _store_session(session_id, request.query, "quick")

    # Try to save to DB (best effort)
    try:
        await memory_manager.save_research_session(
            db=db, session_id=session_id, query=request.query, mode="quick",
            status="running",
            metadata={"include_web": request.include_web, "include_wikipedia": request.include_wikipedia, "max_sources": request.max_sources}
        )
    except Exception as e:
        logger.warning(f"DB session save failed: {e}")

    graph_input = {
        "query": request.query, "mode": "quick",
        "include_web": request.include_web, "include_wikipedia": request.include_wikipedia,
        "max_sources": request.max_sources, "sources": [], "contradictions": [],
        "confidence_score": 0.0, "summary": "", "deep_summary": "", "timeline": [],
        "technical_analysis": "", "beginner_explanation": "", "expert_explanation": "",
        "future_predictions": "", "conclusions": "", "entities": [],
        "agent_logs": ["System: Initializing quick research session."]
    }

    background_tasks.add_task(run_research_background, session_id=session_id, query=request.query, mode="quick", graph_input=graph_input)
    return {"session_id": session_id, "status": "running"}


@router.post("/deep", response_model=Dict[str, str])
async def start_deep_research(
    request: DeepResearchRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """Start a deep research session in the background."""
    session_id = generate_id()

    _store_session(session_id, request.query, "deep")

    try:
        await memory_manager.save_research_session(
            db=db, session_id=session_id, query=request.query, mode="deep", status="running",
            metadata={"depth": request.depth, "include_timeline": request.include_timeline, "include_predictions": request.include_predictions}
        )
    except Exception as e:
        logger.warning(f"DB session save failed: {e}")

    graph_input = {
        "query": request.query, "mode": "deep", "include_web": True, "include_wikipedia": True,
        "max_sources": request.depth * 5, "sources": [], "contradictions": [],
        "confidence_score": 0.0, "summary": "", "deep_summary": "", "timeline": [],
        "technical_analysis": "", "beginner_explanation": "", "expert_explanation": "",
        "future_predictions": "", "conclusions": "", "entities": [],
        "agent_logs": ["System: Initializing deep research session."]
    }

    background_tasks.add_task(run_research_background, session_id=session_id, query=request.query, mode="deep", graph_input=graph_input)
    return {"session_id": session_id, "status": "running"}


@router.get("/session/{session_id}")
async def get_session_details(
    session_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get details and results of a research session. Checks in-memory store first."""

    # ── PRIMARY: Check in-memory store ──
    if session_id in _session_store:
        session_data = _session_store[session_id]
        status = session_data["status"]
        result = session_data.get("result")

        if status == "running" or result is None:
            return {
                "session_id": session_id,
                "query": session_data["query"],
                "mode": session_data["mode"],
                "status": "running",
                "summary": "",
                "sources": [],
                "keywords": [],
                "confidence_score": 0.0
            }

        # Status is "done" - return the result
        sources = result.get("sources", [])
        # Normalize sources to always be plain dicts with required fields
        normalized_sources = []
        for s in sources:
            if isinstance(s, dict):
                normalized_sources.append({
                    "title": s.get("title", "Unknown Source"),
                    "url": s.get("url", ""),
                    "snippet": s.get("snippet", ""),
                    "source_type": s.get("source_type", "web"),
                    "relevance_score": s.get("relevance_score", None)
                })

        return {
            "session_id": session_id,
            "query": result.get("query", session_data["query"]),
            "mode": result.get("mode", session_data["mode"]),
            "status": "done",
            "summary": result.get("summary", ""),
            "deep_summary": result.get("deep_summary", ""),
            "sources": normalized_sources,
            "keywords": result.get("keywords", []),
            "confidence_score": result.get("confidence_score", 0.0),
            "technical_analysis": result.get("technical_analysis", ""),
            "conclusions": result.get("conclusions", ""),
            "future_predictions": result.get("future_predictions", ""),
            "created_at": session_data.get("created_at", datetime.utcnow().isoformat())
        }

    # ── FALLBACK: Check DB ──
    try:
        details = await memory_manager.get_session_details(db, session_id)
        if not details or not details["session"]:
            raise HTTPException(status_code=404, detail="Research session not found")

        session = details["session"]
        res = details["results"]

        if not res:
            return {
                "session_id": session.id, "query": session.query, "mode": session.mode,
                "status": session.status, "summary": "", "sources": [], "keywords": [], "confidence_score": 0.0
            }

        sources_list = [s.model_dump() for s in [Source(**s) for s in (res.sources or [])]]
        return {
            "session_id": session.id, "query": session.query, "mode": session.mode,
            "status": session.status, "summary": res.summary or "",
            "deep_summary": res.deep_summary or "", "sources": sources_list,
            "keywords": res.keywords or [], "confidence_score": res.confidence_score or 0.0,
            "created_at": res.created_at.isoformat() if res.created_at else None
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"DB lookup failed for session {session_id}: {e}")
        raise HTTPException(status_code=404, detail="Session not found")


@router.get("/sessions", response_model=List[ResearchSessionSummary])
async def get_sessions(
    limit: int = Query(default=20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Get list of previous research sessions."""
    try:
        sessions = await memory_manager.get_session_history(db, limit)
        return [
            ResearchSessionSummary(
                id=s.id, query=s.query, mode=s.mode, status=s.status,
                created_at=s.created_at, completed_at=s.completed_at
            ) for s in sessions
        ]
    except Exception as e:
        logger.error(f"Failed to get session history: {e}")
        return []


@router.get("/session/{session_id}/stream")
async def stream_session_logs(session_id: str):
    """SSE endpoint (kept for compatibility)."""
    async def event_generator():
        yield f"data: {json.dumps({'event_type': 'info', 'message': 'Use polling endpoint for status.'})}\n\n"
    return StreamingResponse(event_generator(), media_type="text/event-stream")
