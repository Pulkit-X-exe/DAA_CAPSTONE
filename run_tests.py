"""
PlagScan End-to-End Test and System Health Verification Runner.

Runs the complete Pytest suite and verifies:
- All 3 String Matching Algorithms (Naive, Rabin-Karp, KMP)
- Text processing, tokenization, and shingle generation
- File extraction (TXT, PDF, DOCX)
- Flask web routes and REST API endpoints
- PDF report generation
- Mathematical similarity and containment metrics
- Command-line interface (CLI) execution
"""

import sys
import subprocess
import time


def main():
    print("=" * 70)
    print("  PLAGSCAN FULL SYSTEM VERIFICATION & TEST RUNNER")
    print("=" * 70)

    start_time = time.perf_counter()

    cmd = [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"]
    result = subprocess.run(cmd)

    elapsed = time.perf_counter() - start_time
    print("-" * 70)

    if result.returncode == 0:
        print(f"  ALL TESTS PASSED SUCCESSFULLY! (Time: {elapsed:.2f}s)")
        print("  System is 100% healthy and ready for College Viva Demonstration.")
        print("=" * 70)
        return 0
    else:
        print(f"  SOME TESTS FAILED! (Exit code: {result.returncode})", file=sys.stderr)
        print("=" * 70)
        return 1


if __name__ == "__main__":
    sys.exit(main())
