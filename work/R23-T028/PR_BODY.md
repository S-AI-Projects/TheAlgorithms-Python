## Summary of Changes

### Task R23-T028: Strict Ruff audit, code fixes, and review documentation

This pull request completes Task R23-T028 (8 of 10) on `conversions/pressure_conversions.py`.

### 1. Goal and Decisions
- Evaluated `conversions/pressure_conversions.py` under Ruff's strictest rule set (`--select ALL`).
- Resolved **6 rule codes** (exceeding the requirement of at least 3):
  - **`D101`** (`missing-docstring-public-class`): Added clear docstring to `class FromTo(NamedTuple)`.
  - **`D205`** (`missing-blank-line-after-summary`): Added blank line between docstring summary and body.
  - **`D212`** (`multi-line-summary-first-line`): Aligned multi-line docstring summaries to the opening line.
  - **`D400`** (`ends-in-period`): Ensured summary sentences end with proper period punctuation.
  - **`D415`** (`ends-in-punctuation`): Ensured docstring summary punctuation compliance.
  - **`COM812`** (`missing-trailing-comma`): Added trailing commas to multi-line `ValueError` raise calls.
- Justified and kept non-applicable or domain-specific rules in `work/R23-T028/REVIEW.md`:
  - **`CPY001`** (Missing copyright notice): Kept as TheAlgorithms-Python does not use per-file copyright headers.
  - **`E501`** (Line too long / URLs): Kept reference URLs intact for documentation utility.
  - **`PLR2004`** (Magic numbers): Kept numeric literals in `PRESSURE_CONVERSION` as physical constants.
  - **`pep8-naming` (`inHg`)**: Kept scientific meteorological unit abbreviation intact.

### 2. Verification & Test Evidence
- **Repo-Config Ruff Check**: `uvx ruff check conversions/pressure_conversions.py` passes (0 errors).
- **Ruff Format Check**: `uvx ruff format --check conversions/pressure_conversions.py` passes.
- **Doctests**: All 9 existing doctests pass (`9 passed. Test passed.`).
- **Pytest**: `uv run --with pytest pytest --doctest-modules conversions/pressure_conversions.py` passes (1 passed in 0.02s).

### 3. Submission Checklist
- [x] Strict Ruff audit performed and documented in `work/R23-T028/REVIEW.md`.
- [x] At least 3 rule codes fixed in `conversions/pressure_conversions.py` (6 fixed).
- [x] Repo-config Ruff passes with 0 warnings.
- [x] All 9 doctests pass.
- [x] Clean upstream branch `student/E26B07F0850/R23-T028-upstream` prepared with only code changes.
