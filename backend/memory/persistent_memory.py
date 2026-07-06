"""
RESEARCHMINDAI - Short-term Session and Long-term SQLite Memory Manager
"""
from typing import List, Dict, Any, Optional
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import MemoryEntry as DBMemoryEntry, ResearchSession as DBResearchSession, ResearchResult as DBResearchResult
from models.research import Source
import json
import logging

logger = logging.getLogger(__name__)

class MemoryManager:
    """Manages short-term context sessions and long-term research records in SQL and ChromaDB."""

    async def save_research_session(
        self,
        db: AsyncSession,
        session_id: str,
        query: str,
        mode: str,
        status: str = "pending",
        metadata: Dict[str, Any] = None
    ) -> DBResearchSession:
        session = DBResearchSession(
            id=session_id,
            query=query,
            mode=mode,
            status=status,
            metadata_=metadata or {}
        )
        db.add(session)
        await db.commit()
        return session

    async def update_session_status(
        self,
        db: AsyncSession,
        session_id: str,
        status: str,
        completed_at: Optional[Any] = None
    ):
        result = await db.execute(select(DBResearchSession).where(DBResearchSession.id == session_id))
        session = result.scalars().first()
        if session:
            session.status = status
            if completed_at:
                session.completed_at = completed_at
            await db.commit()

    async def save_research_result(
        self,
        db: AsyncSession,
        session_id: str,
        result_data: Dict[str, Any]
    ) -> DBResearchResult:
        # Convert Pydantic source models or raw dicts to JSON-compatible forms
        sources = result_data.get("sources", [])
        if sources and isinstance(sources[0], Source):
            sources_json = [s.model_dump() for s in sources]
        else:
            sources_json = sources

        result = DBResearchResult(
            session_id=session_id,
            summary=result_data.get("summary"),
            deep_summary=result_data.get("deep_summary"),
            keywords=result_data.get("keywords", []),
            sources=sources_json,
            confidence_score=result_data.get("confidence_score", 0.0),
            timeline=result_data.get("timeline", []),
            technical_analysis=result_data.get("technical_analysis"),
            beginner_explanation=result_data.get("beginner_explanation"),
            expert_explanation=result_data.get("expert_explanation"),
            future_predictions=result_data.get("future_predictions"),
            conclusions=result_data.get("conclusions"),
            contradictions=result_data.get("contradictions", []),
            entities=result_data.get("entities", []),
            sentiment=result_data.get("sentiment", "neutral")
        )
        db.add(result)
        
        # Also create a long-term semantic memory entry for this research session
        memory_content = (
            f"Research query: {result_data.get('query') or ''}\n"
            f"Summary: {result_data.get('summary') or ''}\n"
            f"Key Findings: {result_data.get('conclusions') or ''}"
        )
        memory = DBMemoryEntry(
            type="research",
            title=f"Research: {result_data.get('query') or 'Untitled'}",
            content=memory_content,
            metadata_={"session_id": session_id}
        )
        db.add(memory)

        await db.commit()
        return result

    async def get_session_history(self, db: AsyncSession, limit: int = 20) -> List[DBResearchSession]:
        stmt = select(DBResearchSession).order_by(DBResearchSession.created_at.desc()).limit(limit)
        result = await db.execute(stmt)
        return list(result.scalars().all())

    async def get_session_details(self, db: AsyncSession, session_id: str) -> Optional[Dict[str, Any]]:
        session_stmt = select(DBResearchSession).where(DBResearchSession.id == session_id)
        session_res = await db.execute(session_stmt)
        session = session_res.scalars().first()
        if not session:
            return None

        result_stmt = select(DBResearchResult).where(DBResearchResult.session_id == session_id)
        result_res = await db.execute(result_stmt)
        res_detail = result_res.scalars().first()

        return {
            "session": session,
            "results": res_detail
        }

memory_manager = MemoryManager()
