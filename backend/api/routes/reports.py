"""
RESEARCHMINDAI - API Routes: Reports
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime
import os
import logging
from typing import Dict, Any

from database import get_db, Report as DBReport, ResearchSession as DBResearchSession, Document as DBDocument
from models.report import GenerateReportRequest, ReportResponse, ReportFormat
from reporting.report_generator import report_generator
from utils.helpers import generate_id
from config import settings

logger = logging.getLogger(__name__)
router = APIRouter()

# ─── Endpoints ────────────────────────────────────────────────────────────────

@router.post("/generate", response_model=ReportResponse)
async def generate_report(
    request: GenerateReportRequest,
    db: AsyncSession = Depends(get_db)
):
    """Compile research sessions or document analyses into a PDF, DOCX, PPTX, or Markdown report."""
    if not request.session_id and not request.document_id:
        raise HTTPException(
            status_code=400,
            detail="Either session_id or document_id must be provided to generate a report."
        )

    report_id = generate_id()
    content_data = {}
    source_type = ""
    default_title = "Research Report"

    # 1. Fetch source data from DB
    if request.session_id:
        source_type = "research"
        session_stmt = select(DBResearchSession).where(DBResearchSession.id == request.session_id)
        session_res = await db.execute(session_stmt)
        session = session_res.scalars().first()
        if not session:
            raise HTTPException(status_code=404, detail="Research session not found")
            
        result_stmt = select(session.results)
        result_res = await db.execute(select(session.results.property.mapper.class_).where(
            session.results.property.mapper.class_.session_id == request.session_id
        ))
        result = result_res.scalars().first()
        if not result:
            raise HTTPException(status_code=400, detail="Research session has no results compiled yet.")

        default_title = f"Research: {session.query}"
        content_data = {
            "query": session.query,
            "mode": session.mode,
            "summary": result.summary,
            "deep_summary": result.deep_summary,
            "sources": result.sources or [],
            "contradictions": result.contradictions or [],
            "timeline": result.timeline or [],
            "technical_analysis": result.technical_analysis,
            "beginner_explanation": result.beginner_explanation,
            "expert_explanation": result.expert_explanation,
            "future_predictions": result.future_predictions,
            "conclusions": result.conclusions,
            "confidence_score": result.confidence_score
        }

    else:
        source_type = "document"
        doc_stmt = select(DBDocument).where(DBDocument.id == request.document_id)
        doc_res = await db.execute(doc_stmt)
        doc = doc_res.scalars().first()
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")
            
        if doc.status != "analyzed" or not doc.analysis:
            raise HTTPException(
                status_code=400,
                detail=f"Document must be fully analyzed before generating reports. Current status: {doc.status}"
            )

        default_title = f"Analysis: {doc.filename}"
        analysis = doc.analysis
        content_data = {
            "filename": doc.filename,
            "file_type": doc.file_type,
            "page_count": doc.page_count,
            "word_count": doc.word_count,
            "summary": analysis.get("summary"),
            "deep_summary": analysis.get("deep_summary"),
            "keywords": analysis.get("keywords", []),
            "topics": analysis.get("topics", []),
            "entities": analysis.get("entities", []),
            "sentiment": analysis.get("sentiment"),
            "sentiment_score": analysis.get("sentiment_score")
        }

    # 2. Determine title and filename
    report_title = request.title or default_title
    ext = request.format.value
    reports_dir = Path(settings.reports_dir).resolve()
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = reports_dir / f"{report_id}.{ext}"

    # 3. Call the report generator engine to write the file
    try:
        success = report_generator.generate(
            file_path=str(file_path),
            title=report_title,
            data=content_data,
            source_type=source_type,
            fmt=request.format,
            options={
                "include_sources": request.include_sources,
                "include_timeline": request.include_timeline,
                "include_charts": request.include_charts
            }
        )
        if not success:
            raise RuntimeError("Report generator failed to write file.")
            
    except Exception as e:
        logger.error(f"Failed to generate report file: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Report writing failed: {str(e)}"
        )

    # 4. Save report log entry to DB
    db_report = DBReport(
        id=report_id,
        session_id=request.session_id,
        document_id=request.document_id,
        title=report_title,
        format=ext,
        file_path=str(file_path)
    )
    db.add(db_report)
    await db.commit()

    # 5. Compile download URL
    download_url = f"/api/reports/download/{report_id}"
    
    return ReportResponse(
        report_id=report_id,
        title=report_title,
        format=ext,
        download_url=download_url,
        created_at=db_report.created_at
    )


@router.get("/download/{report_id}")
async def download_report(
    report_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Download a generated report as a downloadable file attachment."""
    result = await db.execute(select(DBReport).where(DBReport.id == report_id))
    report = result.scalars().first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    file_path = report.file_path
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail="Report file no longer exists on server storage."
        )

    # Clean the filename for presentation in browser
    safe_title = "".join(c for c in report.title if c.isalnum() or c in " _-").strip()
    safe_title = safe_title or "report"
    filename = f"{safe_title}.{report.format}"

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/octet-stream"
    )
