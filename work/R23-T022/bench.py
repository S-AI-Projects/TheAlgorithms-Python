# ruff: noqa: INP001
"""Benchmarking and comparison counting for Exponential Search vs. Binary Search.

This script benchmarks the running time and counts exact element comparisons
for exponential search and binary search across multiple doubling input sizes.
"""

from __future__ import annotations

import sys
import timeit
from pathlib import Path

# Add repo root to sys.path so we can import searches.exponential_search
repo_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(repo_root))

from searches.exponential_search import exponential_search  # noqa: E402

# ==============================================================================
# Instrumented Implementations (Count Exact Element Comparisons)
# ==============================================================================


def binary_search_instrumented(
    sorted_collection: list[int], item: int
) -> tuple[int, int]:
    """Pure binary search instrumented to count element comparisons.

    Returns:
        (found_index, comparison_count)
    """
    comparisons = 0

    def _search(left: int, right: int) -> int:
        nonlocal comparisons
        if right < left:
            return -1
        midpoint = left + (right - left) // 2

        comparisons += 1
        if sorted_collection[midpoint] == item:
            return midpoint

        comparisons += 1
        if sorted_collection[midpoint] > item:
            return _search(left, midpoint - 1)
        else:
            return _search(midpoint + 1, right)

    found_idx = _search(0, len(sorted_collection) - 1)
    return found_idx, comparisons


def exponential_search_instrumented(
    sorted_collection: list[int], item: int
) -> tuple[int, int]:
    """Exponential search instrumented to count element comparisons.

    Returns:
        (found_index, comparison_count)
    """
    if not sorted_collection:
        return -1, 0

    comparisons = 1
    if sorted_collection[0] == item:
        return 0, comparisons

    bound = 1
    while bound < len(sorted_collection):
        comparisons += 1
        if not (sorted_collection[bound] < item):
            break
        bound *= 2

    left = bound // 2
    right = min(bound, len(sorted_collection) - 1)

    # Now binary search on the bounded range
    def _search(left_idx: int, right_idx: int) -> int:
        nonlocal comparisons
        if right_idx < left_idx:
            return -1
        midpoint = left_idx + (right_idx - left_idx) // 2
        comparisons += 1
        if sorted_collection[midpoint] == item:
            return midpoint
        comparisons += 1
        if sorted_collection[midpoint] > item:
            return _search(left_idx, midpoint - 1)
        else:
            return _search(midpoint + 1, right_idx)

    found_idx = _search(left, right)
    return found_idx, comparisons


# Uninstrumented pure search without O(n) list sorted validation check
# for clean algorithmic time profiling:
def pure_exponential_search(sorted_collection: list[int], item: int) -> int:
    if not sorted_collection:
        return -1
    if sorted_collection[0] == item:
        return 0
    bound = 1
    while bound < len(sorted_collection) and sorted_collection[bound] < item:
        bound *= 2
    left = bound // 2
    right = min(bound, len(sorted_collection) - 1)

    left_idx, right_idx = left, right
    while left_idx <= right_idx:
        mid_idx = left_idx + (right_idx - left_idx) // 2
        if sorted_collection[mid_idx] == item:
            return mid_idx
        elif sorted_collection[mid_idx] > item:
            right_idx = mid_idx - 1
        else:
            left_idx = mid_idx + 1
    return -1


def pure_binary_search(sorted_collection: list[int], item: int) -> int:
    left_idx, right_idx = 0, len(sorted_collection) - 1
    while left_idx <= right_idx:
        mid_idx = left_idx + (right_idx - left_idx) // 2
        if sorted_collection[mid_idx] == item:
            return mid_idx
        elif sorted_collection[mid_idx] > item:
            right_idx = mid_idx - 1
        else:
            left_idx = mid_idx + 1
    return -1


# ==============================================================================
# Benchmarking & Data Collection
# ==============================================================================


