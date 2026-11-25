"""
Similarity Calculation and Text Highlighting Engine.

Calculates:
- Unique matched word token sets (preventing duplicate matches from inflating score)
- Clean, bounded similarity percentage
- Merged matching section intervals
- Safe HTML highlight generation for both original and compared documents
"""

import html
from typing import List, Set, Tuple, Dict, Any, Callable


def calculate_similarity_metrics(
    doc1_tokens: List[str],
    doc2_tokens: List[str],
    matched_doc2_token_indices: Set[int]
) -> Dict[str, Any]:
    """
    Calculates plagiarism / similarity metrics.

    Formula:
    Similarity % = (Unique Matched Word Count in Compared Doc / Total Words in Compared Doc) * 100

    This metric measures the proportion of the compared document that appears
    in the original document (containment measure), strictly bounded between 0% and 100%.

    Args:
        doc1_tokens: Tokens in original document.
        doc2_tokens: Tokens in compared document.
        matched_doc2_token_indices: Set of unique token indices in doc2 that were matched.

    Returns:
        Dict with similarity metrics.
    """
    total_doc1_words = len(doc1_tokens)
    total_doc2_words = len(doc2_tokens)
    matched_words_count = len(matched_doc2_token_indices)

    if total_doc2_words == 0:
        similarity_percentage = 0.0
    else:
        raw_pct = (matched_words_count / total_doc2_words) * 100.0
        similarity_percentage = round(min(100.0, max(0.0, raw_pct)), 2)

    return {
        "doc1_word_count": total_doc1_words,
        "doc2_word_count": total_doc2_words,
        "matched_word_count": matched_words_count,
        "similarity_percentage": similarity_percentage
    }


def merge_token_intervals(token_indices: Set[int]) -> List[Tuple[int, int]]:
    """
    Converts a set of individual token indices into merged contiguous [start, end] intervals.
    Example: {0, 1, 2, 5, 6, 7} -> [(0, 2), (5, 7)]
    """
    if not token_indices:
        return []

    sorted_indices = sorted(token_indices)
    intervals: List[Tuple[int, int]] = []

    start = sorted_indices[0]
    prev = sorted_indices[0]

    for idx in sorted_indices[1:]:
        if idx == prev + 1:
            prev = idx
        else:
            intervals.append((start, prev))
            start = idx
            prev = idx

    intervals.append((start, prev))
    return intervals


def generate_highlighted_html(raw_text: str, matched_token_ranges: List[Tuple[int, int]], tokens: List[str]) -> str:
    """
    Generates safe HTML markup displaying text with matching sections wrapped in <mark> tags.
    All user text is escaped using html.escape to guarantee security against XSS.

    Args:
        raw_text: Original raw input string.
        matched_token_ranges: List of (start_token_idx, end_token_idx) inclusive.
        tokens: Tokenized words of raw_text.

    Returns:
        Safe HTML string with <mark class="match-highlight">...</mark> tags.
    """
    if not tokens or not raw_text.strip():
        return html.escape(raw_text)

    # If no matches, return plain escaped text
    if not matched_token_ranges:
        return html.escape(raw_text)

    # Build set of matched indices
    matched_indices: Set[int] = set()
    for start, end in matched_token_ranges:
        for i in range(start, end + 1):
            matched_indices.add(i)

    # Construct highlighted token representation
    output_parts: List[str] = []
    in_mark = False

    for idx, token in enumerate(tokens):
        is_matched = idx in matched_indices

        if is_matched and not in_mark:
            output_parts.append('<mark class="match-highlight">')
            in_mark = True
        elif not is_matched and in_mark:
            output_parts.append('</mark>')
            in_mark = False

        output_parts.append(html.escape(token))
        output_parts.append(" ")

    if in_mark:
        output_parts.append('</mark>')

    return "".join(output_parts).strip()
