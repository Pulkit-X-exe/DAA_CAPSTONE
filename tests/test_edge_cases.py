"""
Comprehensive Edge Case and Equivalence Test Suite for PlagScan.

Tests:
1. Cross-algorithm matching equivalence (Naive == Rabin-Karp == KMP)
2. Empty and whitespace-only inputs
3. Single word / single character documents
4. Pathological worst-case patterns (e.g. repeated prefixes)
5. Repeated words and shingle boundary edge cases
6. Case sensitivity and irregular whitespace normalization
7. Large documents within limits
"""

import pytest
from algorithms.naive import naive_search
from algorithms.rabin_karp import rabin_karp_search
from algorithms.kmp import kmp_search
from services.comparison_service import compare_documents


def test_cross_algorithm_equivalence():
    """All 3 algorithms MUST return identical match positions on the same inputs."""
    test_cases = [
        ("the quick brown fox jumps over the lazy dog", "the"),
        ("AAAAABAAAAABAAAAAB", "AAAAB"),
        ("banana", "ana"),
        ("algorithm analysis and design", "design"),
        ("no matching pattern here", "python"),
        ("xyz", "xyz"),
        ("repeating words words words words", "words words")
    ]

    for text, pattern in test_cases:
        naive_res = naive_search(text, pattern)
        rk_res = rabin_karp_search(text, pattern)
        kmp_res = kmp_search(text, pattern)

        assert naive_res == rk_res == kmp_res, (
            f"Algorithm discrepancy on text='{text}', pattern='{pattern}':\n"
            f"Naive: {naive_res}, RK: {rk_res}, KMP: {kmp_res}"
        )


def test_empty_and_whitespace_documents():
    res = compare_documents("", "", algorithm_key="kmp")
    assert res["similarity_percentage"] == 0.0
    assert res["matched_word_count"] == 0

    res2 = compare_documents("   \n\t  ", "   ", algorithm_key="naive")
    assert res2["similarity_percentage"] == 0.0


def test_single_word_documents():
    res = compare_documents("Algorithm", "Algorithm", algorithm_key="rabin_karp", shingle_size=5)
    assert res["similarity_percentage"] == 100.0
    assert res["matched_word_count"] == 1

    res_diff = compare_documents("Algorithm", "DataStructure", algorithm_key="kmp", shingle_size=5)
    assert res_diff["similarity_percentage"] == 0.0


def test_repeated_words_shingle_overlap():
    text1 = "data data data data data data data"
    text2 = "data data data data data"
    res = compare_documents(text1, text2, algorithm_key="kmp", shingle_size=3)
    assert res["similarity_percentage"] == 100.0
    assert res["matched_word_count"] == 5


def test_case_and_whitespace_insensitivity():
    doc1 = "Knuth-Morris-Pratt Algorithm Is Efficient!"
    doc2 = "  knuth-morris-pratt   algorithm   is   efficient!  "
    res = compare_documents(doc1, doc2, algorithm_key="kmp", shingle_size=4)
    assert res["similarity_percentage"] == 100.0


def test_pathological_worst_case_comparison():
    doc1 = "A" * 500 + "B"
    doc2 = "A" * 500 + "B"
    res = compare_documents(doc1, doc2, algorithm_key="kmp", shingle_size=2)
    assert res["similarity_percentage"] == 100.0
