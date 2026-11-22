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

This pull request completes **Task R23-T026**: bringing `physics/newtons_second_law_of_motion.py` up to repository standards by replacing exception-swallowing code with strict input validation guards and expanding doctests from 2 to 10 to achieve **100% test coverage**.

### Problems Resolved:
1. **Silent Exception Swallowing**: Previously, `newtons_second_law_of_motion` used `try ... except Exception: return -0.0`, which silently masked invalid inputs, strings, or bugs by returning `-0.0`.
2. **Missing Input Validation**: Negative mass (unphysical in classical mechanics) and non-numeric inputs were not validated with descriptive exceptions.
3. **Low Coverage**: Baseline test coverage was only 43%, with uncovered error branches.

### Physical & Mathematical Decisions:
* **Mass ($m$)**: Must be non-negative ($m \ge 0$). Zero mass is allowed ($F = 0.0$); negative mass raises `ValueError("Mass must be a non-negative value")`. Non-numeric types and booleans raise `TypeError`.
* **Acceleration ($a$)**: Can be positive, zero, or negative (representing opposing vector direction, e.g. downward gravitational acceleration). Non-numeric types and booleans raise `TypeError`.

## Type of Change

- [x] Bug Fix
- [ ] New Feature
- [ ] UI/UX Improvement
- [ ] Performance Improvement
- [x] Tests
- [x] Documentation
- [ ] Refactoring / Maintenance
- [ ] CI/CD

## Input Decisions & Taxonomy Table

| Input Variable | Category / Case | Value Tested | Decision | Physical & Mathematical Justification |
|---|---|---|---|---|
| **`mass`** | Standard Valid | `10`, `2.0` | **Allowed** | Standard macroscopic inertial mass ($m > 0$). |
| **`mass`** | Boundary Zero | `0` | **Allowed** | Idealized massless limit / zero force condition ($F = 0 \cdot a = 0$). |
| **`mass`** | Negative Mass | `-5` | **Raise `ValueError`** | Inertial mass in classical Newtonian mechanics is non-negative ($m \ge 0$). |
| **`mass`** | Non-numeric (str, None) | `"10"`, `None` | **Raise `TypeError`** | Invalid operand type for mathematical multiplication. |
| **`mass`** | Boolean (`True`) | `True` | **Raise `TypeError`** | Avoids silent Python `bool` as integer arithmetic. |
| **`acceleration`** | Standard Valid | `10`, `1` | **Allowed** | Standard positive acceleration ($a > 0$). |
| **`acceleration`** | Boundary Zero | `0` | **Allowed** | Balanced forces / uniform velocity ($a = 0 \implies F = 0$). |
| **`acceleration`** | Negative Acceleration | `-9.8` | **Allowed** | Acceleration is a directional vector quantity ($F = m \cdot (-9.8) = -19.6$ N). |
| **`acceleration`** | Non-numeric (str, None) | `"10"`, `None` | **Raise `TypeError`** | Invalid operand type for acceleration. |
| **`acceleration`** | Boolean (`False`) | `False` | **Raise `TypeError`** | Booleans are logical flags, not physical units of acceleration. |

## Changes Made

- `physics/newtons_second_law_of_motion.py`:
  - Replaced `try ... except Exception: return -0.0` with explicit type guards and negative mass checks.
  - Added docstring sections for `Args:`, `Returns:`, and `Raises:` (`TypeError`, `ValueError`).
  - Added 8 new doctests covering zero mass, zero acceleration, negative directional acceleration, negative mass, non-numeric mass/acceleration, and booleans.
  - Retained both original doctests intact (`(10, 10) -> 100` and `(2.0, 1) -> 2.0`).
- `work/R23-T026/`:
  - `FINDINGS.md`: Complete theoretical justification, coverage progression, and test documentation.
  - `test_output.txt`: Logs of doctest execution, pytest coverage, ruff lint, ruff format, and ty type check.

## Coverage & Verification

* **Doctest Summary**:
  ```text
  10 tests in 2 items.
  10 passed.
  Test passed.
  ```
* **Coverage Progression**:
  * Before: **43%** (Missed lines 77–78, 83–92)
  * After: **100%** (10/10 statements covered, 0 missed lines)
* **Quality Checks**:
  * `python3 -m doctest -v physics/newtons_second_law_of_motion.py` -> 10/10 passed.
  * `uv run --with pytest-cov pytest physics/newtons_second_law_of_motion.py --doctest-modules --cov=physics --cov-report=term-missing` -> 100% coverage.
  * `uvx ruff check physics/newtons_second_law_of_motion.py` -> All checks passed.
  * `uvx ruff format --check physics/newtons_second_law_of_motion.py` -> 1 file already formatted.
  * `uvx ty check --exit-zero physics/newtons_second_law_of_motion.py` -> 0 diagnostics.

## Additional Notes

- A second clean branch `student/E26B07F0850/R23-T026-upstream` (and `R23-T026-upstream`) containing only the changes in `physics/newtons_second_law_of_motion.py` has been created and pushed for a later upstream PR.
