"""
RESEARCHMINDAI - LangGraph Agent Orchestration
"""
from typing import Dict, Any, List, TypedDict, Optional
import json
import logging
from datetime import datetime

from langgraph.graph import StateGraph, START, END
from langchain_core.messages import SystemMessage, HumanMessage

from agents.search_agent import search_agent
from agents.wikipedia_agent import wikipedia_agent
from agents.fact_checker_agent import fact_checker_agent
from agents.summary_agent import summary_agent
from utils.llm_factory import get_llm

logger = logging.getLogger(__name__)

# ─── Research State Definition ────────────────────────────────────────────────

class ResearchState(TypedDict):
    query: str
    mode: str  # "quick" | "deep"
    include_web: bool
    include_wikipedia: bool
    max_sources: int
    sources: List[Dict[str, Any]]
    contradictions: List[Dict[str, Any]]
    confidence_score: float
    summary: str
    deep_summary: str
    timeline: List[Dict[str, Any]]
    technical_analysis: str
    beginner_explanation: str
    expert_explanation: str
    future_predictions: str
    conclusions: str
    entities: List[str]
    sentiment: str
    agent_logs: List[str]

# ─── Node Definitions ─────────────────────────────────────────────────────────

def web_search_node(state: ResearchState) -> Dict[str, Any]:
    """Execute Web Search Agent if include_web is enabled."""
    if not state.get("include_web", True):
        logs = state.get("agent_logs", [])
        logs.append("Search Agent: Web search disabled, skipping.")
        return {"agent_logs": logs}
    
    return search_agent.run(state)


def wikipedia_node(state: ResearchState) -> Dict[str, Any]:
    """Execute Wikipedia Agent if include_wikipedia is enabled."""
    if not state.get("include_wikipedia", True):
        logs = state.get("agent_logs", [])
        logs.append("Wikipedia Agent: Wikipedia search disabled, skipping.")
        return {"agent_logs": logs}
        
    return wikipedia_agent.run(state)


def fact_checker_node(state: ResearchState) -> Dict[str, Any]:
    """Execute Fact Checker Agent to identify source contradictions."""
    # Runs the fact checker agent
    return fact_checker_agent.run(state)


def quick_summary_node(state: ResearchState) -> Dict[str, Any]:
    """Generate quick summary and keywords."""
    return summary_agent.run(state)


def deep_writer_node(state: ResearchState) -> Dict[str, Any]:
    """Generate comprehensive analysis, structured perspectives, and timeline."""
    query = state.get("query")
    sources = state.get("sources", [])
    contradictions = state.get("contradictions", [])
    logs = state.get("agent_logs", [])
    
    logs.append("Deep Writer Agent: Executing advanced synthesis, perspectives, and timeline extraction...")
    
    if not sources:
        logs.append("Deep Writer Agent: No sources available. Exiting.")
        return {
            "deep_summary": "No sources retrieved to perform deep writing analysis.",
            "agent_logs": logs
        }
        
    context_str = ""
    for idx, src in enumerate(sources):
        context_str += f"Source [{idx+1}] ({src.get('title') or 'No Title'}): {src.get('snippet') or ''}\n\n"
        
    contradictions_str = json.dumps(contradictions, indent=2)

    # Instantiate LLM for structured deep generation
    llm = get_llm(temperature=0.4)
    
    system_prompt = SystemMessage(content=(
        "You are an Elite Research Writer. Your task is to analyze the provided sources and contradictions "
        "and generate a highly detailed analysis of the topic. You must output a JSON object containing the "
        "following keys:\n"
        "1. \"deep_summary\": A multi-paragraph, authoritative summary synthesizing all data.\n"
        "2. \"technical_analysis\": Detailed breakdown of technical mechanisms, underlying logic, or methodologies.\n"
        "3. \"beginner_explanation\": A simple, conceptual ELI5 (Explain Like I'm 5) explanation.\n"
        "4. \"expert_explanation\": An advanced, professional-grade analysis with deep insights.\n"
        "5. \"future_predictions\": Trends, developments, or outlook for this topic over the next 3-5 years.\n"
        "6. \"conclusions\": Final takeaways and synthesis.\n"
        "7. \"entities\": A list of key organizations, persons, concepts, or technologies mentioned.\n"
        "8. \"sentiment\": A string indicating general sentiment: \"positive\", \"negative\", or \"neutral\".\n"
        "9. \"timeline\": A list of chronological event objects, where each object has: \n"
        "   - \"date\": \"Year/Date of event\",\n"
        "   - \"event\": \"Short title/description of the event\",\n"
        "   - \"significance\": \"Why this event matters in the history/lifecycle of this topic\".\n"
        "\n"
        "Ensure your response is valid JSON enclosed in a ```json ``` codeblock. Make all textual sections detailed."
    ))
    
    human_prompt = HumanMessage(content=(
        f"Research Query: {query}\n\n"
        f"Sources:\n{context_str}\n\n"
        f"Known Contradictions:\n{contradictions_str}\n\n"
        "Generate JSON Report:"
    ))
    
    try:
        response = llm.invoke([system_prompt, human_prompt])
        resp_text = response.content
        
        cleaned = resp_text.strip()
        if "```json" in cleaned:
            cleaned = cleaned.split("```json")[1].split("```")[0].strip()
        elif "```" in cleaned:
            cleaned = cleaned.split("```")[1].split("```")[0].strip()
            
        data = json.loads(cleaned)
        
        logs.append("Deep Writer Agent: Successfully generated deep perspectives and chronological timeline.")
        return {
            "deep_summary": data.get("deep_summary", ""),
            "technical_analysis": data.get("technical_analysis", ""),
            "beginner_explanation": data.get("beginner_explanation", ""),
            "expert_explanation": data.get("expert_explanation", ""),
            "future_predictions": data.get("future_predictions", ""),
            "conclusions": data.get("conclusions", ""),
            "entities": data.get("entities", []),
            "sentiment": data.get("sentiment", "neutral"),
            "timeline": data.get("timeline", []),
            "agent_logs": logs
        }
        
    except Exception as e:
        logger.error(f"Deep Writer Node failed: {e}")
        logs.append(f"Deep Writer Agent: Failed to generate structured JSON ({e}). Fallback to standard summary.")
        return {
            "deep_summary": "Failed to compile deep analysis due to generation error.",
            "agent_logs": logs
        }

# ─── Routing Logic ────────────────────────────────────────────────────────────

def route_by_mode(state: ResearchState) -> str:
    """Choose the final node depending on whether this is a quick or deep research session."""
    if state.get("mode") == "deep":
        return "deep_writer"
    return "quick_summary"

# ─── Graph Construction ────────────────────────────────────────────────────────

workflow = StateGraph(ResearchState)

# Add Nodes
workflow.add_node("web_search", web_search_node)
workflow.add_node("wikipedia", wikipedia_node)
workflow.add_node("fact_checker", fact_checker_node)
workflow.add_node("quick_summary", quick_summary_node)
workflow.add_node("deep_writer", deep_writer_node)

# Set Entry Point
workflow.add_edge(START, "web_search")

# Sequential flow for research gathering and checking
workflow.add_edge("web_search", "wikipedia")
workflow.add_edge("wikipedia", "fact_checker")

# Conditional Router after fact checking
workflow.add_conditional_edges(
    "fact_checker",
    route_by_mode,
    {
        "quick_summary": "quick_summary",
        "deep_writer": "deep_writer"
    }
)

# Connect Terminals
workflow.add_edge("quick_summary", END)
workflow.add_edge("deep_writer", END)

# Compile Graph
research_graph = workflow.compile()
