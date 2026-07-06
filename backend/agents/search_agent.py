"""
RESEARCHMINDAI - Search Agent (Web Tavily Search)
"""
from typing import Dict, Any
from agents.base_agent import BaseAgent
from tools.tavily_tool import tavily_tool

class SearchAgent(BaseAgent):
    """Responsible for executing internet queries and parsing findings."""

    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        query = state.get("query")
        max_sources = state.get("max_sources", 5)
        
        # Append search status updates
        logs = state.get("agent_logs", [])
        logs.append("Search Agent: Beginning Tavily web search...")

        web_results = tavily_tool.search(query, max_results=max_sources)
        
        sources = state.get("sources", [])
        sources.extend(web_results)

        logs.append(f"Search Agent: Retrieved {len(web_results)} web resources.")

        return {
            "sources": sources,
            "agent_logs": logs
        }

search_agent = SearchAgent()
