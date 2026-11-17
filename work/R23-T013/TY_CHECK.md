# Task R23-T013: Make `graphs/graphs_floyd_warshall.py` Fully Typed

## Objective
Add full type hints to all unhinted functions in `graphs/graphs_floyd_warshall.py` (`_print_dist` and `floyd_warshall`).
Ensure the distance matrix accurately expresses `float('inf')` using `list[list[float]]` and `ty check` emits zero diagnostics for this file.

## Functions Updated
1. `_print_dist(dist, v) -> None:`
   - Before: Missing parameter type annotations for `dist` and `v`.
   - After: `def _print_dist(dist: list[list[float]], v: int) -> None:`
2. `floyd_warshall(graph, v):`
   - Before: Missing parameter and return type annotations.
   - After: `def floyd_warshall(graph: list[list[float]], v: int) -> tuple[list[list[float]], int]:`

## Type Checker Verification (`ty`)
Command:
```bash
uv run --python 3.15 --with ty ty check graphs/graphs_floyd_warshall.py
```
Diagnostics on `graphs/graphs_floyd_warshall.py`: **0 errors / 0 diagnostics**.

## Automated Test Results
Command:
```bash
uv run pytest graphs/graphs_floyd_warshall.py
```
Output:
```
============================== 1 passed in 0.07s ===============================
```
All 4 doctests passed unchanged.
