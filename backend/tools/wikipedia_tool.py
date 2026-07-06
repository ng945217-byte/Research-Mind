"""
RESEARCHMINDAI - Tools: Wikipedia Search & Context Extractor Tool
"""
from typing import List, Dict, Any
import wikipediaapi
import logging

logger = logging.getLogger(__name__)

class WikipediaSearchTool:
    """Wrapper tool for searching and extracting Wikipedia summaries."""

    def __init__(self):
        # We need a proper user agent string for Wikipedia API compliance
        self.wiki = wikipediaapi.Wikipedia(
            user_agent="RESEARCHMINDAI/1.0 (contact@researchmindai.local)",
            language="en"
        )

    def search_and_extract(self, query: str, max_results: int = 3) -> List[Dict[str, Any]]:
        try:
            # First search using Wikipedia Search (via standard API endpoints)
            # Wikipedia-API package doesn't have list search built-in directly in page model.
            # We fetch the exact page if we can match it, or search for potential page names.
            # For simplicity, we split/extract terms from the query to find pages.
            page = self.wiki.page(query)
            if page.exists():
                return [{
                    "title": page.title,
                    "url": page.fullurl,
                    "snippet": page.summary[:1000],  # Get first 1000 chars of summary
                    "source_type": "wikipedia",
                    "relevance_score": 0.95
                }]
            
            # Simple fallback search by matching keywords
            keywords = query.split()
            results = []
            for kw in keywords[:3]:
                if len(kw) < 4:
                    continue
                p = self.wiki.page(kw)
                if p.exists():
                    results.append({
                        "title": p.title,
                        "url": p.fullurl,
                        "snippet": p.summary[:800],
                        "source_type": "wikipedia",
                        "relevance_score": 0.85
                    })
            return results
        except Exception as e:
            logger.error(f"Wikipedia search failed: {e}")
            return []

wikipedia_tool = WikipediaSearchTool()
