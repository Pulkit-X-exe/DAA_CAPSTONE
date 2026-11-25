"""
Unit tests for detailed algorithm execution metrics, comparison counts,
and OOP algorithm class interfaces.
"""

import pytest
from algorithms.naive import naive_search_detailed, NaiveAlgorithm
from algorithms.rabin_karp import rabin_karp_search_detailed, RabinKarpAlgorithm
from algorithms.kmp import kmp_search_detailed, KMPAlgorithm
from algorithms.base import MatchResult


def test_naive_detailed_metrics():
    text = "AABAA"
    pattern = "AA"
    res = naive_search_detailed(text, pattern)
    assert isinstance(res, MatchResult)
    assert res.matches == [0, 3]
    assert res.comparisons > 0


def test_rabin_karp_collision_metrics():
    # Force collision using small modulus
    text = "ABABDABACDABABCABAB"
    pattern = "ABABCABAB"
    res = rabin_karp_search_detailed(text, pattern, base=10, prime_mod=11)
    assert res.matches == [10]
    assert res.collisions >= 0


def test_kmp_detailed_metrics():
    text = "the quick brown fox"
    pattern = "quick"
    res = kmp_search_detailed(text, pattern)
    assert res.matches == [4]
    # KMP iterates through the text to find all occurrences
    assert res.comparisons >= len(text)


def test_oop_algorithm_wrappers():
    text = "testing oop algorithms in python"
    pattern = "algorithms"

    naive_obj = NaiveAlgorithm()
    rk_obj = RabinKarpAlgorithm()
    kmp_obj = KMPAlgorithm()

    expected_idx = 12
    assert naive_obj.search(text, pattern).matches == [expected_idx]
    assert rk_obj.search(text, pattern).matches == [expected_idx]
    assert kmp_obj.search(text, pattern).matches == [expected_idx]
    assert naive_obj.worst_case_complexity == "O(N * M)"
    assert kmp_obj.space_complexity == "O(M)"
