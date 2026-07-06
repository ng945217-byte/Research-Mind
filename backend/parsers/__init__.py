"""RESEARCHMINDAI - Parsers __init__"""
from .pdf_parser import pdf_parser
from .docx_parser import docx_parser
from .pptx_parser import pptx_parser
from .txt_csv_parser import txt_parser, csv_parser
from pathlib import Path
from typing import Dict, Any


def parse_document(file_path: str, apply_ocr: bool = False) -> Dict[str, Any]:
    """Universal document parser — routes by file extension."""
    ext = Path(file_path).suffix.lower()
    if ext == ".pdf":
        return pdf_parser.parse(file_path, apply_ocr=apply_ocr)
    elif ext == ".docx":
        return docx_parser.parse(file_path)
    elif ext in (".pptx", ".ppt"):
        return pptx_parser.parse(file_path)
    elif ext == ".txt":
        return txt_parser.parse(file_path)
    elif ext == ".csv":
        return csv_parser.parse(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")


SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".pptx", ".ppt", ".txt", ".csv"}

__all__ = ["parse_document", "SUPPORTED_EXTENSIONS"]
