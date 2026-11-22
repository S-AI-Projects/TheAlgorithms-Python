"""
Comparative Evaluation & Benchmark Suite for KNN Implementations.

Compares machine_learning.k_nearest_neighbors.KNN against
scikit-learn's KNeighborsClassifier on the Iris dataset.
"""

import sys
import time
from pathlib import Path

import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from machine_learning.k_nearest_neighbors import KNN  # noqa: E402


def run_comparison(k: int = 5, random_state: int = 42) -> dict[str, float]:
    """
    Train and compare the repository KNN vs scikit-learn KNeighborsClassifier.
    Returns summary statistics including agreement percentage and latencies.
    """
    iris = datasets.load_iris()
    data_x = np.array(iris["data"])
    data_y = np.array(iris["target"])
    target_names = list(iris["target_names"])

    x_train, x_test, y_train, y_test = train_test_split(
        data_x, data_y, test_size=0.30, random_state=random_state
    )

    # 1. Repository KNN
    start_repo_init = time.perf_counter()
    repo_knn = KNN(x_train, y_train, target_names)
    _ = time.perf_counter() - start_repo_init

    start_repo_pred = time.perf_counter()
    repo_preds = [repo_knn.classify(sample, k=k) for sample in x_test]
    repo_pred_time = time.perf_counter() - start_repo_pred

    # 2. Scikit-Learn KNeighborsClassifier
    start_sk_train = time.perf_counter()
    sk_knn = KNeighborsClassifier(n_neighbors=k, metric="euclidean")
    sk_knn.fit(x_train, y_train)
    _ = time.perf_counter() - start_sk_train

    start_sk_pred = time.perf_counter()
    sk_pred_indices = sk_knn.predict(x_test)
    sk_preds = [target_names[idx] for idx in sk_pred_indices]
    sk_pred_time = time.perf_counter() - start_sk_pred

    # 3. Agreement & Accuracy Calculation
    matches = sum(p1 == p2 for p1, p2 in zip(repo_preds, sk_preds, strict=True))
    total_samples = len(x_test)
    agreement_pct = (matches / total_samples) * 100.0
    repo_acc = (
        sum(p == target_names[y] for p, y in zip(repo_preds, y_test, strict=True))
        / total_samples
        * 100.0
    )
    sk_acc = (
        sum(p == y for p, y in zip(sk_pred_indices, y_test, strict=True))
        / total_samples
        * 100.0
    )

    print("=" * 65)
    print("KNN IMPLEMENTATION COMPARISON ON IRIS DATASET")
    print("=" * 65)
    print(f"Total test samples: {total_samples} (Evaluation on >= 10 samples)")
    print(f"Hyperparameters: k={k}, split=70/30, random_state={random_state}")
    print(f"Agreement Count: {matches}/{total_samples}")
    print(f"Agreement Percentage: {agreement_pct:.2f}%")
    print(f"Ground-Truth Accuracy (Both): {repo_acc:.2f}% / {sk_acc:.2f}%")
    print("-" * 65)
    print(f"Repository KNN Total Pred Time:   {repo_pred_time * 1000:.3f} ms")
    print(
        f"Repository KNN Per-Sample Latency: "
        f"{(repo_pred_time / total_samples) * 1000:.3f} ms"
    )
    print(f"Scikit-Learn Total Pred Time:     {sk_pred_time * 1000:.3f} ms")
    print(
        f"Scikit-Learn Per-Sample Latency:  "
        f"{(sk_pred_time / total_samples) * 1000:.3f} ms"
    )
    print(f"Speedup Factor (scikit-learn):    {repo_pred_time / sk_pred_time:.2f}x")
    print("=" * 65)

    print("\nSample Comparisons (First 10 Shared Inputs):")
    print("| Index | Features | Repo KNN | Scikit-Learn | Agreement |")
    print("|---|---|---|---|---|")
    for i in range(min(10, total_samples)):
        feat_str = np.array2string(x_test[i], precision=1, separator=", ")
        match_str = "MATCH" if repo_preds[i] == sk_preds[i] else "MISMATCH"
        print(
            f"| {i + 1:2d} | {feat_str} | {repo_preds[i]:10s} | "
            f"{sk_preds[i]:10s} | {match_str} |"
        )

    return {
        "matches": float(matches),
        "total": float(total_samples),
        "agreement_pct": agreement_pct,
        "repo_time_ms": repo_pred_time * 1000,
        "sk_time_ms": sk_pred_time * 1000,
    }


def main() -> None:
    stats = run_comparison(k=5, random_state=42)
    assert stats["agreement_pct"] >= 95.0, (
        f"Agreement {stats['agreement_pct']}% below 95% threshold"
    )


if __name__ == "__main__":
    main()
