from pathlib import Path

from pypdf import PdfReader


def extract_pdf_text(path: str | Path) -> str:
    reader = PdfReader(str(path))
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(pages).strip()


def split_text(text: str, chunk_size: int = 4000) -> list[str]:
    return [text[index : index + chunk_size] for index in range(0, len(text), chunk_size)]
