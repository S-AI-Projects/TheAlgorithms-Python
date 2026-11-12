# Randomized meldable heap: an explainer you can re-implement from

File: `data_structures/heap/randomized_heap.py`.
Reference: https://en.wikipedia.org/wiki/Randomized_meldable_heap

## 1. The idea in one paragraph
A priority queue needs two things: "give me the smallest" and "add this". A heap keeps the
smallest value at the root. The trick of a *meldable* heap is that you only need to write
**one** operation, `merge(heap_a, heap_b)`, and everything else is built from it:

| operation | how it uses merge |
|---|---|
| `insert(x)` | `root = merge(root, Node(x))` (merge with a one-node heap) |
| `pop()` | remember `root.value`, then `root = merge(root.left, root.right)` |
| `top()` | just return `root.value` |

The data structure is a plain binary tree where every node is **<=** its children (a min-heap).
It is *not* kept balanced or complete; the random coin flip inside `merge` is what keeps it fast.

## 2. The algorithm
```
merge(a, b):
    if a is empty: return b
    if b is empty: return a
    if a.value > b.value: swap a and b        # now a has the smaller root
    if coin_flip():                           # 50 % / 50 %
        swap a.left and a.right
    a.left = merge(a.left, b)                 # always continue down the LEFT child
    return a
```
- **Why it keeps heap order:** the smaller of the two roots becomes the root, and everything else is merged *below* it, so every node is still <= its children.
- **Why the coin flip:** `merge` always walks down the left child, so flipping the children first means it walks down a *random* child. See section 4.
- **Cost:** each recursive call goes one level deeper in one of the two heaps, so the cost is the length of that walk.

## 3. Worked example by hand
Merge H1 and H2, then pop once. I fix the coin flips (T = swap children, F = don't) so the
steps are reproducible; in the real code they are random.

```
   H1            H2
    2             4
   / \           /
  5   9         6
```

**merge(H1, H2)**

| step | call | what happens | coin |
|---|---|---|---|
| 1 | merge(2, 4) | 2 <= 4, so 2 stays root. Swap 2's children: left = 9, right = 5. Recurse: 2.left = merge(9, 4) | T |
| 2 | merge(9, 4) | 9 > 4, so swap the two heaps: root = 4 (left child 6), other = 9. Don't swap 4's children. Recurse: 4.left = merge(6, 9) | F |
| 3 | merge(6, 9) | 6 <= 9, so 6 stays root. Swap its (empty) children: nothing changes. Recurse: 6.left = merge(None, 9) = 9 | T |
| 4 | merge(None, 9) | first is empty, return 9 | - |

Unwinding gives 6 with left child 9, then 4 with left child 6, then 2 with left child 4 (and right child 5):

```
        2
       / \
      4   5
     /
    6
   /
  9
```

**pop()**: remember 2, remove the root, and merge its two children `4(6(9))` and `5`:

| step | call | what happens | coin |
|---|---|---|---|
| 1 | merge(4, 5) | 4 <= 5, so 4 stays root. Don't swap. Recurse: 4.left = merge(6(9), 5) | F |
| 2 | merge(6, 5) | 6 > 5, so swap the heaps: root = 5, other = 6(9). Don't swap. Recurse: 5.left = merge(None, 6(9)) = 6(9) | F |

Result (pop returned 2):
```
      4
     /
    5
   /
  6
 /
9
```
Popping again gives 4, 5, 6, 9, in sorted order. (I checked both trees by running the real code with
`random.choice` forced to return exactly these coin flips.)

## 4. Why is the merge randomised?
`merge` costs one recursive call per level it walks down. If the tree gets tall and skinny, the walk is long.
- **Without the coin flip** (always go left) the structure degenerates: every merge goes down the left side, so the tree becomes a long left chain. Inserting 1, 2, 3, ... walks the whole chain every time.
- **With the coin flip**, the walk down each heap is a *random path*, and the expected length of a random root-to-empty-child path in a tree with n nodes is at most `log2(n + 1)`. Sketch: there are n + 1 empty child slots; the walk reaches the slot at depth d with probability 2^-d. So E[2^depth] = (sum over the n + 1 slots of 2^-d * 2^d) = n + 1, and by Jensen's inequality E[depth] = E[log2 2^depth] <= log2 E[2^depth] = log2(n + 1). A merge walks one such path in each of the two heaps, so it takes **O(log n) expected time**.
- **Why not a deterministic rule?** Leftist or skew heaps keep balance information (ranks) or use an amortised argument. The randomised version needs *no extra fields*: a node is just `value, left, right`. The price is that O(log n) is the *expected* time; one unlucky merge can be slow, but that is very unlikely.

## 5. Experiments (`experiment.py`, run from the repo root)
**A) Sorted pop order.** 200 different seeds, each building a heap from 1,000 random values and popping all of them:
**200 / 200** gave exactly `sorted(values)` and an empty heap. This is the doctest added to the module docstring (seed 0: first five values `[-1000, -1000, -998, -997, -996]`).

**B) Does the coin flip matter?** Average recursive `merge` calls per operation, with the real coin flip versus a "never swap" variant:

| n | log2(n) | insert order | coin flip: insert | coin flip: pop | never swap: insert | never swap: pop |
|---|---|---|---|---|---|---|
| 1000 | 10.0 | random | 7.0 | 10.1 | 250.1 | 1.0 |
| 1000 | 10.0 | ascending | 9.3 | 10.1 | 500.5 | 1.0 |
| 1000 | 10.0 | descending | 2.0 | 1.0 | 2.0 | 1.0 |
| 2000 | 11.0 | random | 7.8 | 11.3 | 499.8 | 1.0 |
| 2000 | 11.0 | ascending | 10.3 | 11.6 | 1000.5 | 1.0 |
| 4000 | 12.0 | random | 8.4 | 12.8 | 992.4 | 1.0 |
| 4000 | 12.0 | ascending | 11.3 | 13.0 | 2000.5 | 1.0 |

With the coin flip the cost stays near log2(n) (and grows by about 1 each time n doubles). Without it, inserting costs
about n/4 (random order) to n/2 (ascending) calls, i.e. it grows linearly with n.

**Surprise:** with "never swap", `pop` is O(1) (always 1 call), because every node's right child is empty, so a heap is just
a left chain. All the cost moves into `insert`. The coin flip spreads nodes over both children, which balances the cost
of the two operations.

## 6. Pitfalls when you re-implement it
- Compare `a.value > b.value` and swap **before** the coin flip, so the root stays the minimum.
- Flip the children of `a` (the smaller root) only, and always recurse into `a.left`.
- `merge(None, x)` returns `x`, and `merge(x, None)` returns `x`; this is the base case.
- Equal values work (`>` not `>=`); the heap is **not stable**.
- `pop()` on an empty heap raises `IndexError("Can't get top element for the empty heap.")`.
- The sorted result never depends on the coin flips, only the *shape* of the tree does. That is why the doctest can safely check `popped == sorted(values)`.

## 7. Try it: derive a doctest result from this page
Without running the code, work out `RandomizedHeapNode.merge(RandomizedHeapNode(5), RandomizedHeapNode(0)).value`
(hint: which root is smaller, and does the coin flip change that?). The answer is the existing doctest. Then
record how it went in `FEEDBACK.md`.
