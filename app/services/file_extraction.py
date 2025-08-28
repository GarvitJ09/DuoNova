import io
import re
from typing import Union  
import fitz   # from PyMuPDF
import docx   # from python-docx


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
        """Extract PDF text with improved formatting and structure preservation."""
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        text_parts = []

        for page_num, page in enumerate(doc):
            # Try multiple extraction methods for best results
            
            # Method 1: Simple text extraction (most reliable)
            simple_text = page.get_text()
            
            # Method 2: Block-based extraction for better structure
            blocks = page.get_text("blocks")
            block_text = []
            for block in blocks:
                if len(block) >= 5 and block[4].strip():  # block[4] is text content
                    block_text.append(block[4].strip())
            
            # Choose the better extraction
            if len(simple_text.strip()) > len(" ".join(block_text).strip()):
                page_text = simple_text
            else:
                page_text = "\n".join(block_text)
            
            # Clean up the text
            page_text = FileExtractionService._clean_text(page_text)
            
            if page_text.strip():
                text_parts.append(page_text)

        final_text = "\n\n".join(text_parts)
        return FileExtractionService._post_process_text(final_text)

    @staticmethod
    def _clean_text(text: str) -> str:
        """Clean and normalize extracted text."""
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Fix broken words (common in PDF extraction)
        text = re.sub(r'(\w)-\s+(\w)', r'\1\2', text)
        
        # Ensure proper line breaks for sections
        text = re.sub(r'\s*(PROFILE|EXPERIENCE|EDUCATION|SKILLS|PROJECTS|ACHIEVEMENTS|CONTACT)\s*', r'\n\n\1\n', text, flags=re.IGNORECASE)
        
        return text.strip()

    @staticmethod
    def _post_process_text(text: str) -> str:
        """Final post-processing of extracted text."""
        if not text:
            return ""
        
        # Split into lines and clean each line
        lines = []
        for line in text.split('\n'):
            line = line.strip()
            if line and len(line) > 1:  # Skip very short lines that are likely artifacts
                lines.append(line)
        
        # Join with single newlines and normalize spacing
        result = '\n'.join(lines)
        
        # Fix multiple consecutive newlines
        result = re.sub(r'\n\s*\n\s*\n+', '\n\n', result)
        
        return result.strip()

    @staticmethod
    def _extract_docx(file_bytes: bytes) -> str:
        """Extract text from DOCX with hyperlinks inline."""
        doc = docx.Document(io.BytesIO(file_bytes))
        text_parts = []

        # Normal paragraphs
        for para in doc.paragraphs:
            text_parts.append(para.text)

        # Insert hyperlinks inline
        for rel in doc.part.rels.values():
            if "hyperlink" in rel.reltype:
                link = rel.target_ref
                if link not in "\n".join(text_parts):
                    text_parts.append(f"[LINK] {link}")

        return "\n".join(text_parts)

    @staticmethod
    def extract_entities(text: str) -> dict:
        """Extract emails, phones, and links from raw text."""
        emails = re.findall(r"[\w\.-]+@[\w\.-]+\.\w+", text)
        phones = re.findall(r"\+?\d[\d\s-]{7,15}", text)
        links  = re.findall(r"https?://[^\s]+", text)

        return {
            "raw_text": text,
            "emails": list(set(emails)),
            "phones": list(set(phones)),
            "links": list(set(links))
        }

