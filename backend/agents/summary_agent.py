"""
RESEARCHMINDAI - Summary Agent
"""
from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from utils.helpers import extract_keywords_simple
from langchain_core.messages import SystemMessage, HumanMessage

class SummaryAgent(BaseAgent):
    """Produces concise or deep summaries based on context sources."""

    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        query = state.get("query")
        sources = state.get("sources", [])
        logs = state.get("agent_logs", [])
        
        logs.append("Summary Agent: Synthesizing information...")

        if not sources:
            return {
                "summary": "No search sources available to summarize.",
                "keywords": [],
                "agent_logs": logs
            }

        # Build context
        context_str = ""
        for idx, src in enumerate(sources):
            context_str += f"[{idx+1}] Title: {src.get('title')}\nContent: {src.get('snippet')}\n\n"

        system_msg = SystemMessage(
            content=(
                "You are an expert summaries generator. Synthesize the provided sources into a high-quality, "
                "accurate, and informative summary answering the original query. Highlight key facts and structure "
                "the text with headings/bullet points as appropriate. Keep the output professional and objective."
            )
        )
        human_msg = HumanMessage(
            content=f"Query: {query}\n\nSources:\n{context_str}\n\nGenerated Summary:"
        )

        response = self.llm.invoke([system_msg, human_msg])
        summary_text = response.content

        # Extracted keywords
        keywords = extract_keywords_simple(summary_text, top_n=10)

        logs.append("Summary Agent: Summary synthesized.")

        return {
            "summary": summary_text,
            "keywords": keywords,
            "agent_logs": logs
        }

summary_agent = SummaryAgent()
