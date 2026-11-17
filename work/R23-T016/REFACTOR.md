# Task R23-T016: Refactor `ciphers/xor_cipher.py`

## Overview
`ciphers/xor_cipher.py` originally repeated identical XOR transformation, key normalization, string building, and file I/O logic across multiple public methods:
1. `encrypt` and `decrypt` had identical code lines.
2. `encrypt_string` and `decrypt_string` repeated character-by-character accumulator loops.
3. `encrypt_file` and `decrypt_file` repeated file opening, line-by-line streaming, and error handling.

## Refactoring Changes
Extracted 3 shared private helpers:
1. `_normalize_key(self, key: int) -> int`: Validates integer key type, applies instance default key, and maps modulo 256.
2. `_xor_chars(self, content: str, key: int) -> list[str]`: Applies XOR transformation across characters in content.
3. `_transform_file(self, in_file: str, out_file: str, key: int) -> bool`: Consolidates file stream reading, line encryption, and exception handling for `encrypt_file` and `decrypt_file`.

The public methods now delegate directly to these helpers:
- `encrypt(content, key)` $\rightarrow$ `self._xor_chars(content, key)`
- `decrypt(content, key)` $\rightarrow$ `self._xor_chars(content, key)`
- `encrypt_string(content, key)` $\rightarrow$ `"".join(self._xor_chars(content, key))`
- `decrypt_string(content, key)` $\rightarrow$ `"".join(self._xor_chars(content, key))`
- `encrypt_file(file, key)` $\rightarrow$ `self._transform_file(file, "encrypt.out", key)`
- `decrypt_file(file, key)` $\rightarrow$ `self._transform_file(file, "decrypt.out", key)`

## Cyclomatic Complexity (McCabe C90 / C901) Before and After

Measured via `uvx ruff check --select C901 --config "lint.mccabe.max-complexity=1" ciphers/xor_cipher.py`:

| Method | Complexity Before | Complexity After | Status |
|---|---|---|---|
| `encrypt_file` | 3 | **1** | Reduced ($\mathbf{-67\%}$) |
| `decrypt_file` | 3 | **1** | Reduced ($\mathbf{-67\%}$) |
| `encrypt_string` | 2 | **1** | Reduced ($\mathbf{-50\%}$) |
| `decrypt_string` | 2 | **1** | Reduced ($\mathbf{-50\%}$) |
| `encrypt` | 1 | 1 | Unchanged |
| `decrypt` | 1 | 1 | Unchanged |
| `_transform_file` (new helper) | N/A | 3 | Extracted helper |
| `_xor_chars` (new helper) | N/A | 1 | Extracted helper |
| `_normalize_key` (new helper) | N/A | 1 | Extracted helper |

**Worst public method complexity reduced from 3 to 1.**

## Test Verification
- All 16 existing doctests across `encrypt`, `decrypt`, `encrypt_string`, and `decrypt_string` passed.
- `uv run pytest ciphers/xor_cipher.py`: 4 test items passed.
- `uvx ruff check ciphers/xor_cipher.py`: All checks passed.
- Public method names, parameter types, and signatures remain 100% backward compatible.
