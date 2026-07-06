"""RESEARCHMINDAI - DOCX Parser"""
from pathlib import Path
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class DOCXParser:
    def parse(self, file_path: str) -> Dict[str, Any]:
        try:
            from docx import Document
        except ImportError:
            raise ImportError("python-docx required: pip install python-docx")

        path = Path(file_path)
        doc = Document(str(path))

        paragraphs = []
        full_text = ""
        for para in doc.paragraphs:
            if para.text.strip():
                paragraphs.append(para.text.strip())
                full_text += para.text + "\n"

        # Extract tables
        tables_text = []
        for table in doc.tables:
            rows = []
            for row in table.rows:
                cells = [cell.text.strip() for cell in row.cells]
                rows.append(" | ".join(cells))
            tables_text.append("\n".join(rows))

        if tables_text:
            full_text += "\n\nTABLES:\n" + "\n\n".join(tables_text)

        word_count = len(full_text.split())
        return {
            "full_text": full_text.strip(),
            "paragraphs": paragraphs,
            "tables": tables_text,
            "word_count": word_count,
            "file_name": path.name,
            "page_count": None,  # DOCX doesn't have fixed pages
        }


docx_parser = DOCXParser()
