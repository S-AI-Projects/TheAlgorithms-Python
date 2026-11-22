### Describe your change

* [ ] Add an algorithm?
* [x] Fix a bug or typo in an existing algorithm?
* [x] Add or change doctests? -- Note: Please avoid changing both code and tests in a single pull request.
* [x] Documentation change?

### Checklist

* [x] I have read [CONTRIBUTING.md](https://github.com/TheAlgorithms/Python/blob/master/CONTRIBUTING.md).
* [x] This pull request is all my own work -- I have not plagiarized.
* [x] I know that pull requests will not be merged if they fail the automated tests.
* [x] This PR only changes one algorithm file. To ease review, please open separate PRs for separate algorithms.
* [x] All new Python files are placed inside an existing directory.
* [x] All filenames are in all lowercase characters with no spaces or dashes.
* [x] All functions and variable names follow Python naming conventions.
* [x] All function parameters and return values are annotated with Python [type hints](https://docs.python.org/3/library/typing.html).
* [x] All functions have [doctests](https://docs.python.org/3/library/doctest.html) that pass the automated testing.
* [x] All new algorithms include at least one URL that points to Wikipedia or another similar explanation.
* [ ] If this pull request resolves one or more open issues, then the description above includes the issue number(s) with a [closing keyword](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue): "Fixes #ISSUE-NUMBER".

---

## Description

This pull request completes **Task R23-T024**: establishing a strict input contract and robust exception handling for `decimal_to_negative_base_2` in `maths/base_neg2_conversion.py`.

Prior to this change:
- Bools (`True`/`False`) were silently treated as integers, returning `1` and `0`.
- Floats (`3.5`, `-2.5`) caused internal string accumulator crashes (`ValueError: invalid literal for int() with base 10: '1.01.01.5'`), and `0.0` silently bypassed type checks.
- Non-numbers (`str`, `None`, collections) triggered unhandled internal `divmod` TypeErrors.

We added an upfront type guard raising `TypeError: num must be an integer, not <type>`, added 5 new doctests covering floats, bools, strings, None, and huge ints, and preserved all 4 original doctests (`0`, `-19`, `4`, `7`).

## Type of Change

- [x] Bug Fix
- [ ] New Feature
- [ ] UI/UX Improvement
- [ ] Performance Improvement
- [x] Tests
- [x] Documentation
- [ ] Refactoring / Maintenance
- [ ] CI/CD

## Input Probing Analysis (Old vs. New Behavior)

| Input Category | Test Value | Original (Old) Behavior | New Behavior | Status / Resolution |
|---|---|---|---|---|
| **Boolean True** | `True` | `1` (returned value) | `TypeError: num must be an integer, not bool` | Fixed silent error |
| **Boolean False** | `False` | `0` (returned value) | `TypeError: num must be an integer, not bool` | Fixed silent error |
| **Float (positive fractional)** | `3.5` | `ValueError: invalid literal for int() with base 10: '1.01.01.5'` | `TypeError: num must be an integer, not float` | Fixed obscure crash |
| **Float (integral zero)** | `0.0` | `0` (returned value) | `TypeError: num must be an integer, not float` | Fixed silent type bypass |
| **Float (negative fractional)** | `-2.5` | `ValueError: invalid literal for int() with base 10: '1.01.0-0.01.5'` | `TypeError: num must be an integer, not float` | Fixed obscure crash |
| **String (numeric digits)** | `'10'` | `TypeError: unsupported operand type(s) for divmod(): 'str' and 'int'` | `TypeError: num must be an integer, not str` | Clear contract exception |
| **String (empty)** | `''` | `TypeError: unsupported operand type(s) for divmod(): 'str' and 'int'` | `TypeError: num must be an integer, not str` | Clear contract exception |
| **String (symbols)** | `'###'` | `TypeError: unsupported operand type(s) for divmod(): 'str' and 'int'` | `TypeError: num must be an integer, not str` | Clear contract exception |
| **NoneType** | `None` | `TypeError: unsupported operand type(s) for divmod(): 'NoneType' and 'int'` | `TypeError: num must be an integer, not NoneType` | Clear contract exception |
| **List collection** | `[1, 2]` | `TypeError: unsupported operand type(s) for divmod(): 'list' and 'int'` | `TypeError: num must be an integer, not list` | Clear contract exception |
| **Complex number** | `(1+2j)` | `TypeError: unsupported operand type(s) for divmod(): 'complex' and 'int'` | `TypeError: num must be an integer, not complex` | Clear contract exception |
| **Huge integer** | `10**18` | `1001000100001110010111111010011111000101001000000000000000000` | `1001000100001110010111111010011111000101001000000000000000000` | Supported & verified |
| **Negative integer** | `-19` | `111101` | `111101` | Preserved (existing doctest) |
| **Zero integer** | `0` | `0` | `0` | Preserved (existing doctest) |

## Changes Made

- `maths/base_neg2_conversion.py`:
  - Added input validation guard `if isinstance(num, bool) or not isinstance(num, int): raise TypeError(...)`.
  - Added `Raises: TypeError` section in docstring.
  - Added doctests for float (`3.5`), bool (`True`), string (`"10"`), None (`None`), and huge int (`10**18`).
  - All 4 original doctests (`0`, `-19`, `4`, `7`) preserved and passing.
- `work/R23-T024/`:
  - `probe_inputs.py`: Automated testing script comparing old vs. new behavior across 14 inputs.
  - `FINDINGS.md`: Complete theoretical explanation, failure mode root causes, and verification details.
  - `test_output.txt`: Test execution logs for doctests, pytest, ruff, and ty check.

## Testing & Verification

- `python3 -m doctest -v maths/base_neg2_conversion.py` -> 9/9 doctests passed.
- `uv run --with pytest pytest --doctest-modules maths/base_neg2_conversion.py` -> 1 passed in 0.02s.
- `uvx ruff check maths/base_neg2_conversion.py work/R23-T024/probe_inputs.py` -> All checks passed.
- `uvx ruff format --check maths/base_neg2_conversion.py work/R23-T024/probe_inputs.py` -> 2 files already formatted.
- `uvx ty check --exit-zero maths/base_neg2_conversion.py` -> 0 diagnostics.

## Additional Notes

- A second clean branch `student/E26B07F0850/R23-T024-upstream` (and `R23-T024-upstream`) containing only the changes in `maths/base_neg2_conversion.py` has been created and pushed for a later upstream PR.
