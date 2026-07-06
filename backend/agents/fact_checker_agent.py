"""
RESEARCHMINDAI - Fact Checker Agent
"""
from typing import Dict, Any, List
import json
from agents.base_agent import BaseAgent
from langchain_core.messages import SystemMessage, HumanMessage

class FactCheckerAgent(BaseAgent):
    """Detects contradictions, confirms claims, and rates factual consistency across sources."""

    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        query = state.get("query")
        sources = state.get("sources", [])
        logs = state.get("agent_logs", [])
        
        logs.append("Fact Checker Agent: Running cross-source inconsistency checks...")

        if not sources or len(sources) < 2:
            return {
                "contradictions": [],
                "confidence_score": 0.9,
                "agent_logs": logs
            }

        context_str = ""
        for idx, src in enumerate(sources):
            context_str += f"Source [{idx+1}] ({src.get('url')} - {src.get('title')}): {src.get('snippet')}\n\n"

        system_prompt = SystemMessage(content=(
            "You are a rigorous Fact Checker. Your job is to read search snippets and detect contradictions "
            "between different sources. If two sources assert conflicting claims (e.g. source A says 100 people died, "
            "source B says 10 people died), output them. Output only valid JSON inside a codeblock. "
            "JSON structure:\n"
            "[\n"
            "  {\n"
            "    \"claim_a\": \"claim from source A\",\n"
            "    \"claim_b\": \"conflicting claim from source B\",\n"
            "    \"source_a\": \"title or url of source A\",\n"
            "    \"source_b\": \"title or url of source B\",\n"
            "    \"severity\": \"low/medium/high\"\n"
            "  }\n"
            "]\n"
            "If no contradictions are found, output an empty JSON list []."
        ))
        
        human_prompt = HumanMessage(content=f"Context Sources:\n{context_str}\n\nFind contradictions:")

        response = self.llm.invoke([system_prompt, human_prompt])
        resp_text = response.content

        # Clean JSON from LLM output
        contradictions = []
        try:
            cleaned = resp_text.strip()
            if "```json" in cleaned:
                cleaned = cleaned.split("```json")[1].split("```")[0].strip()
            elif "```" in cleaned:
                cleaned = cleaned.split("```")[1].split("```")[0].strip()
            contradictions = json.loads(cleaned)
        except Exception as e:
            logs.append(f"Fact Checker Agent: Failed to parse contradictions ({e}). Defaulting to empty list.")

        # Calculate confidence score
        base_score = 1.0 - (len(contradictions) * 0.15)
        confidence_score = max(0.1, min(1.0, base_score))

        logs.append(f"Fact Checker Agent: Fact check completed. Found {len(contradictions)} contradictions.")

        return {
            "contradictions": contradictions,
            "confidence_score": round(confidence_score, 2),
            "agent_logs": logs
        }

fact_checker_agent = FactCheckerAgent()
