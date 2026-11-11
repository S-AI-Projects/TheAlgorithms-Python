# R23-T054: ELU vs SELU vs Leaky ReLU

Files compared (all in `neural_network/activation_functions/`):
`exponential_linear_unit.py`, `scaled_exponential_linear_unit.py`,
`leaky_rectified_linear_unit.py`.
Evidence: `compare_test.py` (19 checks, all pass) and `bench_compare.py`.

## API differences
| | ELU | SELU | Leaky ReLU |
|---|---|---|---|
| Function | `exponential_linear_unit(vector, alpha)` | `scaled_exponential_linear_unit(vector, alpha=1.6732, lambda_=1.0507)` | `leaky_rectified_linear_unit(vector, alpha)` |
| Input arg | `vector` | `vector` | `vector` |
| `alpha` | required, no default | optional (default 1.6732) | required, no default |
| What alpha means | negative side saturates at `-alpha` | same as ELU | slope for negative inputs |
| Extra arg | none | `lambda_` (scale; trailing `_` because `lambda` is a Python keyword) | none |
| Positive side | `x` | `lambda_ * x` | `x` |
| Negative side | `alpha * (e^x - 1)` | `lambda_ * alpha * (e^x - 1)` | `alpha * x` |

All three are typed `np.ndarray -> np.ndarray` and use `np.where`. None validates
its input. A plain Python float is accepted by accident and returns a 0-d array
(`exponential_linear_unit(2.0, 0.3)` -> `array(2.)`); an int array returns floats.
The ELU docstring says `alpha >= 0` but this is not enforced (and NaN in gives NaN out).

## Results: where they agree
(`compare_test.py`, 14 shared inputs from -1000 to 700, alphas 0, 0.067, 0.3, 1.0, 1.6732)
- **ELU == SELU** exactly (`np.array_equal`) when SELU's `lambda_` is 1 and alpha is the same.
- **SELU defaults == 1.0507 * ELU(x, alpha=1.6732)** (`np.allclose`).
- **ELU == Leaky ReLU == x for every positive input**, for any alpha.
- **All three give 0 at x = 0.**
- They cannot agree on negative inputs: ELU curves toward `-alpha`, Leaky ReLU keeps a straight line of slope alpha.

## Edge values
| input | ELU(alpha=0.3) | Leaky ReLU(alpha=0.3) |
|---|---|---|
| 0 | 0 | 0 |
| -1 | -0.1896 | -0.3 |
| -1000 (large negative) | -0.3 (saturates at -alpha) | -300 (unbounded) |
| 700 | 700 | 700 |
| 1000 (large positive) | 1000, **but** `RuntimeWarning: overflow encountered in exp` | 1000, no warning |

The warning happens because `np.where` evaluates both branches: `exp(1000)` overflows
to `inf` in the unused negative branch. The returned value is still correct. Both ELU
and SELU have this; Leaky ReLU has no `exp`, so it does not. (Not changed in this PR,
which only adds doctests.)

## Speed
Min of 5 repeats, ms per call, random normal inputs (one run on a cloud machine, so
treat as rough):

| size | ELU | SELU | Leaky ReLU |
|---|---|---|---|
| 1,000 | 0.004 | 0.004 | 0.002 |
| 100,000 | 0.184 | 0.216 | 0.101 |
| 1,000,000 | 2.440 | 2.818 | 1.754 |

Leaky ReLU is fastest (no `exp`). SELU is a little slower than ELU because it does one
extra multiplication of the whole array.

## Recommendation for a beginner
**Leaky ReLU.** It is one line (`x` if positive else `alpha * x`), has no exponential,
no overflow warning, and is the fastest. Move to ELU when you want smooth negative
outputs that saturate; use SELU only when you want its self-normalising behaviour
with its fixed constants.
