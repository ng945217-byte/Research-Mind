"""
RESEARCHMINDAI - Helper Utilities
"""
import uuid
import re
from collections import Counter
from typing import List


def generate_id() -> str:
    return str(uuid.uuid4())


def truncate_text(text: str, max_chars: int = 2000) -> str:
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "..."


def extract_keywords_simple(text: str, top_n: int = 15) -> List[str]:
    """Simple keyword extraction using word frequency (no ML required)."""
    stop_words = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to",
        "for", "of", "with", "by", "is", "are", "was", "were", "be",
        "been", "being", "have", "has", "had", "do", "does", "did",
        "will", "would", "could", "should", "may", "might", "shall",
        "this", "that", "these", "those", "it", "its", "they", "them",
        "their", "we", "our", "you", "your", "he", "she", "his", "her",
        "from", "as", "into", "about", "which", "who", "what", "how",
        "when", "where", "not", "no", "also", "can", "more", "than",
    }
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
    filtered = [w for w in words if w not in stop_words]
    most_common = Counter(filtered).most_common(top_n)
    return [word for word, _ in most_common]


def clean_text(text: str) -> str:
    """Remove excessive whitespace and special chars."""
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    return text.strip()


def calculate_confidence(sources_count: int, contradictions_count: int) -> float:
    """Estimate confidence score based on source count and contradictions."""
    base = min(0.5 + (sources_count * 0.05), 0.9)
    penalty = contradictions_count * 0.05
    return round(max(0.1, base - penalty), 2)
