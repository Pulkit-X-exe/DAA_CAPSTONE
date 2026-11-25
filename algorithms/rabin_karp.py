"""
Rabin-Karp String Matching Algorithm (Rolling Hash).

DAA Concept:
Instead of comparing characters at every position, Rabin-Karp computes
a numerical hash value of the pattern and a sliding window of the text.
Only when window_hash == pattern_hash does it perform a character-by-character
verification to confirm the match and eliminate spurious hits (hash collisions).

Rolling Hash Principle:
Calculating the hash of a new window takes O(1) time by:
1. Subtracting the leading character's weighted value: (old_hash - text[i] * h)
2. Multiplying by the base: * base
3. Adding the new trailing character: + text[i + m]
4. Taking modulo q to prevent large integer growth.

Complexity Analysis:
- Preprocessing Time: O(M) to compute initial hashes of pattern and first window.
- Average Case Matching: O(N + M) under uniform hashing with minimal collisions.
- Worst Case Matching: O(N * M) if every window causes a hash collision.
- Auxiliary Space: O(1).
"""

from typing import List
from algorithms.base import StringMatchingAlgorithm, MatchResult


def rabin_karp_search(
    text: str,
    pattern: str,
    base: int = 256,
    prime_mod: int = 1000000007
) -> List[int]:
    """
    Finds all 0-based starting indices where 'pattern' occurs in 'text'
    using the Rabin-Karp algorithm with rolling hash.

    Args:
        text (str): The document text.
        pattern (str): The pattern to search for.
        base (int): Alphabet size / radix base (default 256 for ASCII).
        prime_mod (int): Large prime modulus to reduce collisions (default 10^9 + 7).

    Returns:
        List[int]: List of match start indices.
    """
    res = rabin_karp_search_detailed(text, pattern, base, prime_mod)
    return res.matches


def rabin_karp_search_detailed(
    text: str,
    pattern: str,
    base: int = 256,
    prime_mod: int = 1000000007
) -> MatchResult:
    """
    Detailed Rabin-Karp search returning match indices, character comparisons,
    and spurious hit (hash collision) counts.
    """
    matches: List[int] = []
    comparisons: int = 0
    collisions: int = 0

    n: int = len(text)
    m: int = len(pattern)

    if m == 0 or n == 0 or m > n:
        return MatchResult(
            algorithm_name="Rabin-Karp Rolling Hash",
            matches=matches,
            comparisons=0,
            collisions=0
        )

    # h = (base^(m-1)) % prime_mod
    h: int = 1
    for _ in range(m - 1):
        h = (h * base) % prime_mod

    pattern_hash: int = 0
    window_hash: int = 0

    for i in range(m):
        pattern_hash = (pattern_hash * base + ord(pattern[i])) % prime_mod
        window_hash = (window_hash * base + ord(text[i])) % prime_mod

    for i in range(n - m + 1):
        if pattern_hash == window_hash:
            match_found: bool = True
            for j in range(m):
                comparisons += 1
                if text[i + j] != pattern[j]:
                    match_found = False
                    collisions += 1  # Spurious hit / hash collision!
                    break
            if match_found:
                matches.append(i)

        if i < n - m:
            window_hash = (base * (window_hash - ord(text[i]) * h) + ord(text[i + m])) % prime_mod
            if window_hash < 0:
                window_hash += prime_mod

    return MatchResult(
        algorithm_name="Rabin-Karp Rolling Hash",
        matches=matches,
        comparisons=comparisons,
        collisions=collisions
    )


class RabinKarpAlgorithm(StringMatchingAlgorithm):
    """Object-oriented wrapper implementing StringMatchingAlgorithm interface."""

    def __init__(self, base: int = 256, prime_mod: int = 1000000007):
        self.base = base
        self.prime_mod = prime_mod

    @property
    def name(self) -> str:
        return "Rabin-Karp Rolling Hash"

    @property
    def worst_case_complexity(self) -> str:
        return "O(N * M)"

    @property
    def space_complexity(self) -> str:
        return "O(1)"

    def search(self, text: str, pattern: str) -> MatchResult:
        return rabin_karp_search_detailed(text, pattern, self.base, self.prime_mod)
