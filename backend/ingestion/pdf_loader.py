from typing import List, Dict
from pathlib import Path
from pypdf import PdfReader

def load_pdf(file_path: str) -> List[Dict]:
    """
    Load a PDF file page by page and return raw documents.

    Each page is returned as a dict with text + metadata.
    No chunking, no embeddings here.
    
    """
    
    pdf_path = Path(file_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {file_path}")

    reader = PdfReader(str(pdf_path))

    documents: List[Dict] = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()

        if not text or not text.strip():
            continue  

        documents.append(
            {
                "text": text,
                "metadata": {
                    "source": "pdf",
                    "file_name": pdf_path.name,
                    "page_number": page_number,
                },
            }
        )

    return documents
