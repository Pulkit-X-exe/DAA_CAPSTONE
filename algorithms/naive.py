"""
Naive Pattern Matching Algorithm.

DAA Concept:
Brute-force algorithmic paradigm. Slides the pattern of length M over
the text of length N, checking character by character at every possible
alignment position from 0 up to (N - M).

Complexity Analysis:
- Best Case Time: O(N) — when the first character of pattern doesn't match text at all.
- Worst Case Time: O((N - M + 1) * M) -> O(N * M) — when all characters match except the last,
  e.g., text = "AAAAAAAAAB", pattern = "AAAB".
- Average Case Time: O(N) for random natural language alphabets.
- Auxiliary Space: O(1) — strictly constant extra memory.
"""

from typing import List
from algorithms.base import StringMatchingAlgorithm, MatchResult


def naive_search(text: str, pattern: str) -> List[int]:
    """
    Finds all 0-based starting indices where 'pattern' occurs in 'text'
    using the brute-force Naive string matching approach.

    Args:
        text (str): The document or target text to search within.
        pattern (str): The query pattern/shingle to search for.

    Returns:
        List[int]: List of starting indices where pattern matches text.
    """
    res = naive_search_detailed(text, pattern)
    return res.matches


def naive_search_detailed(text: str, pattern: str) -> MatchResult:
    """
    Finds matches with detailed character comparison counting for DAA analysis.
    """
    matches: List[int] = []
    comparisons: int = 0

    n: int = len(text)
    m: int = len(pattern)

    if m == 0 or n == 0 or m > n:
        return MatchResult(algorithm_name="Naive Pattern Matching", matches=matches, comparisons=0)

    for i in range(n - m + 1):
        match_found: bool = True
        for j in range(m):
            comparisons += 1
            if text[i + j] != pattern[j]:
                match_found = False
                break

        if match_found:
            matches.append(i)

    return MatchResult(
        algorithm_name="Naive Pattern Matching",
        matches=matches,
        comparisons=comparisons
    )


class NaiveAlgorithm(StringMatchingAlgorithm):
    """Object-oriented wrapper implementing StringMatchingAlgorithm interface."""

    @property
    def name(self) -> str:
        return "Naive Pattern Matching"

    @property
    def worst_case_complexity(self) -> str:
        return "O(N * M)"

    @property
    def space_complexity(self) -> str:
        return "O(1)"

    def search(self, text: str, pattern: str) -> MatchResult:
        return naive_search_detailed(text, pattern)
