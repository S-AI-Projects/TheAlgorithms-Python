# R23-T053: bad inputs for ciphers/porta_cipher.py

Probe script: `work/R23-T053/probe_bad_inputs.py` (run from the repo root).
"Before" is the original code (no `raise` statements); "After" is with validation.

| # | Input | Function | Before | After |
|---|---|---|---|---|
| 1 | empty key `('', 'hello')` | `encrypt` | raises `IndexError: list index out of range` | raises `ValueError: key must not be empty` |
| 2 | digits in key `('ab1', 'hello')` | `encrypt` | raises `KeyError: '1'` | raises `ValueError: key must contain only the letters A-Z, found '1'` |
| 3 | space in key `('my key', 'hello')` | `encrypt` | raises `KeyError: ' '` | raises `ValueError: key must contain only the letters A-Z, found ' '` |
| 4 | non-ASCII letter in key `('clé', 'hello')` | `encrypt` | raises `KeyError: 'É'` | raises `ValueError: key must contain only the letters A-Z, found 'é'` |
| 5 | german sharp s in key `('ß', 'hello')` | `encrypt` | returns `'YVPPK'` | raises `ValueError: key must contain only the letters A-Z, found 'ß'` |
| 6 | key is None `(None, 'hello')` | `encrypt` | raises `AttributeError: 'NoneType' object has no attribute 'upper'` | raises `TypeError: key must be a str, not NoneType` |
| 7 | key is int `(123, 'hello')` | `encrypt` | raises `AttributeError: 'int' object has no attribute 'upper'` | raises `TypeError: key must be a str, not int` |
| 8 | key is bytes `(b'key', 'hello')` | `encrypt` | raises `KeyError: 75` | raises `TypeError: key must be a str, not bytes` |
| 9 | text is None `('key', None)` | `encrypt` | raises `AttributeError: 'NoneType' object has no attribute 'upper'` | raises `TypeError: words must be a str, not NoneType` |
| 10 | text has a space `('key', 'hello world')` | `encrypt` | raises `ValueError: substring not found` | raises `ValueError: words must contain only the letters A-Z, found ' '` |
| 11 | text has digits `('key', 'abc123')` | `encrypt` | raises `ValueError: substring not found` | raises `ValueError: words must contain only the letters A-Z, found '1'` |
| 12 | empty text, valid key `('key', '')` | `encrypt` | returns `''` | returns `''` |
| 13 | mixed-case key and text `('MaRvIn', 'JeSsIcA')` | `encrypt` | returns `'QRACRWU'` | returns `'QRACRWU'` |
| 14 | generate_table(empty key) `('',)` | `generate_table` | returns `[]` | raises `ValueError: key must not be empty` |
| 15 | generate_table(None) `(None,)` | `generate_table` | raises `AttributeError: 'NoneType' object has no attribute 'upper'` | raises `TypeError: key must be a str, not NoneType` |
| 16 | decrypt, empty key `('', 'QRACRWU')` | `decrypt` | raises `IndexError: list index out of range` | raises `ValueError: key must not be empty` |
| 17 | decrypt, text has digit `('marvin', 'QRA1')` | `decrypt` | raises `ValueError: substring not found` | raises `ValueError: words must contain only the letters A-Z, found '1'` |
| 18 | very long key (10**6 letters) `('<long>', 'hi')` | `encrypt` | returns `'UV'` | returns `'UV'` |

## Decisions
- **Key** must be a non-empty `str` of ASCII letters A-Z / a-z (case is ignored). Anything else raises: wrong type -> `TypeError`; empty or non-letter character -> `ValueError` naming the bad character.
- **Text** (`words`) must be a `str` of ASCII letters; same errors. Spaces, digits and punctuation are not supported by the cipher tables, so they now raise a clear `ValueError` instead of `ValueError: substring not found`. An empty text is valid and returns `''`.
- `ß` is rejected. Before, `'ß'.upper()` is `'SS'`, so a one-letter key silently became a two-letter key and gave a different cipher text than the user expects (row 5). Requiring ASCII letters closes this.
- Mixed case stays valid (row 13): input is upper-cased.
- A very long key still works (row 18); no limit was added.

## Why TypeError vs ValueError
Wrong type (`None`, `int`, `bytes`) -> `TypeError`; right type but unusable content (empty, digit, space, non-ASCII) -> `ValueError`, as CONTRIBUTING.md and the Python convention suggest.
