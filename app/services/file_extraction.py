import io
from typing import Union  
import pdfplumber
import docx

class FileExtractionService:
    """
    Service for extracting text from PDF and DOCX files.
    """
    @staticmethod
    def extract_text(file_bytes: bytes, file_type: str) -> str:
        if file_type.lower() == '.pdf':
            return FileExtractionService._extract_pdf(file_bytes)
        elif file_type.lower() in ['.docx', '.doc']:
            return FileExtractionService._extract_docx(file_bytes)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

    @staticmethod
    def _extract_pdf(file_bytes: bytes) -> str:
        text_parts = []
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                text_parts.append(page.extract_text() or "")
        return "\n".join(text_parts)

    @staticmethod
    def _extract_docx(file_bytes: bytes) -> str:
        doc = docx.Document(io.BytesIO(file_bytes))
        text_parts = []

        for para in doc.paragraphs:
            text_parts.append(para.text)

        # Hyperlink handling (simple heuristic)
        for rel in doc.part.rels.values():
            if "hyperlink" in rel.reltype:
                link = rel.target_ref
                if link not in "\n".join(text_parts):
                    text_parts.append(f"[LINK] {link}")

        return "\n".join(text_parts)
