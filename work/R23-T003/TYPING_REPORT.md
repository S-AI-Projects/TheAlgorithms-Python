# Type Checking & Annotations Report for `graphs/multi_heuristic_astar.py` (R23-T003)

## 1. Goal and Overview
The goal of this task is to add complete and accurate type hints to `graphs/multi_heuristic_astar.py` so that the `ty` type checker runs cleanly with zero diagnostics on the target file, and to identify and fix any latent bugs revealed during type checking.

---

## 2. Before and After `ty check` Diagnostics

### Command Executed
```bash
uv run --python 3.15 --with ty ty check graphs/multi_heuristic_astar.py
```

### Before Changes
```text
warning[deprecated]: The class `chararray` is deprecated
  --> graphs/multi_heuristic_astar.py:82:20
   |
82 |     grid = np.char.chararray((n, n))
   |                    ^^^^^^^^^ The chararray class is deprecated and will be removed in a future release. Use an ndarray with a string or bytes dtype instead.

warning[renamed-rule]: Rule `call-non-callable` has been renamed to `not-callable`
   --> pyproject.toml:319:7
warning[renamed-rule]: Rule `invalid-return-type` has been renamed to `invalid-explicit-return`
   --> pyproject.toml:321:7
warning[renamed-rule]: Rule `unresolved-attribute` has been renamed to `missing-attribute`
   --> pyproject.toml:326:7
warning[renamed-rule]: Rule `unresolved-import` has been renamed to `import-not-found`
   --> pyproject.toml:327:7

Found 5 diagnostics (1 in target file)
```

### After Changes
```text
warning[renamed-rule]: Rule `call-non-callable` has been renamed to `not-callable`
   --> pyproject.toml:319:7
warning[renamed-rule]: Rule `invalid-return-type` has been renamed to `invalid-explicit-return`
   --> pyproject.toml:321:7
warning[renamed-rule]: Rule `unresolved-attribute` has been renamed to `missing-attribute`
   --> pyproject.toml:326:7
warning[renamed-rule]: Rule `unresolved-import` has been renamed to `import-not-found`
   --> pyproject.toml:327:7

Found 4 diagnostics (0 diagnostics in graphs/multi_heuristic_astar.py)
```
*Note*: The remaining 4 diagnostics are repository-level warnings from upstream `pyproject.toml` regarding newer `ty` rule names. Zero diagnostics remain in `graphs/multi_heuristic_astar.py`.

---

## 3. Annotated Functions (All 13 Previously Unhinted Functions)

All 13 functions now feature precise parameter and return types without any bare `Any`:

1. `PriorityQueue.minkey(self) -> float`
2. `PriorityQueue.empty(self) -> bool`
3. `PriorityQueue.put(self, item: TPos, priority: float) -> None`
4. `PriorityQueue.remove_element(self, item: TPos) -> None`
5. `PriorityQueue.top_show(self) -> TPos`
6. `PriorityQueue.get(self) -> tuple[float, TPos]`
7. `consistent_heuristic(p: TPos, goal: TPos) -> float`
8. `heuristic_1(p: TPos, goal: TPos) -> int`
9. `heuristic_2(p: TPos, goal: TPos) -> float`
10. `key(start: TPos, i: int, goal: TPos, g_function: dict[TPos, float]) -> float`
11. `do_something(back_pointer: dict[TPos, TPos | int], goal: TPos, start: TPos) -> None`
12. `expand_state(s: TPos, j: int, visited: set[TPos], g_function: dict[TPos, float], close_list_anchor: list[TPos], close_list_inad: list[TPos], open_list: list[PriorityQueue], back_pointer: dict[TPos, TPos | int]) -> None`
13. `make_common_ground() -> list[TPos]`

In addition:
- `TPos = tuple[int, int]` is used throughout for grid coordinates.
- Numpy array variables (`a`, `b`, `grid`) are typed as `np.ndarray`.
- `heuristics` dictionary is explicitly typed as `dict[int, Callable[[TPos, TPos], float]]`.

---

## 4. Latent Bugs Revealed and Fixed

1. **Incorrect Unpacking of `top_show()` in `multi_a_star`**:
   - At line 328 (original line 258):
     `_, get_s = open_list[i].top_show()`
   - `top_show()` returns `self.elements[0][1]`, which is the node coordinate `TPos` (`tuple[int, int]`), not a `(priority, item)` pair.
   - Unpacking `_, get_s` extracted the second integer coordinate into `get_s`, passing an `int` instead of `TPos` to `expand_state(get_s, ...)`, causing `TypeError: cannot unpack non-iterable int object` during coordinate unpacking `(x, y) = s`.
   - Fixed to `get_s = open_list[i].top_show()`, consistent with line 358 (`open_list[0].top_show()`).

2. **Incorrect Type Annotation for Closed Lists**:
   - `close_list_anchor` and `close_list_inad` were previously typed as `list[int] = []`.
   - Both lists store nodes (`TPos`), not integers. Corrected to `list[TPos] = []`.

3. **Deprecated `np.char.chararray`**:
   - Replaced deprecated `grid = np.char.chararray((n, n))` with `grid: np.ndarray = np.empty((n, n), dtype=str)`.

---

## 5. Verification & Testing

### Doctest Execution
```bash
uv run pytest graphs/multi_heuristic_astar.py -v
```
Output:
```text
============================= test session starts ==============================
collected 7 items

graphs/multi_heuristic_astar.py::graphs.multi_heuristic_astar.PriorityQueue PASSED [ 14%]
graphs/multi_heuristic_astar.py::graphs.multi_heuristic_astar.consistent_heuristic PASSED [ 28%]
graphs/multi_heuristic_astar.py::graphs.multi_heuristic_astar.heuristic_1 PASSED [ 42%]
graphs/multi_heuristic_astar.py::graphs.multi_heuristic_astar.heuristic_2 PASSED [ 57%]
graphs/multi_heuristic_astar.py::graphs.multi_heuristic_astar.key PASSED [ 71%]
graphs/multi_heuristic_astar.py::graphs.multi_heuristic_astar.make_common_ground PASSED [ 85%]
graphs/multi_heuristic_astar.py::graphs.multi_heuristic_astar.valid PASSED [100%]

============================== 7 passed in 0.07s ===============================
```

### Ruff Formatting & Linting
```bash
uvx ruff check graphs/multi_heuristic_astar.py
uvx ruff format --check graphs/multi_heuristic_astar.py
```
Output:
```text
All checks passed!
1 file already formatted
```
