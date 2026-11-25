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
Example for "ABABC":
- Substring "A" -> prefix: "", suffix: "" -> LPS[0] = 0
- Substring "AB" -> LPS[1] = 0
- Substring "ABA" -> prefix "A" matches suffix "A" -> LPS[2] = 1
- Substring "ABAB" -> prefix "AB" matches suffix "AB" -> LPS[3] = 2
- Substring "ABABC" -> LPS[4] = 0

Complexity Analysis:
- Preprocessing Time: O(M) to construct the LPS array.
- Search Time: O(N) — text pointer 'i' never decreases or backtracks.
- Total Time Complexity: O(N + M) guaranteed in all cases (best, average, worst).
- Auxiliary Space: O(M) to store the LPS array.
"""

from typing import List


def compute_lps_array(pattern: str) -> List[int]:
    """
    Computes the LPS (Longest Proper Prefix that is also Suffix) array for pattern.

    Args:
        pattern (str): The pattern string.

    Returns:
        List[int]: The LPS array of size len(pattern).
    """
    m: int = len(pattern)
    lps: List[int] = [0] * m

    # Length of the previous longest prefix suffix
    length: int = 0
    i: int = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                # Fall back to the previous prefix length without incrementing i
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps


def kmp_search(text: str, pattern: str) -> List[int]:
    """
    Finds all 0-based starting indices where 'pattern' occurs in 'text'
    using the Knuth-Morris-Pratt (KMP) algorithm.

    Args:
        text (str): The text document to search within.
        pattern (str): The query pattern to search for.

    Returns:
        List[int]: List of match start indices.
    """
    matches: List[int] = []

    n: int = len(text)
    m: int = len(pattern)

    # Edge cases: empty pattern, empty text, or pattern longer than text
    if m == 0 or n == 0 or m > n:
        return matches

    # Step 1: Precompute LPS array in O(m) time
    lps: List[int] = compute_lps_array(pattern)

    # Step 2: Search through text in O(n) time
    i: int = 0  # index for text
    j: int = 0  # index for pattern

    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == m:
            # Full match found starting at index (i - j)
            matches.append(i - j)
            # Use LPS to find next potential match without resetting i
            j = lps[j - 1]
        elif i < n and pattern[j] != text[i]:
            # Mismatch after j matches
            if j != 0:
                # Shift pattern by consulting LPS array (do NOT decrement i)
                j = lps[j - 1]
            else:
                # First character mismatch, advance text pointer
                i += 1

    return matches
