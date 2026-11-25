"""
Document Comparison Service for PlagScan.

Coordinates:
- Text normalization and tokenization of both documents
- Shingle generation
- Execution of selected string matching algorithm (Naive, Rabin-Karp, or KMP)
- Finding matches of shingles in the target document
- Highlighting matched sections
- Returning comprehensive comparison results
"""

import time
from typing import Dict, Any, List, Set, Tuple

from algorithms.naive import naive_search
from algorithms.rabin_karp import rabin_karp_search
from algorithms.kmp import kmp_search
from utils.text_processing import normalize_text, tokenize_words, generate_word_shingles
from utils.similarity import calculate_similarity_metrics, merge_token_intervals, generate_highlighted_html


ALGORITHM_MAP = {
    "naive": ("Naive Pattern Matching", naive_search),
    "rabin_karp": ("Rabin-Karp Algorithm", rabin_karp_search),
    "kmp": ("Knuth-Morris-Pratt (KMP) Algorithm", kmp_search),
}


def compare_documents(
    doc1_text: str,
    doc2_text: str,
    algorithm_key: str = "kmp",
    shingle_size: int = 5
) -> Dict[str, Any]:
    """
    Compares doc2 (Compared Document) against doc1 (Original Reference Document)
    using the specified algorithm.

    Args:
        doc1_text (str): Reference / Original document raw text.
        doc2_text (str): Suspect / Compared document raw text.
        algorithm_key (str): 'naive', 'rabin_karp', or 'kmp'.
        shingle_size (int): Shingle window size in words (default 5).

    Returns:
        Dict[str, Any]: Detailed comparison result dictionary.
    """
    algo_name, algo_fn = ALGORITHM_MAP.get(
        algorithm_key.lower(),
        ("Knuth-Morris-Pratt (KMP) Algorithm", kmp_search)
    )

    # Step 1: Preprocess and tokenize both documents (outside timed matching)
    norm_doc1 = normalize_text(doc1_text)
    norm_doc2 = normalize_text(doc2_text)

    tokens_doc1 = tokenize_words(norm_doc1)
    tokens_doc2 = tokenize_words(norm_doc2)

    # Shingles from compared document to check against original document
    shingles_doc2 = generate_word_shingles(tokens_doc2, k=shingle_size)

    # Search target text is the space-joined tokens of doc1
    search_target_text = " ".join(tokens_doc1)

    matched_doc2_token_indices: Set[int] = set()
    matched_sections_snippets: List[str] = []

    # Step 2: Time ONLY the string matching algorithm execution for fair benchmarking
    start_time = time.perf_counter()

    for item in shingles_doc2:
        pattern = item["shingle"]
        # Execute the chosen DAA string-matching algorithm
        match_positions = algo_fn(search_target_text, pattern)

        if match_positions:
            # Record matching token indices in doc2 (prevent duplicate counting)
            for t_idx in range(item["start_token"], item["end_token"] + 1):
                matched_doc2_token_indices.add(t_idx)

            if len(matched_sections_snippets) < 50:  # store up to 50 sample snippets
                matched_sections_snippets.append(pattern)

    execution_time_sec = time.perf_counter() - start_time
    execution_time_ms = round(execution_time_sec * 1000.0, 3)

    # Step 3: Compute similarity metrics
    metrics = calculate_similarity_metrics(tokens_doc1, tokens_doc2, matched_doc2_token_indices)

    # Step 4: Group matched tokens into contiguous sections
    doc2_merged_intervals = merge_token_intervals(matched_doc2_token_indices)

    # Also detect matching token positions in doc1 for highlighting doc1
    matched_doc1_token_indices: Set[int] = set()
    shingles_doc1 = generate_word_shingles(tokens_doc1, k=shingle_size)
    search_target_doc2 = " ".join(tokens_doc2)

    for item in shingles_doc1:
        if algo_fn(search_target_doc2, item["shingle"]):
            for t_idx in range(item["start_token"], item["end_token"] + 1):
                matched_doc1_token_indices.add(t_idx)

    doc1_merged_intervals = merge_token_intervals(matched_doc1_token_indices)

    # Step 5: Generate safe HTML highlights for both documents
    highlighted_doc1 = generate_highlighted_html(doc1_text, doc1_merged_intervals, tokens_doc1)
    highlighted_doc2 = generate_highlighted_html(doc2_text, doc2_merged_intervals, tokens_doc2)

    # Deduplicate matching snippets for display
    unique_snippets = list(dict.fromkeys(matched_sections_snippets))

    return {
        "algorithm_key": algorithm_key,
        "algorithm_name": algo_name,
        "shingle_size": shingle_size,
        "doc1_word_count": metrics["doc1_word_count"],
        "doc2_word_count": metrics["doc2_word_count"],
        "matched_word_count": metrics["matched_word_count"],
        "similarity_percentage": metrics["similarity_percentage"],
        "matching_sections_count": len(doc2_merged_intervals),
        "matched_snippets": unique_snippets[:20],  # Top 20 distinct matched snippets
        "highlighted_doc1": highlighted_doc1,
        "highlighted_doc2": highlighted_doc2,
        "execution_time_ms": execution_time_ms
    }
