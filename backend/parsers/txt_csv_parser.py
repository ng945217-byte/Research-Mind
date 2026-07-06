"""RESEARCHMINDAI - TXT & CSV Parsers"""
from pathlib import Path
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class TXTParser:
    def parse(self, file_path: str) -> Dict[str, Any]:
        path = Path(file_path)
        with open(str(path), "r", encoding="utf-8", errors="ignore") as f:
            full_text = f.read()
        return {
            "full_text": full_text.strip(),
            "word_count": len(full_text.split()),
            "file_name": path.name,
            "page_count": None,
        }


class CSVParser:
    def parse(self, file_path: str) -> Dict[str, Any]:
        import pandas as pd
        path = Path(file_path)
        df = pd.read_csv(str(path))

        # Convert to text representation
        summary_lines = [
            f"CSV File: {path.name}",
            f"Rows: {len(df)}, Columns: {len(df.columns)}",
            f"Column Names: {', '.join(df.columns.tolist())}",
            "",
            "First 10 rows:",
            df.head(10).to_string(index=False),
            "",
            "Statistical Summary:",
            df.describe().to_string(),
        ]
        full_text = "\n".join(summary_lines)

        return {
            "full_text": full_text,
            "word_count": len(full_text.split()),
            "file_name": path.name,
            "page_count": None,
            "rows": len(df),
            "columns": df.columns.tolist(),
            "preview": df.head(10).to_dict(orient="records"),
        }


txt_parser = TXTParser()
csv_parser = CSVParser()
