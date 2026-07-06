"""
RESEARCHMINDAI - PDF Parser (PyMuPDF + optional OCR)
"""
import fitz  # PyMuPDF
from pathlib import Path
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class PDFParser:
    """Parse PDF files: text extraction with optional OCR fallback."""

    def parse(self, file_path: str, apply_ocr: bool = False) -> Dict[str, Any]:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"PDF not found: {file_path}")

        doc = fitz.open(str(path))
        pages_text: List[str] = []
        full_text = ""
        page_count = doc.page_count

        for page_num in range(page_count):
            page = doc[page_num]
            text = page.get_text("text")

            # If page has very little text and OCR is requested, try OCR
            if len(text.strip()) < 50 and apply_ocr:
                text = self._ocr_page(page)

            pages_text.append(text)
            full_text += text + "\n\n"

        doc.close()

        word_count = len(full_text.split())
        return {
            "full_text": full_text.strip(),
            "pages": pages_text,
            "page_count": page_count,
            "word_count": word_count,
            "file_name": path.name,
            "ocr_applied": apply_ocr,
        }

    def _ocr_page(self, page) -> str:
        """Attempt OCR on a page using pytesseract."""
        try:
            import pytesseract
            from PIL import Image
            import io

            mat = fitz.Matrix(2, 2)  # 2x zoom for better OCR
            pix = page.get_pixmap(matrix=mat)
            img_bytes = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_bytes))
            return pytesseract.image_to_string(img)
        except Exception as e:
            logger.warning(f"OCR failed for page: {e}")
            return ""


pdf_parser = PDFParser()
