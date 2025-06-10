"""
Extract raw text from PDF or DOCX résumé.
"""

from pathlib import Path
import docx
from pdfminer.high_level import extract_text


def parse_resume(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(path)

    match path.suffix.lower():
        case ".pdf":
            return extract_text(str(path))
        case ".docx" | ".doc":
            return "\n".join(p.text for p in docx.Document(str(path)).paragraphs)
        case _:
            raise ValueError("Unsupported résumé format")