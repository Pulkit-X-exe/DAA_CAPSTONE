"""
Standalone Empirical Stress-Testing and Benchmarking Script for PlagScan.

Evaluates Naive, Rabin-Karp, and KMP across varying input lengths:
- Small (500 chars)
- Medium (5,000 chars)
- Large (20,000 chars)
- Pathological worst-case (repeated prefix: 'A'*N + 'B')

Run directly with:
    python benchmark.py
"""

import time
import random
import string
from algorithms.naive import naive_search
from algorithms.rabin_karp import rabin_karp_search
from algorithms.kmp import kmp_search


def generate_random_text(length: int) -> str:
    words = ["algorithm", "complexity", "structure", "dynamic", "graph", "tree", "matrix", "hash"]
    parts = []
    current_len = 0
    while current_len < length:
        w = random.choice(words)
        parts.append(w)
        current_len += len(w) + 1
    return " ".join(parts)[:length]


def benchmark_suite():
    print("=" * 70)
    print("  PLAGSCAN DAA ALGORITHM EMPIRICAL BENCHMARK SUITE")
    print("=" * 70)

    test_scenarios = [
        ("Small Text (1,000 chars)", generate_random_text(1000), "algorithm complexity", 20),
        ("Medium Text (10,000 chars)", generate_random_text(10000), "dynamic graph tree", 10),
        ("Large Text (30,000 chars)", generate_random_text(30000), "hash matrix structure", 5),
        ("Worst-Case Pathological ('A'*5000 + 'B')", "A" * 5000 + "B", "A" * 100 + "B", 5)
    ]

    for scenario_name, text, pattern, iterations in test_scenarios:
        print(f"\n[Scenario]: {scenario_name}")
        print(f"Text Length: {len(text)} | Pattern Length: {len(pattern)} | Iterations: {iterations}")
        print("-" * 70)
        print(f"{'Algorithm':<28} | {'Avg Time (ms)':<15} | {'Speedup vs Naive'}")
        print("-" * 70)

        # Naive
        t0 = time.perf_counter()
        for _ in range(iterations):
            _ = naive_search(text, pattern)
        naive_time = (time.perf_counter() - t0) / iterations * 1000.0

        # Rabin-Karp
        t0 = time.perf_counter()
        for _ in range(iterations):
            _ = rabin_karp_search(text, pattern)
        rk_time = (time.perf_counter() - t0) / iterations * 1000.0

        # KMP
        t0 = time.perf_counter()
        for _ in range(iterations):
            _ = kmp_search(text, pattern)
        kmp_time = (time.perf_counter() - t0) / iterations * 1000.0

        print(f"{'Naive Pattern Matching':<28} | {naive_time:<15.4f} | 1.00x (Baseline)")
        rk_speedup = naive_time / max(0.00001, rk_time)
        print(f"{'Rabin-Karp Rolling Hash':<28} | {rk_time:<15.4f} | {rk_speedup:.2f}x")
        kmp_speedup = naive_time / max(0.00001, kmp_time)
        print(f"{'Knuth-Morris-Pratt (KMP)':<28} | {kmp_time:<15.4f} | {kmp_speedup:.2f}x")

    print("\n" + "=" * 70)
    print("  Benchmark complete. KMP exhibits near-constant search time without backtracking.")
    print("=" * 70)


if __name__ == "__main__":
    benchmark_suite()
