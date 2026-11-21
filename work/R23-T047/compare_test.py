"""Compare Euler, modified Euler, and classical RK4 on shared inputs."""

import math
import statistics
import sys
from collections.abc import Callable
from pathlib import Path
from time import perf_counter

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from maths.euler_method import explicit_euler
from maths.euler_modified import euler_modified
from maths.numerical_analysis.runge_kutta import runge_kutta

type ODE = Callable[[float, float], float]
type InputCase = tuple[float, float, float, float]
type Solver = Callable[[ODE, float, float, float, float], np.ndarray]

SHARED_INPUTS: tuple[InputCase, ...] = (
    (1.0, 0.0, 0.1, 1.0),
    (1.0, 0.0, 0.05, 1.0),
    (1.0, 0.0, 0.025, 1.0),
    (2.0, 0.0, 0.1, 0.5),
    (-1.0, 0.0, 0.1, 0.5),
    (0.5, 0.0, 0.05, 0.5),
    (3.0, 0.2, 0.1, 0.7),
    (-2.0, 0.1, 0.05, 0.6),
    (1.5, -0.2, 0.1, 0.3),
    (0.25, 0.25, 0.05, 0.75),
    (-0.5, -0.5, 0.05, 0.0),
)

SOLVERS: tuple[tuple[str, Solver], ...] = (
    ("explicit_euler", explicit_euler),
    ("euler_modified", euler_modified),
    ("runge_kutta", runge_kutta),
)


def derivative(_x: float, y: float) -> float:
    """Return the derivative for dy/dx = y."""
    return y


@pytest.mark.parametrize(("y0", "x0", "step_size", "x_end"), SHARED_INPUTS)
def test_solvers_on_shared_inputs(
    y0: float, x0: float, step_size: float, x_end: float
) -> None:
    """All solvers accept common positional inputs and approximate exp(x)."""
    for _, solver in SOLVERS:
        values = solver(derivative, y0, x0, step_size, x_end)
        expected_steps = math.ceil((x_end - x0) / step_size)
        exact_values = [
            y0 * math.exp(index * step_size) for index in range(expected_steps + 1)
        ]

        assert isinstance(values, np.ndarray)
        assert len(values) == expected_steps + 1
        assert values[0] == y0
        assert values == pytest.approx(exact_values, rel=0.06, abs=1e-12)


def test_errors_show_expected_convergence_orders() -> None:
    """Halving h reduces global error by factors near 1/2, 1/4, and 1/16."""
    for _, solver in SOLVERS:
        errors = [
            abs(float(solver(derivative, 1.0, 0.0, step_size, 1.0)[-1]) - math.e)
            for step_size in (0.1, 0.05, 0.025)
        ]

        assert errors[0] > errors[1] > errors[2]
        ratio_1 = errors[1] / errors[0]
        ratio_2 = errors[2] / errors[1]

        if solver is explicit_euler:
            assert 0.45 < ratio_1 < 0.53
            assert 0.45 < ratio_2 < 0.53
        elif solver is euler_modified:
            assert 0.22 < ratio_1 < 0.28
            assert 0.22 < ratio_2 < 0.28
        else:
            assert 0.05 < ratio_1 < 0.08
            assert 0.05 < ratio_2 < 0.08


def benchmark_solvers(repeats: int = 5, batches: int = 1000) -> dict[str, float]:
    """Return median microseconds per solve over the same shared input cases."""
    timings: dict[str, float] = {}
    for name, solver in SOLVERS:
        samples = []
        for _ in range(repeats):
            start = perf_counter()
            for _ in range(batches):
                for case in SHARED_INPUTS:
                    solver(derivative, *case)
            samples.append(perf_counter() - start)
        timings[name] = (
            statistics.median(samples) * 1_000_000 / (batches * len(SHARED_INPUTS))
        )
    return timings


def main() -> None:
    """Print the benchmark medians for the shared inputs."""
    for name, microseconds in benchmark_solvers().items():
        print(f"{name}: {microseconds:.2f} us/solve")


if __name__ == "__main__":
    main()