def run_benchmark() -> None:
    # 7 doubling sizes (minimum 6 required)
    sizes = [1000, 2000, 4000, 8000, 16000, 32000, 64000]

    print("=" * 80)
    print("EXPONENTIAL SEARCH VS BINARY SEARCH: COMPARISON COUNTS")
    print("=" * 80)
    print(
        f"{'Size (n)':>10} | {'Target Pos':>12} | {'Index (i)':>10} | "
        f"{'Exp Search':>12} | {'Bin Search':>12} | {'Ratio (Exp/Bin)':>15}"
    )
    print("-" * 80)

    comparison_results: dict[str, list[dict]] = {
        "start": [],
        "mid": [],
        "end": [],
        "absent": [],
    }

    for n in sizes:
        arr = list(range(n))

        test_cases = [
            ("start", 0, arr[0]),
            ("mid", n // 2, arr[n // 2]),
            ("end", n - 1, arr[n - 1]),
            ("absent", -1, n + 100),  # absent target
        ]

        for label, idx, target in test_cases:
            _exp_res, exp_comps = exponential_search_instrumented(arr, target)
            _bin_res, bin_comps = binary_search_instrumented(arr, target)

            ratio = exp_comps / bin_comps if bin_comps else 0.0
            comparison_results[label].append(
                {
                    "n": n,
                    "target": target,
                    "exp_comps": exp_comps,
                    "bin_comps": bin_comps,
                    "ratio": ratio,
                }
            )

            idx_str = str(idx) if idx >= 0 else "N/A"
            print(
                f"{n:>10} | {label:>12} | {idx_str:>10} | "
                f"{exp_comps:>12} | {bin_comps:>12} | {ratio:>15.2f}"
            )
        print("-" * 80)

    # --------------------------------------------------------------------------
    # Timing with timeit
    # --------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("RUNNING TIME (timeit) FOR MAIN FUNCTION exponential_search")
    print("=" * 80)

    number_of_runs = 200
    timing_results: dict[str, list[float]] = {
        "start": [],
        "mid": [],
        "end": [],
        "pure_start": [],
        "pure_mid": [],
        "pure_end": [],
        "pure_bin_start": [],
        "pure_bin_mid": [],
        "pure_bin_end": [],
    }

    for n in sizes:
        arr = list(range(n))
        target_start = arr[0]
        target_mid = arr[n // 2]
        target_end = arr[n - 1]

        # Time main repo function
        t_start = (
            timeit.timeit(
                lambda a=arr, t=target_start: exponential_search(a, t),
                number=number_of_runs,
            )
            / number_of_runs
            * 1e6
        )
        t_mid = (
            timeit.timeit(
                lambda a=arr, t=target_mid: exponential_search(a, t),
                number=number_of_runs,
            )
            / number_of_runs
            * 1e6
        )
        t_end = (
            timeit.timeit(
                lambda a=arr, t=target_end: exponential_search(a, t),
                number=number_of_runs,
            )
            / number_of_runs
            * 1e6
        )

        timing_results["start"].append(t_start)
        timing_results["mid"].append(t_mid)
        timing_results["end"].append(t_end)

        # Time pure search core (algorithmic execution without list validation)
        t_pure_start = (
            timeit.timeit(
                lambda a=arr, t=target_start: pure_exponential_search(a, t),
                number=number_of_runs * 10,
            )
            / (number_of_runs * 10)
            * 1e6
        )
        t_pure_mid = (
            timeit.timeit(
                lambda a=arr, t=target_mid: pure_exponential_search(a, t),
                number=number_of_runs * 10,
            )
            / (number_of_runs * 10)
            * 1e6
        )
        t_pure_end = (
            timeit.timeit(
                lambda a=arr, t=target_end: pure_exponential_search(a, t),
                number=number_of_runs * 10,
            )
            / (number_of_runs * 10)
            * 1e6
        )

        timing_results["pure_start"].append(t_pure_start)
        timing_results["pure_mid"].append(t_pure_mid)
        timing_results["pure_end"].append(t_pure_end)

        t_pure_bin_start = (
            timeit.timeit(
                lambda a=arr, t=target_start: pure_binary_search(a, t),
                number=number_of_runs * 10,
            )
            / (number_of_runs * 10)
            * 1e6
        )
        t_pure_bin_mid = (
            timeit.timeit(
                lambda a=arr, t=target_mid: pure_binary_search(a, t),
                number=number_of_runs * 10,
            )
            / (number_of_runs * 10)
            * 1e6
        )
        t_pure_bin_end = (
            timeit.timeit(
                lambda a=arr, t=target_end: pure_binary_search(a, t),
                number=number_of_runs * 10,
            )
            / (number_of_runs * 10)
            * 1e6
        )

        timing_results["pure_bin_start"].append(t_pure_bin_start)
        timing_results["pure_bin_mid"].append(t_pure_bin_mid)
        timing_results["pure_bin_end"].append(t_pure_bin_end)

        print(
            f"n={n:>6}: repo start={t_start:.2f}µs, mid={t_mid:.2f}µs, "
            f"end={t_end:.2f}µs | pure exp start={t_pure_start:.3f}µs, "
            f"mid={t_pure_mid:.3f}µs, end={t_pure_end:.3f}µs | "
            f"pure bin start={t_pure_bin_start:.3f}µs, "
            f"mid={t_pure_bin_mid:.3f}µs, end={t_pure_bin_end:.3f}µs"
        )

    # --------------------------------------------------------------------------
    # Plotting with matplotlib
    # --------------------------------------------------------------------------
    import matplotlib.pyplot as plt
    import numpy as np

    _fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Subplot 1: Comparison counts (Algorithmic Complexity)
    exp_start_comps = [d["exp_comps"] for d in comparison_results["start"]]
    exp_mid_comps = [d["exp_comps"] for d in comparison_results["mid"]]
    exp_end_comps = [d["exp_comps"] for d in comparison_results["end"]]

    bin_start_comps = [d["bin_comps"] for d in comparison_results["start"]]
    bin_mid_comps = [d["bin_comps"] for d in comparison_results["mid"]]
    bin_end_comps = [d["bin_comps"] for d in comparison_results["end"]]

    ax1.plot(
        sizes,
        exp_start_comps,
        "o-",
        color="tab:blue",
        label="Exponential Search (start: i=0)",
        linewidth=2,
    )
    ax1.plot(
        sizes,
        exp_mid_comps,
        "s--",
        color="tab:green",
        label="Exponential Search (mid: i=n/2)",
        linewidth=2,
    )
    ax1.plot(
        sizes,
        exp_end_comps,
        "^:",
        color="tab:red",
        label="Exponential Search (end: i=n-1)",
        linewidth=2,
    )

    ax1.plot(
        sizes,
        bin_start_comps,
        "o-.",
        color="tab:cyan",
        label="Binary Search (start: i=0)",
        alpha=0.7,
    )
    ax1.plot(
        sizes,
        bin_mid_comps,
        "s-.",
        color="tab:olive",
        label="Binary Search (mid: i=n/2)",
        alpha=0.7,
    )
    ax1.plot(
        sizes,
        bin_end_comps,
        "^--",
        color="tab:orange",
        label="Binary Search (end: i=n-1)",
        alpha=0.7,
    )

    # Theoretical reference curve
    n_dense = np.linspace(sizes[0], sizes[-1], 200)
    theoretical_log_n = 2 * np.log2(n_dense)
    ax1.plot(
        n_dense,
        theoretical_log_n,
        "k-.",
        label=r"Theoretical $2 \cdot \log_2(n)$",
        alpha=0.5,
    )

    ax1.set_xscale("log", base=2)
    ax1.set_xlabel(r"Input size $n$ ($\log_2$ scale)", fontsize=11)
    ax1.set_ylabel("Element Comparisons", fontsize=11)
    ax1.set_title(
        r"Element Comparisons vs. $n$ ($O(\log i)$ Empirical Proof)", fontsize=12
    )
    ax1.grid(True, which="both", linestyle="--", alpha=0.5)
    ax1.legend(loc="upper left", fontsize=9)

    # Subplot 2: Execution Time (Pure Algorithm vs n)
    ax2.plot(
        sizes,
        timing_results["pure_start"],
        "o-",
        color="tab:blue",
        label=r"Pure Exp Search (start: $i=0$) [$O(1)$]",
        linewidth=2,
    )
    ax2.plot(
        sizes,
        timing_results["pure_mid"],
        "s--",
        color="tab:green",
        label=r"Pure Exp Search (mid: $i=n/2$) [$O(\log i)$]",
        linewidth=2,
    )
    ax2.plot(
        sizes,
        timing_results["pure_end"],
        "^:",
        color="tab:red",
        label=r"Pure Exp Search (end: $i=n-1$) [$O(\log n)$]",
        linewidth=2,
    )

    ax2.plot(
        sizes,
        timing_results["pure_bin_start"],
        "o-.",
        color="tab:cyan",
        label=r"Pure Bin Search (start: $i=0$) [$O(\log n)$]",
        alpha=0.7,
    )
    ax2.plot(
        sizes,
        timing_results["pure_bin_mid"],
        "s-.",
        color="tab:olive",
        label=r"Pure Bin Search (mid: $i=n/2$) [$O(1)$]",
        alpha=0.7,
    )
    ax2.plot(
        sizes,
        timing_results["pure_bin_end"],
        "^--",
        color="tab:orange",
        label=r"Pure Bin Search (end: $i=n-1$) [$O(\log n)$]",
        alpha=0.7,
    )

    ax2.set_xscale("log", base=2)
    ax2.set_xlabel(r"Input size $n$ ($\log_2$ scale)", fontsize=11)
    ax2.set_ylabel("Execution Time (microseconds)", fontsize=11)
    ax2.set_title(r"Search Time vs. Input Size $n$", fontsize=12)
    ax2.grid(True, which="both", linestyle="--", alpha=0.5)
    ax2.legend(loc="upper left", fontsize=9)

    plt.tight_layout()
    output_png = Path(__file__).resolve().parent / "exponential_search_benchmark.png"
    plt.savefig(output_png, dpi=300)
    print(f"\nPlot saved successfully to: {output_png}")


if __name__ == "__main__":
    run_benchmark()
