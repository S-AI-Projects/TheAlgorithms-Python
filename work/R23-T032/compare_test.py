# ruff: noqa: INP001
"""Compare the two fractional-knapsack implementations and benchmark both."""

from __future__ import annotations

import sys
from pathlib import Path
from statistics import median
from timeit import repeat

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from greedy_methods.fractional_knapsack import frac_knapsack
from greedy_methods.fractional_knapsack_2 import fractional_knapsack

Case = tuple[str, list[int], list[int], int, float, list[float], float]

CASES: tuple[Case, ...] = (
    ("partial last item", [60, 100, 120], [10, 20, 30], 50, 240, [1, 1, 2 / 3], 240),
    ("zero capacity", [60, 100, 120], [10, 20, 30], 0, 0, [0, 0, 0], 0),
    (
        "capacity above total weight",
        [60, 100, 120],
        [10, 20, 30],
        80,
        280,
        [1, 1, 1],
        280,
    ),
    (
        "capacity equals total weight",
        [60, 100, 120],
        [10, 20, 30],
        60,
        280,
        [1, 1, 1],
        280,
    ),
    ("single item partly fits", [10], [3], 1, 10 / 3, [1 / 3], 0),
    (
        "selection in original item order",
        [10, 40, 30, 50],
        [5, 4, 6, 3],
        8,
        95,
        [0, 1, 1 / 6, 1],
        95,
    ),
    ("empty input", [], [], 0, 0, [], 0),
    ("highest-ratio item partly fits", [5, 8], [5, 4], 1, 2, [0, 1 / 4], 0),
    ("mixed full and partial items", [5, 8, 20], [5, 4, 10], 7, 14, [0, 1, 0.3], 14),
    ("equal ratios", [12, 9, 20], [3, 3, 10], 9, 27, [1, 1, 0.3], 27),
)


def test_implementations_on_ten_shared_inputs() -> None:
    """Compare values and per-item fractions on ten positive-weight inputs."""
    assert len(CASES) == 10
    for (
        name,
        values,
        weights,
        capacity,
        expected_value,
        expected_fractions,
        expected_scalar_value,
    ) in CASES:
        detailed_value, fractions = fractional_knapsack(values, weights, capacity)
        scalar_value = frac_knapsack(values, weights, capacity, len(values))

        assert detailed_value == pytest.approx(expected_value), name
        assert fractions == pytest.approx(expected_fractions), name
        assert scalar_value == pytest.approx(expected_scalar_value), name
        if expected_value == expected_scalar_value:
            assert detailed_value == pytest.approx(scalar_value), name
        else:
            assert detailed_value != pytest.approx(scalar_value), name


def _run_detailed_cases() -> None:
    """Run the detailed-result implementation across the shared cases."""
    for _, values, weights, capacity, _, _, _ in CASES:
        fractional_knapsack(values, weights, capacity)


def _run_scalar_cases() -> None:
    """Run the scalar-result implementation across the shared cases."""
    for _, values, weights, capacity, _, _, _ in CASES:
        frac_knapsack(values, weights, capacity, len(values))


def benchmark() -> tuple[float, float]:
    """Return median microseconds per case for each implementation."""
    iterations = 20_000
    repeats = 5
    detailed_samples = repeat(_run_detailed_cases, number=iterations, repeat=repeats)
    scalar_samples = repeat(_run_scalar_cases, number=iterations, repeat=repeats)
    cases_per_sample = iterations * len(CASES)
    detailed_us = median(detailed_samples) * 1_000_000 / cases_per_sample
    scalar_us = median(scalar_samples) * 1_000_000 / cases_per_sample
    return detailed_us, scalar_us


if __name__ == "__main__":
    detailed_us, scalar_us = benchmark()
    print(f"fractional_knapsack_2: {detailed_us:.3f} us/case")
    print(f"fractional_knapsack.py: {scalar_us:.3f} us/case")
    print(f"scalar/detailed time ratio: {scalar_us / detailed_us:.2f}x")
