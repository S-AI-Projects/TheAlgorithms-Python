### Describe your change

* [ ] Add an algorithm?
* [ ] Fix a bug or typo in an existing algorithm?
* [x] Add or change doctests? -- Note: Please avoid changing both code and tests in a single pull request.
* [x] Documentation change?

### Checklist

* [x] I have read [CONTRIBUTING.md](https://github.com/TheAlgorithms/Python/blob/master/CONTRIBUTING.md).
* [x] This pull request is all my own work -- I have not plagiarized.
* [x] I know that pull requests will not be merged if they fail the automated tests.
* [x] This PR only changes one algorithm file. To ease review, please open separate PRs for separate algorithms.
* [x] All new Python files are placed inside an existing directory.
* [x] All filenames are in all lowercase characters with no spaces or dashes.
* [x] All functions and variable names follow Python naming conventions.
* [x] All function parameters and return values are annotated with Python [type hints](https://docs.python.org/3/library/typing.html).
* [x] All functions have [doctests](https://docs.python.org/3/library/doctest.html) that pass the automated testing.
* [x] All new algorithms include at least one URL that points to Wikipedia or another similar explanation.
* [ ] If this pull request resolves one or more open issues, then the description above includes the issue number(s) with a [closing keyword](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue): "Fixes #ISSUE-NUMBER".

---

## Description

This pull request completes **Task R23-T022**: validating the empirical performance of **Exponential Search** against its theoretical time complexity $O(\log i)$ (where $i$ is the target's index) and comparing its element comparison counts against standard **Binary Search**.

The docstring of `exponential_search` is updated with a concise mathematical derivation of $O(\log i)$ complexity and backed by measured element comparison counts across 7 doubling input sizes. Three new doctests covering edge cases (target at start, target at end, absent target) are added, and all 13 original doctests remain intact and passing.

## Type of Change

- [ ] Bug Fix
- [ ] New Feature
- [ ] UI/UX Improvement
- [x] Performance Improvement
- [x] Tests
- [x] Documentation
- [ ] Refactoring / Maintenance
- [ ] CI/CD

## Changes Made

- `searches/exponential_search.py`:
  - Updated docstring for `exponential_search`: documented theoretical time complexity $O(\log i)$ where $i$ is the target index with a 2-phase derivation (range bounding + bounded binary search).
  - Included an empirical comparison counts table comparing Exponential Search vs. Binary Search across input sizes $n \in [1,000, \dots, 64,000]$.
  - Added new doctests:
    - Target at start: `exponential_search([10, 20, 30, 40, 50, 60, 70, 80], 10) -> 0`
    - Target at end: `exponential_search([10, 20, 30, 40, 50, 60, 70, 80], 80) -> 7`
    - Absent target: `exponential_search([10, 20, 30, 40, 50, 60, 70, 80], 45) -> -1`
  - All 13 existing doctests across `binary_search_by_recursion` and `exponential_search` preserved.
- `work/R23-T022/`:
  - `bench.py`: Timing benchmark script with `timeit` across 7 doubling input sizes and instrumented comparison counters for targets at index $0$, $n // 2$, $n - 1$, and absent.
  - `exponential_search_benchmark.png`: Dual-panel plot visualizing comparison counts vs. theoretical $2 \cdot \log_2 n$ curve and runtime scaling.
  - `FINDINGS.md`: Complete theoretical derivation, mathematical bounds, and empirical analysis.
  - `test_output.txt`: Doctest and pytest execution logs.
  - `ty_check.txt`: Static type checker diagnostics.

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

## Testing

- `python3 -m doctest -v searches/exponential_search.py` -> 16/16 tests passed.
- `uv run --with pytest pytest --doctest-modules searches/exponential_search.py` -> 2 passed in 0.02s.
- `uvx ruff check searches/exponential_search.py work/R23-T022/bench.py` -> All checks passed.
- `uvx ruff format --check searches/exponential_search.py work/R23-T022/bench.py` -> 1 file already formatted.
- `uvx ty check --exit-zero searches/exponential_search.py` -> 0 diagnostics for the file.

## Additional Notes

- Findings:
  1. Exponential Search achieves $O(1)$ best case with **exactly 1 comparison** for targets at index $0$, reducing comparisons by **up to 97%** compared to Binary Search (1 vs 29 comparisons at $n=64,000$).
  2. For targets near the middle ($i=n/2$), Exponential Search is comparable to Binary Search ($\approx 28$ vs 29 comparisons).
  3. For targets near the end ($i=n-1$), Exponential Search performs $\approx 1.48\times$ comparisons of Binary Search due to the doubling phase, maintaining $O(\log n)$ asymptotic bound.
  4. A second clean branch `student/E26B07F0850/R23-T022-upstream` (and `R23-T022-upstream`) containing only the code change (no `work/` folder) has been created and pushed for a later upstream PR.
