"""
Tests for PlagScan Command Line Interface.
"""

import sys
import pytest
from cli import run_cli


def test_cli_execution_success(capsys):
    args = [
        "--doc1", "samples/original_computer_science.txt",
        "--doc2", "samples/plagiarized_computer_science.txt",
        "--algo", "kmp",
        "--shingle", "4",
        "--benchmark"
    ]
    exit_code = run_cli(args)
    captured = capsys.readouterr()
    assert exit_code == 0
    assert "PLAGSCAN" in captured.out
    assert "Similarity Score" in captured.out
    assert "ALGORITHM BENCHMARK" in captured.out


def test_cli_invalid_file(capsys):
    args = [
        "--doc1", "non_existent_file.txt",
        "--doc2", "samples/plagiarized_computer_science.txt"
    ]
    exit_code = run_cli(args)
    assert exit_code == 1
