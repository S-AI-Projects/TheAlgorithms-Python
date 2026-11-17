"""Time Lucas number implementations and plot measured and expected growth."""

# ruff: noqa: INP001

import csv
import statistics
import sys
from pathlib import Path
from timeit import repeat

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from maths.lucas_series import (  # noqa: E402
    dynamic_lucas_number,
    recursive_lucas_number,
)

SIZES = range(5, 31)
REPEATS = 5
DYNAMIC_NUMBER = 10_000
PHI = (1 + 5**0.5) / 2
OUTPUT_DIR = Path(__file__).resolve().parent


if __name__ == "__main__":
    rows = []
    for n in SIZES:
        recursive_samples = repeat(
            lambda n=n: recursive_lucas_number(n), number=1, repeat=REPEATS
        )
        dynamic_samples = repeat(
            lambda n=n: dynamic_lucas_number(n),
            number=DYNAMIC_NUMBER,
            repeat=REPEATS,
        )
        rows.append(
            {
                "n": n,
                "recursive_seconds": statistics.median(recursive_samples),
                "dynamic_seconds": statistics.median(dynamic_samples)
                / DYNAMIC_NUMBER,
            }
        )

    results_path = OUTPUT_DIR / "lucas_timings.csv"
    with results_path.open("w", newline="", encoding="utf-8") as results_file:
        writer = csv.DictWriter(results_file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    sizes = [row["n"] for row in rows]
    recursive_times = [row["recursive_seconds"] for row in rows]
    dynamic_times = [row["dynamic_seconds"] for row in rows]
    recursive_expected = [
        recursive_times[0] * PHI ** (n - sizes[0]) for n in sizes
    ]
    dynamic_expected = [
        dynamic_times[0] * n / sizes[0] for n in sizes
    ]

    plt.figure(figsize=(9, 6))
    plt.plot(sizes, recursive_times, "o-", label="Recursive: measured")
    plt.plot(sizes, recursive_expected, "--", label=r"Recursive: $O(\varphi^n)$")
    plt.plot(sizes, dynamic_times, "o-", label="Dynamic: measured")
    plt.plot(sizes, dynamic_expected, "--", label="Dynamic: $O(n)$")
    plt.yscale("log")
    plt.xlabel("n")
    plt.ylabel("Median time per call (seconds, log scale)")
    plt.title("Lucas number running time: measurements and expected growth")
    plt.grid(True, which="both", linestyle=":", alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plot_path = OUTPUT_DIR / "lucas_complexity.png"
    plt.savefig(plot_path, dpi=160)
    plt.close()

    print(f"Timings saved to {results_path}")
    print(f"Plot saved to {plot_path}")
    for row in rows:
        print(
            f"n={row['n']:2}: recursive={row['recursive_seconds']:.6g}s, "
            f"dynamic={row['dynamic_seconds']:.6g}s"
        )
