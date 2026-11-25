"""
Tests for file handler and text extraction from various formats.
"""

import io
import pytest
from utils.file_handler import allowed_file, extract_text_from_txt, process_uploaded_document
from werkzeug.datastructures import FileStorage


def test_allowed_file():
    assert allowed_file("document.txt") is True
    assert allowed_file("research.pdf") is True
    assert allowed_file("assignment.docx") is True
    assert allowed_file("ASSIGNMENT.DOCX") is True
    assert allowed_file("script.py") is False
    assert allowed_file("image.png") is False
    assert allowed_file("no_extension") is False
    assert allowed_file("") is False


def test_extract_text_from_txt():
    content = b"This is a test plain text document for PlagScan."
    file_obj = io.BytesIO(content)
    text = extract_text_from_txt(file_obj)
    assert text == "This is a test plain text document for PlagScan."


def test_process_uploaded_document_textarea_fallback():
    text, source, err = process_uploaded_document(None, fallback_text="Direct input text sample")
    assert err is None
    assert text == "Direct input text sample"
    assert source == "Direct Input"


def test_process_uploaded_document_empty():
    text, source, err = process_uploaded_document(None, fallback_text="")
    assert text is None
    assert "No document or text" in err


def test_process_uploaded_document_file_txt():
    storage = FileStorage(
        stream=io.BytesIO(b"Sample file content"),
        filename="test.txt",
        content_type="text/plain"
    )
    text, source, err = process_uploaded_document(storage)
    assert err is None
    assert text == "Sample file content"
    assert source == "test.txt"
