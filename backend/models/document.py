"""RESEARCHMINDAI - Models: Document"""
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class DocumentAnalysisRequest(BaseModel):
    document_id: str
    apply_ocr: bool = False
    extract_entities: bool = True
    sentiment_analysis: bool = True
    topic_modeling: bool = True
    generate_summary: bool = True
    generate_deep_summary: bool = False
    qa_questions: Optional[List[str]] = None


class EntityItem(BaseModel):
    text: str
    label: str  # PERSON, ORG, GPE, DATE, etc.


class TopicItem(BaseModel):
    topic: str
    keywords: List[str]
    weight: float


class DocumentAnalysisResult(BaseModel):
    document_id: str
    filename: str
    file_type: str
    page_count: Optional[int] = None
    word_count: Optional[int] = None
    summary: Optional[str] = None
    deep_summary: Optional[str] = None
    keywords: Optional[List[str]] = None
    topics: Optional[List[TopicItem]] = None
    entities: Optional[List[EntityItem]] = None
    sentiment: Optional[str] = None
    sentiment_score: Optional[float] = None
    qa_answers: Optional[Dict[str, str]] = None
    raw_text_preview: Optional[str] = None
    status: str = "done"
    created_at: datetime


class DocumentUploadResponse(BaseModel):
    document_id: str
    filename: str
    file_type: str
    file_size: int
    status: str = "uploaded"
    message: str
