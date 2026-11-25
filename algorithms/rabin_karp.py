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

from typing import List, Tuple, Optional


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
    matches: List[int] = []

    n: int = len(text)
    m: int = len(pattern)

    # Edge cases
    if m == 0 or n == 0 or m > n:
        return matches

    # h is the multiplier for the most significant character: (base^(m-1)) % prime_mod
    h: int = 1
    for _ in range(m - 1):
        h = (h * base) % prime_mod

    pattern_hash: int = 0
    window_hash: int = 0

    # Calculate initial hash for pattern and first window of text
    for i in range(m):
        pattern_hash = (pattern_hash * base + ord(pattern[i])) % prime_mod
        window_hash = (window_hash * base + ord(text[i])) % prime_mod

    # Slide the window over the text
    for i in range(n - m + 1):
        # When hash values match, verify character by character to handle collisions
        if pattern_hash == window_hash:
            match_found: bool = True
            for j in range(m):
                if text[i + j] != pattern[j]:
                    match_found = False
                    break  # Spurious hit / hash collision!
            if match_found:
                matches.append(i)

        # Compute rolling hash for the next window if not at the end
        if i < n - m:
            # Remove leading character, shift left (multiply by base), and add trailing character
            window_hash = (base * (window_hash - ord(text[i]) * h) + ord(text[i + m])) % prime_mod

            # Handle negative result in modulo arithmetic
            if window_hash < 0:
                window_hash += prime_mod

    return matches
