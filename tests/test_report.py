"""
Tests for PDF report generation using ReportLab.
"""

import io
import pytest
from utils.report_generator import generate_pdf_report


def test_generate_pdf_report_valid():
    sample_data = {
        "doc1_name": "Original_Paper.docx",
        "doc2_name": "Student_Submission.pdf",
        "similarity_percentage": 42.5,
        "algorithm_name": "Knuth-Morris-Pratt (KMP) Algorithm",
        "execution_time_ms": 3.82,
        "matched_word_count": 85,
        "doc1_word_count": 200,
        "doc2_word_count": 200,
        "matching_sections_count": 4,
        "shingle_size": 5,
        "benchmark": {
            "results": [
                {"name": "Naive Pattern Matching", "execution_time_ms": 8.12},
                {"name": "Rabin-Karp Algorithm", "execution_time_ms": 4.50},
                {"name": "Knuth-Morris-Pratt (KMP)", "execution_time_ms": 3.82}
            ]
        }
    }

    pdf_buffer = generate_pdf_report(sample_data)
    assert isinstance(pdf_buffer, io.BytesIO)
    pdf_bytes = pdf_buffer.getvalue()
    # Check that PDF header is present
    assert pdf_bytes.startswith(b"%PDF")
    assert len(pdf_bytes) > 1000
