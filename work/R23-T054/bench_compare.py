"""Benchmark ELU, SELU and Leaky ReLU on the same inputs (R23-T054).

Run from the repo root:  python work/R23-T054/bench_compare.py
"""

import sys
import timeit

import numpy as np

sys.path.insert(0, ".")
from neural_network.activation_functions.exponential_linear_unit import (
    exponential_linear_unit,
)
from neural_network.activation_functions.leaky_rectified_linear_unit import (
    leaky_rectified_linear_unit,
)
from neural_network.activation_functions.scaled_exponential_linear_unit import (
    scaled_exponential_linear_unit,
)

rng = np.random.default_rng(0)
print("| size | elu (ms) | selu (ms) | leaky relu (ms) |")
print("|---|---|---|---|")
for n in (1_000, 100_000, 1_000_000):
    x = rng.normal(0, 3, n)
    reps = 200 if n <= 100_000 else 20
    t = [
        min(timeit.repeat(lambda f=f: f(x), number=reps, repeat=5)) / reps * 1000
        for f in (
            lambda v: exponential_linear_unit(v, 1.6732),
            scaled_exponential_linear_unit,
            lambda v: leaky_rectified_linear_unit(v, 0.01),
        )
    ]
    print(f"| {n:,} | {t[0]:.3f} | {t[1]:.3f} | {t[2]:.3f} |")
