"""
Tests for Naive String Matching Algorithm.
Covers:
- Standard single and multiple occurrences
- No match
- Pattern equals text
- Empty pattern and empty text
- Pattern longer than text
- Overlapping patterns (e.g. "AAAA" in "AAAAAA")
- Case sensitivity and special characters/spaces
"""

import pytest
from algorithms.naive import naive_search


def test_naive_basic_match():
    text = "the quick brown fox jumps over the lazy dog"
    pattern = "the"
    assert naive_search(text, pattern) == [0, 31]


def test_naive_no_match():
    text = "hello world"
    pattern = "python"
    assert naive_search(text, pattern) == []


def test_naive_exact_match():
    text = "algorithm"
    pattern = "algorithm"
    assert naive_search(text, pattern) == [0]


def test_naive_empty_inputs():
    assert naive_search("", "abc") == []
    assert naive_search("abc", "") == []
    assert naive_search("", "") == []


def test_naive_pattern_longer_than_text():
    assert naive_search("short", "longer_pattern") == []


def test_naive_overlapping_matches():
    text = "AAAAAA"
    pattern = "AAA"
    # Overlapping occurrences at indices 0, 1, 2, 3
    assert naive_search(text, pattern) == [0, 1, 2, 3]


def test_naive_worst_case_pattern():
    # Canonical worst case: repeated matching prefix followed by mismatch
    text = "AAAAAAAAAAAAAAAAAB"
    pattern = "AAAAB"
    assert naive_search(text, pattern) == [13]


def test_naive_special_characters_and_spaces():
    text = "data structures & algorithms in python!"
    pattern = "& algorithms"
    assert naive_search(text, pattern) == [16]
