# Recursive depth-first sum trace

## Debugger setup

I ran the module under `python3 -m pdb` and stopped at line 62 in
`depth_first_search`. The breakpoint was conditional on the complete doctest
tree being present, then made unconditional to capture each recursive call.
At each stop I inspected `node.value` (or `None`) and used `where` to record
the active `depth_first_search` stack.

The tree is:

```text
        10
       /  \
      5   -3
     /    / \
    12   8   0
```

`depth_first_search` evaluates the left recursive call before the right one.
The call stack below lists the active calls from the root to the current call.
Empty children are explicit calls with `node is None`, each returning zero.

| Step | `node.value` | Stack path from root | Child sums | Returned sum |
|---:|---:|---|---:|---:|
| 1 | 10 | `10` | left 17, right 5 | 32 |
| 2 | 5 | `10 -> 5` | left 12, right 0 | 17 |
| 3 | 12 | `10 -> 5 -> 12` | left 0, right 0 | 12 |
| 4 | `None` | `10 -> 5 -> 12 -> None` (left) | n/a | 0 |
| 5 | `None` | `10 -> 5 -> 12 -> None` (right) | n/a | 0 |
| 6 | `None` | `10 -> 5 -> None` (right) | n/a | 0 |
| 7 | -3 | `10 -> -3` | left 8, right 0 | 5 |
| 8 | 8 | `10 -> -3 -> 8` | left 0, right 0 | 8 |
| 9 | `None` | `10 -> -3 -> 8 -> None` (left) | n/a | 0 |
| 10 | `None` | `10 -> -3 -> 8 -> None` (right) | n/a | 0 |
| 11 | 0 | `10 -> -3 -> 0` | left 0, right 0 | 0 |
| 12 | `None` | `10 -> -3 -> 0 -> None` (left) | n/a | 0 |
| 13 | `None` | `10 -> -3 -> 0 -> None` (right) | n/a | 0 |

The returned values unwind in postorder: `12`, then `17`; `8` and `0`
combine to `5`; finally `10 + 17 + 5 = 32`.

## What surprised me

Even a leaf causes two more recursive calls: its missing left and right
children are each visited as `None` and contribute zero. This explains why
the debugger recorded 13 calls for a tree with only 6 nodes.
