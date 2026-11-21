# R23-T048 baseline

Captured before changing `graphs/minimum_spanning_tree_prims2.py` on
`R23-T048` (base `574d100b7181956e9c8384552fd078165e4cc326`).

## Tests and coverage

Command:

```bash
uv run pytest graphs/minimum_spanning_tree_prims2.py --cov=graphs.minimum_spanning_tree_prims2 --cov-report=term
```

Result: 5 pytest items passed. Coverage was 126 statements, 9 missed, 93%.

The direct doctest run reported 24 doctest examples passed across the priority
queue, heap index helpers, and `prims_algo`.

## Complexity

`uvx ruff check --select C90 graphs/minimum_spanning_tree_prims2.py` passed
with Ruff's default maximum complexity of 10. For numeric measurements, the
same check was run with `lint.mccabe.max-complexity=1` to report each function:

| Function | Baseline complexity |
| --- | ---: |
| `extract_min` | 3 |
| `update_key` | 3 |
| `_bubble_up` | 3 |
| `_bubble_down` | 7 |
| `add_node` | 2 |
| `prims_algo` | 8 |

`prims_algo` was the worst function at complexity 8.
