## Summary of Changes

### Task R23-T030: Refactor `ciphers/simple_keyword_cypher.py` to separate I/O from cipher logic

This pull request completes Task R23-T030 (10 of 10) by restructuring `ciphers/simple_keyword_cypher.py` using tests as a safety net.

### 1. Goal and Architectural Improvements
- Separated console I/O from pure cipher logic in `main()`:
  - Extracted pure dispatch and validation function `process_cipher(message, key, option)` with complete doctests.
  - Reduced `main()` to pure sequential I/O delegation (`input()` $\rightarrow$ `process_cipher()` $\rightarrow$ `print()`).
- Added 7 doctests to `create_cipher_map(key)` (previously had 0).
- Kept existing doctests for `encipher`, `decipher`, and `remove_duplicates` unchanged and passing.

### 2. Complexity & Coverage Evidence (`work/R23-T030/REFACTOR.md`)
- **Cyclomatic Complexity (Ruff C901 / McCabe)**:
  - `main()` complexity reduced from **2 to 1** (-50%).
- **Test Coverage**:
  - Code coverage increased from **68% to 82%**.
  - Doctests increased from 4 to 15 (all 15 passing).

### 3. Verification & Test Evidence
- `uvx ruff check ciphers/simple_keyword_cypher.py`: Passed (0 errors).
- `uvx ruff format --check ciphers/simple_keyword_cypher.py`: Passed (1 file already formatted).
- `python3 -m doctest -v ciphers/simple_keyword_cypher.py`: All 15 doctests passed.
- `pytest --cov`: All tests passed with 82% coverage.
- `python3 scripts/validate_filenames.py`: Passed cleanly.

### 4. Submission Checklist
- [x] Logic separated from `input()` in `main()` into pure function `process_cipher`.
- [x] `create_cipher_map` gained doctests (7 new tests).
- [x] `REFACTOR.md` documents before/after cyclomatic complexity and coverage.
- [x] Existing doctests for `encipher`, `decipher`, and `remove_duplicates` remain unchanged and passing.
- [x] Clean upstream branch `student/E26B07F0850/R23-T030-upstream` prepared with only code changes.
