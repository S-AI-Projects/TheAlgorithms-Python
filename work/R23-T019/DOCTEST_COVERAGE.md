# Task R23-T019: Complete the Doctests in `strings/is_isogram.py`

## Overview
Enhanced doctest suite for `is_isogram(string: str)` in `strings/is_isogram.py`, elevating test coverage to 100% and fulfilling CONTRIBUTING.md standards for valid, boundary, and erroneous inputs.

## Input Categories Tested
1. **Valid Isograms**:
   - `'Uncopyrightable'` $\rightarrow$ `True` (standard multi-syllable isogram).
2. **Repeated Characters (Non-isograms)**:
   - `'allowance'` $\rightarrow$ `False` (repeated lowercase 'a' and 'l').
3. **Mixed-Case Repeated Characters**:
   - `'Alphabet'` $\rightarrow$ `False` ('A' and 'a' repeat case-insensitively).
4. **Boundary Condition (Empty String)**:
   - `''` $\rightarrow$ `True` (vacuously true: no letter repeats).
5. **Erroneous Inputs (Non-alphabetic Characters)**:
   - `'copy1'` $\rightarrow$ raises `ValueError: String must only contain alphabetic characters.`
   - `'six-year-old'` $\rightarrow$ raises `ValueError: String must only contain alphabetic characters.`

## Doctest Output Summary
```
Trying:
    is_isogram('Uncopyrightable')
Expecting:
    True
ok
Trying:
    is_isogram('allowance')
Expecting:
    False
ok
Trying:
    is_isogram('Alphabet')
Expecting:
    False
ok
Trying:
    is_isogram('')
Expecting:
    True
ok
Trying:
    is_isogram('copy1')
Expecting:
    Traceback (most recent call last):
     ...
    ValueError: String must only contain alphabetic characters.
ok
Trying:
    is_isogram('six-year-old')
Expecting:
    Traceback (most recent call last):
     ...
    ValueError: String must only contain alphabetic characters.
ok
1 item had no tests:
    is_isogram
1 item passed all tests:
   6 tests in is_isogram.is_isogram
6 tests in 2 items.
6 passed.
Test passed.
```

## Coverage Report
Command:
```bash
uv run pytest strings/is_isogram.py --cov=strings.is_isogram --cov-report=term-missing
```
Report:
```
Name                    Stmts   Miss  Cover   Missing
-----------------------------------------------------
strings/is_isogram.py       5      0   100%
-----------------------------------------------------
TOTAL                       5      0   100%
```
Achieved **100% test coverage**.
