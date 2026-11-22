# Refactoring Analysis: Separation of Concerns & Complexity Reduction in `ciphers/simple_keyword_cypher.py`
**Task ID**: R23-T030  
**Repository**: [S-AI-Projects/TheAlgorithms-Python](https://github.com/S-AI-Projects/TheAlgorithms-Python)  
**Target File**: `ciphers/simple_keyword_cypher.py`  
**Working Branch**: `student/E26B07F0850/R23-T030` (alias `R23-T030`)  

---

## 1. Executive Summary

In `ciphers/simple_keyword_cypher.py`, the `main()` function previously coupled CLI input gathering (`input()`), input normalization, validation branching, error handling (`try ... except KeyError`), cipher map instantiation, and operation dispatch with console output (`print()`). Because cipher operations were intertwined with standard input calls, the end-to-end encryption/decryption workflow could not be unit tested or doctested without mocking interactive terminal inputs.

To resolve this without altering any external behavior:
1. We extracted the core execution and dispatch logic into a pure function `process_cipher(message: str, key: str, option: str) -> str`.
2. `main()` was reduced to pure, linear I/O delegation (`input()` $\rightarrow$ `process_cipher()` $\rightarrow$ `print()`).
3. We added comprehensive doctests to `create_cipher_map` (which previously had 0 doctests).
4. We verified that existing doctests for `remove_duplicates`, `encipher`, and `decipher` remain unchanged and pass.

---

## 2. Cyclomatic Complexity Metrics (Ruff C901 / McCabe)

Cyclomatic complexity measures the number of linearly independent paths through program source code. Running Ruff's McCabe complexity audit (`uvx ruff check --select C901 --config "lint.mccabe.max-complexity=1"`):

| Function | Complexity (Before) | Complexity (After) | Change | Details |
| :--- | :---: | :---: | :---: | :--- |
| **`main()`** | **2** | **1** | **-50%** | Removed `try/except` and dictionary branching; reduced to sequential I/O delegation. |
| **`process_cipher()`** | *N/A (new)* | **2** | *New* | Encapsulates input option normalization, validation (`if`), and dispatch. |
| **`create_cipher_map()`** | **3** | **3** | Unchanged | Retained algorithm structure while adding 7 doctests. |
| **`remove_duplicates()`** | **3** | **3** | Unchanged | Existing doctests untouched and passing. |
| **`encipher()`** | **1** | **1** | Unchanged | Existing doctests untouched and passing. |
| **`decipher()`** | **1** | **1** | Unchanged | Existing doctests untouched and passing. |

---

## 3. Test Coverage & Safety Net Comparison

Using `pytest --cov=ciphers.simple_keyword_cypher`:

| Metric | Before Refactoring | After Refactoring | Change |
| :--- | :---: | :---: | :---: |
| **Total Statements** | 37 | 39 | +2 |
| **Covered Statements** | 25 | 32 | **+7** |
| **Missed Statements** | 12 | 7 | **-5** |
| **Coverage Percentage** | **68%** | **82%** | **+14%** |
| **Total Doctests** | 4 | 15 | **+11 tests** |

### Doctest Distribution
- `remove_duplicates`: 1 test (unchanged)
- `encipher`: 1 test (unchanged)
- `decipher`: 2 tests (unchanged)
- `create_cipher_map`: **7 tests** (was 0: tests key generation, length 26, alphabet mapping, identity mapping)
- `process_cipher`: **4 tests** (new: encipher mode, decipher mode, case insensitivity, invalid option exception)

---

## 4. Architectural & Safety Benefits

1. **Separation of Concerns**:
   - `main()` strictly coordinates user interaction (`input()` prompts and displaying results).
   - `process_cipher()` handles string normalization, dictionary selection, error enforcement, and cipher pipeline delegation as a pure deterministic function.

2. **100% Backwards Compatibility**:
   - The CLI prompts in `main()` remain identical:
     - `"Enter message to encode or decode: "`
     - `"Enter keyword: "`
     - `"Encipher or decipher? E/D:"`
   - Exception behavior is preserved (`KeyError("invalid input option")` raised upon invalid option).
   - All existing function signatures (`remove_duplicates`, `create_cipher_map`, `encipher`, `decipher`) remain untouched.

3. **Linter & Style Compliance**:
   - Passes `uvx ruff check` with 0 warnings.
   - Passes `uvx ruff format --check`.
   - Passes `python3 scripts/validate_filenames.py`.
