"""
Benchmark comparing kth_largest_element, searches/quick_select.py, and
searches/median_of_medians.py on identical inputs.
"""

from __future__ import annotations

import random
import sys
import time
from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from data_structures.arrays.kth_largest_element import (  # noqa: E402
    kth_largest_element,
)
from searches.median_of_medians import (  # noqa: E402
    quick_select as qs_median_of_medians,
)
from searches.quick_select import quick_select as qs_random  # noqa: E402


def run_benchmarks() -> None:
    random.seed(42)
    sizes = [10, 100, 1000, 5000]
    repeats = 20

    print("=" * 80)
    print("BENCHMARK COMPARISON: k-th Selection Algorithms")
    print("=" * 80)
    print(
        f"{'Size (N)':<10} | {'kth_largest (ms)':<18} | "
        f"{'quick_select (ms)':<18} | {'median_of_medians (ms)':<22}"
    )
    print("-" * 80)

    for n in sizes:
        base_arr = [random.randint(0, 1_000_000) for _ in range(n)]
        k_largest = n // 2
        qs_idx = n - k_largest
        mom_rank = n - k_largest + 1

        # 1. kth_largest_element (Lomuto in-place partition)
        t_kth: list[float] = []
        for _ in range(repeats):
            arr = base_arr.copy()
            t0 = time.perf_counter()
            kth_largest_element(arr, k_largest)
            t_kth.append(time.perf_counter() - t0)
        avg_kth = (sum(t_kth) / len(t_kth)) * 1000

        # 2. searches/quick_select (3-way partition with random pivot)
        t_qs: list[float] = []
        for _ in range(repeats):
            arr = base_arr.copy()
            t0 = time.perf_counter()
            qs_random(arr, qs_idx)
            t_qs.append(time.perf_counter() - t0)
        avg_qs = (sum(t_qs) / len(t_qs)) * 1000

        # 3. searches/median_of_medians (Deterministic linear time pivot)
        t_mom: list[float] = []
        for _ in range(repeats):
            arr = base_arr.copy()
            t0 = time.perf_counter()
            qs_median_of_medians(arr, mom_rank)
            t_mom.append(time.perf_counter() - t0)
        avg_mom = (sum(t_mom) / len(t_mom)) * 1000

        print(f"{n:<10d} | {avg_kth:<18.4f} | {avg_qs:<18.4f} | {avg_mom:<22.4f}")


if __name__ == "__main__":
    run_benchmarks()
