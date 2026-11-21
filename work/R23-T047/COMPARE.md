# Euler method comparison

## Interfaces

All three functions take the same positional arguments in the same order:
an ODE callable, initial value `y0`, initial position `x0`, step size, and
endpoint. The parameter names differ in `runge_kutta` (`f` and `h` rather than
`ode_func` and `step_size`), and only `explicit_euler` and `euler_modified`
annotate their arguments and NumPy-array return value. Each returns a NumPy
array containing the initial value and one value per step. Each computes the
number of steps with `ceil((x_end - x0) / h)`, so a non-divisible interval can
end past `x_end`.

The algorithms use one derivative evaluation per step for explicit Euler, two
for modified Euler (predictor-corrector/Heun), and four for classical RK4.

## Error results

For `dy/dx = y`, `y(0) = 1` on `[0, 1]`, the exact endpoint is `e`. The table
shows absolute endpoint error:

| Step size `h` | Explicit Euler | Modified Euler | Classical RK4 |
| ---: | ---: | ---: | ---: |
| 0.1 | 0.124539368359 | 0.004200981851 | 2.084323879e-6 |
| 0.05 | 0.064984123315 | 0.001090774104 | 1.358027100e-7 |
| 0.025 | 0.033217990069 | 0.000277884088 | 8.666190432e-9 |
| Observed order, `h=0.1` to `0.025` | 0.9533 | 1.9591 | 3.9550 |

The measured orders are close to the expected `O(h)`, `O(h**2)`, and `O(h**4)`.
Halving `h` reduces error by roughly `1/2`, `1/4`, and `1/16`, respectively.

## Speed results

The benchmark runs all three solvers on the same 11 shared inputs. It reports
the median of five measurements, each running 1,000 batches of all 11 inputs.
Times are microseconds per solver call:

| Solver | Median time |
| --- | ---: |
| Explicit Euler | 6.03 us |
| Modified Euler | 12.49 us |
| Classical RK4 | 17.72 us |

Measured on macOS arm64 with Python 3.15.0rc3 free-threading build. These short
runs are machine- and load-dependent; they show the relative cost for these
small test inputs, not a general performance guarantee.

## Recommendation for a beginner

Start with explicit Euler: its update is simplest to understand and fastest in
this comparison, while making the first-order accuracy tradeoff clear. Then
compare modified Euler's predictor-corrector improvement and RK4's much higher
accuracy per step when accuracy matters more than a small increase in work.

## Validation

- `uv run pytest work/R23-T047/compare_test.py` — passed (12 tests).
- `uv run pytest maths/euler_method.py maths/euler_modified.py maths/numerical_analysis/runge_kutta.py --doctest-modules` — passed (3 modules).
- `uvx ruff check maths/euler_method.py work/R23-T047/compare_test.py` — passed.
- `uvx ruff format --check maths/euler_method.py work/R23-T047/compare_test.py` — passed.
