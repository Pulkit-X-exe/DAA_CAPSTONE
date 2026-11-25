"""
Unit tests for similarity calculation and comparison service.
"""

import pytest
from utils.similarity import calculate_similarity_metrics, merge_token_intervals, generate_highlighted_html
from services.comparison_service import compare_documents


def test_calculate_similarity_metrics():
    doc1 = ["apple", "banana", "cherry"]
    doc2 = ["apple", "banana", "orange", "grape"]
    matched_indices = {0, 1}  # apple, banana matched (2 out of 4)
    metrics = calculate_similarity_metrics(doc1, doc2, matched_indices)
    assert metrics["doc1_word_count"] == 3
    assert metrics["doc2_word_count"] == 4
    assert metrics["matched_word_count"] == 2
    assert metrics["similarity_percentage"] == 50.0


def test_merge_token_intervals():
    indices = {0, 1, 2, 5, 6, 9}
    intervals = merge_token_intervals(indices)
    assert intervals == [(0, 2), (5, 6), (9, 9)]
    assert merge_token_intervals(set()) == []


def test_generate_highlighted_html():
    raw = "hello world python programming"
    tokens = ["hello", "world", "python", "programming"]
    ranges = [(1, 2)]  # "world python" matched
    html_output = generate_highlighted_html(raw, ranges, tokens)
    assert '<mark class="match-highlight">world python </mark>' in html_output
    assert "hello" in html_output


def test_compare_documents_identical():
    text = "Design and Analysis of Algorithms capstone project plagiarism detection system."
    result = compare_documents(text, text, algorithm_key="kmp", shingle_size=4)
    assert result["similarity_percentage"] == 100.0
    assert result["matched_word_count"] == result["doc2_word_count"]
    assert result["matching_sections_count"] >= 1


def test_compare_documents_completely_different():
    doc1 = "The solar system consists of the Sun and planetary bodies orbiting it."
    doc2 = "Quantum computing uses qubits and quantum superposition for calculation."
    result = compare_documents(doc1, doc2, algorithm_key="naive", shingle_size=3)
    assert result["similarity_percentage"] == 0.0
    assert result["matched_word_count"] == 0
    assert result["matching_sections_count"] == 0


def test_compare_documents_partial_match():
    doc1 = "Artificial intelligence and machine learning are revolutionizing modern computer science."
    doc2 = "Modern computer science has been transformed because artificial intelligence and machine learning are revolutionizing data."
    result = compare_documents(doc1, doc2, algorithm_key="rabin_karp", shingle_size=4)
    assert 0.0 < result["similarity_percentage"] < 100.0
    assert result["matched_word_count"] > 0
