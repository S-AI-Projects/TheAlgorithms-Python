# R23-T024 Findings: Robust Input Contract & Exception Handling for `decimal_to_negative_base_2`

## 1. Overview & Objective

The objective of Task **R23-T024** is to probe `maths/base_neg2_conversion.py` (`decimal_to_negative_base_2`) against bad, edge-case, and malformed inputs to identify silent failures, crashes, and obscure exceptions, and enforce a strict input contract as required by repository guidelines (`CONTRIBUTING.md`).

---

## 2. Input Probing Analysis (Old vs. New Behavior)

We probed the function with 14 distinct inputs covering booleans, fractional/integral floats, strings, empty values, NoneType, collections, complex numbers, negative numbers, and huge integers.

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

---

## 3. Failure Mode & Root Cause Analysis

### 1. Booleans (`True`, `False`)
* **Mechanism**: In Python, `bool` is a concrete subclass of `int` (`issubclass(bool, int) is True`). Consequently, `isinstance(True, int)` evaluates to `True`.
* **Flaw**: `decimal_to_negative_base_2(True)` passed directly into the division loop, performing base -2 division on `1` and returning `1`. `decimal_to_negative_base_2(False)` hit the `if num == 0:` guard and returned `0`.
* **Fix**: Explicitly check `isinstance(num, bool)` prior to general `int` check.

### 2. Floating-Point Numbers (`float`)
* **Mechanism**: When a non-zero float (e.g. `3.5` or `-2.5`) enters the loop, `divmod(num, -2)` returns float quotients and remainders (e.g. `rem = 1.5`, `rem = -0.5`). These float strings (`"1.0"`, `"1.5"`) are concatenated into `ans = "1.01.01.5"`.
* **Flaw**: The subsequent `int(ans)` conversion fails with an unhandled, confusing `ValueError: invalid literal for int() with base 10: '1.01.01.5'`, leaking internal implementation details. Furthermore, `0.0` satisfied `num == 0` and silently returned `0`.
* **Fix**: Check `not isinstance(num, int)` to immediately reject `float` with `TypeError("num must be an integer, not float")`.

### 3. Non-Numbers (`str`, `None`, collections)
* **Mechanism**: When passed into `divmod(num, -2)`, Python raises internal operand errors (`unsupported operand type(s) for divmod()`).
* **Fix**: Reject upfront with descriptive `TypeError: num must be an integer, not <type>`.

### 4. Huge Integers
* **Validation**: For large numbers like $10^{18}$, Python's arbitrary-precision integers correctly compute the negabinary expansion:
  $$\sum_{i=0}^{k} d_i (-2)^i = 10^{18}$$
  The expansion produces a 61-digit binary representation, which converts back to `int` safely within the standard string conversion limits.

---

## 4. Code Changes in `maths/base_neg2_conversion.py`

1. **Type Guard**:
   ```python
   if isinstance(num, bool) or not isinstance(num, int):
       raise TypeError(f"num must be an integer, not {type(num).__name__}")
   ```
2. **Docstring Enhancement**:
   * Added `num (int)` specification under `Args:`.
   * Added `Raises:` documentation.
   * Added doctests for `3.5` (float), `True` (bool), `"10"` (str), `None` (NoneType), and `10**18` (huge int).
   * All 4 original doctests (`0`, `-19`, `4`, `7`) remain intact and passing.
