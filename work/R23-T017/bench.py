"""Benchmark and scaling analysis for sorts/pigeon_sort.py (Task R23-T017)."""

import os
import random
import sys
import timeit

# Ensure repository root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import matplotlib.pyplot as plt
from sorts.pigeon_sort import pigeon_sort


def benchmark_varying_n():
    """Benchmark pigeon_sort with varying n and fixed range (range = 1,000)."""
    sizes = [1000, 2000, 4000, 8000, 16000, 32000]
    fixed_range = 1000
    times = []

    print("\n--- Varying n with Fixed Range (R = 1,000) ---")
    print(f"{'n':<10} | {'Time (ms)':<12}")
    print("-" * 25)
    for n in sizes:
        arr = [random.randint(0, fixed_range) for _ in range(n)]
        # Measure 20 runs
        timer = timeit.Timer(lambda a=arr: pigeon_sort(list(a)))
        elapsed_ms = (timer.timeit(number=20) / 20) * 1000
        times.append(elapsed_ms)
        print(f"{n:<10} | {elapsed_ms:<12.3f}")

    return sizes, times


def benchmark_varying_range():
    """Benchmark pigeon_sort with fixed n (n = 5,000) and varying range."""
    fixed_n = 5000
    ranges = [1000, 2000, 4000, 8000, 16000, 32000]
    times = []

    print("\n--- Varying Range with Fixed n (n = 5,000) ---")
    print(f"{'Range':<10} | {'Time (ms)':<12}")
    print("-" * 25)
    for r in ranges:
        arr = [random.randint(0, r) for _ in range(fixed_n)]
        timer = timeit.Timer(lambda a=arr: pigeon_sort(list(a)))
        elapsed_ms = (timer.timeit(number=20) / 20) * 1000
        times.append(elapsed_ms)
        print(f"{r:<10} | {elapsed_ms:<12.3f}")

    return ranges, times


def generate_plots(sizes, times_n, ranges, times_r, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

    # Plot 1: Varying n
    ax1.plot(sizes, times_n, marker="o", color="blue", label="Measured time")
    ax1.set_title("Varying n (Fixed Range = 1,000)")
    ax1.set_xlabel("Input Size (n)")
    ax1.set_ylabel("Execution Time (ms)")
    ax1.grid(True, linestyle="--", alpha=0.6)
    ax1.legend()

    # Plot 2: Varying range
    ax2.plot(ranges, times_r, marker="s", color="red", label="Measured time")
    ax2.set_title("Varying Range (Fixed n = 5,000)")
    ax2.set_xlabel("Value Range (max - min)")
    ax2.set_ylabel("Execution Time (ms)")
    ax2.grid(True, linestyle="--", alpha=0.6)
    ax2.legend()

    plt.tight_layout()
    plot_path = os.path.join(output_dir, "pigeon_sort_benchmarks.png")
    fig.savefig(plot_path, dpi=150)
    print(f"\nSaved scaling benchmark plots to: {plot_path}")


if __name__ == "__main__":
    random.seed(42)
    output_directory = os.path.dirname(os.path.abspath(__file__))
    n_sizes, n_times = benchmark_varying_n()
    r_sizes, r_times = benchmark_varying_range()
    generate_plots(n_sizes, n_times, r_sizes, r_times, output_directory)
