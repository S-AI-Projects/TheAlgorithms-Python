# R23-T058: refactor `electronics/resistor_color_code.py` (no behaviour change)

## What was duplicated
`get_multiplier`, `get_tolerance`, `get_temperature_coeffecient` and `get_significant_digits`
each repeated the same pattern: "if the colour is not in this band's table, build an
error message and raise ValueError, otherwise return the table value". `check_validity` and
`calculate_resistance` were deeply nested with `None` placeholders and an if/else that could never reach its `else`.

## What changed
1. **New shared helper** `get_color_value(color, color_values, band_name)`: the one place that does the lookup and raises `ValueError(f"{color} is not a valid color for {band_name}")`. The four `get_*` functions now call it with their own band name, so every error message is character-for-character the same as before (including the original "coeffecient" spelling).
2. **`check_validity`**: nested `if/if/for/else/else` replaced by guard clauses (same three errors, same order, same messages). Nesting depth 4 -> 2.
3. **`calculate_resistance`**: guard clause instead of `if is_valid: ... else:`; removed the `tolerance_color`/`temperature_coeffecient_color` `None` placeholders and the redundant `str(...)` wrappers; read the optional bands directly (`if number_of_bands >= 4` / `== 6`); fixed the local variable typo `resisitance` -> `resistance`.
4. Public names, signatures, tables and all 24 original doctests are untouched. Two doctests were added for the new helper (26 total).

## Complexity (McCabe, `ruff check --select C901 --config 'lint.mccabe.max-complexity = 0'`)
| function | before | after |
|---|---|---|
| get_color_value (new) | - | 2 |
| get_significant_digits | 3 | 1 |
| get_multiplier | 2 | 1 |
| get_tolerance | 2 | 1 |
| get_temperature_coeffecient | 2 | 1 |
| get_band_type_count | 3 | 3 |
| check_validity | **5** | **5** |
| calculate_resistance | **5** | **3** |
| total | 22 | 17 |

The worst functions before were `check_validity` and `calculate_resistance` (both 5).
`calculate_resistance` (the longest function: 35 -> 25 lines of code) is now 3.
`check_validity` stays at 5 because its three error conditions and the colour loop are inherent;
it is flatter and easier to read, but the score does not drop. (Repo config allows up to 17, so
`ruff check --select C90` passed before and after.)

## Behaviour proof
- `python -m doctest -v electronics/resistor_color_code.py`: 24 passed before; 26 passed after (24 original + 2 new).
- `work/R23-T058/equivalence_test.py` (60 tests) loads the **original** file and the **refactored** one and compares results and exception type + message on: every colour in every getter (valid, invalid, empty, wrong case, `None`, `int`), all band counts, 5,000 random `check_validity` calls, 20,000 random `calculate_resistance` calls, all 12^3 three-band and 12^4 four-band colour combinations, and one input per `raise` statement. All pass. A deliberate one-word change to an error message makes 7 of them fail, so the test does detect differences.
- Raise paths: all 10 `raise` statements remain. The last one (`raise ValueError("Input is invalid")` in `calculate_resistance`) can never run, because `check_validity` returns True or raises; it was kept so behaviour and the raise count are unchanged.

## Coverage
Baseline and after output are in `coverage_before.txt` / `coverage_after.txt`. The same three statements are
uncovered before and after: the unreachable `raise ValueError("Input is invalid")` and the two lines of the
`if __name__ == "__main__":` block. The refactor reduced the file's statement count (about 74 -> 54 by a line tracer) without losing coverage.
