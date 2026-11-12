# R23-T021 Findings: SkipList Type Hints and Bug Fix

## Task Overview
Add accurate type hints so the type checker CI runs (`ty`) has nothing to report for `data_structures/linked_list/skip_list.py`.
Four functions lacked hints in the generic `SkipList[KT, VT]`:
- `__iter__`
- `_locate_node`
- `traverse_keys`
- `is_sorted`

## Findings and Implementation Details

### 1. `SkipList.__iter__`
- **Location**: `data_structures/linked_list/skip_list.py:110`
- **Signature**: `def __iter__(self) -> Iterator[KT]:`
- **Analysis**:
  `SkipList` is parameterized over `[KT, VT]`. The iterator traverses user-inserted elements in `node.forward[0]` and yields their keys.
  Because the header sentinel `self.head` is instantiated with default key `"root"` (`key: KT | str = "root"` on `Node`), `Node.key` has type `KT | str`.
  When `__iter__` yields `node.forward[0].key`, the type checker initially flags an `invalid-yield` (`KT | str` is not assignable to `KT`).
  Since only user-inserted nodes (`key: KT`) exist in `node.forward[0]`, `cast(KT, node.forward[0].key)` cleanly asserts the key type without altering runtime behaviour.

### 2. `SkipList._locate_node`
- **Location**: `data_structures/linked_list/skip_list.py:129`
- **Signature**: `def _locate_node(self, key: KT) -> tuple[Node[KT, VT] | None, list[Node[KT, VT]]]:`
- **Analysis**:
  The parameter `key` previously had no type annotation. Adding `key: KT` makes it consistent with `delete(key: KT)` and `insert(key: KT, value: VT)`.

### 3. `traverse_keys`
- **Location**: Inside `test_delete_doesnt_leave_dead_nodes()` (line 387)
- **Signature**: `def traverse_keys(node: Node[str, int]) -> Iterator[str]:`
- **Analysis**:
  In `test_delete_doesnt_leave_dead_nodes`, `skip_list` contains string keys (`"Key1"`, `"V"`, etc.) and integer values (`12`, `13`, etc.).
  The recursive generator visits nodes starting at `skip_list.head: Node[str, int]` and yields `node.key: str`.
  We use precise types `Node[str, int]` and `Iterator[str]` rather than `Any`.

### 4. `is_sorted`
- **Location**: Inside `test_iter_always_yields_sorted_values()` (line 396)
- **Signature**: `def is_sorted(lst: list[int]) -> bool:`
- **Analysis**:
  In `test_iter_always_yields_sorted_values`, `list(skip_list)` produces `list[int]` because integer keys are inserted.
  Annotated with parameter `lst: list[int]` and return type `bool`.

### 5. Bug Exposed by Type Checker
- **Location**: `SkipList.find` (line 227)
- **Issue**:
  The method previously had the signature:
  `def find(self, key: VT) -> VT | None:`
  The parameter `key` was incorrectly annotated as value type `VT` instead of key type `KT`.
  When `_locate_node(self, key: KT)` received its type annotation, calling `self._locate_node(key)` inside `find` resulted in:
  `Expected KT@SkipList, found VT@SkipList`
- **Fix**:
  Updated parameter to `def find(self, key: KT) -> VT | None:`.
- **Doctest Added**:
  Added a doctest to `find` demonstrating lookup on a `SkipList[str, int]` where `KT != VT`:
  ```python
  >>> str_skip_list: SkipList[str, int] = SkipList()
  >>> str_skip_list.insert("Key", 100)
  >>> str_skip_list.find("Key")
  100
  >>> str_skip_list.find("Missing") is None
  True
  ```

## Verification
- `uv run --python 3.15 --with ty ty check data_structures/linked_list/skip_list.py`:
  Zero diagnostics for `data_structures/linked_list/skip_list.py`.
- `uv run --python 3.15 pytest -v data_structures/linked_list/skip_list.py`:
  All 16 test items passed.
- `uv run --python 3.15 python -m doctest -v data_structures/linked_list/skip_list.py`:
  All 36 doctests passed.
