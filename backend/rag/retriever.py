"""
RESEARCHMINDAI - RAG: Hybrid Retriever and Re-ranker
"""
from typing import List, Dict, Any, Optional
from rank_bm25 import BM25Okapi
import re
from rag.vector_store import vector_store, DOCUMENTS_COLLECTION, RESEARCH_COLLECTION
import logging

logger = logging.getLogger(__name__)

class HybridRetriever:
    """Combines Dense similarity search (ChromaDB) with Sparse keyword search (BM25)."""

    def retrieve(
        self,
        query: str,
        collection_name: str,
        n_results: int = 5,
        where: Optional[Dict] = None,
    ) -> List[Dict[str, Any]]:
        # 1. Retrieve dense candidates from ChromaDB
        dense_results = vector_store.query(
            collection_name=collection_name,
            query_text=query,
            n_results=n_results * 2,  # retrieve more for re-ranking
            where=where
        )

        if not dense_results:
            return []

        # 2. Extract docs and prepare BM25
        corpus = [doc["text"] for doc in dense_results]
        tokenized_corpus = [self._tokenize(doc) for doc in corpus]

        if not tokenized_corpus or len(tokenized_corpus) == 0:
            return dense_results[:n_results]

        bm25 = BM25Okapi(tokenized_corpus)
        tokenized_query = self._tokenize(query)

        # 3. Compute BM25 scores
        bm25_scores = bm25.get_scores(tokenized_query)

        # 4. RRF (Reciprocal Rank Fusion) or hybrid scoring
        # We'll normalize scores and combine them
        hybrid_results = []
        for idx, doc in enumerate(dense_results):
            # Dense score = 1 - distance (since ChromaDB returns cosine distance for cosine space)
            distance = doc.get("distance")
            dense_score = (1.0 - distance) if distance is not None else 0.5
            
            # Sparse score = BM25 score
            sparse_score = bm25_scores[idx] if idx < len(bm25_scores) else 0.0

            # Combined score (weighted average)
            combined_score = (0.7 * dense_score) + (0.3 * (sparse_score / (max(bm25_scores) + 1e-9)))

            hybrid_results.append({
                "text": doc["text"],
                "id": doc["id"],
                "metadata": doc["metadata"],
                "score": round(float(combined_score), 4)
            })

        # Sort by combined score descending
        hybrid_results.sort(key=lambda x: x["score"], reverse=True)
        return hybrid_results[:n_results]

    def _tokenize(self, text: str) -> List[str]:
        """Simple tokenizer."""
        return re.findall(r'\b\w+\b', text.lower())

hybrid_retriever = HybridRetriever()
