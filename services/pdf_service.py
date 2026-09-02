from pypdf import PdfReader
from io import BytesIO

def extract_and_chunk_pdf(file_bytes: bytes, chunk_size: int = 1000) -> list[str]:
    reader = PdfReader(BytesIO(file_bytes))
    full_text = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += text + "\n"
            
    chunks = [full_text[i:i+chunk_size] for i in range(0, len(full_text), chunk_size)]
    return chunks