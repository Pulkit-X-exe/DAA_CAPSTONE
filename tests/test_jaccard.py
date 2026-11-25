"""
Unit tests for Jaccard and containment metrics.
"""

import pytest
from utils.jaccard import jaccard_similarity, containment_index, compute_all_metrics


def test_jaccard_identical_sets():
    s = {"apple", "banana", "cherry"}
    assert jaccard_similarity(s, s) == 100.0


def test_jaccard_disjoint_sets():
    s1 = {"apple", "banana"}
    s2 = {"cat", "dog"}
    assert jaccard_similarity(s1, s2) == 0.0


def test_jaccard_partial_overlap():
    s1 = {"a", "b", "c"}
    s2 = {"b", "c", "d"}
    # intersection = 2, union = 4 -> 50%
    assert jaccard_similarity(s1, s2) == 50.0


def test_containment_index():
    ref = {"a", "b", "c", "d", "e"}
    suspect = {"b", "c"}
    # All of suspect is contained in ref -> 100%
    assert containment_index(ref, suspect) == 100.0


def test_compute_all_metrics():
    s1 = {"w1", "w2", "w3"}
    s2 = {"w2", "w3", "w4", "w5"}
    res = compute_all_metrics(s1, s2)
    assert res["jaccard"] == 40.0
    assert res["containment"] == 50.0
    assert res["overlap"] == 66.67
