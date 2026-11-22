"""
Monte Carlo Pi Estimation Convergence Experiment.

Evaluates estimation error |estimate - pi| across varying sample sizes N
and compares empirical scaling against the theoretical 1/sqrt(N) convergence.
"""

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from maths.pi_monte_carlo_estimation import estimate_pi  # noqa: E402


def run_convergence_experiment() -> tuple[list[int], list[float], list[list[float]]]:
    """
    Run Monte Carlo estimation across sample sizes N from 10^2 to 10^6.
    Computes mean absolute error and individual trial errors across seeds.
    """
    sample_sizes = [
        100,
        300,
        1_000,
        3_000,
        10_000,
        30_000,
        100_000,
        30_000_0,
        1_000_000,
    ]
    seeds = [1, 7, 42, 99, 123, 456, 789, 1024, 2048, 4096]

    mean_errors: list[float] = []
    trial_errors_per_n: list[list[float]] = []

    for n in sample_sizes:
        current_errors: list[float] = []
        for s in seeds:
            est = estimate_pi(n, seed=s)
            current_errors.append(abs(est - math.pi))
        mean_errors.append(sum(current_errors) / len(current_errors))
        trial_errors_per_n.append(current_errors)

    return sample_sizes, mean_errors, trial_errors_per_n


def generate_plot(
    sample_sizes: list[int],
    mean_errors: list[float],
    trial_errors_per_n: list[list[float]],
    output_path: Path,
) -> None:
    """
    Generate log-log plot of |estimate - pi| vs. N with 1/sqrt(N) reference line.
    """
    plt.figure(figsize=(10, 6), dpi=150)

    # Plot individual simulation trials
    for i, n in enumerate(sample_sizes):
        plt.scatter(
            [n] * len(trial_errors_per_n[i]),
            trial_errors_per_n[i],
            color="#3b82f6",
            alpha=0.3,
            s=25,
            edgecolors="none",
        )

    # Plot empirical mean absolute error
    plt.loglog(
        sample_sizes,
        mean_errors,
        marker="o",
        color="#1d4ed8",
        linewidth=2.2,
        label="Empirical Mean Error $|\\hat{\\pi}_N - \\pi|$",
    )

    # Theoretical reference line: 1.0 / sqrt(N)
    ref_y = [1.0 / math.sqrt(n) for n in sample_sizes]
    plt.loglog(
        sample_sizes,
        ref_y,
        linestyle="--",
        color="#dc2626",
        linewidth=2.0,
        label=r"Theoretical Reference: $1/\sqrt{N}$ (Slope = $-0.5$)",
    )

    # Secondary reference line scaled to match constant factor: sqrt(pi*(4-pi))/sqrt(N)
    c = math.sqrt(math.pi * (4 - math.pi) * 2 / math.pi)
    ref_exact = [c / math.sqrt(n) for n in sample_sizes]
    plt.loglog(
        sample_sizes,
        ref_exact,
        linestyle=":",
        color="#d97706",
        linewidth=1.8,
        label=r"Expected Absolute Error $\approx 1.31/\sqrt{N}$",
    )

    plt.title(
        r"Monte Carlo $\pi$ Estimation Error vs. Sample Size $N$"
        "\nLog-Log Scale Convergence Demonstration",
        fontsize=13,
        fontweight="bold",
        pad=12,
    )
    plt.xlabel(r"Number of Simulated Points $N$ (log scale)", fontsize=11)
    plt.ylabel(
        r"Absolute Estimation Error $|\hat{\pi} - \pi|$ (log scale)", fontsize=11
    )
    plt.grid(True, which="both", linestyle="--", alpha=0.5)
    plt.legend(fontsize=10, loc="upper right")
    plt.tight_layout()

    plt.savefig(output_path)
    plt.close()
    print(f"Plot saved successfully to: {output_path}")


def main() -> None:
    output_dir = Path(__file__).resolve().parent
    output_img = output_dir / "error_vs_n_plot.png"

    print("Running Monte Carlo convergence experiment across 9 sample sizes...")
    sizes, mean_errs, trial_errs = run_convergence_experiment()

    print("\n| Sample Size N | Mean Error | Theoretical 1/sqrt(N) | Ratio |")
    print("|---|---|---|---|")
    for s, m in zip(sizes, mean_errs, strict=True):
        theory = 1.0 / math.sqrt(s)
        ratio = m / theory
        print(f"| {s:10,d} | {m:10.6f} | {theory:10.6f} | {ratio:5.2f} |")

    generate_plot(sizes, mean_errs, trial_errs, output_img)


if __name__ == "__main__":
    main()
