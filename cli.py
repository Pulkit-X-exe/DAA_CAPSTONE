"""
PlagScan Command Line Interface (CLI).

Enables terminal-based plagiarism detection and algorithm benchmarking.
Ideal for quick demonstrations, scripts, and college viva presentations.

Usage:
    python cli.py --doc1 <file_path> --doc2 <file_path> [--algo <kmp|rabin_karp|naive>] [--shingle <k>]
"""

import sys
import argparse
from services.comparison_service import compare_documents
from services.benchmark_service import run_algorithm_benchmark


def read_file_content(path: str) -> str:
    """Reads raw text content from given path."""
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read().strip()


def run_cli(args=None):
    parser = argparse.ArgumentParser(
        description="PlagScan — Intelligent Plagiarism Detection System (DAA Capstone)"
    )
    parser.add_argument("--doc1", required=True, help="Path to original / reference document (.txt)")
    parser.add_argument("--doc2", required=True, help="Path to suspect / compared document (.txt)")
    parser.add_argument(
        "--algo",
        choices=["kmp", "rabin_karp", "naive"],
        default="kmp",
        help="Matching algorithm (default: kmp)"
    )
    parser.add_argument(
        "--shingle",
        type=int,
        default=5,
        help="Word shingle window size (default: 5)"
    )
    parser.add_argument(
        "--benchmark",
        action="store_true",
        help="Run benchmark comparing all 3 algorithms"
    )

    parsed = parser.parse_args(args)

    try:
        doc1_text = read_file_content(parsed.doc1)
        doc2_text = read_file_content(parsed.doc2)
    except Exception as e:
        print(f"Error reading input files: {e}", file=sys.stderr)
        return 1

    print("=" * 65)
    print("  PLAGSCAN — Intelligent Plagiarism Detection System (DAA)")
    print("=" * 65)
    print(f"  Reference Document : {parsed.doc1}")
    print(f"  Compared Document  : {parsed.doc2}")
    print(f"  Algorithm Selected : {parsed.algo.upper()}")
    print(f"  Shingle Size (k)   : {parsed.shingle} words")
    print("-" * 65)

    result = compare_documents(
        doc1_text=doc1_text,
        doc2_text=doc2_text,
        algorithm_key=parsed.algo,
        shingle_size=parsed.shingle
    )

    print(f"  Similarity Score   : {result['similarity_percentage']}%")
    print(f"  Matched Words      : {result['matched_word_count']} / {result['doc2_word_count']}")
    print(f"  Matching Sections  : {result['matching_sections_count']}")
    print(f"  Execution Time     : {result['execution_time_ms']} ms")
    print("-" * 65)

    if parsed.benchmark:
        print("  ALGORITHM BENCHMARK ON EQUIVALENT INPUT:")
        print(f"  {'Algorithm':<28} | {'Time (ms)':<12} | {'Complexity'}")
        print("  " + "-" * 55)
        bm = run_algorithm_benchmark(doc1_text, doc2_text, shingle_size=parsed.shingle)
        for b in bm["results"]:
            comp = "O(N * M)" if b["key"] == "naive" else ("O(N + M) avg" if b["key"] == "rabin_karp" else "O(N + M)")
            print(f"  {b['name']:<28} | {b['execution_time_ms']:<12} | {comp}")
        print("=" * 65)

    return 0


if __name__ == "__main__":
    sys.exit(run_cli())
