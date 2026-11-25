"""
Algorithm Benchmarking Service for PlagScan.

Benchmarks Naive, Rabin-Karp, and KMP on IDENTICAL preprocessed inputs
to provide a strictly fair empirical comparison of their execution times.
"""

import time
from typing import Dict, Any, List
from algorithms.naive import naive_search
from algorithms.rabin_karp import rabin_karp_search
from algorithms.kmp import kmp_search
from utils.text_processing import normalize_text, tokenize_words, generate_word_shingles


def run_algorithm_benchmark(doc1_text: str, doc2_text: str, shingle_size: int = 5) -> Dict[str, Any]:
    """
    Executes all three algorithms on the exact same text and shingles,
    measuring execution time with time.perf_counter().

    Preprocessing is performed ONCE outside the timed block so that
    only the pure string matching algorithmic performance is measured.
    """
    norm_doc1 = normalize_text(doc1_text)
    norm_doc2 = normalize_text(doc2_text)

    tokens_doc1 = tokenize_words(norm_doc1)
    tokens_doc2 = tokenize_words(norm_doc2)

    shingles_doc2 = generate_word_shingles(tokens_doc2, k=shingle_size)
    search_target = " ".join(tokens_doc1)

    algorithms = [
        ("Naive", "naive", naive_search),
        ("Rabin-Karp", "rabin_karp", rabin_karp_search),
        ("KMP", "kmp", kmp_search),
    ]

    benchmark_results: List[Dict[str, Any]] = []

    for display_name, key, algo_fn in algorithms:
        # Time the algorithm execution
        start_time = time.perf_counter()
        match_count = 0

        for item in shingles_doc2:
            matches = algo_fn(search_target, item["shingle"])
            if matches:
                match_count += 1

        elapsed_sec = time.perf_counter() - start_time
        elapsed_ms = round(elapsed_sec * 1000.0, 4)

        benchmark_results.append({
            "name": display_name,
            "key": key,
            "execution_time_ms": elapsed_ms,
            "matched_shingles": match_count,
            "total_shingles": len(shingles_doc2)
        })

    return {
        "results": benchmark_results,
        "shingle_count": len(shingles_doc2),
        "target_length": len(search_target)
    }
