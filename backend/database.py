"""
RESEARCHMINDAI - Database Setup (SQLAlchemy + SQLite async)
"""
import uuid
from datetime import datetime
from pathlib import Path

from sqlalchemy import (
    Column, String, Text, Float, Boolean,
    DateTime, Integer, JSON, ForeignKey, create_engine
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from config import settings

Base = declarative_base()


# ─── Models ──────────────────────────────────────────────────────────────────

class ResearchSession(Base):
    __tablename__ = "research_sessions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    query = Column(Text, nullable=False)
    mode = Column(String, nullable=False)  # quick | deep
    status = Column(String, nullable=False, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    metadata_ = Column("metadata", JSON, nullable=True)

    results = relationship("ResearchResult", back_populates="session", cascade="all, delete")
    reports = relationship("Report", back_populates="session", cascade="all, delete")


class ResearchResult(Base):
    __tablename__ = "research_results"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, ForeignKey("research_sessions.id"), nullable=False)
    summary = Column(Text, nullable=True)
    deep_summary = Column(Text, nullable=True)
    keywords = Column(JSON, nullable=True)
    sources = Column(JSON, nullable=True)
    confidence_score = Column(Float, nullable=True)
    timeline = Column(JSON, nullable=True)
    technical_analysis = Column(Text, nullable=True)
    beginner_explanation = Column(Text, nullable=True)
    expert_explanation = Column(Text, nullable=True)
    future_predictions = Column(Text, nullable=True)
    conclusions = Column(Text, nullable=True)
    contradictions = Column(JSON, nullable=True)
    entities = Column(JSON, nullable=True)
    sentiment = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("ResearchSession", back_populates="results")


class Document(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    filename = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_size = Column(Integer, nullable=True)
    ocr_applied = Column(Boolean, default=False)
    status = Column(String, nullable=False, default="uploaded")
    page_count = Column(Integer, nullable=True)
    word_count = Column(Integer, nullable=True)
    analysis = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Report(Base):
    __tablename__ = "reports"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, ForeignKey("research_sessions.id"), nullable=True)
    document_id = Column(String, ForeignKey("documents.id"), nullable=True)
    title = Column(String, nullable=False)
    format = Column(String, nullable=False)  # pdf | docx | pptx | md
    file_path = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("ResearchSession", back_populates="reports")


class MemoryEntry(Base):
    __tablename__ = "memory_entries"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    type = Column(String, nullable=False)  # research | document | conversation
    title = Column(String, nullable=True)
    content = Column(Text, nullable=False)
    embedding_id = Column(String, nullable=True)
    metadata_ = Column("metadata", JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


# ─── Async Engine ─────────────────────────────────────────────────────────────

def get_db_url() -> str:
    db_path = Path(settings.sqlite_db_path).resolve()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return f"sqlite+aiosqlite:///{db_path}"


async_engine = create_async_engine(get_db_url(), echo=False)
AsyncSessionLocal = async_sessionmaker(
    async_engine, expire_on_commit=False, class_=AsyncSession
)


async def init_db():
    """Create all tables."""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db():
    """Dependency: yields an async DB session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
