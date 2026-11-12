"""Experiments on data_structures/heap/randomized_heap.py (R23-T060).

Run from the repo root:  python work/R23-T060/experiment.py

A) Build heaps from 1,000 random values and check the pop order is sorted.
B) Why is merging randomised? Count the recursive merge() calls with the real coin
   flip versus a "never swap" variant (random.choice always False), for random,
   ascending and descending insertion order.
"""

import math
import random
import sys

sys.path.insert(0, ".")
sys.setrecursionlimit(50_000)
from data_structures.heap.randomized_heap import RandomizedHeap, RandomizedHeapNode

# ---------------------------------------------------------------- A) sortedness
print("A) pop order of heaps built from 1,000 random values")
seeds = range(200)
ok = 0
for seed in seeds:
    random.seed(seed)
    values = [random.randint(-10**6, 10**6) for _ in range(1000)]
    heap = RandomizedHeap(values)
    popped = [heap.pop() for _ in range(len(values))]
    ok += popped == sorted(values) and not heap
print(f"   {ok}/{len(seeds)} seeds: popped list == sorted(values) and heap empty")
random.seed(0)
values = [random.randint(-1000, 1000) for _ in range(1000)]
heap = RandomizedHeap(values)
popped = [heap.pop() for _ in range(1000)]
print(f"   seed 0 (the doctest): sorted={popped == sorted(values)}, first 5={popped[:5]}, last 5={popped[-5:]}")

# ------------------------------------------------------------- B) cost of merge
calls = 0
_real_merge = RandomizedHeapNode.merge


def counting_merge(root1, root2):
    global calls
    calls += 1
    return _real_merge(root1, root2)


RandomizedHeapNode.merge = staticmethod(counting_merge)
_real_choice = random.choice


def cost(values, never_swap):
    """Return (calls for n inserts, calls for n pops) per operation."""
    global calls
    random.choice = (lambda seq: False) if never_swap else _real_choice
    heap = RandomizedHeap()
    calls = 0
    for v in values:
        heap.insert(v)
    insert_calls = calls
    calls = 0
    for _ in values:
        heap.pop()
    pop_calls = calls
    return insert_calls / len(values), pop_calls / len(values)


print("\nB) average recursive merge() calls per operation (n = number of values)")
print("| n | log2(n) | insert order | coin flip: insert | coin flip: pop | never swap: insert | never swap: pop |")
print("|---|---|---|---|---|---|---|")
for n in (1000, 2000, 4000):
    rng = random.Random(1)
    inputs = {
        "random": [rng.randint(0, 10**6) for _ in range(n)],
        "ascending": list(range(n)),
        "descending": list(range(n, 0, -1)),
    }
    for name, vals in inputs.items():
        random.seed(2)
        ci, cp = cost(vals, never_swap=False)
        ni, np_ = cost(vals, never_swap=True)
        print(f"| {n} | {math.log2(n):.1f} | {name} | {ci:.1f} | {cp:.1f} | {ni:.1f} | {np_:.1f} |")
