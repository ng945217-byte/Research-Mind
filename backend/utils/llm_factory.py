"""
RESEARCHMINDAI - Utilities: LLM Factory
Supports Gemini and Groq with automatic fallback.
"""
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_core.language_models import BaseChatModel
from config import settings
import logging

logger = logging.getLogger(__name__)


def get_llm(provider: str = None, temperature: float = 0.3) -> BaseChatModel:
    """Return the appropriate LLM instance."""
    provider = provider or settings.default_llm

    if provider == "gemini" and settings.gemini_api_key:
        try:
            return ChatGoogleGenerativeAI(
                model=settings.gemini_model,
                google_api_key=settings.gemini_api_key,
                temperature=temperature,
                convert_system_message_to_human=True,
            )
        except Exception as e:
            logger.warning(f"Gemini init failed: {e}. Falling back to Groq.")

    if settings.groq_api_key:
        try:
            return ChatGroq(
                model=settings.groq_model,
                groq_api_key=settings.groq_api_key,
                temperature=temperature,
            )
        except Exception as e:
            logger.error(f"Groq init failed: {e}")
            raise RuntimeError("No LLM available. Check API keys in .env")

    raise RuntimeError("No LLM configured. Set GEMINI_API_KEY or GROQ_API_KEY in .env")


def get_fast_llm() -> BaseChatModel:
    """Get a fast, lightweight LLM for simple tasks."""
    if settings.groq_api_key:
        return ChatGroq(
            model="llama-3.1-8b-instant",
            groq_api_key=settings.groq_api_key,
            temperature=0.1,
        )
    return get_llm(temperature=0.1)
