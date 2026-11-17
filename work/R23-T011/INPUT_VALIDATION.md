# Task R23-T011: Harden `conversions/excel_title_to_column.py` Against Bad Input

## Problem Description
`conversions/excel_title_to_column.py` converts an Excel-style column title (e.g., `"A"` -> 1, `"AB"` -> 28) into its corresponding 1-based column number. Prior to hardening:
1. **Wrong Types (int, float, list, etc.)**: Crashed with unhandled `AttributeError: 'int' object has no attribute 'isalpha'`.
2. **`None` Input**: Was caught by `if not column_title`, incorrectly raising `ValueError: Column title must contain only alphabetic characters.` instead of `TypeError`.
3. **Non-ASCII Alphabetic Characters**: In Python, Unicode alphabetic characters such as `'α'` (Greek small alpha) pass `str.isalpha()`. The subsequent calculation `(ord(char) - 64)` evaluated to `(913 - 64) = 849`, silently producing an erroneous result.

## Input Probing & Comparison Table (12 Inputs Tested)

| Input | Description | Old Behavior | New Behavior | Status / Rationale |
|---|---|---|---|---|
| `""` | Empty string | `ValueError: Column title must contain only alphabetic characters.` | `ValueError: Column title must contain only alphabetic characters.` | Kept (existing raise unchanged) |
| `"a"` | Lowercase title | Returns `1` | Returns `1` | Kept (valid per docstring & existing doctests) |
| `"A1"` | Digits in title | `ValueError: Column title must contain only alphabetic characters.` | `ValueError: Column title must contain only alphabetic characters.` | Kept (existing raise unchanged) |
| `" A"` | Leading space | `ValueError: Column title must contain only alphabetic characters.` | `ValueError: Column title must contain only alphabetic characters.` | Handled via `ValueError` |
| `"ZZZZ"` | Large valid title | Returns `475254` | Returns `475254` | Valid title accepted |
| `123` | Integer (non-str) | `AttributeError: 'int' object has no attribute 'isalpha'` | `TypeError: column_title must be a str, got int` | Fixed: Raises clear `TypeError` |
| `None` | `NoneType` | `ValueError: Column title must contain only alphabetic characters.` | `TypeError: column_title must be a str, got NoneType` | Fixed: Raises clear `TypeError` |
| `['A']` | List (non-str) | `AttributeError: 'list' object has no attribute 'isalpha'` | `TypeError: column_title must be a str, got list` | Fixed: Raises clear `TypeError` |
| `"α"` | Greek letter alpha | Silently returned `849` (corrupt calculation) | `ValueError: Column title must contain only alphabetic characters.` | Fixed: Raises `ValueError` via `isascii()` check |
| `"A B"` | Internal space | `ValueError: Column title must contain only alphabetic characters.` | `ValueError: Column title must contain only alphabetic characters.` | Handled via `ValueError` |
| `-5` | Negative integer | `AttributeError: 'int' object has no attribute 'isalpha'` | `TypeError: column_title must be a str, got int` | Fixed: Raises clear `TypeError` |
| `3.14` | Float (non-str) | `AttributeError: 'float' object has no attribute 'isalpha'` | `TypeError: column_title must be a str, got float` | Fixed: Raises clear `TypeError` |

## Changes Made
1. **Input Contract Documentation**:
   - Documented in docstring that `column_title` must be an instance of `str`.
   - Documented that `column_title` must be a non-empty string of ASCII letters.
   - Documented that lowercase column titles are accepted and converted to uppercase.
2. **Type Checking**:
   - Added `if not isinstance(column_title, str): raise TypeError(...)`.
3. **ASCII Alphabetic Validation**:
   - Augmented validation to check `isascii()`, preventing silent bugs with non-ASCII Unicode characters.
4. **Doctests**:
   - Retained all 8 existing doctests and existing `ValueError` raise unchanged.
   - Added doctests covering invalid types (`int`, `NoneType`), whitespace (`" A"`), and non-ASCII character (`"\\u03b1"`).
