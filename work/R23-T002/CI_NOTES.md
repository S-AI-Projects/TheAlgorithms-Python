# CI and Tooling Analysis for `graphs/graph_adjacency_list.py` (R23-T002)

## 1. Overview and Goal
This document investigates how Continuous Integration (CI) and repository tooling in `TheAlgorithms/Python` discover, collect, execute, report on, and index `graphs/graph_adjacency_list.py`. 

Specifically, this file contains both Python doctests and an embedded `unittest.TestCase` class (`TestGraphAdjacencyList`). We explore how pytest discovers both forms of tests, analyze timing and performance (`--durations`), examine code coverage, and trace how repository maintenance scripts (`build_directory_md.py` and `validate_filenames.py`) treat this file.

---

## 2. CI Pytest Command & Configuration

### Pytest Command in `.github/workflows/build.yml`
The CI workflow defined in `.github/workflows/build.yml` runs the following pytest command:

```yaml
run: uv run --with=pytest-run-parallel pytest
  --iterations=8 --parallel-threads=auto --ignore-gil-enabled
  --ignore=computer_vision/flip_augmentation.py
  --ignore=computer_vision/harris_corner.py
  --ignore=computer_vision/mosaic_augmentation.py
  --ignore=data_compression/peak_signal_to_noise_ratio.py
  --ignore=digital_image_processing/
  --ignore=docs/conf.py
  --ignore=project_euler/
  --ignore=scripts/validate_solutions.py
  --ignore=web_programming/current_stock_price.py
  --ignore=web_programming/fetch_anime_and_play.py
  --cov-report=term-missing:skip-covered
  --cov=. .
```

### Pytest Defaults in `pyproject.toml`
In `pyproject.toml`, the `[tool.pytest]` section specifies default options (`addopts`):
```toml
[tool.pytest]
ini_options.addopts = [
  "--durations=10",
  "--doctest-modules",
  "--showlocals",
]
```

### How Pytest Discovers and Collects Both Doctests and Unittest Classes
1. **`--doctest-modules`**:
   Because `--doctest-modules` is configured in `ini_options.addopts`, pytest inspects Python files (`.py`) for docstrings containing interactive Python sessions (`>>> ...`). Each function or method containing docstring tests is collected as a doctest item under the path `graphs/graph_adjacency_list.py::graphs.graph_adjacency_list.<Class>.<method>`.
2. **`unittest.TestCase` Discovery**:
   Pytest includes built-in support for standard Python `unittest`. Any class subclassing `unittest.TestCase` (here, `class TestGraphAdjacencyList(unittest.TestCase)`) is automatically recognized. Pytest collects all methods prefixed with `test_` inside that class as distinct test cases under the identifier `graphs/graph_adjacency_list.py::TestGraphAdjacencyList::<method_name>`.
3. **Unified Execution**:
   Pytest executes both the doctests and the unittest methods within the same test runner session, reporting results uniformly.

---

## 3. Test Collection & Execution Evidence (`-v`)

Running the CI-equivalent command for this file:
```bash
uv run pytest graphs/graph_adjacency_list.py --cov=graphs --cov-report=term-missing -v
```

### Collected Test IDs (7 Doctests + 14 Unittest Methods = 21 Total)
```text
graphs/graph_adjacency_list.py::graphs.graph_adjacency_list.GraphAdjacencyList.add_edge PASSED [  4%]
graphs/graph_adjacency_list.py::graphs.graph_adjacency_list.GraphAdjacencyList.add_vertex PASSED [  9%]
graphs/graph_adjacency_list.py::graphs.graph_adjacency_list.GraphAdjacencyList.clear_graph PASSED [ 14%]
graphs/graph_adjacency_list.py::graphs.graph_adjacency_list.GraphAdjacencyList.contains_edge PASSED [ 19%]
graphs/graph_adjacency_list.py::graphs.graph_adjacency_list.GraphAdjacencyList.contains_vertex PASSED [ 23%]
graphs/graph_adjacency_list.py::graphs.graph_adjacency_list.GraphAdjacencyList.remove_edge PASSED [ 28%]
graphs/graph_adjacency_list.py::graphs.graph_adjacency_list.GraphAdjacencyList.remove_vertex PASSED [ 33%]
graphs/graph_adjacency_list.py::TestGraphAdjacencyList::test_add_and_remove_edges_repeatedly PASSED [ 38%]
graphs/graph_adjacency_list.py::TestGraphAdjacencyList::test_add_and_remove_vertices_repeatedly PASSED [ 42%]
graphs/graph_adjacency_list.py::TestGraphAdjacencyList::test_add_edge PASSED [ 47%]
graphs/graph_adjacency_list.py::TestGraphAdjacencyList::test_add_edge_exception_check PASSED [ 52%]
graphs/graph_adjacency_list.py::TestGraphAdjacencyList::test_add_vertex_exception_check PASSED [ 57%]
graphs/graph_adjacency_list.py::TestGraphAdjacencyList::test_add_vertices PASSED [ 61%]
graphs/graph_adjacency_list.py::TestGraphAdjacencyList::test_contains_edge PASSED [ 66%]
graphs/graph_adjacency_list.py::TestGraphAdjacencyList::test_contains_edge_exception_check PASSED [ 71%]
graphs/graph_adjacency_list.py::TestGraphAdjacencyList::test_contains_vertex PASSED [ 76%]
graphs/graph_adjacency_list.py::TestGraphAdjacencyList::test_init_check PASSED [ 80%]
graphs/graph_adjacency_list.py::TestGraphAdjacencyList::test_remove_edge PASSED [ 85%]
graphs/graph_adjacency_list.py::TestGraphAdjacencyList::test_remove_edge_exception_check PASSED [ 90%]
graphs/graph_adjacency_list.py::TestGraphAdjacencyList::test_remove_vertex_exception_check PASSED [ 95%]
graphs/graph_adjacency_list.py::TestGraphAdjacencyList::test_remove_vertices PASSED [100%]
```

