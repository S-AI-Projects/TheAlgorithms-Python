### Describe your change

* [ ] Add an algorithm?
* [x] Fix a bug or typo in an existing algorithm?
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

This pull request completes **Task R23-T027**: comparing the repository's kNN classifier (`machine_learning/k_nearest_neighbors.py`) against scikit-learn's `KNeighborsClassifier` on the Iris dataset, resolving a critical single-use iterator exhaustion defect, and expanding doctests with a 5-point known-answer dataset.

### Findings & Comparison Highlights:
1. **100% Classification Agreement**: Across all 45 test samples (70/30 split, $k=5$, `random_state=42`), repository `KNN` and scikit-learn achieved **100.00% agreement** (45/45 matches).
2. **Execution Latency**: Scikit-learn is $\approx 6.0\times$ faster on the Iris test set ($0.53\text{ ms}$ vs. $3.15\text{ ms}$) due to Cython optimizations and vectorized matrix operations.
3. **Critical Bug Fixed**: In `KNN.__init__`, `self.data = zip(...)` stored a one-time generator iterator. Classifying a single point exhausted the iterator, causing any subsequent `.classify()` call to crash with `IndexError: list index out of range`. This is now resolved with `self.data = list(zip(...))`.
4. **Regression Doctests**: Added a 5-point known-answer dataset testing multiple consecutive classifications. All 8 original doctests remain intact and passing.

## Type of Change

- [x] Bug Fix
- [ ] New Feature
- [ ] UI/UX Improvement
- [ ] Performance Improvement
- [x] Tests
- [x] Documentation
- [ ] Refactoring / Maintenance
- [ ] CI/CD

## Agreement & Benchmark Summary

| Metric | Repository `KNN` | Scikit-Learn `KNeighborsClassifier` |
|---|---|---|
| **Agreement on Iris ($N=45$)** | **45 / 45 (100.00%)** | **45 / 45 (100.00%)** |
| **Total Prediction Time** | $3.150\text{ ms}$ | $0.529\text{ ms}$ |
| **Per-Sample Latency** | $0.070\text{ ms}$ | $0.012\text{ ms}$ |
| **Speedup Factor** | $1.0\times$ (Baseline) | $\mathbf{\approx 6.0\times}$ |
| **Algorithmic Search** | Linear scan via `nsmallest` | Vectorized KD-tree / Ball-tree |

## Changes Made

- `machine_learning/k_nearest_neighbors.py`:
  - Resolved iterator exhaustion bug: `self.data = list(zip(train_data, train_target))` in `KNN.__init__`.
  - Added regression doctest on a 5-point dataset verifying consecutive `.classify()` calls on distinct test points.
  - All 8 original doctests preserved and passing (total 14 doctest items passing).
- `work/R23-T027/`:
  - `compare_test.py`: Benchmark and agreement verification script on the Iris dataset.
  - `COMPARE.md`: Detailed technical comparison covering API paradigms, tie-breaking mechanisms, runtime complexities, and beginner recommendations.
  - `test_output.txt`: Test logs for doctests, pytest, ruff, and ty check.

## Testing & Verification

- `uv run python work/R23-T027/compare_test.py` -> 100.00% agreement, all checks passed.
- `python3 -m doctest -v machine_learning/k_nearest_neighbors.py` -> 14/14 passed.
- `uv run --with pytest pytest --doctest-modules machine_learning/k_nearest_neighbors.py` -> 1 passed in 0.32s.
- `uvx ruff check machine_learning/k_nearest_neighbors.py work/R23-T027/compare_test.py` -> All checks passed.
- `uvx ruff format --check machine_learning/k_nearest_neighbors.py work/R23-T027/compare_test.py` -> 2 files already formatted.
- `uvx ty check --exit-zero machine_learning/k_nearest_neighbors.py` -> 0 diagnostics.

## Additional Notes

- A second clean branch `student/E26B07F0850/R23-T027-upstream` (and `R23-T027-upstream`) containing only the changes in `machine_learning/k_nearest_neighbors.py` has been created and pushed for a later upstream PR.
