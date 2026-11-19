# Scaling & Complexity Analysis for `merge_sort_linked_list.py` (R23-T006)

## 1. Theoretical Complexity Derivation

Merge sort is a classic divide-and-conquer algorithm adapted for singly linked lists.

### Time Complexity: $O(n \log n)$
1. **Divide Phase**:
   - The list is divided into two roughly equal halves using the slow and fast pointer ("runner") technique in `get_middle(head)`. Finding the middle node of a list with $k$ nodes requires scanning $\lfloor k/2 \rfloor$ steps, costing $\Theta(k)$ linear time.
   - The list is divided until sublists contain 0 or 1 node, creating a recursion tree of depth $\lceil \log_2 n \rceil$.
2. **Conquer & Merge Phase**:
   - `merge(left, right)` compares the heads of the two sublists and recursively links the smaller node, iterating until both lists are merged.
   - For sublists of combined length $k$, merging takes at most $k$ pointer comparisons and reassignments, costing $\Theta(k)$ linear time.
3. **Total Work**:
   - At recursion level $i$ ($0 \le i < \log_2 n$), there are $2^i$ subproblems, each of size $n / 2^i$. The combined work at level $i$ is:
     $$2^i \cdot \mathcal{O}\left(\frac{n}{2^i}\right) = \mathcal{O}(n)$$
   - Summing across all $\log_2 n$ levels yields:
     $$T(n) = 2 T(n/2) + \mathcal{O}(n) \implies T(n) = \mathcal{O}(n \log n)$$
   - This bound holds in best, average, and worst cases because division and merging occur regardless of initial node order.

### Space Complexity: $O(\log n)$ to $O(n)$
- **Auxiliary Stack Space**:
  - The call stack for `merge_sort_linked_list` reaches depth $\mathcal{O}(\log n)$.
  - The recursive `merge` implementation takes $\mathcal{O}(n)$ stack frames in the worst case without tail-call optimization.
- **Node Reallocation**: $\mathcal{O}(1)$ auxiliary memory since nodes are relinked in-place without copying or allocating new `Node` instances.

---

## 2. Empirical Benchmark Results

Benchmarked across 7 doubling input sizes with 15 iterations per size, comparing `merge_sort_linked_list` to Python's C-implemented `sorted()` (Timsort) on identical values:

| Input Size ($N$) | Linked List Merge Sort (ms) | Python `sorted()` (ms) | Overhead / Ratio |
|:---:|:---:|:---:|:---:|
| 50 | 0.0306 | 0.0011 | 28.1x |
| 100 | 0.0696 | 0.0023 | 30.1x |
| 200 | 0.1493 | 0.0041 | 36.2x |
| 400 | 0.3610 | 0.0092 | 39.3x |
| 800 | 0.8006 | 0.0218 | 36.8x |
| 1600 | 1.7986 | 0.0418 | 43.0x |
| 3200 | 3.9921 | 0.1041 | 38.4x |

### Scaling Analysis:
When doubling $N$ (e.g., from 800 to 1600):
$$\frac{1600 \log_2 1600}{800 \log_2 800} = 2 \cdot \frac{10.64}{9.64} \approx 2.21$$
The observed execution time scales from $0.8006\text{ ms}$ to $1.7986\text{ ms}$ ($\times 2.25$), closely tracking the theoretical $\mathcal{O}(n \log n)$ curve.

### Comparison with Python `sorted()`:
- Python's `sorted()` uses Timsort implemented in optimized C operating on contiguous array buffers in RAM with hardware cache locality.
- In contrast, the linked list implementation traverses heap-allocated Python objects via reference pointers (`.next`), involving Python interpreter bytecode overhead, attribute lookups, and function call frame allocations, producing a consistent ~30-43x constant factor slowdown.

---

## 3. Benchmark Plot

The benchmark script saved a high-resolution plot to:
`work/R23-T006/benchmark_plot.png`

The plot depicts:
1. `Linked List Merge Sort` exhibiting smooth $\mathcal{O}(n \log n)$ scaling.
2. `Python built-in sorted()` following parallel asymptotic growth at a lower baseline time.
