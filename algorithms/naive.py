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
    matches: List[int] = []

    n: int = len(text)
    m: int = len(pattern)

    # Edge cases: empty pattern, empty text, or pattern longer than text
    if m == 0 or n == 0 or m > n:
        return matches

    # Slide pattern over text from index 0 to (n - m)
    for i in range(n - m + 1):
        match_found: bool = True

        # Check each character of pattern against text[i + j]
        for j in range(m):
            if text[i + j] != pattern[j]:
                match_found = False
                break  # Mismatch encountered; shift pattern by 1

        if match_found:
            matches.append(i)

    return matches
