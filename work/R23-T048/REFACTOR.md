# Prim heap refactor

## What changed

- `get_child_right_position` now derives its result from
  `get_child_left_position(position) + 1`, so the shared `2 * position + 1`
  calculation is written once.
- `_bubble_down` selects the smaller existing child once, then compares that
  child's weight with the current node. This replaces separate right- and
  left-child swap paths while retaining strict comparisons (equal child
  weights still prefer the left child).
- `get_parent_position` remains shared by `update_key` and `_bubble_up`.
- No doctests were changed.

## C90 complexity

Ruff's default C90 check uses a maximum complexity of 10 and passed both before
and after. To show numeric values for every reported function, complexity was
measured with `lint.mccabe.max-complexity=1`.

| Function | Before | After |
| --- | ---: | ---: |
| `extract_min` | 3 | 3 |
| `update_key` | 3 | 3 |
| `_bubble_up` | 3 | 3 |
| `_bubble_down` | 7 | 4 |
| `add_node` | 2 | 2 |
| `prims_algo` | 8 | 8 |

`prims_algo` remains the file-wide worst function at 8. The refactored heap
method `_bubble_down` decreased from 7 to 4.

## Test and coverage results

| Check | Before | After |
| --- | --- | --- |
| `uv run pytest graphs/minimum_spanning_tree_prims2.py` | 5 passed | 5 passed |
| Direct doctests | 24 passed | 24 passed |
| Target file coverage | 93% (126 statements, 9 missed) | 95% (116 statements, 6 missed) |
| `uvx ruff check graphs/minimum_spanning_tree_prims2.py` | passed | passed |
| `uvx ruff check --select C90 graphs/minimum_spanning_tree_prims2.py` | passed | passed |

After the refactor, 100 seeded priority-queue trials with 50 elements and 100
key updates per trial also extracted elements in nondecreasing priority order.
