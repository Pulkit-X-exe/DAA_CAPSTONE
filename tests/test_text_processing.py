"""
Unit tests for text processing utilities.
"""

import pytest
from utils.text_processing import normalize_text, tokenize_words, generate_word_shingles, auto_select_shingle_size


def test_auto_select_shingle_size():
    assert auto_select_shingle_size(5) == 2
    assert auto_select_shingle_size(25) == 3
    assert auto_select_shingle_size(100) == 5
    assert auto_select_shingle_size(500) == 6



def test_normalize_text():
    raw = "  Hello,   WORLD!\n\tThis is a   TEST.  "
    expected = "hello, world! this is a test."
    assert normalize_text(raw) == expected
    assert normalize_text("") == ""


def test_tokenize_words():
    text = "Data Structures & Algorithms in Python 2026!"
    tokens = tokenize_words(text)
    assert tokens == ["data", "structures", "algorithms", "in", "python", "2026"]
    assert tokenize_words("") == []


def test_generate_word_shingles():
    tokens = ["the", "quick", "brown", "fox", "jumps", "over", "the", "lazy", "dog"]
    shingles = generate_word_shingles(tokens, k=4)
    # n = 9, k = 4 -> 9 - 4 + 1 = 6 shingles
    assert len(shingles) == 6
    assert shingles[0]["shingle"] == "the quick brown fox"
    assert shingles[0]["start_token"] == 0
    assert shingles[0]["end_token"] == 3
    assert shingles[-1]["shingle"] == "over the lazy dog"


def test_generate_word_shingles_short_document():
    tokens = ["just", "two", "words"]
    shingles = generate_word_shingles(tokens, k=5)
    # k > n -> single shingle containing all tokens
    assert len(shingles) == 1
    assert shingles[0]["shingle"] == "just two words"
    assert shingles[0]["start_token"] == 0
    assert shingles[0]["end_token"] == 2
