# Input Hardening & Vulnerability Analysis: `ciphers/caesar_cipher.py` (R23-T008)

## 1. Executive Summary

In adherence to CONTRIBUTING.md standards and Task R23-T008 requirements, `ciphers/caesar_cipher.py` has been audited and hardened against invalid, malformed, and boundary inputs.

Previously, `ciphers/caesar_cipher.py` lacked explicit type and value validation, leading to silent logical errors (such as irreversible encryption with repeated-character alphabets), obscure downstream runtime crashes (`TypeError: string indices must be integers`), or unhandled edge cases. This hardening establishes a strict input contract, adds explicit exception handling with descriptive error messages, preserves backwards-compatible fallback behavior, and extends the test suite to 19 passing doctests without altering existing baseline doctests.

---

## 2. Table of Bad / Boundary Inputs: Old vs. New Behavior

The following table documents 9 probed inputs to `encrypt` and `decrypt`, detailing their root causes, prior vulnerabilities, and hardened behavior:

| # | Probed Input / Condition | Example Input Call | Baseline / Old Behavior | Hardened / New Behavior | Rationale / Resolution |
|:--|:---|:---|:---|:---|:---|
| 1 | **Float Key** | `encrypt("hello", 2.5)` | Obscure runtime crash: `(index + 2.5) % len` yields a `float`, crashing at `alpha[float]` with `TypeError: string indices must be integers, not float`. | Raises `TypeError("key must be an integer")` immediately. | Caesar cipher relies on discrete character permutation index shifts; fractional shifts are mathematically and structurally invalid. |
| 2 | **Boolean Key** | `encrypt("hello", True)` | Silent logic failure: Python treats `True` as `1` (`isinstance(True, int) == True`), shifting text by 1 without warning. | Raises `TypeError("key must be an integer")`. | Boolean flags must not masquerade as shift values. Explicit check `not isinstance(key, int) or isinstance(key, bool)` rejects booleans. |
| 3 | **Non-String Input Message** | `encrypt(123, 5)` | Crashing loop: `for character in 123` raises uninformative `TypeError: 'int' object is not iterable`. | Raises `TypeError("input_string must be a string")`. | Clarifies function contract at entry before processing commences. |
| 4 | **Alphabet with Repeated Characters** | `encrypt("hello", 5, "aba")` | **Silent data corruption**: `alpha.index(character)` always returns the first occurrence of duplicate characters (`'a' -> 0`), causing character collisions and preventing `decrypt` from inverting `encrypt`. | Raises `ValueError("alphabet must contain unique characters")`. | Bijective mapping requires all alphabet symbols to be unique; non-unique alphabets corrupt ciphertext irreversibly. |
| 5 | **Non-String Custom Alphabet** | `encrypt("hello", 5, 123)` | Runtime crash in boolean fallback evaluation or iteration: `character not in 123` raises `TypeError: argument of type 'int' is not iterable`. | Raises `TypeError("alphabet must be a string or None")`. | Custom alphabet must strictly be a string sequence or `None`. |
| 6 | **Empty Alphabet Fallback** | `encrypt("hello", 5, "")` | `alpha = alphabet or ascii_letters` evaluates to `ascii_letters`, silently substituting the default alphabet. | **Preserved and documented**: Returns valid ciphertext `'mjqqt'` using `ascii_letters`. | Adheres to repository specification requiring empty alphabet string fallback to be documented and tested in docstrings. |
| 7 | **Explicit `None` Alphabet** | `encrypt("hello", 5, None)` | Evaluates `None or ascii_letters`, using `ascii_letters`. | **Preserved**: Correctly defaults to standard 52-character `ascii_letters`. | Default parameter behavior specified in function signature. |
| 8 | **Negative Integer Key** | `encrypt("hello", -5)` | Computes `(index - 5) % 52`, shifting backwards along the alphabet. | **Preserved and tested**: Returns `'cZggj'`. | Valid mathematical shift; modular arithmetic `(idx + key) % len` natively supports negative offsets. |
| 9 | **Large Integer Key ($> \text{len}$)** | `encrypt("A very large key", 8000)` | Modulo reduction `(idx + 8000) % 52` wraps around the alphabet cleanly. | **Preserved and tested**: Returns `'s nWjq dSjYW cWq'`. | Modular arithmetic natively guarantees period invariance for any integer shift size. |

---

## 3. Empty-Alphabet Fallback Analysis

The expression:
```python
alpha = alphabet or ascii_letters
```
allows `alphabet=""` or `alphabet=None` to evaluate to `ascii_letters`.

### Decision:
The fallback behavior is **retained** because:
1. `None` is the declared default parameter value in the function signature `alphabet: str | None = None`.
2. An empty string `""` passed as an alphabet contains zero valid substitution characters; falling back to `ascii_letters` provides a safe, non-crashing default consistent with existing client expectations.
3. The behavior has been explicitly formalized in the function docstrings and verified with targeted doctests (`>>> encrypt('hello', 5, '')` $\to$ `'mjqqt'`).

---

## 4. Test Verification & Suite Integrity

All test runs passed with zero errors:

1. **Doctest Validation**:
   ```bash
   uv run python -m doctest -v ciphers/caesar_cipher.py
   # 19 tests in 4 items. 19 passed. Test passed.
   ```
   - `encrypt`: 10 doctests (3 baseline + 7 hardening tests).
   - `decrypt`: 7 doctests (3 baseline + 4 hardening tests).
   - `brute_force`: 2 doctests (100% baseline compatibility preserved).

2. **Pytest Suite**:
   ```bash
   uv run pytest ciphers/caesar_cipher.py
   # 3 passed in 0.05s
   ```

3. **Style & Static Analysis**:
   ```bash
   uvx ruff check ciphers/caesar_cipher.py
   python3 scripts/validate_filenames.py
   # All checks passed!
   ```
