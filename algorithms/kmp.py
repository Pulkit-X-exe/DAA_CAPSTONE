"""
Knuth-Morris-Pratt (KMP) String Matching Algorithm.

DAA Concept:
The KMP algorithm optimizes string matching by eliminating unnecessary
backtracking in the target text. When a character mismatch occurs, the algorithm
knows previous characters already matched and uses the precomputed LPS array
(Longest Proper Prefix which is also a Suffix) to skip forward in the pattern.

LPS Array Principle:
For pattern P of length M:
LPS[i] = the length of the longest proper prefix of P[0..i] that matches
a proper suffix of P[0..i].

Complexity Analysis:
- Preprocessing Time: O(M) to construct the LPS array.
- Search Time: O(N) — text pointer 'i' never decreases or backtracks.
- Total Time Complexity: O(N + M) guaranteed in all cases (best, average, worst).
- Auxiliary Space: O(M) to store the LPS array.
"""

from typing import List
from algorithms.base import StringMatchingAlgorithm, MatchResult


def compute_lps_array(pattern: str) -> List[int]:
    """
    Computes the LPS (Longest Proper Prefix that is also Suffix) array for pattern.
    """
    m: int = len(pattern)
    lps: List[int] = [0] * m

    length: int = 0
    i: int = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps


def kmp_search(text: str, pattern: str) -> List[int]:
    """
    Finds all 0-based starting indices where 'pattern' occurs in 'text'
    using the Knuth-Morris-Pratt (KMP) algorithm.
    """
    res = kmp_search_detailed(text, pattern)
    return res.matches


def kmp_search_detailed(text: str, pattern: str) -> MatchResult:
    """
    Detailed KMP search returning match indices, comparisons count, and execution stats.
    """
    matches: List[int] = []
    comparisons: int = 0

    n: int = len(text)
    m: int = len(pattern)

    if m == 0 or n == 0 or m > n:
        return MatchResult(
            algorithm_name="Knuth-Morris-Pratt (KMP)",
            matches=matches,
            comparisons=0
        )

    lps: List[int] = compute_lps_array(pattern)

    i: int = 0  # text index
    j: int = 0  # pattern index

    while i < n:
        comparisons += 1
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == m:
            matches.append(i - j)
            j = lps[j - 1]
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return MatchResult(
        algorithm_name="Knuth-Morris-Pratt (KMP)",
        matches=matches,
        comparisons=comparisons
    )


class KMPAlgorithm(StringMatchingAlgorithm):
    """Object-oriented wrapper implementing StringMatchingAlgorithm interface."""

    @property
    def name(self) -> str:
        return "Knuth-Morris-Pratt (KMP)"

    @property
    def worst_case_complexity(self) -> str:
        return "O(N + M)"

    @property
    def space_complexity(self) -> str:
        return "O(M)"

    def search(self, text: str, pattern: str) -> MatchResult:
        return kmp_search_detailed(text, pattern)
