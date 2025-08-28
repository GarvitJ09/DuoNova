import io
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
        """Extract PDF text with hyperlinks inline by mapping links to nearest words/lines."""
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        text_parts = []

        for page in doc:
            words = page.get_text("words")  # [x0, y0, x1, y1, "word", block, line, word_no]
            links = [l for l in page.get_links() if l.get("uri")]
            words_sorted = sorted(words, key=lambda w: (w[6], w[0]))  # sort by line, then x

            line_map = {}  # line_no -> [words...]
            for w in words_sorted:
                _, _, _, _, word, _, line_no, _ = w
                line_map.setdefault(line_no, []).append(word)

            # Build text lines
            page_lines = {}
            for line_no, ws in line_map.items():
                page_lines[line_no] = " ".join(ws)

            # Attach links to nearest line
            for l in links:
                uri = l["uri"]
                lx1, ly1, lx2, ly2 = l["from"]

                # Find words inside link bbox
                linked_words = [w for w in words if lx1 <= w[0] <= lx2 and ly1 <= w[1] <= ly2]
                if linked_words:
                    line_no = linked_words[0][6]
                    page_lines[line_no] += f" ({uri})"
                else:
                    # No word inside → attach to closest previous line
                    closest_line = max(page_lines.keys())
                    page_lines[closest_line] += f" ({uri})"

            # Merge lines in order
            ordered_text = "\n".join([page_lines[k] for k in sorted(page_lines.keys())])
            text_parts.append(ordered_text)

        return "\n".join(text_parts)

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

