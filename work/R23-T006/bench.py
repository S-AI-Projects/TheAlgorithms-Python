"""
Benchmark script for data_structures/linked_list/merge_sort_linked_list.py (R23-T006).

Measures running time of merge_sort_linked_list across doubling input sizes
and compares with Python's built-in sorted() on the same values.
Plots both curves and saves the figure as benchmark_plot.png.
"""

from __future__ import annotations

import random
import sys
import time
from pathlib import Path

import matplotlib.pyplot as plt

# Ensure repo root is in sys.path
repo_root = Path(__file__).resolve().parent.parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from data_structures.linked_list.merge_sort_linked_list import (  # noqa: E402
    Node,
    merge_sort_linked_list,
)

# Increase recursion depth for deep linked lists
sys.setrecursionlimit(50000)


def list_to_linked_list(values: list[int]) -> Node | None:
    head: Node | None = None
    for val in reversed(values):
        head = Node(val, head)
    return head


def benchmark() -> None:
    random.seed(42)
    # 7 doubling input sizes: 50, 100, 200, 400, 800, 1600, 3200
    sizes = [50, 100, 200, 400, 800, 1600, 3200]
    repeats = 15

    ll_times: list[float] = []
    py_times: list[float] = []

    print("=" * 80)
    print("BENCHMARK: merge_sort_linked_list vs. Python sorted()")
    print("=" * 80)
    print(
        f"{'Size (N)':<10} | {'LL Merge Sort (ms)':<20} | "
        f"{'Python sorted() (ms)':<22} | {'Slowdown Ratio':<15}"
    )
    print("-" * 80)

    for n in sizes:
        base_vals = [random.randint(0, 1_000_000) for _ in range(n)]

        # Time merge_sort_linked_list
        t_ll: list[float] = []
        for _ in range(repeats):
            ll_head = list_to_linked_list(base_vals)
            start = time.perf_counter()
            merge_sort_linked_list(ll_head)
            end = time.perf_counter()
            t_ll.append(end - start)
        avg_ll = sum(t_ll) / len(t_ll)
        ll_times.append(avg_ll * 1000)  # ms

        # Time built-in sorted()
        t_py: list[float] = []
        for _ in range(repeats):
            copied = list(base_vals)
            start = time.perf_counter()
            sorted(copied)
            end = time.perf_counter()
            t_py.append(end - start)
        avg_py = sum(t_py) / len(t_py)
        py_times.append(avg_py * 1000)  # ms

        ratio = avg_ll / avg_py if avg_py > 0 else 0.0
        print(
            f"{n:<10d} | {avg_ll * 1000:<20.4f} | "
            f"{avg_py * 1000:<22.4f} | {ratio:<15.1f}x"
        )

    # Plot results
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, ll_times, marker="o", linewidth=2, label="Linked List Merge Sort")
    plt.plot(
        sizes,
        py_times,
        marker="s",
        linewidth=2,
        label="Python built-in sorted() (Timsort)",
    )

    plt.title(
        "Empirical Scaling: Linked List Merge Sort vs. Python sorted()",
        fontsize=14,
        fontweight="bold",
    )
    plt.xlabel("Input Size (Number of Elements N)", fontsize=12)
    plt.ylabel("Execution Time (milliseconds)", fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(fontsize=11)

    plot_path = Path(__file__).resolve().parent / "benchmark_plot.png"
    plt.tight_layout()
    plt.savefig(plot_path, dpi=300)
    plt.close()
    print(f"\nBenchmark plot saved successfully to: {plot_path}")


if __name__ == "__main__":
    benchmark()
