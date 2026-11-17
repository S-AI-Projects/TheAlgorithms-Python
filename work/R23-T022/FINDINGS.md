# R23-T022 Findings: Exponential Search Complexity & Comparison Counting

## 1. Theoretical Complexity & Derivation

Exponential search operates in two distinct phases on an ascendingly sorted array $A$ of size $n$:

### Phase 1: Range Bounding (Exponential Doubling)
1. **Check $A[0]$**: If $A[0] = \text{target}$, return index $0$ immediately in $O(1)$ time (exactly 1 comparison).
2. **Exponential Probe**: If $A[0] \neq \text{target}$, initialize $\text{bound} = 1$. While $\text{bound} < n$ and $A[\text{bound}] < \text{target}$, double the bound ($\text{bound} \leftarrow \text{bound} \times 2$).
   - For an item located at index $i > 0$, the loop terminates as soon as $\text{bound} \ge i$.
   - The values of $\text{bound}$ tested are $2^0, 2^1, 2^2, \dots, 2^k$, where $2^{k-1} < i \le 2^k$.
   - Thus, $k = \lceil \log_2(i) \rceil$.
   - Phase 1 performs at most $\lceil \log_2 i \rceil$ element comparisons.

### Phase 2: Bounded Binary Search
- Once the range $[2^{k-1}, \min(2^k, n - 1)]$ is identified, binary search is executed on this sub-array.
- The size of this search interval is:
  $$\text{length} = \min(2^k, n - 1) - 2^{k-1} + 1 \le 2^{k-1} + 1 \le i + 1$$
- Binary search on an interval of size $L \le i + 1$ requires at most $\lfloor \log_2 L \rfloor + 1 \le \lceil \log_2 i \rceil + 1$ probes.
- Each probe executes at most 2 element comparisons (equality check followed by order check).

### Combined Time Complexity: $O(\log i)$
$$\text{Total Time} = T_{\text{phase 1}} + T_{\text{phase 2}} = O(\log i) + O(\log i) = O(\log i)$$
Where $i$ is the index of the search target in the sorted collection.

- **Best Case ($i = 0$):** $O(1)$ time and exactly 1 element comparison.
- **Target Near Start ($i \ll n$):** $O(\log i) \ll O(\log n)$. Exponential search avoids traversing or bisecting the remainder of the array.
- **Target Near End ($i \approx n - 1$):** $O(\log n)$ time, requiring $\approx 2 \log_2 n$ comparisons (doubling phase plus bounded binary search).
- **Absent Target:** Takes $O(\log i)$ where $i$ is the insertion point index where the element would belong.

---

## 2. Empirical Benchmark Methodology

We implemented instrumented copies of both Exponential Search and Binary Search in `work/R23-T022/bench.py` to count exact element comparisons.
We tested 7 doubling input sizes $n \in \{1000, 2000, 4000, 8000, 16000, 32000, 64000\}$ across 4 target scenarios:
1. **Start ($i = 0$):** First element $A[0]$.
2. **Middle ($i = n // 2$):** Center element $A[n // 2]$.
3. **End ($i = n - 1$):** Final element $A[n - 1]$.
4. **Absent:** Element larger than any element in the array ($n + 100$).

---

## 3. Comparison Count Results

| Input Size $n$ | Target Position | Target Index $i$ | Exponential Search | Binary Search | Ratio (Exp / Bin) |
|---|---|---|---|---|---|
| **1,000** | start | 0 | **1** | 17 | **0.06** |
| 1,000 | mid | 500 | 22 | 17 | 1.29 |
| 1,000 | end | 999 | 28 | 19 | 1.47 |
| 1,000 | absent | N/A | 29 | 20 | 1.45 |
| **2,000** | start | 0 | **1** | 19 | **0.05** |
| 2,000 | mid | 1,000 | 23 | 19 | 1.21 |
| 2,000 | end | 1,999 | 31 | 21 | 1.48 |
| 2,000 | absent | N/A | 32 | 22 | 1.45 |
| **4,000** | start | 0 | **1** | 21 | **0.05** |
| 4,000 | mid | 2,000 | 24 | 21 | 1.14 |
| 4,000 | end | 3,999 | 34 | 23 | 1.48 |
| 4,000 | absent | N/A | 35 | 24 | 1.46 |
| **8,000** | start | 0 | **1** | 23 | **0.04** |
| 8,000 | mid | 4,000 | 25 | 23 | 1.09 |
| 8,000 | end | 7,999 | 37 | 25 | 1.48 |
| 8,000 | absent | N/A | 38 | 26 | 1.46 |
| **16,000** | start | 0 | **1** | 25 | **0.04** |
| 16,000 | mid | 8,000 | 26 | 25 | 1.04 |
| 16,000 | end | 15,999 | 40 | 27 | 1.48 |
| 16,000 | absent | N/A | 41 | 28 | 1.46 |
| **32,000** | start | 0 | **1** | 27 | **0.04** |
| 32,000 | mid | 16,000 | 27 | 27 | 1.00 |
| 32,000 | end | 31,999 | 43 | 29 | 1.48 |
| 32,000 | absent | N/A | 44 | 30 | 1.47 |
| **64,000** | start | 0 | **1** | 29 | **0.03** |
| 64,000 | mid | 32,000 | 28 | 29 | 0.97 |
| 64,000 | end | 63,999 | 46 | 31 | 1.48 |
| 64,000 | absent | N/A | 47 | 32 | 1.47 |

---

## 4. Analysis & Key Takeaways

1. **Targets Near Start ($i = 0$):**
   - Exponential search achieves an immediate $O(1)$ exit with **exactly 1 comparison**.
   - Binary search must repeatedly bisect the entire array down to index $0$, taking $2 \log_2 n - 1$ comparisons (up to 29 comparisons at $n=64,000$).
   - Exponential search achieves a **97% reduction** in comparisons.

2. **Targets in Middle ($i = n // 2$):**
   - Exponential search takes $\approx 2 \log_2(n/2)$ comparisons.
   - Binary search takes $\approx 2 \log_2 n$ comparisons (or fewer if midpoint coincides).
   - Comparison counts are virtually identical (ratio $\approx 0.97 - 1.29$).

3. **Targets Near End ($i = n - 1$):**
   - Exponential search incurs the overhead of the doubling phase ($\approx \log_2 n$ bound checks) plus the bounded binary search ($\approx \log_2 n$ probes).
   - Total comparisons scale at $\approx 1.48 \times$ binary search, confirming that both remain strictly $O(\log n)$ at the upper bound.

4. **Runtime Measurement (`timeit`):**
   - Pure algorithmic search time at start is **0.034 µs** (flat, independent of $n$), confirming $O(1)$ best-case behavior.
   - At mid and end, search time scales logarithmically from **0.47 µs to 1.01 µs**.
   - The generated plot `exponential_search_benchmark.png` confirms the logarithmic scaling and matches the theoretical $2 \cdot \log_2 n$ curve.

