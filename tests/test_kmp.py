"""
Tests for Knuth-Morris-Pratt (KMP) String Matching Algorithm.
Covers:
- LPS array calculation accuracy
- Standard single and multiple occurrences
- No match
- Exact match
- Empty inputs
- Pattern longer than text
- Overlapping matches
- Classical repetitive patterns (e.g., "AAAA")
- Special characters and punctuation
"""

import pytest
from algorithms.kmp import compute_lps_array, kmp_search


def test_compute_lps_array():
    assert compute_lps_array("A") == [0]
    assert compute_lps_array("AA") == [0, 1]
    assert compute_lps_array("AAA") == [0, 1, 2]
    assert compute_lps_array("ABABC") == [0, 0, 1, 2, 0]
    assert compute_lps_array("ABCDABD") == [0, 0, 0, 0, 1, 2, 0]


def test_kmp_basic_match():
    text = "the quick brown fox jumps over the lazy dog"
    pattern = "the"
    assert kmp_search(text, pattern) == [0, 31]


def test_kmp_no_match():
    text = "hello world"
    pattern = "python"
    assert kmp_search(text, pattern) == []


def test_kmp_exact_match():
    text = "algorithm"
    pattern = "algorithm"
    assert kmp_search(text, pattern) == [0]


def test_kmp_empty_inputs():
    assert kmp_search("", "abc") == []
    assert kmp_search("abc", "") == []
    assert kmp_search("", "") == []


def test_kmp_pattern_longer_than_text():
    assert kmp_search("short", "longer_pattern") == []


def test_kmp_overlapping_matches():
    text = "AAAAAA"
    pattern = "AAA"
    assert kmp_search(text, pattern) == [0, 1, 2, 3]


def test_kmp_complex_backtrack_avoidance():
    text = "ABABDABACDABABCABAB"
    pattern = "ABABCABAB"
    assert kmp_search(text, pattern) == [10]


def test_kmp_special_characters_and_spaces():
    text = "kmp deterministic O(N + M) complexity!"
    pattern = "O(N + M)"
    assert kmp_search(text, pattern) == [18]
