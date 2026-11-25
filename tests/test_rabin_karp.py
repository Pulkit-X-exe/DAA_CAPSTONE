"""
Tests for Rabin-Karp String Matching Algorithm.
Covers:
- Standard single and multiple occurrences
- No match
- Exact match
- Empty inputs
- Pattern longer than text
- Overlapping matches
- Collision handling verification (small modulus)
- Special characters and spaces
"""

import pytest
from algorithms.rabin_karp import rabin_karp_search


def test_rabin_karp_basic_match():
    text = "the quick brown fox jumps over the lazy dog"
    pattern = "the"
    assert rabin_karp_search(text, pattern) == [0, 31]


def test_rabin_karp_no_match():
    text = "hello world"
    pattern = "python"
    assert rabin_karp_search(text, pattern) == []


def test_rabin_karp_exact_match():
    text = "algorithm"
    pattern = "algorithm"
    assert rabin_karp_search(text, pattern) == [0]


def test_rabin_karp_empty_inputs():
    assert rabin_karp_search("", "abc") == []
    assert rabin_karp_search("abc", "") == []
    assert rabin_karp_search("", "") == []


def test_rabin_karp_pattern_longer_than_text():
    assert rabin_karp_search("short", "longer_pattern") == []


def test_rabin_karp_overlapping_matches():
    text = "AAAAAA"
    pattern = "AAA"
    assert rabin_karp_search(text, pattern) == [0, 1, 2, 3]


def test_rabin_karp_collision_handling():
    # Force frequent collisions by using a tiny prime modulus (e.g. 11)
    # The algorithm must still produce 100% correct matches due to character verification
    text = "ABABDABACDABABCABAB"
    pattern = "ABABCABAB"
    result = rabin_karp_search(text, pattern, base=10, prime_mod=11)
    assert result == [10]


def test_rabin_karp_special_characters_and_spaces():
    text = "rolling hash is O(N + M) average time!"
    pattern = "O(N + M)"
    assert rabin_karp_search(text, pattern) == [16]
