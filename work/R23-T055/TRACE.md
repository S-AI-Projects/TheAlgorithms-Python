# R23-T055: tracing `maths/chinese_remainder_theorem.py`

How to reproduce (from the repo root):

    python -m pdb work/R23-T055/trace_driver.py
    (Pdb) b /full/path/to/maths/chinese_remainder_theorem.py:32     # the `return (y, x - k * y)` line
    (Pdb) c
    (Pdb) p (a, b, x, y, k)
    (Pdb) c                                                        # repeat

The values below were read at that breakpoint with pdb and also checked by hand.
`extended_euclid(a, b)` returns `(x, y)` with `a*x + b*y = gcd(a, b)`.

## 1. `extended_euclid(10, 6)`

Going down (each call recurses on `(b, a % b)`):

| call | a | b | a % b | next call |
|---|---|---|---|---|
| 1 | 10 | 6 | 4 | (6, 4) |
| 2 | 6 | 4 | 2 | (4, 2) |
| 3 | 4 | 2 | 0 | (2, 0) |
| 4 | 2 | 0 | - | base case, returns `(1, 0)` |

Coming back up (`k = a // b`, returns `(y, x - k*y)`, where `(x, y)` is what the deeper call returned):

| call | a | b | x (from below) | y (from below) | k | returns (y, x - k*y) | check a*x' + b*y' |
|---|---|---|---|---|---|---|---|
| 4 | 2 | 0 | | | | (1, 0) | 2*1 + 0*0 = 2 |
| 3 | 4 | 2 | 1 | 0 | 2 | (0, 1) | 4*0 + 2*1 = 2 |
| 2 | 6 | 4 | 0 | 1 | 1 | (1, -1) | 6*1 + 4*(-1) = 2 |
| 1 | 10 | 6 | 1 | -1 | 1 | (-1, 2) | 10*(-1) + 6*2 = 2 |

Result `(-1, 2)`. Every row ends at 2, because gcd(10, 6) = 2.

## 2. `chinese_remainder_theorem(5, 1, 7, 3)`

First `extended_euclid(5, 7)`:

| call | a | b | x (from below) | y (from below) | k = a // b | returns (y, x - k*y) | check |
|---|---|---|---|---|---|---|---|
| 5 | 1 | 0 | | | | (1, 0) | 1*1 = 1 |
| 4 | 2 | 1 | 1 | 0 | 2 | (0, 1) | 2*0 + 1*1 = 1 |
| 3 | 5 | 2 | 0 | 1 | 2 | (1, -2) | 5*1 + 2*(-2) = 1 |
| 2 | 7 | 5 | 1 | -2 | 1 | (-2, 3) | 7*(-2) + 5*3 = 1 |
| 1 | 5 | 7 | -2 | 3 | 0 | (3, -2) | 5*3 + 7*(-2) = 1 |

(Call order going down: (5,7) -> (7,5) -> (5,2) -> (2,1) -> (1,0).)
So `x, y = 3, -2`.

Then the CRT formula, with `n1=5, r1=1, n2=7, r2=3`:

| step | value |
|---|---|
| m = n1 * n2 | 35 |
| n = r2*x*n1 + r1*y*n2 | 3*3*5 + 1*(-2)*7 = 45 - 14 = 31 |
| (n % m + m) % m | (31 + 35) % 35 = 31 |

Check: 31 % 5 = 1 and 31 % 7 = 3, both correct.

## Observations turned into doctests
- Intermediate results of the (10, 6) trace: `extended_euclid(2, 0) == (1, 0)`, `extended_euclid(4, 2) == (0, 1)`, `extended_euclid(6, 4) == (1, -1)`.
- `10*x + 6*y == 2` (the gcd, not 1) for `extended_euclid(10, 6)`.
- `extended_euclid(5, 7) == (3, -2)` and the first step has `k = 0` (it just swaps the arguments).
- `chinese_remainder_theorem(5,1,7,3) % 5, % 7 == (1, 3)`.
- Non-coprime input: see below.

## What surprised me
The existing doctest `chinese_remainder_theorem(6, 1, 4, 3) -> 14` looks like a normal
passing example but **14 is wrong**: 14 % 6 = 2 (not 1) and 14 % 4 = 2 (not 3).
6 and 4 are not coprime (gcd 2), so `extended_euclid(6, 4)` gives `(1, -1)` with
`6*1 + 4*(-1) = 2` instead of 1, and the formula `n = r2*x*n1 + r1*y*n2` only works when
that sum is 1: here n = 3*1*6 + 1*(-1)*4 = 14. A real answer exists (7 satisfies
7 % 6 = 1 and 7 % 4 = 3, valid modulo lcm = 12), but this implementation does not find it.
The algorithm's own docstring says "If GCD(a,b) = 1", so non-coprime input is outside the
contract, and the function silently returns a wrong number instead of raising.
I did not change the code (this task is doctests only); the new doctests document the
behaviour, and a future change could raise `ValueError` when `gcd(n1, n2) != 1`.
