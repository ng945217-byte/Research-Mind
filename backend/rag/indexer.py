"""
RESEARCHMINDAI - RAG: Ingestion & Indexer
"""
import uuid
from typing import List, Dict, Any
from rag.vector_store import vector_store, DOCUMENTS_COLLECTION
from utils.helpers import clean_text
import logging

logger = logging.getLogger(__name__)

class IngestionPipeline:
    """Chunks, cleans, and embeds document content into ChromaDB."""

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def index_document(self, doc_id: str, doc_name: str, full_text: str, metadata: Dict[str, Any] = None) -> int:
        """Chunks and stores the text content of a parsed document into ChromaDB."""
        cleaned_text = clean_text(full_text)
        chunks = self._chunk_text(cleaned_text)

        if not chunks:
            logger.warning(f"No text extracted or chunked for document {doc_name}")
            return 0

        ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]
        metadatas = []
        for i in range(len(chunks)):
            meta = {
                "document_id": doc_id,
                "filename": doc_name,
                "chunk_index": i,
                **(metadata or {})
            }
            metadatas.append(meta)

        vector_store.add_texts(
            collection_name=DOCUMENTS_COLLECTION,
            texts=chunks,
            ids=ids,
            metadatas=metadatas
        )

        logger.info(f"Indexed document {doc_name} ({len(chunks)} chunks)")
        return len(chunks)

    def _chunk_text(self, text: str) -> List[str]:
        """Simple sliding window text chunker."""
        words = text.split()
        chunks = []
        i = 0
        while i < len(words):
            chunk_words = words[i:i + self.chunk_size]
            if not chunk_words:
                break
            chunks.append(" ".join(chunk_words))
            i += self.chunk_size - self.chunk_overlap
        return chunks

indexer = IngestionPipeline()
