"""
RESEARCHMINDAI - API Routes: Documents
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime
import os
import shutil
import json
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path
from pydantic import BaseModel

from database import get_db, Document as DBDocument
from models.document import (
    DocumentAnalysisRequest, DocumentAnalysisResult, DocumentUploadResponse,
    EntityItem, TopicItem
)
from parsers.pdf_parser import pdf_parser
from parsers.docx_parser import docx_parser
from parsers.pptx_parser import pptx_parser
from parsers.txt_csv_parser import txt_parser, csv_parser
from rag.indexer import indexer
from rag.retriever import hybrid_retriever
from rag.vector_store import DOCUMENTS_COLLECTION
from utils.llm_factory import get_llm
from utils.helpers import generate_id, truncate_text
from config import settings
from langchain_core.messages import SystemMessage, HumanMessage

logger = logging.getLogger(__name__)
router = APIRouter()

class DocumentQARequest(BaseModel):
    question: str

# ─── Endpoints ────────────────────────────────────────────────────────────────

@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    """Upload a file to the upload directory and create database entry."""
    filename = file.filename
    ext = Path(filename).suffix.lower()
    
    if ext not in [".pdf", ".docx", ".pptx", ".txt", ".csv"]:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {ext}. Supported types: PDF, DOCX, PPTX, TXT, CSV"
        )
        
    doc_id = generate_id()
    upload_dir = Path(settings.upload_dir).resolve()
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = upload_dir / f"{doc_id}{ext}"
    
    try:
        # Write file contents
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        file_size = file_path.stat().st_size
        
        # Save to DB
        db_doc = DBDocument(
            id=doc_id,
            filename=filename,
            file_type=ext.replace(".", ""),
            file_path=str(file_path),
            file_size=file_size,
            status="uploaded"
        )
        db.add(db_doc)
        await db.commit()
        
        return DocumentUploadResponse(
            document_id=doc_id,
            filename=filename,
            file_type=ext.replace(".", ""),
            file_size=file_size,
            status="uploaded",
            message="Document uploaded successfully."
        )
    except Exception as e:
        logger.error(f"Failed to upload document {filename}: {e}")
        if file_path.exists():
            file_path.unlink()
        raise HTTPException(status_code=500, detail=f"Failed to upload document: {str(e)}")


@router.post("/{document_id}/analyze", response_model=DocumentAnalysisResult)
async def analyze_document(
    document_id: str,
    request: DocumentAnalysisRequest,
    db: AsyncSession = Depends(get_db)
):
    """Parse document content, index into ChromaDB vector store, and perform LLM analysis."""
    # 1. Fetch document from DB
    result = await db.execute(select(DBDocument).where(DBDocument.id == document_id))
    db_doc = result.scalars().first()
    if not db_doc:
        raise HTTPException(status_code=404, detail="Document not found")
        
    if db_doc.status == "analyzing":
        raise HTTPException(status_code=400, detail="Document analysis already in progress")

    db_doc.status = "analyzing"
    await db.commit()

    file_path = db_doc.file_path
    ext = Path(db_doc.filename).suffix.lower()

    try:
        # 2. Parse text based on document type
        parse_res = {}
        if ext == ".pdf":
            parse_res = pdf_parser.parse(file_path, apply_ocr=request.apply_ocr)
        elif ext == ".docx":
            parse_res = docx_parser.parse(file_path)
        elif ext == ".pptx":
            parse_res = pptx_parser.parse(file_path)
        elif ext in [".txt", ".csv"]:
            if ext == ".txt":
                parse_res = txt_parser.parse(file_path)
            else:
                parse_res = csv_parser.parse(file_path)
                
        full_text = parse_res.get("full_text", "").strip()
        page_count = parse_res.get("page_count")
        word_count = parse_res.get("word_count", 0)
        
        if not full_text:
            raise ValueError("No text could be extracted from this file.")

        # 3. Index text in ChromaDB (RAG pipeline)
        chunks_count = indexer.index_document(
            doc_id=document_id,
            doc_name=db_doc.filename,
            full_text=full_text,
            metadata={"document_id": document_id}
        )

        # 4. Generate structured analysis using LLM
        summary_text = ""
        deep_summary_text = ""
        keywords = []
        topics = []
        entities = []
        sentiment = "neutral"
        sentiment_score = 0.5
        qa_answers = {}

        if request.generate_summary:
            llm = get_llm(temperature=0.3)
            # Use truncated text for context safely
            truncated_context = truncate_text(full_text, max_chars=12000)
            
            system_prompt = SystemMessage(content=(
                "You are an expert Document Analyst. Your task is to analyze the provided document text "
                "and extract the following structured analysis in JSON format:\n"
                "{\n"
                "  \"summary\": \"Concise summary of the document (2-3 sentences)\",\n"
                "  \"deep_summary\": \"Authoritative multi-paragraph summary\",\n"
                "  \"keywords\": [\"keyword1\", \"keyword2\", ...],\n"
                "  \"topics\": [\n"
                "    {\"topic\": \"Primary Topic Name\", \"keywords\": [\"kw1\", \"kw2\"], \"weight\": 0.8}\n"
                "  ],\n"
                "  \"entities\": [\n"
                "    {\"text\": \"Entity text\", \"label\": \"PERSON/ORG/GPE/DATE\"}\n"
                "  ],\n"
                "  \"sentiment\": \"positive/negative/neutral\",\n"
                "  \"sentiment_score\": 0.5\n"
                "}\n"
                "Ensure your response is valid JSON enclosed inside a ```json ``` block."
            ))
            
            human_prompt = HumanMessage(content=f"Document Text:\n{truncated_context}\n\nAnalyze document:")
            response = llm.invoke([system_prompt, human_prompt])
            resp_text = response.content
            
            try:
                cleaned = resp_text.strip()
                if "```json" in cleaned:
                    cleaned = cleaned.split("```json")[1].split("```")[0].strip()
                elif "```" in cleaned:
                    cleaned = cleaned.split("```")[1].split("```")[0].strip()
                analysis_data = json.loads(cleaned)
                
                summary_text = analysis_data.get("summary", "")
                deep_summary_text = analysis_data.get("deep_summary", "")
                keywords = analysis_data.get("keywords", [])
                topics = analysis_data.get("topics", [])
                entities = analysis_data.get("entities", [])
                sentiment = analysis_data.get("sentiment", "neutral")
                sentiment_score = analysis_data.get("sentiment_score", 0.5)
            except Exception as parse_err:
                logger.error(f"Failed to parse LLM analysis JSON: {parse_err}")
                summary_text = truncate_text(full_text, max_chars=300)
                
        # 5. Answer sample QA questions if requested
        if request.qa_questions:
            llm = get_llm(temperature=0.2)
            for q in request.qa_questions:
                # Retrieve relevant document context
                retrieved_chunks = hybrid_retriever.retrieve(
                    query=q,
                    collection_name=DOCUMENTS_COLLECTION,
                    n_results=3,
                    where={"document_id": document_id}
                )
                context_str = "\n\n".join([c["text"] for c in retrieved_chunks])
                
                qa_sys = SystemMessage(content="Answer the user's question accurately using ONLY the provided document context. If you cannot find the answer, state that it is not in the document.")
                qa_hum = HumanMessage(content=f"Context:\n{context_str}\n\nQuestion: {q}\n\nAnswer:")
                qa_resp = llm.invoke([qa_sys, qa_hum])
                qa_answers[q] = qa_resp.content.strip()

        # 6. Save results to database record
        analysis_json = {
            "summary": summary_text,
            "deep_summary": deep_summary_text,
            "keywords": keywords,
            "topics": topics,
            "entities": entities,
            "sentiment": sentiment,
            "sentiment_score": sentiment_score,
            "qa_answers": qa_answers
        }

        db_doc.page_count = page_count
        db_doc.word_count = word_count
        db_doc.analysis = analysis_json
        db_doc.ocr_applied = request.apply_ocr
        db_doc.status = "analyzed"
        await db.commit()

        # Build response items
        topic_items = [TopicItem(**t) for t in topics]
        entity_items = [EntityItem(**e) for e in entities]

        return DocumentAnalysisResult(
            document_id=document_id,
            filename=db_doc.filename,
            file_type=db_doc.file_type,
            page_count=page_count,
            word_count=word_count,
            summary=summary_text,
            deep_summary=deep_summary_text,
            keywords=keywords,
            topics=topic_items,
            entities=entity_items,
            sentiment=sentiment,
            sentiment_score=sentiment_score,
            qa_answers=qa_answers,
            raw_text_preview=truncate_text(full_text, max_chars=1000),
            status="done",
            created_at=db_doc.created_at
        )

    except Exception as e:
        logger.error(f"Document analysis failed for {document_id}: {e}", exc_info=True)
        db_doc.status = "error"
        await db.commit()
        raise HTTPException(status_code=500, detail=f"Document analysis failed: {str(e)}")


@router.get("/", response_model=List[Dict[str, Any]])
async def list_documents(db: AsyncSession = Depends(get_db)):
    """List all uploaded documents."""
    result = await db.execute(select(DBDocument).order_by(DBDocument.created_at.desc()))
    docs = result.scalars().all()
    return [
        {
            "id": d.id,
            "filename": d.filename,
            "file_type": d.file_type,
            "file_size": d.file_size,
            "status": d.status,
            "ocr_applied": d.ocr_applied,
            "page_count": d.page_count,
            "word_count": d.word_count,
            "created_at": d.created_at
        } for d in docs
    ]


@router.get("/{document_id}")
async def get_document_details(
    document_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Retrieve database details of a specific document."""
    result = await db.execute(select(DBDocument).where(DBDocument.id == document_id))
    db_doc = result.scalars().first()
    if not db_doc:
        raise HTTPException(status_code=404, detail="Document not found")
        
    return db_doc


