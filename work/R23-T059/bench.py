"""Measure attempts and time of blockchain/simple_proof_of_work.proof_of_work.

Expected: the hash must start with `difficulty` hex zeros, each nonce succeeds with
probability 16**-difficulty, so the expected number of attempts is 16**difficulty
and the time grows by about x16 per extra level.

Run from the repo root:  python work/R23-T059/bench.py
Writes work/R23-T059/results.csv and (if matplotlib is installed) pow_benchmark.png.
Attempts are exactly reproducible (SHA-256 is deterministic); times depend on the machine.
"""

import csv
import math
import statistics
import sys
import timeit
from pathlib import Path

sys.path.insert(0, ".")
from blockchain.simple_proof_of_work import proof_of_work

OUT = Path(__file__).parent
# (difficulty, number of runs). Each run uses a different block number, because the
# function is deterministic: the same input always gives the same nonce.
LEVELS = [(0, 100), (1, 20000), (2, 5000), (3, 1000), (4, 400), (5, 60)]
TRANSACTIONS = "Alice sends 1 BTC to Bob"
PREVIOUS_HASH = "00000abcdef1234567890"

rows = []
for difficulty, runs in LEVELS:
    attempts, seconds = [], []
    for block_number in range(runs):
        result = []
        t = timeit.timeit(
            lambda b=block_number, d=difficulty: result.append(
                proof_of_work(b, TRANSACTIONS, PREVIOUS_HASH, d)
            ),
            number=1,
        )
        attempts.append(result[0][0] + 1)  # nonce 0 is the first attempt
        seconds.append(t)
    expected = 16**difficulty
    mean_att = statistics.fmean(attempts)
    # attempts are geometric: standard deviation is about the mean, so SE = mean/sqrt(n)
    se = statistics.stdev(attempts) / math.sqrt(runs) if runs > 1 else 0.0
    rows.append(
        {
            "difficulty": difficulty,
            "runs": runs,
            "expected_attempts": expected,
            "mean_attempts": round(mean_att, 1),
            "ci95_low": round(mean_att - 1.96 * se, 1),
            "ci95_high": round(mean_att + 1.96 * se, 1),
            "median_attempts": statistics.median(attempts),
            "mean_over_expected": round(mean_att / expected, 3),
            "mean_time_s": statistics.fmean(seconds),
            "us_per_attempt": 1e6 * sum(seconds) / sum(attempts),
        }
    )

print("| difficulty | runs | expected 16^d | mean attempts | 95% CI | mean/expected | mean time (s) | us/attempt | attempts x vs previous | time x vs previous |")
print("|---|---|---|---|---|---|---|---|---|---|")
for i, r in enumerate(rows):
    att_x = r["mean_attempts"] / rows[i - 1]["mean_attempts"] if i else float("nan")
    time_x = r["mean_time_s"] / rows[i - 1]["mean_time_s"] if i else float("nan")
    r["attempts_x_prev"], r["time_x_prev"] = round(att_x, 2), round(time_x, 2)
    print(
        f"| {r['difficulty']} | {r['runs']} | {r['expected_attempts']:,} | {r['mean_attempts']:,} "
        f"| {r['ci95_low']:,} - {r['ci95_high']:,} | {r['mean_over_expected']} "
        f"| {r['mean_time_s']:.6f} | {r['us_per_attempt']:.2f} | {att_x:.1f} | {time_x:.1f} |"
    )

with open(OUT / "results.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)

try:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
except ImportError:
    print("matplotlib not installed: skipping the plot")
else:
    d = [r["difficulty"] for r in rows]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))
    err = [
        [r["mean_attempts"] - r["ci95_low"] for r in rows],
        [r["ci95_high"] - r["mean_attempts"] for r in rows],
    ]
    ax1.errorbar(d, [r["mean_attempts"] for r in rows], yerr=err, fmt="o", capsize=4, label="measured mean (95% CI)")
    ax1.plot(d, [16**x for x in d], "--", label="expected 16^difficulty")
    ax1.set_yscale("log")
    ax1.set_xlabel("difficulty (leading hex zeros)")
    ax1.set_ylabel("attempts (log scale)")
    ax1.set_title("Attempts vs difficulty")
    ax1.legend()
    ax2.plot(d, [r["mean_time_s"] for r in rows], "o-", label="measured mean time")
    per_attempt = sum(r["mean_time_s"] for r in rows) / sum(r["mean_attempts"] for r in rows)
    ax2.plot(d, [per_attempt * 16**x for x in d], "--", label="expected: const x 16^difficulty")
    ax2.set_yscale("log")
    ax2.set_xlabel("difficulty (leading hex zeros)")
    ax2.set_ylabel("time per run, seconds (log scale)")
    ax2.set_title("Time vs difficulty")
    ax2.legend()
    fig.tight_layout()
    fig.savefig(OUT / "pow_benchmark.png", dpi=150)
    print("saved pow_benchmark.png")
