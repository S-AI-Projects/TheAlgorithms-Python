# R23-T022: Empirical Complexity Analysis & Doctests for Exponential Search

## Summary

This pull request addresses **Task R23-T022**: validating the empirical performance of **Exponential Search** against its theoretical time complexity $O(\log i)$ (where $i$ is the target's index) and comparing its element comparison counts against standard **Binary Search**.

### Changes Made
1. **`searches/exponential_search.py`**:
   - Updated the docstring of `exponential_search` with the mathematical derivation of $O(\log i)$ complexity.
   - Added empirical comparison count data comparing Exponential Search against Binary Search across doubling input sizes.
   - Added new doctests covering:
     - Target at the start of the collection (index $0$).
     - Target at the end of the collection (index $n - 1$).
     - Absent target (not present in the collection).
   - Preserved all 13 existing doctests across `binary_search_by_recursion` and `exponential_search`.
2. **`work/R23-T022/`**:
   - `bench.py`: Comprehensive benchmark script timing execution with `timeit` across 7 doubling input sizes ($n \in [1,000, \dots, 64,000]$) and counting exact element comparisons for start, middle, end, and absent targets.
   - `exponential_search_benchmark.png`: Dual-panel plot visualizing comparison counts vs. theoretical $2 \cdot \log_2 n$ curve and runtime scaling.
   - `FINDINGS.md`: Complete theoretical derivation, mathematical bounds, and empirical analysis.
   - `test_output.txt`: Doctest and pytest execution logs.
   - `ty_check.txt`: Static type checker diagnostics.

---

## Theoretical Complexity Derivation

Given a sorted collection of size $n$ and an item at index $i$:
1. **Doubling Phase (Range Bounding):**
   - If $A[0] = \text{target}$, return index $0$ in $O(1)$ time (1 comparison).
   - Otherwise, bound values double: $1, 2, 4, \dots, 2^k$ until $2^k \ge i$.
   - The loop terminates in $k = \lceil \log_2 i \rceil$ iterations, executing at most $\lceil \log_2 i \rceil$ element comparisons to identify the interval $[2^{k-1}, \min(2^k, n - 1)]$.
2. **Bounded Binary Search Phase:**
   - Interval length is $\le 2^{k-1} + 1 \le i + 1$.
   - Binary search requires at most $\lfloor \log_2(i + 1) \rfloor + 1 \le \lceil \log_2 i \rceil + 1$ probes.
3. **Total Complexity:**
   $$O(\log i) + O(\log i) = O(\log i)$$

---

## Measured Comparison Counts (Exponential vs. Binary Search)

| Size $n$ | Target Position | Index $i$ | Exponential Search | Binary Search | Ratio (Exp / Bin) |
|---|---|---|---|---|---|
| **1,000** | start | 0 | **1** | 17 | **0.06** |
| 1,000 | mid | 500 | 22 | 17 | 1.29 |
| 1,000 | end | 999 | 28 | 19 | 1.47 |
| **2,000** | start | 0 | **1** | 19 | **0.05** |
| 2,000 | mid | 1,000 | 23 | 19 | 1.21 |
| 2,000 | end | 1,999 | 31 | 21 | 1.48 |
| **4,000** | start | 0 | **1** | 21 | **0.05** |
| 4,000 | mid | 2,000 | 24 | 21 | 1.14 |
| 4,000 | end | 3,999 | 34 | 23 | 1.48 |
| **8,000** | start | 0 | **1** | 23 | **0.04** |
| 8,000 | mid | 4,000 | 25 | 23 | 1.09 |
| 8,000 | end | 7,999 | 37 | 25 | 1.48 |
| **16,000** | start | 0 | **1** | 25 | **0.04** |
| 16,000 | mid | 8,000 | 26 | 25 | 1.04 |
| 16,000 | end | 15,999 | 40 | 27 | 1.48 |
| **32,000** | start | 0 | **1** | 27 | **0.04** |
| 32,000 | mid | 16,000 | 27 | 27 | 1.00 |
| 32,000 | end | 31,999 | 43 | 29 | 1.48 |
| **64,000** | start | 0 | **1** | 29 | **0.03** |
| 64,000 | mid | 32,000 | 28 | 29 | 0.97 |
| 64,000 | end | 63,999 | 46 | 31 | 1.48 |

### Key Findings
* **Target Near Start ($i = 0$):** Exponential search achieves $O(1)$ time with **1 comparison**, compared to 29 comparisons in binary search at $n=64,000$ (a **97% reduction**).
* **Target Near Middle ($i = n // 2$):** Both algorithms perform virtually identical comparison counts ($\approx 28$ vs. $29$ at $n=64,000$).
* **Target Near End ($i = n - 1$):** Exponential search performs $\approx 1.48\times$ comparisons of binary search due to doubling-phase overhead, while maintaining the same asymptotic bound $O(\log n)$.

---

## Verification

- **Doctest (`python3 -m doctest -v searches/exponential_search.py`)**:
  - 16 tests in 3 items, **all 16 passed** (including the 13 original tests and 3 new edge cases).
- **Pytest (`uv run --with pytest pytest --doctest-modules searches/exponential_search.py`)**:
  - **2 passed in 0.02s**.
- **Linter (`uvx ruff check searches/exponential_search.py work/R23-T022/bench.py`)**:
  - Clean, 0 diagnostics.
- **Formatter (`uvx ruff format --check searches/exponential_search.py work/R23-T022/bench.py`)**:
  - Clean, already formatted.
- **Type Checker (`uvx ty check --exit-zero searches/exponential_search.py`)**:
  - 0 diagnostics for `searches/exponential_search.py`.
