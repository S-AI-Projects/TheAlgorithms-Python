### Describe your change

* [ ] Add an algorithm?
* [x] Fix a bug or typo in an existing algorithm?
* [x] Add or change doctests? -- Note: Please avoid changing both code and tests in a single pull request.
* [ ] Documentation change?

### Checklist

* [x] I have read [CONTRIBUTING.md](https://github.com/TheAlgorithms/Python/blob/master/CONTRIBUTING.md).
* [x] This pull request is all my own work -- I have not plagiarized.
* [x] I know that pull requests will not be merged if they fail the automated tests.
* [x] This PR only changes one algorithm file. To ease review, please open separate PRs for separate algorithms.
* [x] All new Python files are placed inside an existing directory.
* [x] All filenames are in all lowercase characters with no spaces or dashes.
* [x] All functions and variable names follow Python naming conventions.
* [x] All function parameters and return values are annotated with Python [type hints](https://docs.python.org/3/library/typing.html).
* [x] All functions have [doctests](https://docs.python.org/3/library/doctest.html) that pass the automated testing.
* [x] All new algorithms include at least one URL that points to Wikipedia or another similar explanation.
* [x] If this pull request resolves one or more open issues, then the description above includes the issue number(s) with a [closing keyword](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue): "Fixes #3".

---

## Description

Adds accurate parameter and return type annotations to all four unhinted functions in `data_structures/linked_list/skip_list.py`: `__iter__`, `_locate_node`, `traverse_keys`, and `is_sorted`, keeping generics consistent with `SkipList[KT, VT]`. Fixes a real bug exposed in `find()` where parameter `key` was typed as `VT` instead of `KT`, and adds a doctest verifying lookup on a `SkipList[str, int]`.

## Related Issue

Fixes: #3

## Type of Change

- [x] Bug Fix
- [ ] New Feature
- [ ] UI/UX Improvement
- [ ] Performance Improvement
- [x] Tests
- [ ] Documentation
- [x] Refactoring / Maintenance
- [ ] CI/CD

## Changes Made

- `data_structures/linked_list/skip_list.py`:
  - `SkipList.__iter__(self) -> Iterator[KT]`: Added return type hint using `collections.abc.Iterator[KT]` and `cast(KT, node.forward[0].key)` so that `__iter__` consistently yields `KT`.
  - `SkipList._locate_node(self, key: KT) -> tuple[Node[KT, VT] | None, list[Node[KT, VT]]]`: Annotated parameter `key: KT`.
  - `SkipList.find(self, key: KT) -> VT | None`: Fixed parameter type from `VT` to `KT` (exposed by type checking `_locate_node(key)`), and added a doctest verifying lookup on `SkipList[str, int]`.
  - `traverse_keys(node: Node[str, int]) -> Iterator[str]`: Inside `test_delete_doesnt_leave_dead_nodes()`, annotated parameter and return with concrete types.
  - `is_sorted(lst: list[int]) -> bool`: Inside `test_iter_always_yields_sorted_values()`, annotated parameter as `list[int]` and return type as `bool`.
- `work/R23-T021/`: Added `FINDINGS.md`, `ty_before.txt`, `ty_after.txt`, and `test_output.txt` documenting before/after type checking runs and test results.

## Screenshots / Recordings

Not applicable (no UI changes).

## Testing

- `uv run --python 3.15 --with ty ty check data_structures/linked_list/skip_list.py` -> 0 diagnostics for the file.
- `uv run --python 3.15 pytest -v data_structures/linked_list/skip_list.py` -> 16/16 passed.
- `uv run --python 3.15 python -m doctest -v data_structures/linked_list/skip_list.py` -> 36/36 passed.

## Additional Notes

- Findings:
  1. In `SkipList.__iter__`, `node.forward[0].key` carries type `KT | str` because `Node.key` defaults to `"root"` on `self.head`. Using `cast(KT, ...)` reflects that only user-inserted nodes (`key: KT`) exist in `node.forward`.
  2. Annotating `_locate_node(key: KT)` directly exposed a type bug in `find(key: VT)`: `find` was passing `key: VT` into `_locate_node(key: KT)`. Correcting `find(key: KT)` resolves this issue.
  3. A second branch `R23-T021-upstream` containing only the code change (no `work/` folder) has been created and pushed for a later upstream PR.
