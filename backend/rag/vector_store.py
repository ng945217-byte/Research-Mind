"""
RESEARCHMINDAI - RAG: ChromaDB Vector Store
"""
import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict, Any, Optional
from pathlib import Path
from config import settings
import logging

logger = logging.getLogger(__name__)


class VectorStore:
    """ChromaDB-backed vector store for research and document embeddings."""

    def __init__(self):
        self._client: Optional[chromadb.PersistentClient] = None

    def get_client(self) -> chromadb.PersistentClient:
        if self._client is None:
            persist_dir = Path(settings.chroma_persist_dir).resolve()
            persist_dir.mkdir(parents=True, exist_ok=True)
            self._client = chromadb.PersistentClient(
                path=str(persist_dir),
                settings=ChromaSettings(anonymized_telemetry=False),
            )
            logger.info(f"ChromaDB initialized at: {persist_dir}")
        return self._client

    def get_collection(self, name: str):
        client = self.get_client()
        return client.get_or_create_collection(
            name=name,
            metadata={"hnsw:space": "cosine"},
        )

    def add_texts(
        self,
        collection_name: str,
        texts: List[str],
        ids: List[str],
        metadatas: Optional[List[Dict]] = None,
    ):
        """Add text documents to a collection."""
        collection = self.get_collection(collection_name)
        collection.add(
            documents=texts,
            ids=ids,
            metadatas=metadatas or [{} for _ in texts],
        )
        logger.info(f"Added {len(texts)} docs to collection '{collection_name}'")

    def query(
        self,
        collection_name: str,
        query_text: str,
        n_results: int = 5,
        where: Optional[Dict] = None,
    ) -> List[Dict[str, Any]]:
        """Query collection for similar documents."""
        collection = self.get_collection(collection_name)
        results = collection.query(
            query_texts=[query_text],
            n_results=n_results,
            where=where,
        )
        items = []
        if results["documents"] and results["documents"][0]:
            for i, doc in enumerate(results["documents"][0]):
                items.append({
                    "text": doc,
                    "id": results["ids"][0][i],
                    "distance": results["distances"][0][i] if results.get("distances") else None,
                    "metadata": results["metadatas"][0][i] if results.get("metadatas") else {},
                })
        return items

    def delete_collection(self, collection_name: str):
        client = self.get_client()
        try:
            client.delete_collection(collection_name)
        except Exception as e:
            logger.warning(f"Could not delete collection {collection_name}: {e}")

    def list_collections(self) -> List[str]:
        client = self.get_client()
        return [c.name for c in client.list_collections()]


# Singleton
vector_store = VectorStore()

# Collection names
RESEARCH_COLLECTION = "research_results"
DOCUMENTS_COLLECTION = "uploaded_documents"
MEMORY_COLLECTION = "memory_entries"
