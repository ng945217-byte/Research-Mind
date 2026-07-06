"""
RESEARCHMINDAI - Pydantic Models: Research
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class ResearchMode(str, Enum):
    QUICK = "quick"
    DEEP = "deep"


class ResearchStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    DONE = "done"
    ERROR = "error"


# ─── Request Models ───────────────────────────────────────────────────────────

class QuickResearchRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=500, description="Research query")
    include_wikipedia: bool = Field(default=True)
    include_web: bool = Field(default=True)
    max_sources: int = Field(default=5, ge=1, le=20)


class DeepResearchRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=500)
    depth: int = Field(default=3, ge=1, le=5, description="Research depth (1-5)")
    include_timeline: bool = Field(default=True)
    include_predictions: bool = Field(default=True)
    include_fact_check: bool = Field(default=True)


# ─── Response Models ──────────────────────────────────────────────────────────

class Source(BaseModel):
    title: str
    url: Optional[str] = None
    snippet: Optional[str] = None
    source_type: str = "web"  # web | wikipedia | document
    relevance_score: Optional[float] = None


class TimelineEvent(BaseModel):
    date: str
    event: str
    significance: Optional[str] = None


class Contradiction(BaseModel):
    claim_a: str
    claim_b: str
    source_a: Optional[str] = None
    source_b: Optional[str] = None
    severity: str = "low"  # low | medium | high


class QuickResearchResponse(BaseModel):
    session_id: str
    query: str
    summary: str
    keywords: List[str]
    sources: List[Source]
    confidence_score: float
    mode: str = "quick"
    created_at: datetime


class DeepResearchResponse(BaseModel):
    session_id: str
    query: str
    summary: str
    deep_summary: str
    keywords: List[str]
    sources: List[Source]
    confidence_score: float
    timeline: Optional[List[TimelineEvent]] = None
    technical_analysis: Optional[str] = None
    beginner_explanation: Optional[str] = None
    expert_explanation: Optional[str] = None
    future_predictions: Optional[str] = None
    conclusions: Optional[str] = None
    contradictions: Optional[List[Contradiction]] = None
    entities: Optional[List[str]] = None
    mode: str = "deep"
    created_at: datetime


class ResearchSessionSummary(BaseModel):
    id: str
    query: str
    mode: str
    status: str
    created_at: datetime
    completed_at: Optional[datetime] = None


class AgentEvent(BaseModel):
    """SSE streaming event from agents."""
    event_type: str  # agent_start | agent_done | progress | result | error
    agent_name: str
    message: str
    data: Optional[Dict[str, Any]] = None
    progress: Optional[int] = None  # 0-100
