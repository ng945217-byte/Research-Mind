"""
RESEARCHMINDAI - Base Agent
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from utils.llm_factory import get_llm
from langchain_core.language_models import BaseChatModel

class BaseAgent(ABC):
    """Abstract base agent providing common LLM initialization and helper patterns."""

    def __init__(self, provider: str = None, temperature: float = 0.3):
        self.llm: BaseChatModel = get_llm(provider=provider, temperature=temperature)

    @abstractmethod
    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent logic given the current Graph/Session state."""
        pass
