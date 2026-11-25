# 🎓 PlagScan — College Viva & Oral Examination Guide
## Design and Analysis of Algorithms (DAA) Capstone Project
**Author:** Pulkit Bhardwaj (Pulkit-X-exe)  
**Project:** PlagScan — Intelligent Plagiarism Detection System  
**Repository:** [https://github.com/Pulkit-X-exe/DAA_CAPSTONE](https://github.com/Pulkit-X-exe/DAA_CAPSTONE)

---

## 📑 Table of Contents
1. [Core Project Questions](#1-core-project-questions)
2. [String Matching Fundamentals](#2-string-matching-fundamentals)
3. [Algorithm 1: Naive Pattern Matching](#3-algorithm-1-naive-pattern-matching)
4. [Algorithm 2: Rabin-Karp Algorithm (Rolling Hash)](#4-algorithm-2-rabin-karp-algorithm-rolling-hash)
5. [Algorithm 3: Knuth-Morris-Pratt (KMP) Algorithm](#5-algorithm-3-knuth-morris-pratt-kmp-algorithm)
6. [Comparative Complexity Analysis](#6-comparative-complexity-analysis)
7. [Text Processing & Similarity Calculation](#7-text-processing--similarity-calculation)
8. [Benchmarking & Empirical Results](#8-benchmarking--empirical-results)
9. [Limitations & Academic Integrity](#9-limitations--academic-integrity)
10. [Quick Revision Cheat Sheet (English + Hinglish)](#10-quick-revision-cheat-sheet)

---

## 1. Core Project Questions

### Q1. What is PlagScan and what problem does it solve?
**Answer:**  
PlagScan is an intelligent text-overlap and plagiarism detection system built as a DAA capstone project. It analyzes two text documents (Reference Document vs. Compared Document) and detects verbatim copying or textual borrowing by running three manually implemented string-matching algorithms:
1. **Naive Pattern Matching**
2. **Rabin-Karp Algorithm**
3. **Knuth-Morris-Pratt (KMP) Algorithm**

It calculates a mathematical similarity percentage, highlights matching passages in both documents, and empirically benchmarks the runtime of all three algorithms under identical inputs.

### Q2. Does PlagScan detect AI-generated content or paraphrasing?
**Answer:**  
**No.** PlagScan strictly detects *syntactic text overlap* and verbatim string matches using DAA algorithms. It does not use neural language models or claim to detect AI generation or semantic paraphrasing. An honest project with well-defined boundaries scores highest in college evaluations!

---

## 2. String Matching Fundamentals

### Q3. What is the String Matching Problem in DAA?
**Answer:**  
Given a Text string $T[0 \dots N-1]$ of length $N$ and a Pattern string $P[0 \dots M-1]$ of length $M$ (where $M \le N$), the string matching problem is to find all 0-based valid shift indices $s$ such that:
$$T[s \dots s+M-1] = P[0 \dots M-1]$$
- **Alphabet ($\Sigma$):** The finite set of characters from which $T$ and $P$ are constructed (e.g. ASCII = 256).
- **Prefix:** A leading substring starting at index 0.
- **Suffix:** A trailing substring ending at the final index.

### Q4. Why did we choose these three specific algorithms?
**Answer:**  
These three algorithms represent the classical evolution of algorithmic paradigms in DAA:
1. **Naive (Brute Force):** Simple baseline ($O(N \times M)$ worst case), does no preprocessing.
2. **Rabin-Karp (Hashing Paradigm):** Uses algebraic rolling hashes ($O(N+M)$ average), demonstrates randomized algorithms and collision handling.
3. **KMP (Dynamic Programming / Deterministic Finite Automaton):** Precomputes an LPS array ($O(N+M)$ guaranteed), completely avoids backtracking in the text.

---

## 3. Algorithm 1: Naive Pattern Matching

### Q5. How does the Naive Algorithm work?
**Answer:**  
The Naive algorithm slides the pattern $P$ of length $M$ over the text $T$ of length $N$ one position at a time:
- At each alignment $i$ (from $0$ to $N - M$), compare characters $T[i+j]$ and $P[j]$ for $j = 0 \dots M-1$.
- If a mismatch occurs, immediately break and slide the pattern to $i+1$.
- If all $M$ characters match, record $i$ as a match index.

### Q6. What is the Best, Average, and Worst Case Time Complexity of Naive?
**Answer:**
- **Best Case: $O(N)$**  
  Occurs when the very first character of the pattern mismatches text at every alignment (e.g., $T = \text{"AAAAAAAA"}$, $P = \text{"BA"}$). Only 1 comparison per alignment.
- **Worst Case: $O((N - M + 1) \times M) \approx O(N \times M)$**  
  Occurs when all characters match up until the very last character of the pattern before mismatching (e.g., $T = \text{"AAAAAAAAAB"}$, $P = \text{"AAAB"}$).
- **Auxiliary Space: $O(1)$**  
  Uses zero extra memory besides a few integer loop counters.

---

## 4. Algorithm 2: Rabin-Karp Algorithm (Rolling Hash)

### Q7. What is a "Rolling Hash" and why is it $O(1)$?
**Answer:**  
In a standard hash function, hashing a string of length $M$ takes $O(M)$ time. If we rehashed each window from scratch, Rabin-Karp would take $O(N \times M)$ time!  
A **rolling hash** allows us to compute the hash of the *next* sliding window $T[i+1 \dots i+M]$ from the current window $T[i \dots i+M-1]$ in constant $O(1)$ time:
1. Subtract the leading character's weighted value: $(H - T[i] \times d^{M-1})$.
2. Multiply by base $d$: shift all character positions left by one.
3. Add the incoming character: $+ T[i+M]$.
4. Take modulo $q$ to keep numbers within machine precision:
$$H_{i+1} = \left( d \times (H_i - T[i] \times h) + T[i+M] \right) \pmod q$$
*(where $h = d^{M-1} \pmod q$)*.

### Q8. What is a "Spurious Hit" (Hash Collision) and how do we handle it?
**Answer:**  
- **Hash Collision:** When two different strings produce the exact same hash value: $H(P) = H(T_i)$ even though $P \ne T_i$.
- **Spurious Hit:** A false match caused by a hash collision.
- **Handling:** Rabin-Karp NEVER assumes a match based solely on hash equality. Whenever $H(P) == H(T_i)$, it performs a character-by-character verification of $T[i \dots i+M-1]$ against $P$. If any character differs, the match is discarded as a spurious hit.

### Q9. What are the complexities of Rabin-Karp?
**Answer:**
- **Preprocessing:** $O(M)$ to compute initial hashes of pattern and first window.
- **Average Time:** $O(N + M)$ assuming a large prime modulus with uniform hash distribution and negligible collisions.
- **Worst Case Time:** $O(N \times M)$ if every window produces a hash collision (spurious hit), forcing full character comparisons at every index.
- **Auxiliary Space:** $O(1)$.

---

## 5. Algorithm 3: Knuth-Morris-Pratt (KMP) Algorithm

### Q10. What is the fundamental intuition behind KMP?
**Answer:**  
In the Naive algorithm, when a mismatch occurs after matching several characters, the text pointer $i$ is reset backwards.  
**KMP's insight:** The pattern itself contains information about which characters have already been matched! By precomputing the LPS array, KMP slides the pattern forward and **never decreases or backtracks the text index $i$**.

### Q11. What is the LPS Array?
**Answer:**  
LPS stands for **Longest Proper Prefix which is also a Suffix**.  
For a pattern $P$ of length $M$, $LPS[i]$ stores the length of the longest proper prefix of substring $P[0 \dots i]$ that is also a suffix of $P[0 \dots i]$.  
*(A proper prefix is a prefix that is not equal to the whole string).*

#### Trace Example for Pattern `"ABABC"`:
- Substring `"A"`: prefixes: `""`; suffixes: `""` $\rightarrow LPS[0] = 0$.
- Substring `"AB"`: prefixes: `"A"`; suffixes: `"B"` $\rightarrow LPS[1] = 0$.
- Substring `"ABA"`: prefix `"A"` matches suffix `"A"` $\rightarrow LPS[2] = 1$.
- Substring `"ABAB"`: prefix `"AB"` matches suffix `"AB"` $\rightarrow LPS[3] = 2$.
- Substring `"ABABC"`: no matching prefix/suffix $\rightarrow LPS[4] = 0$.
**Final LPS array for `"ABABC"`:** `[0, 0, 1, 2, 0]`.

### Q12. Why is KMP guaranteed $O(N + M)$ in the worst case?
**Answer:**  
1. **LPS Preprocessing:** Building the LPS array uses a two-pointer approach that takes $O(M)$ time.
2. **Search Phase:** In the search loop, the text pointer $i$ only increments from $0$ to $N$. The pattern pointer $j$ is either incremented (at most $N$ times) or decremented via LPS transitions (which can decrease at most as many times as it was incremented).  
By amortized analysis, the total number of operations in the search phase is at most $2N = O(N)$.  
Total worst-case time is strictly **$O(N + M)$**.

---

## 6. Comparative Complexity Analysis

| Algorithm | Preprocessing Time | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space | Backtracking in Text? |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Naive** | None ($O(1)$) | $O(N)$ | $O(N)$ | $O(N \times M)$ | $O(1)$ | **Yes** (resets $i$) |
| **Rabin-Karp** | $O(M)$ | $O(N + M)$ | $O(N + M)$ | $O(N \times M)$ | $O(1)$ | **No** (slides window) |
| **KMP** | $O(M)$ (LPS) | $O(N)$ | $O(N)$ | $O(N + M)$ | $O(M)$ | **Strictly No** ($i$ only moves forward) |

### Q13. Which algorithm is best and why?
**Answer:**  
- **KMP is best for deterministic, guaranteed performance** because its worst case is bounded at $O(N + M)$ without relying on hash randomization.
- **Rabin-Karp is best for multi-pattern search** (searching for 1,000 patterns simultaneously) because we can store pattern hashes in a hash set and search all of them in a single text pass.
- **Naive is suitable only for short, non-repetitive strings** where the overhead of building an LPS array or calculating modular hashes exceeds the savings.

---

## 7. Text Processing & Similarity Calculation

### Q14. What is a "Word Shingle" (N-Gram)?
**Answer:**  
A word shingle is a continuous sequence of $k$ consecutive words from a text.  
*Example:* For text `"Design and Analysis of Algorithms in Python"`, with $k = 4$:
- Shingle 1: `"Design and Analysis of"`
- Shingle 2: `"and Analysis of Algorithms"`
- Shingle 3: `"Analysis of Algorithms in"`
- Shingle 4: `"of Algorithms in Python"`  
Shingling captures phrase structure rather than isolated words.

### Q15. How is the Similarity Percentage calculated in PlagScan?
**Answer:**  
PlagScan uses a **deduplicated containment metric**:
$$\text{Similarity \%} = \left( \frac{\text{Unique Matched Words in Compared Doc}}{\text{Total Words in Compared Doc}} \right) \times 100$$
- Every time a $k$-word shingle from the compared document matches the reference document, all $k$ word token positions are added to a mathematical `set()`.
- Because sets store unique elements, overlapping shingles do **not** double-count the same words!
- The score is strictly bounded between **0.0% and 100.0%**.

---

## 8. Benchmarking & Empirical Results

### Q16. How did we measure execution time fairly?
**Answer:**  
1. We used Python's high-resolution timer: `time.perf_counter()`.
2. **Crucial DAA Practice:** Text normalization, tokenization, and shingle creation were executed **outside** the timed block.
3. The benchmark measures **only the pure algorithmic string matching execution** of Naive vs. Rabin-Karp vs. KMP on identical strings.

### Q17. What did our empirical benchmarks demonstrate?
**Answer:**  
On natural language text, all three algorithms run quickly. However, on pathological worst-case inputs (e.g. $T = \text{"A"}^{5000} + \text{"B"}$ and $P = \text{"A"}^{100} + \text{"B"}$):
- **Naive took ~43.68 ms** due to $O(N \times M)$ redundant comparisons.
- **Rabin-Karp took ~1.65 ms** (~26.4x speedup).
- **KMP took ~1.02 ms** (~42.9x speedup).  
This empirically validates the theoretical time complexities learned in class.

---

## 9. Limitations & Academic Integrity

### Q18. What are the limitations of PlagScan?
**Answer:**  
1. **Paraphrase & Synonym Blindness:** If a student rewrites sentences using synonyms (e.g., replaces "rapidly" with "swiftly"), verbatim string matching will not flag it.
2. **Translation Blindness:** Does not detect text translated from another language.
3. **No Central Database:** Compares two submitted documents against each other, rather than indexing the entire World Wide Web.

---

## 10. Quick Revision Cheat Sheet (English + Hinglish)

| Term / Concept | Simple Definition | Hinglish Explanation (For Quick Recall) |
| :--- | :--- | :--- |
| **String Matching** | Finding pattern $P$ inside text $T$. | Text me se pattern dhundhna. |
| **Naive Algorithm** | Brute force check at every index. | Ek-ek karke har character match karna. Worst case me $O(N \times M)$. |
| **Rabin-Karp** | Compares numerical hashes first. | Pehle hash match karo, hash mile tabhi character verify karo. |
| **Rolling Hash** | $O(1)$ hash calculation for next window. | Purane hash me se pehla letter hatao, naya letter jodo constant time me. |
| **Spurious Hit** | Hash matches, but characters mismatch. | Hash collision ho gaya, par actual text alag hai. |
| **KMP Algorithm** | Avoids text backtracking using LPS array. | Agar mismatch ho, to text pointer peeche nahi jayega. $O(N+M)$ guaranteed. |
| **LPS Array** | Longest Proper Prefix which is also Suffix. | Substring ka prefix aur suffix kitna match karta hai uska table. |
| **Word Shingle** | Window of $k$ consecutive words. | $k$ continuous shabdon ka tukda (chunk). |
| **Similarity %** | Unique matched words / Total words. | Kitne unique words borrow kiye gaye hain compared document me. |
