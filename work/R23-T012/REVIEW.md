# Strict Ruff Review for `maths/special_numbers/trimorphic_number.py` (Task R23-T012)

## Baseline Checks
- Repo-configured Ruff check: `uvx ruff check maths/special_numbers/trimorphic_number.py` passed with 0 errors.
- Pytest suite: `uv run pytest maths/special_numbers/trimorphic_number.py` passed (10 doctests).

## Findings from `uvx ruff check --select ALL`

Total initial findings: 7 errors across 6 rule codes.

| Rule Code | Rule Name | Count | Status | Rationale |
|---|---|---|---|---|
| `D205` | `blank-line-after-summary` | 1 | **Fixed** | Added a blank line between the one-line summary and the description in the module docstring according to PEP 257. |
| `D212` | `multi-line-summary-first-line` | 2 | **Fixed** | Began multi-line docstrings on the first line after quotes (`"""A Trimorphic Number...` and `"""Check if a number...`). |
| `D401` | `non-imperative-mood` | 1 | **Fixed** | Changed docstring opening sentence from descriptive mood ("Checks if...") to imperative mood ("Check if...") as required by PEP 257 and repository standards. |
| `EM101` | `raw-string-in-exception` | 1 | **Fixed** | Assigned the exception message string to a variable `msg` prior to raising `ValueError(msg)`, matching standard repo practice. |
| `TRY003` | `raise-vanilla-args` | 1 | **Fixed** | Resolving `EM101` (extracting `msg` before `raise ValueError(msg)`) eliminates the inlined complex string in the raise expression. |
| `CPY001` | `missing-copyright-notice` | 1 | **Kept** | The repository uses a global repository root `LICENSE.md` (MIT License) and does not include per-file copyright banners. Adding a copyright notice would violate repository conventions. |

## Verification
- Repo-configured Ruff check (`uvx ruff check maths/special_numbers/trimorphic_number.py`): **Passed**.
- Strict check (`uvx ruff check --select ALL maths/special_numbers/trimorphic_number.py`): Only `CPY001` remains (justified above).
- Automated tests (`uv run pytest maths/special_numbers/trimorphic_number.py`): **10/10 doctests passed**.