@router.post("/{document_id}/qa")
async def document_qa(
    document_id: str,
    request: DocumentQARequest,
    db: AsyncSession = Depends(get_db)
):
    """Retrieve document chunks and generate an answer using RAG."""
    # 1. Verify document exists
    result = await db.execute(select(DBDocument).where(DBDocument.id == document_id))
    db_doc = result.scalars().first()
    if not db_doc:
        raise HTTPException(status_code=404, detail="Document not found")

    try:
        # 2. Retrieve top matching chunks using hybrid retriever
        retrieved_chunks = hybrid_retriever.retrieve(
            query=request.question,
            collection_name=DOCUMENTS_COLLECTION,
            n_results=5,
            where={"document_id": document_id}
        )

        if not retrieved_chunks:
            return {
                "answer": "No relevant text was found in the document to answer your question.",
                "sources": []
            }

        # 3. Construct prompt and invoke LLM
        context_str = ""
        sources = []
        for idx, chunk in enumerate(retrieved_chunks):
            context_str += f"Source Chunk [{idx+1}]:\n{chunk['text']}\n\n"
            sources.append({
                "chunk_id": chunk["id"],
                "score": chunk.get("score"),
                "text": chunk["text"][:300] + "..."  # Snippet
            })

        llm = get_llm(temperature=0.2)
        system_prompt = SystemMessage(content=(
            "You are a helpful QA Assistant. Your goal is to answer the user's question using ONLY "
            "the provided document sections. Be precise, accurate, and stick strictly to the context. "
            "If the answer cannot be derived from the context, respond with 'The document does not contain "
            "sufficient details to answer this question.'"
        ))
        
        human_prompt = HumanMessage(content=f"Document Context:\n{context_str}\n\nQuestion: {request.question}\n\nAnswer:")
        
        response = llm.invoke([system_prompt, human_prompt])
        
        return {
            "answer": response.content.strip(),
            "sources": sources
        }

    except Exception as e:
        logger.error(f"RAG QA failed for document {document_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to query document: {str(e)}")
