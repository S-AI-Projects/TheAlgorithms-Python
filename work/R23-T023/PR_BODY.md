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

This pull request completes **Task R23-T023**: property-based testing and verification of `conversions/hex_to_rgb.py` using **Hypothesis** against mathematical properties and reference invariants, followed by adding boundary doctests to the function.

A comprehensive property test suite (`work/R23-T023/test_hex_to_rgb_properties.py`) tests the function across over 8,500 generated cases, verifying:
1. **Full 6-digit RGB $\leftrightarrow$ Hex round-trip identity**: For all $(r, g, b) \in [0, 255]^3$, an inverse reference helper `rgb_to_hex` round-trips exactly to `f"rgb({r}, {g}, {b})"`.
2. **3-digit shorthand expansion**: Shorthand `#RGB` expands to `#RRGGBB` ($d \mapsto 17d$).
3. **Invariance**: Upper/lower case and optional `#` prefix produce identical results.
4. **Invalid string rejection**: Invalid lengths and non-hex characters raise `ValueError`.
5. **Documented edge-case limitation**: Hypothesis identified that Python's `int(..., 16)` tolerates boundary whitespace/signs (e.g., `'#00000 '`), which is formally documented in `work/R23-T023/PROPERTIES.md`.

## Type of Change

- [ ] Bug Fix
- [ ] New Feature
- [ ] UI/UX Improvement
- [ ] Performance Improvement
- [x] Tests
- [x] Documentation
- [ ] Refactoring / Maintenance
- [ ] CI/CD

## Changes Made

- `conversions/hex_to_rgb.py`:
  - Added doctests covering the 4 boundary cases uncovered during property testing:
    - 3-digit lowercase hex: `hex_to_rgb("#abc") -> 'rgb(170, 187, 204)'`
    - Lowercase 6-digit hex: `hex_to_rgb("#ff2000") -> 'rgb(255, 32, 0)'`
    - Missing `'#'` prefix: `hex_to_rgb("FF0000") -> 'rgb(255, 0, 0)'` and `hex_to_rgb("123") -> 'rgb(17, 34, 51)'`
    - Invalid lengths: `hex_to_rgb("#12345") -> ValueError` and `hex_to_rgb("") -> ValueError`
  - Updated docstring `Note:` section to explicitly document support for uppercase/lowercase and optional `'#'` prefix.
  - All 8 original doctests and the existing `ValueError` raise statement are 100% preserved.
- `work/R23-T023/`:
  - `test_hex_to_rgb_properties.py`: Hypothesis property test suite with 7 test functions covering round-trip bijection, 3-digit expansion, case/prefix invariance, error domain rejection, and edge cases.
  - `PROPERTIES.md`: Detailed mathematical documentation of the color spaces, bijection formulations, property definitions, and Hypothesis discovery analysis.
  - `test_output.txt`: Execution logs of doctests, pytest, hypothesis, ruff lint, ruff format, and ty type check.

## Testing & Verification

All automated tests passed cleanly:
- `python3 -m doctest -v conversions/hex_to_rgb.py` -> 14/14 tests passed.
- `uv run --with hypothesis --with pytest pytest work/R23-T023/test_hex_to_rgb_properties.py` -> 7/7 passed in 1.67s (>8,500 generated cases).
- `uv run --with pytest pytest --doctest-modules conversions/hex_to_rgb.py` -> 1 passed in 0.02s.
- `uvx ruff check conversions/hex_to_rgb.py work/R23-T023/test_hex_to_rgb_properties.py` -> All checks passed.
- `uvx ruff format --check conversions/hex_to_rgb.py work/R23-T023/test_hex_to_rgb_properties.py` -> 2 files already formatted.
- `uvx ty check --exit-zero conversions/hex_to_rgb.py` -> 0 diagnostics.

## Additional Notes

- A second clean branch `student/E26B07F0850/R23-T023-upstream` (and `R23-T023-upstream`) containing only the code change in `conversions/hex_to_rgb.py` has been prepared for future upstream submission.
