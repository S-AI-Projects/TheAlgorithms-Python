## Summary of Changes

### Task R23-T029: Iterative (stack-based) binary tree merge implementation and variant analysis

Contributed a new file `data_structures/binary_tree/merge_two_binary_trees_iterative.py` adhering to all repository standards and verified equivalence with the existing recursive version.

### 1. Goal and Implementation
- Implemented `merge_two_binary_trees_iterative(tree1, tree2)` using an explicit stack of pairs `(Node, Node)` on the heap.
- Pushes right child before left child to ensure exact pre-order traversal execution order.
- Provided comprehensive type annotations (`from __future__ import annotations`, `Node | None`).
- Validated inputs against erroneous types, raising `TypeError` with doctest tracebacks.
- Built identical trees to `merge_two_binary_trees.py` in doctests and verified identical pre-order outputs:
  - `print_preorder(merged)` gives `9, 11, 2, 1, 15, 4`.
  - Direct assertion: `get_preorder(merged_iter) == get_preorder(merged_rec)`.

### 2. Variant & Stack Depth Analysis (`work/R23-T029/VARIANT.md`)
- Detailed time and space complexity comparison.
- Stack depth analysis:
  - Recursive: Constrained by `sys.getrecursionlimit() = 1000`; crashes on skewed trees with `RecursionError` at depth 1,200.
  - Iterative: Stack allocated on the heap; scales gracefully without stack overflow (completes in 73.83 µs at depth 1,200).
- Included full benchmark timing table across balanced and skewed trees.

### 3. Verification & Test Evidence
- `python3 scripts/validate_filenames.py`: Passed (0 errors).
- `uvx ruff check data_structures/binary_tree/merge_two_binary_trees_iterative.py`: All checks passed.
- `uvx ruff format --check data_structures/binary_tree/merge_two_binary_trees_iterative.py`: 1 file already formatted.
- `python3 -m doctest -v`: All 39 doctests passed.
- `pytest --doctest-modules`: 3/3 passed.

### 4. Submission Checklist
- [x] Contributed `data_structures/binary_tree/merge_two_binary_trees_iterative.py` with type hints and doctests.
- [x] Pre-order traversal matches `merge_two_binary_trees.py`.
- [x] `scripts/validate_filenames.py` and `ruff` pass cleanly.
- [x] `work/R23-T029/VARIANT.md` compares stack depth and runtime with timing table.
- [x] Clean upstream branch `student/E26B07F0850/R23-T029-upstream` prepared with only code changes.