---

## 4. Execution Timing & `--durations` Report

From running pytest with `--durations=10`:
```text
============================= slowest 10 durations =============================
0.01s call     graphs/graph_adjacency_list.py::graphs.graph_adjacency_list.GraphAdjacencyList.add_edge
0.00s call     graphs/graph_adjacency_list.py::TestGraphAdjacencyList::test_contains_edge
0.00s call     graphs/graph_adjacency_list.py::graphs.graph_adjacency_list.GraphAdjacencyList.contains_edge
0.00s call     graphs/graph_adjacency_list.py::graphs.graph_adjacency_list.GraphAdjacencyList.remove_edge
0.00s call     graphs/graph_adjacency_list.py::graphs.graph_adjacency_list.GraphAdjacencyList.add_vertex
0.00s call     graphs/graph_adjacency_list.py::TestGraphAdjacencyList::test_remove_vertex_exception_check
0.00s call     graphs/graph_adjacency_list.py::TestGraphAdjacencyList::test_remove_edge_exception_check
0.00s call     graphs/graph_adjacency_list.py::TestGraphAdjacencyList::test_remove_edge
0.00s call     graphs/graph_adjacency_list.py::graphs.graph_adjacency_list.GraphAdjacencyList.remove_vertex
0.00s teardown graphs/graph_adjacency_list.py::TestGraphAdjacencyList::test_remove_edge
```
Total execution time across all 21 test items is ~0.22 seconds, with each individual test executing in $\le 0.01$s.

---

## 5. Code Coverage Report

Running coverage for `graphs/graph_adjacency_list.py`:
```text
Name                             Stmts   Miss  Cover   Missing
--------------------------------------------------------------
graphs/graph_adjacency_list.py     246      9    96%   56-57, 106-110, 192-196, 271, 336, 678
```
The file achieves 96% line coverage. The only unexecuted statements are the `if __name__ == "__main__":` entrypoint block and defensive exception branches for unsupported internal multigraph configurations.

---

## 6. Repository Tooling Integration

### `DIRECTORY.md`
In `DIRECTORY.md`, the file is indexed under the `Graphs` heading:
```markdown
  * [Graph Adjacency List](graphs/graph_adjacency_list.py)
```

### `scripts/build_directory_md.py`
`scripts/build_directory_md.py` traverses all repository directories with `good_file_paths()`. It filters out hidden files and the `scripts/` directory:
- It strips the `.py` extension.
- It replaces underscores (`_`) with spaces.
- It applies `.title()` capitalization: `graph_adjacency_list.py` becomes `Graph Adjacency List`.
- It nests the link under the top-level section `Graphs` (`graphs` -> `Graphs`).

### `scripts/validate_filenames.py`
`scripts/validate_filenames.py` enforces filename conventions across the repository:
1. All lowercase letters (no uppercase).
2. No spaces in filenames or paths.
3. No hyphens (`-`) in python file paths (uses snake_case).
4. Must reside inside an algorithm directory (`os.sep in file`).

`graphs/graph_adjacency_list.py` satisfies all these criteria: it is entirely lowercase snake_case located inside the `graphs/` directory.

---

## 7. Summary of Changes Made
- Added comprehensive doctests to all public methods in `GraphAdjacencyList`:
  - `add_edge`: Covers directed graph edge insertion, undirected graph edge insertion, and duplicate edge error raising (`ValueError`).
  - `remove_vertex`: Covers directed graph vertex deletion (and edge removal), undirected graph vertex deletion, and non-existent vertex error raising (`ValueError`).
  - `remove_edge`: Covers directed graph edge removal, undirected graph edge removal, and non-existent edge error raising (`ValueError`).
  - `contains_vertex`: Covers existing vertex (`True`) and non-existent vertex (`False`).
  - `contains_edge`: Covers directed graph edge presence/absence, undirected graph symmetry, and non-existent vertex error raising (`ValueError`).
  - `clear_graph`: Covers clearing all vertices and edges leaving an empty adjacency dictionary `{}`.
- Preserved existing doctests in `add_vertex` and all 14 unittest test cases in `TestGraphAdjacencyList`.
