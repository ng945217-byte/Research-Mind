"""RESEARCHMINDAI - PPTX Parser"""
from pathlib import Path
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class PPTXParser:
    def parse(self, file_path: str) -> Dict[str, Any]:
        try:
            from pptx import Presentation
        except ImportError:
            raise ImportError("python-pptx required: pip install python-pptx")

        path = Path(file_path)
        prs = Presentation(str(path))

        slides_text: List[str] = []
        full_text = ""

        for i, slide in enumerate(prs.slides):
            slide_content = f"--- Slide {i+1} ---\n"
            for shape in slide.shapes:
                if hasattr(shape, "text") and shape.text.strip():
                    slide_content += shape.text + "\n"
            # Speaker notes
            if slide.has_notes_slide:
                notes = slide.notes_slide.notes_text_frame.text
                if notes.strip():
                    slide_content += f"[Notes: {notes}]\n"
            slides_text.append(slide_content)
            full_text += slide_content + "\n"

        word_count = len(full_text.split())
        return {
            "full_text": full_text.strip(),
            "slides": slides_text,
            "slide_count": len(prs.slides),
            "word_count": word_count,
            "file_name": path.name,
            "page_count": len(prs.slides),
        }


pptx_parser = PPTXParser()
