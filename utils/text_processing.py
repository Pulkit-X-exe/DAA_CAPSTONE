"""
Text Preprocessing Utilities for PlagScan.

Performs:
- Normalization (case-folding, whitespace cleanup, safe punctuation handling)
- Word tokenization
- Configurable word shingling (k-grams of words)
"""

import re
from typing import List, Tuple, Dict, Any


def normalize_text(text: str) -> str:
    """
    Normalizes text for fair comparison:
    - Lowercases all characters
    - Normalizes all whitespace (spaces, tabs, newlines) to single spaces
    - Strips leading and trailing whitespace
    """
    if not text:
        return ""
    # Convert to lowercase
    normalized = text.lower()
    # Replace multiple whitespace characters with a single space
    normalized = re.sub(r"\s+", " ", normalized)
    return normalized.strip()


def tokenize_words(text: str) -> List[str]:
    """
    Splits normalized text into word tokens using whitespace and basic punctuation boundaries.
    """
    if not text:
        return []
    # Extract alphanumeric words and basic punctuation-free tokens
    return [word for word in re.findall(r"\b\w+\b", text.lower()) if word]


def generate_word_shingles(tokens: List[str], k: int = 5) -> List[Dict[str, Any]]:
    """
    Generates k-word shingles (consecutive sequences of k words) with their
    token boundary indices.

    If the document has fewer than k tokens but at least 1 token,
    a single shingle containing all tokens is produced.

    Args:
        tokens (List[str]): List of word tokens.
        k (int): Number of words per shingle (default 5).

    Returns:
        List[Dict[str, Any]]: List of dicts with:
            - 'shingle': The string of words joined by space
            - 'start_token': 0-based start token index
            - 'end_token': 0-based end token index (inclusive)
    """
    shingles: List[Dict[str, Any]] = []
    n: int = len(tokens)

    if n == 0:
        return shingles

    # Fallback for short documents with fewer words than k
    effective_k = min(k, n)
    if effective_k <= 0:
        return shingles

    for i in range(n - effective_k + 1):
        window_words = tokens[i : i + effective_k]
        shingle_text = " ".join(window_words)
        shingles.append({
            "shingle": shingle_text,
            "start_token": i,
            "end_token": i + effective_k - 1,
            "length": effective_k
        })

    return shingles
