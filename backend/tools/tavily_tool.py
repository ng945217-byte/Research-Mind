"""
RESEARCHMINDAI - Tools: Tavily Web Search Tool
"""
from typing import List, Dict, Any, Optional
from tavily import TavilyClient
from config import settings
import logging

logger = logging.getLogger(__name__)

class TavilySearchTool:
    """Wrapper tool for internet search using Tavily API."""

    def __init__(self):
        self.client = None
        if settings.tavily_api_key:
            self.client = TavilyClient(api_key=settings.tavily_api_key)

    def search(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        if not self.client:
            logger.warning("Tavily API key missing. Returning mock web search results.")
            return self._mock_search(query)

        try:
            response = self.client.search(
                query=query,
                search_depth="advanced",
                max_results=max_results,
                include_raw_content=False,
                include_images=False
            )
            results = []
            for item in response.get("results", []):
                results.append({
                    "title": item.get("title", "No Title"),
                    "url": item.get("url"),
                    "snippet": item.get("content", ""),
                    "source_type": "web",
                    "relevance_score": item.get("score", 0.8)
                })
            return results
        except Exception as e:
            logger.error(f"Tavily search failed: {e}")
            return self._mock_search(query)

    def _mock_search(self, query: str) -> List[Dict[str, Any]]:
        """Mock results fallback if API fails or key is missing."""
        return [
            {
                "title": f"Web resource on: {query}",
                "url": "https://example.com/research-results",
                "snippet": f"This is a simulated search result for query '{query}' summarizing primary online discussions.",
                "source_type": "web",
                "relevance_score": 0.5
            }
        ]

tavily_tool = TavilySearchTool()
