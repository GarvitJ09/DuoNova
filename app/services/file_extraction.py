import io
from typing import Union
import PyPDF2
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
        pdf = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        text = "\n".join(page.extract_text() or "" for page in pdf.pages)
        return text

    @staticmethod
    def _extract_docx(file_bytes: bytes) -> str:
        doc = docx.Document(io.BytesIO(file_bytes))
        text = "\n".join(p.text for p in doc.paragraphs)
        return text
