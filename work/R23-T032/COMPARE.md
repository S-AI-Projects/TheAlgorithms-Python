# Fractional-knapsack implementation comparison

The comparison script tests both implementations on the same ten
positive-weight inputs. It compares total values and records each detailed
implementation's per-item fractions in [compare_test.py](./compare_test.py).

## API differences

| Implementation | Call shape | Result | Main approach |
|---|---|---|---|
| `greedy_methods/fractional_knapsack_2.py` | `fractional_knapsack(value, weight, capacity)`; annotated parameters | `(total_value, fractions)`; fractions are returned in the original item order | Sort value/weight ratios, then greedily fill the remaining capacity |
| `greedy_methods/fractional_knapsack.py` | `frac_knapsack(vl, wt, w, n)`; parameters are unannotated and `n` is required | Total value only | Sort item pairs, accumulate weights, and use `bisect` to find the full-item prefix |

Both use descending value-to-weight ratio. Neither validates mismatched list
lengths or zero weights. The first implementation annotates weights as
integers, although its own doctest also uses fractional weights.

## Shared results

`fractional_knapsack_2.py` is shown as `(value, fractions)` and the scalar
implementation as its total value.

| Input values | Weights | Capacity | Detailed result | Scalar result |
|---|---|---:|---|---:|
| `[60, 100, 120]` | `[10, 20, 30]` | 50 | `(240, [1, 1, 2/3])` | 240 |
| `[60, 100, 120]` | `[10, 20, 30]` | 0 | `(0, [0, 0, 0])` | 0 |
| `[60, 100, 120]` | `[10, 20, 30]` | 80 | `(280, [1, 1, 1])` | 280 |
| `[60, 100, 120]` | `[10, 20, 30]` | 60 | `(280, [1, 1, 1])` | 280 |
| `[10]` | `[3]` | 1 | `(10/3, [1/3])` | 0 — mismatch |
| `[10, 40, 30, 50]` | `[5, 4, 6, 3]` | 8 | `(95, [0, 1, 1/6, 1])` | 95 |
| `[]` | `[]` | 0 | `(0, [])` | 0 |
| `[5, 8]` | `[5, 4]` | 1 | `(2, [0, 1/4])` | 0 — mismatch |
| `[5, 8, 20]` | `[5, 4, 10]` | 7 | `(14, [0, 1, 0.3])` | 14 |
| `[12, 9, 20]` | `[3, 3, 10]` | 9 | `(27, [1, 1, 0.3])` | 27 |

The two mismatches occur when the capacity cannot fit even the highest-ratio
item completely. The scalar implementation's `bisect` returns a zero-length
full-item prefix and its `k == 0` branch returns zero, omitting the fractional
first item. The detailed implementation correctly takes that fraction. The
algorithm under change is therefore not patched to reproduce the incorrect
scalar result; a doctest now guards the partial-first-item behavior. Doctests
also cover zero capacity and capacity above total weight.

## Benchmark

The comparison script timed both functions over the same ten inputs, in
20,000 batches per repeat and five repeats per run. Across two runs with the
project's Python 3.15.2 free-threaded environment, the median times were about
0.53 microseconds per case for `fractional_knapsack_2.py` and 0.57
microseconds per case for `fractional_knapsack.py` (about 1.07x scalar /
detailed). This is a tiny-input microbenchmark; the difference is small and
should not be treated as a general performance advantage. The detailed
implementation additionally constructs and returns the fraction list.

## Recommendation

For a beginner, `fractional_knapsack_2.py` is the clearer starting point: its
three-argument interface is shorter, and the per-item fractions make each
greedy choice visible. The scalar implementation is compact, but its extra
`n` argument and prefix/binary-search logic obscure the partial-item case
where the current implementation disagrees.
