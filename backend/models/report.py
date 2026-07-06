"""RESEARCHMINDAI - Models: Report"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class ReportFormat(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    PPTX = "pptx"
    MARKDOWN = "md"


class GenerateReportRequest(BaseModel):
    session_id: Optional[str] = None
    document_id: Optional[str] = None
    format: ReportFormat = ReportFormat.PDF
    title: Optional[str] = None
    include_sources: bool = True
    include_timeline: bool = True
    include_charts: bool = True


class ReportResponse(BaseModel):
    report_id: str
    title: str
    format: str
    download_url: str
    created_at: datetime
