# R23-T056: how CI collects, runs and reports on `maths/abs.py`

**Question:** `abs.py` contains doctests and a `test_abs_val()` function. How does pytest
collect each, and what is the coverage?

**Short answer:** it depends on *how* pytest is pointed at the file.
- Pointed **at the file** (`pytest maths/abs.py`): both are collected, as two separate items.
- Run the way **CI** runs it (`pytest ... .` over the whole repo): only the *doctests* are
  collected. `test_abs_val` runs once, indirectly, because one doctest calls it
  (`>>> test_abs_val()`); the function itself is **not** collected as a test.
- Coverage of the original file is below 100% because of the `if __name__ == "__main__":`
  block, which pytest never executes.

## 1. What CI runs (`.github/workflows/build.yml`)
    uv run --with=pytest-run-parallel pytest --iterations=8 --parallel-threads=auto
        --ignore-gil-enabled --ignore=computer_vision/... (several --ignore entries)
        --cov-report=term-missing:skip-covered --cov=. .
- Python is the one in `.python-version` (3.15t, free-threaded); deps come from `uv sync --group=test`.
- `--iterations=8 --parallel-threads=auto` (pytest-run-parallel) re-runs each test 8 times in parallel threads to catch thread-unsafe tests.
- `--ignore=...` skips files that cannot run in CI (cv2 imports, network calls, `project_euler/`).
- `--cov=. ` with `term-missing:skip-covered` prints only files that are **not** 100% covered, with the missing line numbers.
- `pyproject.toml [tool.pytest]` adds `--durations=10 --doctest-modules --showlocals`; `[tool.coverage]` omits `.env/*` and `project_euler/*` and sorts by Cover.
- After tests pass, CI regenerates `DIRECTORY.md` with `scripts/build_directory_md.py`.

## 2. How pytest collects `abs.py`

### a) Pointing at the file: `pytest maths/abs.py -v`
Explicit file arguments are collected as Python modules whatever their name, so we get
the 4 function doctests, the doctest of `test_abs_val`, **and** `test_abs_val` itself (6 items):

    maths/abs.py::maths.abs.abs_max PASSED
    maths/abs.py::maths.abs.abs_max_sort PASSED
    maths/abs.py::maths.abs.abs_min PASSED
    maths/abs.py::maths.abs.abs_val PASSED
    maths/abs.py::maths.abs.test_abs_val PASSED      <- doctest ">>> test_abs_val()"
    maths/abs.py::test_abs_val PASSED                <- the plain function, run as a test

### b) CI style: pytest pointed at a directory (`pytest maths/ -k abs --collect-only -q`)
`abs.py` does not match pytest's default `python_files` (`test_*.py`, `*_test.py`), so it is
only collected because `--doctest-modules` (from `pyproject.toml`) turns every `.py` file
into a doctest module. The plain function is **not** collected:

    maths/abs.py::maths.abs.abs_max
    maths/abs.py::maths.abs.abs_max_sort
    maths/abs.py::maths.abs.abs_min
    maths/abs.py::maths.abs.abs_val
    maths/abs.py::maths.abs.test_abs_val             <- doctest only
    ...
    maths/test_abs.py::TestAbsVal::test_positive_numbers   <- the separate, real test file
    (maths/test_abs.py has 20 class-based tests; no `maths/abs.py::test_abs_val` appears)

So in CI `test_abs_val()` is exercised only through its doctest wrapper.

## 3. `DIRECTORY.md` and the helper scripts
- `DIRECTORY.md` line 797: `* [Abs](maths/abs.py)` under `## [Maths](maths)`. (`maths/test_abs.py` is listed separately as `* [Test Abs](maths/test_abs.py)`.)
- `scripts/build_directory_md.py` walks the repo (`good_file_paths`), skipping the `scripts` folder, folders starting with `.` or `_` and `venv` folders and `__init__.py`; it keeps `.py`/`.ipynb` files. The title is the file name with `_` -> space and `.title()`: `abs.py` -> "Abs". CI regenerates `DIRECTORY.md` after tests pass, so it is never edited by hand.
- `scripts/validate_filenames.py` (a pre-commit hook) fails on upper-case letters, spaces, hyphens, or files outside a directory. `maths/abs.py` passes all four.

## 4. Coverage and the gap
The only uncovered statements in the original file are in the `__main__` block
(`import doctest`, `doctest.testmod()`, `test_abs_val()`, `print(...)`): pytest imports the
module, so `__name__` is never `"__main__"`. The functions themselves are fully covered
by the doctests.

Fix (in `maths/abs.py`):
1. The assertions of `test_abs_val` are moved into doctests of `abs_val`, `abs_min`, `abs_max` and `abs_max_sort`, and the function is removed (so it no longer appears twice or only via a wrapper).
2. The `__main__` block is marked `# pragma: no cover`, the same convention used elsewhere in the repo (e.g. `ciphers/skytale_cipher.py`, `graphs/minimum_spanning_tree_prims.py`).

Real `pytest-cov` output (command in the PR description) is appended below.

## Side observation
`abs_val(-0.0)` returns `-0.0` (`-num if num < 0 else num`; `-0.0 < 0` is False), whereas the built-in `abs(-0.0)` is `0.0`. Not changed (out of scope), noted here.

### Coverage BEFORE (original abs.py)
```
maths/abs.py::maths.abs.abs_max PASSED                                   [ 16%]
maths/abs.py::maths.abs.abs_max_sort PASSED                              [ 33%]
maths/abs.py::maths.abs.abs_min PASSED                                   [ 50%]
maths/abs.py::maths.abs.abs_val PASSED                                   [ 66%]
maths/abs.py::maths.abs.test_abs_val PASSED                              [ 83%]
maths/abs.py::test_abs_val PASSED                                        [100%]/Users/paulamibhosle/TheAlgorithms-Python/.venv/lib/python3.13/site-packages/coverage/report_core.py:116: CoverageWarning: Couldn't parse Python file '/Users/paulamibhosle/TheAlgorithms-Python/maths/greatest_common_divisor.py' (couldnt-parse); see https://coverage.readthedocs.io/en/7.17.2/messages.html#warning-couldnt-parse
Name                                                        Stmts   Miss  Cover   Missing
maths/abs.py                                                   35      4    89%   89-94
TOTAL                                                        5187   5156     1%
============================== 6 passed in 0.45s ===============================
```

### Coverage AFTER (this PR)
```
maths/abs.py::maths.abs.abs_max PASSED                                   [ 25%]
maths/abs.py::maths.abs.abs_max_sort PASSED                              [ 50%]
maths/abs.py::maths.abs.abs_min PASSED                                   [ 75%]
maths/abs.py::maths.abs.abs_val PASSED                                   [100%]/Users/paulamibhosle/TheAlgorithms-Python/.venv/lib/python3.13/site-packages/coverage/report_core.py:116: CoverageWarning: Couldn't parse Python file '/Users/paulamibhosle/TheAlgorithms-Python/maths/greatest_common_divisor.py' (couldnt-parse); see https://coverage.readthedocs.io/en/7.17.2/messages.html#warning-couldnt-parse
Name                                                        Stmts   Miss  Cover   Missing
maths/abs.py                                                   22      0   100%
TOTAL                                                        5174   5152     1%
============================== 4 passed in 0.43s ===============================
```
