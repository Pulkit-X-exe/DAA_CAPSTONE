"""
File Handler and Document Parser Utility for PlagScan.

Supports:
- Safe filename sanitization
- Extension validation (txt, pdf, docx)
- Text extraction from Plain Text (UTF-8 / Latin-1)
- Text extraction from Adobe PDF via pypdf
- Text extraction from Microsoft Word (.docx) via python-docx
- File size validation and descriptive error reporting
"""

import os
from typing import Tuple, Optional
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import pypdf
import docx

ALLOWED_EXTENSIONS = {"txt", "pdf", "docx"}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16 MB


def allowed_file(filename: str) -> bool:
    """Checks if the uploaded file has a supported extension."""
    if not filename or "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in ALLOWED_EXTENSIONS


def extract_text_from_txt(file_obj) -> str:
    """Extracts text from a plain text file stream."""
    raw_data = file_obj.read()
    if isinstance(raw_data, str):
        return raw_data
    # Attempt UTF-8 first, fallback to latin-1 with error replacement
    try:
        return raw_data.decode("utf-8")
    except UnicodeDecodeError:
        return raw_data.decode("latin-1", errors="replace")


def extract_text_from_pdf(file_obj) -> str:
    """Extracts text from a PDF file stream using pypdf."""
    text_chunks = []
    reader = pypdf.PdfReader(file_obj)
    for page_idx, page in enumerate(reader.pages):
        page_text = page.extract_text()
        if page_text:
            text_chunks.append(page_text)
    return "\n".join(text_chunks)


def extract_text_from_docx(file_obj) -> str:
    """Extracts text from a DOCX document using python-docx."""
    doc = docx.Document(file_obj)
    text_chunks = []
    # Extract from paragraphs
    for para in doc.paragraphs:
        if para.text.strip():
            text_chunks.append(para.text)
    # Extract from tables
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                if cell.text.strip():
                    text_chunks.append(cell.text)
    return "\n".join(text_chunks)


def process_uploaded_document(file_item: Optional[FileStorage], fallback_text: Optional[str] = None) -> Tuple[Optional[str], str, Optional[str]]:
    """
    Validates and extracts plain text from an uploaded file or direct text area input.

    Args:
        file_item: FileStorage object from request.files
        fallback_text: Direct raw string from a textarea if provided

    Returns:
        Tuple: (extracted_text, filename_or_source, error_message)
    """
    # Case 1: File was uploaded
    if file_item and file_item.filename:
        filename = secure_filename(file_item.filename)
        if not filename or not allowed_file(filename):
            return None, filename, f"Unsupported file type for '{filename}'. Allowed: .txt, .pdf, .docx"

        # Check file length if seekable
        file_item.seek(0, os.SEEK_END)
        size = file_item.tell()
        file_item.seek(0)

        if size > MAX_FILE_SIZE:
            return None, filename, f"File '{filename}' exceeds maximum allowed size of 16MB."

        if size == 0:
            return None, filename, f"File '{filename}' is empty (0 bytes)."

        ext = filename.rsplit(".", 1)[1].lower()
        try:
            if ext == "txt":
                text = extract_text_from_txt(file_item)
            elif ext == "pdf":
                text = extract_text_from_pdf(file_item)
            elif ext == "docx":
                text = extract_text_from_docx(file_item)
            else:
                return None, filename, f"Unknown format: {ext}"
        except Exception as e:
            return None, filename, f"Error reading '{filename}': {str(e)}"

        if not text or not text.strip():
            return None, filename, f"File '{filename}' does not contain extractable text."

        return text.strip(), filename, None

    # Case 2: Direct text input from UI textarea
    if fallback_text and fallback_text.strip():
        return fallback_text.strip(), "Direct Input", None

    return None, "None", "No document or text was provided."
