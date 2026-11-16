# ruff: noqa: INP001
"""Benchmark and measure memory for longest common substring implementations."""

from __future__ import annotations

import gc
import sys
import tracemalloc
from collections.abc import Callable
from pathlib import Path
from statistics import median
from timeit import Timer

import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from dynamic_programming.longest_common_substring import longest_common_substring

SIZES = (64, 128, 256, 512, 1024, 2048)
DOCTEST_INPUTS = (
    ("", ""),
    ("a", ""),
    ("", "a"),
    ("a", "a"),
    ("abcdef", "bcd"),
    ("abcdef", "xabded"),
    ("GeeksforGeeks", "GeeksQuiz"),
    ("abcdxyz", "xyzabcd"),
    ("zxabcdezy", "yzabcdezx"),
    ("OldSite:GeeksforGeeks.org", "NewSite:GeeksQuiz.com"),
    ("xyz", "axyz"),
    ("abc", "xyz"),
    ("abc", "zzabcx"),
)


def _full_table_reference(text1: str, text2: str) -> str:
    """Run the original full-table algorithm for before/after comparison."""
    if not (isinstance(text1, str) and isinstance(text2, str)):
        raise ValueError("longest_common_substring() takes two strings for inputs")
    if not text1 or not text2:
        return ""

    dp = [[0] * (len(text2) + 1) for _ in range(len(text1) + 1)]
    end_pos = 0
    max_length = 0
    for i in range(1, len(text1) + 1):
        for j in range(1, len(text2) + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                if dp[i][j] > max_length:
                    end_pos = i
                    max_length = dp[i][j]
    return text1[end_pos - max_length : end_pos]


def _verify_doctest_results() -> None:
    """Check the optimized function against the reference on valid examples."""
    for text1, text2 in DOCTEST_INPUTS:
        reference_result = _full_table_reference(text1, text2)
        optimized_result = longest_common_substring(text1, text2)
        if optimized_result != reference_result:
            message = (
                f"Results differ for {text1!r}, {text2!r}: "
                f"{reference_result!r} != {optimized_result!r}"
            )
            raise AssertionError(message)


def _measure_seconds(
    function: Callable[[str, str], str], text1: str, text2: str
) -> float:
    """Return median seconds per call over three autoranged timeit samples."""
    timer = Timer(lambda: function(text1, text2))
    iterations, _ = timer.autorange()
    samples = timer.repeat(repeat=3, number=iterations)
    return median(samples) / iterations


def _peak_memory_bytes(
    function: Callable[[str, str], str], text1: str, text2: str
) -> int:
    """Return peak traced memory for one function call."""
    gc.collect()
    tracemalloc.start()
    try:
        function(text1, text2)
        _, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    return peak


def _plot_timings(
    sizes: tuple[int, ...], reference_times: list[float], optimized_times: list[float]
) -> Path:
    """Plot measured times and a normalized quadratic reference curve."""
    expected_quadratic = [optimized_times[0] * (size / sizes[0]) ** 2 for size in sizes]
    figure, axis = plt.subplots()
    axis.loglog(sizes, reference_times, marker="o", label="original full table")
    axis.loglog(sizes, optimized_times, marker="o", label="optimized two rows")
    axis.loglog(sizes, expected_quadratic, "--", label="O(n²) reference")
    axis.set_xlabel("String length (n = m)")
    axis.set_ylabel("Median seconds per call")
    axis.set_title("Longest common substring runtime")
    axis.grid(True, which="both", alpha=0.25)
    axis.legend()
    figure.tight_layout()
    output_path = Path(__file__).with_name("benchmark.png")
    figure.savefig(output_path, dpi=160)
    plt.close(figure)
    return output_path


def benchmark() -> None:
    """Compare running time and peak memory before and after the optimization."""
    _verify_doctest_results()
    reference_times: list[float] = []
    optimized_times: list[float] = []

    print("n\toriginal (ms)\ttwo rows (ms)")
    for size in SIZES:
        text1 = "a" * size
        text2 = "a" * size
        if _full_table_reference(text1, text2) != longest_common_substring(
            text1, text2
        ):
            message = f"Results differ at input length {size}"
            raise AssertionError(message)
        reference_seconds = _measure_seconds(_full_table_reference, text1, text2)
        optimized_seconds = _measure_seconds(longest_common_substring, text1, text2)
        reference_times.append(reference_seconds)
        optimized_times.append(optimized_seconds)
        print(
            f"{size}\t{reference_seconds * 1000:.3f}\t\t{optimized_seconds * 1000:.3f}"
        )

    plot_path = _plot_timings(SIZES, reference_times, optimized_times)
    print(f"Timing plot: {plot_path}")

    memory_text = "a" * 2000
    reference_peak = _peak_memory_bytes(_full_table_reference, memory_text, memory_text)
    optimized_peak = _peak_memory_bytes(
        longest_common_substring, memory_text, memory_text
    )
    print(f"2,000 x 2,000 original peak: {reference_peak:,} bytes")
    print(f"2,000 x 2,000 two-row peak: {optimized_peak:,} bytes")
    print(f"Peak-memory reduction: {reference_peak / optimized_peak:.1f}x")


if __name__ == "__main__":
    benchmark()
