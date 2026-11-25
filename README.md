# PlagScan — Intelligent Plagiarism Detection System

**DAA Capstone Project** | *Design and Analysis of Algorithms*  
Author: Pulkit Bhardwaj (Pulkit-X-exe)  
Repository: [https://github.com/Pulkit-X-exe/DAA_CAPSTONE](https://github.com/Pulkit-X-exe/DAA_CAPSTONE)

---

## 📌 Overview

**PlagScan** is a plagiarism and text-overlap detection web application built to analyze and demonstrate string-matching algorithms learned in Design and Analysis of Algorithms (DAA).

The system compares two text documents and identifies similar or matching text using three manually implemented string-matching algorithms:
1. **Naive Pattern Matching**
2. **Rabin-Karp Algorithm** (Rolling Hash)
3. **Knuth-Morris-Pratt (KMP) Algorithm** (Prefix-Suffix / LPS Array)

> **Important Academic Note:** PlagScan detects text overlap, verbatim copying, and syntactic similarity. It does not claim to detect semantic rewriting, paraphrase paraphrasing, or AI-generated content.

---

## 🚀 Key Features

- **Multi-Format Document Upload:** Supports `.txt`, `.pdf`, and `.docx`.
- **Three Pure DAA Algorithms:** Zero reliance on Python's built-in `find()` or external matching libraries for core matching.
- **N-Gram / Shingle Comparison Engine:** Configurable word shingle matching (default 5-word shingles) with position tracking and duplicate prevention.
- **Execution Benchmarking:** Millisecond-accurate benchmarking using Python's `time.perf_counter()` on identical inputs.
- **Interactive UI & Visualizations:** Dark navy SaaS-style UI with dual-panel text highlighting and Chart.js performance graphs.
- **Downloadable PDF Reports:** Professional PDF summary of comparison metrics, matching sections, and complexity analysis.

---

## 🛠️ Tech Stack

- **Backend:** Python 3.11, Flask
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5
- **Data Visualization:** Chart.js
- **Testing:** Pytest
- **Document Processing:** python-docx, pypdf, reportlab

---

## 📊 Algorithm Complexity Summary

| Algorithm | Preprocessing Time | Best Case Matching | Average Case Matching | Worst Case Matching | Auxiliary Space |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Naive** | None ($O(1)$) | $O(N)$ | $O(N)$ | $O(N \times M)$ | $O(1)$ |
| **Rabin-Karp** | $O(M)$ (hash computation) | $O(N + M)$ | $O(N + M)$ | $O(N \times M)$ | $O(1)$ |
| **KMP** | $O(M)$ (LPS array) | $O(N)$ | $O(N)$ | $O(N + M)$ | $O(M)$ |

*(Where $N$ is text length and $M$ is pattern length).*

---

## ⚙️ Quick Start

```bash
# Clone repository
git clone https://github.com/Pulkit-X-exe/DAA_CAPSTONE.git
cd DAA_CAPSTONE

# Install dependencies
pip install -r requirements.txt

# Run automated tests
pytest

# Start development server
python app.py
```
Open your browser at `http://localhost:5000`.
