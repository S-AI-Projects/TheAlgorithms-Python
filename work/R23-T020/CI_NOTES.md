# Task R23-T020: How CI Tests `dynamic_programming/abbreviation.py`

## 1. CI Workflow and Pytest Configuration

### Quoted from `.github/workflows/build.yml` (lines 34–47):
```yaml
        run: uv run --with=pytest-run-parallel pytest
          --iterations=8 --parallel-threads=auto --ignore-gil-enabled
          --ignore=computer_vision/flip_augmentation.py
          --ignore=computer_vision/harris_corner.py
          --ignore=computer_vision/mosaic_augmentation.py
          --ignore=data_compression/peak_signal_to_noise_ratio.py
          --ignore=digital_image_processing/
          --ignore=docs/conf.py
          --ignore=project_euler/
          --ignore=scripts/validate_solutions.py
          --ignore=web_programming/current_stock_price.py
          --ignore=web_programming/fetch_anime_and_play.py
          --cov-report=term-missing:skip-covered
          --cov=. .
```

### Quoted from `pyproject.toml` (lines 330–335):
```toml
[tool.pytest]
ini_options.addopts = [
  "--durations=10",
  "--doctest-modules",
  "--showlocals",
]
```

### How `--doctest-modules` Integrates `abbr()` into CI:
By default, `pytest` searches for files named `test_*.py` or `*_test.py` and functions named `test_*`. In `TheAlgorithms-Python`, algorithm implementations live directly in their category directories (such as `dynamic_programming/abbreviation.py`) without separate test files.
The configuration `--doctest-modules` instructs `pytest` to inspect every Python file in the repository for docstring code blocks starting with `>>>`. When `pytest` encounters `abbr()` in `dynamic_programming/abbreviation.py`, it automatically parses each example, executes it, verifies the output, and reports it as an independent test item (`dynamic_programming/abbreviation.py::dynamic_programming.abbreviation.abbr`).

---

## 2. CI Test Execution for `dynamic_programming/`

Running:
```bash
uv run pytest dynamic_programming/ -v
```
Output excerpt showing `abbr`'s doctests collected and passed as the very first test:
```
============================= test session starts ==============================
platform darwin -- Python 3.15.2, pytest-9.1.1, pluggy-1.6.0 -- /Users/muqeet/Documents/TheAlgorithms-Python/.venv/bin/python
cachedir: .pytest_cache
rootdir: /Users/muqeet/Documents/TheAlgorithms-Python
configfile: pyproject.toml
plugins: cov-7.1.0, anyio-4.15.1
collecting ... collected 71 items

dynamic_programming/abbreviation.py::dynamic_programming.abbreviation.abbr PASSED [  1%]
dynamic_programming/all_construct.py::dynamic_programming.all_construct.all_construct PASSED [  2%]
...
dynamic_programming/word_break.py::dynamic_programming.word_break.word_break PASSED [100%]
============================== 71 passed in 0.51s ==============================
```

---

## 3. Directory and Filename Validation

### Entry in `DIRECTORY.md` (Line 465):
```markdown
  * [Abbreviation](dynamic_programming/abbreviation.py)
```

### How Repository Tooling Treats This File:
1. `scripts/build_directory_md.py`:
   Traverses repository subdirectories via `good_file_paths()`, filters out hidden files and caches, converts snake_case filenames to Title Case links (`abbreviation.py` $\rightarrow$ `[Abbreviation](dynamic_programming/abbreviation.py)`), and generates `DIRECTORY.md`.
2. `scripts/validate_filenames.py`:
   Validates all tracked paths against open-source repository style rules:
   - `file == file.lower()`: Ensures no uppercase letters in filenames.
   - `" " not in file`: Ensures no whitespace in filenames.
   - `"-" not in file`: Enforces snake_case underscores over hyphens.
   - `os.sep in file`: Requires all algorithm files to reside inside a category folder.
   `dynamic_programming/abbreviation.py` complies with all four rules.

---

## 4. Doctest Expansion and Coverage

### Edge Cases Added to `abbr()`:
- **Empty strings**:
  - `abbr("", "")` $\rightarrow$ `True` (two empty strings match).
  - `abbr("", "A")` $\rightarrow$ `False` (cannot match non-empty target from empty string).
  - `abbr("a", "")` $\rightarrow$ `True` (deleting lowercase 'a' yields empty string).
- **All-lowercase strings**:
  - `abbr("abc", "ABC")` $\rightarrow$ `True` (capitalizing all lowercase letters).
  - `abbr("abc", "AC")` $\rightarrow$ `True` (deleting lowercase 'b' and capitalizing 'a' and 'c').
- **Impossible matches**:
  - `abbr("A", "B")` $\rightarrow$ `False` (uppercase letters cannot be changed or deleted).
  - `abbr("AB", "A")` $\rightarrow$ `False` (uppercase 'B' cannot be deleted).

### Coverage Report
```
Name                                  Stmts   Miss  Cover   Missing
-------------------------------------------------------------------
dynamic_programming/abbreviation.py      13      0   100%
-------------------------------------------------------------------
TOTAL                                    13      0   100%
```
The DP table and state transitions now achieve **100% statement coverage**.
