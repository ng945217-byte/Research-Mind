"""
RESEARCHMINDAI - Wikipedia Agent
"""
from typing import Dict, Any
from agents.base_agent import BaseAgent
from tools.wikipedia_tool import wikipedia_tool

class WikipediaAgent(BaseAgent):
    """Responsible for searching and fetching content from Wikipedia."""

    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        query = state.get("query")
        
        logs = state.get("agent_logs", [])
        logs.append("Wikipedia Agent: Querying Wikipedia API...")

        wiki_results = wikipedia_tool.search_and_extract(query, max_results=3)

        sources = state.get("sources", [])
        sources.extend(wiki_results)

        logs.append(f"Wikipedia Agent: Extracted Wikipedia context for query.")

        return {
            "sources": sources,
            "agent_logs": logs
        }

wikipedia_agent = WikipediaAgent()
