"""
Persistent segment tree for range minimum queries.

Point updates create a new root while sharing untouched subtrees, so queries
can target any earlier version. Building takes O(n) time and space; each update
and inclusive range query takes O(log n) time, and each update adds O(log n)
nodes.

Reference: https://cp-algorithms.com/data_structures/segment_tree.html
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class _Node:
    """An immutable segment-tree node."""

    minimum: int
    left: _Node | None = None
    right: _Node | None = None


class PersistentSegmentTreeMin:
    """
    Store immutable versions of a list and answer inclusive range-minimum queries.

    Updating a version does not change it or any other existing version:
    >>> tree = PersistentSegmentTreeMin([8, 3, 7, 2, 6])
    >>> original = [8, 3, 7, 2, 6]
    >>> first_version = tree.update(0, 1, 9)
    >>> first_update = [8, 9, 7, 2, 6]
    >>> second_version = tree.update(first_version, 3, -4)
    >>> second_update = [8, 9, 7, -4, 6]
    >>> versions = [original, first_update, second_update]
    >>> all(
    ...     tree.query(version, left, right) == min(values[left : right + 1])
    ...     for version, values in enumerate(versions)
    ...     for left, right in ((0, 2), (1, 4), (2, 3))
    ... )
    True
    >>> tree.query(0, 0, 4), tree.query(first_version, 0, 4)
    (2, 2)
    >>> tree.query(second_version, 0, 4)
    -4

    The sum sibling keeps the same versioning pattern but returns sums:
    >>> from data_structures.binary_tree.persistent_segment_tree import (
    ...     PersistentSegmentTree,
    ... )
    >>> sum_tree = PersistentSegmentTree(original)
    >>> sum_first_version = sum_tree.update(0, 1, 9)
    >>> sum_second_version = sum_tree.update(sum_first_version, 3, -4)
    >>> [
    ...     (sum_tree.query(version, 0, 4), tree.query(version, 0, 4))
    ...     for version in (0, first_version, second_version)
    ... ]
    [(26, 2), (32, 2), (26, -4)]

    Unchanged subtrees are shared by versions:
    >>> tree.roots[0].right is tree.roots[first_version].right
    True
    >>> tree.roots[first_version].left is tree.roots[second_version].left
    True
    """

    def __init__(self, values: Sequence[int]) -> None:
        """
        Build the initial version from a non-empty sequence of integers.

        >>> PersistentSegmentTreeMin([])
        Traceback (most recent call last):
        ...
        ValueError: values must not be empty
        """
        if not values:
            raise ValueError("values must not be empty")

        self.n: int = len(values)
        self.roots: list[_Node] = [self._build(values, 0, self.n - 1)]

    def _build(self, values: Sequence[int], start: int, end: int) -> _Node:
        """Build a tree whose nodes store the minimum of their segment."""
        if start == end:
            return _Node(values[start])

        middle = (start + end) // 2
        left_node = self._build(values, start, middle)
        right_node = self._build(values, middle + 1, end)
        return _Node(min(left_node.minimum, right_node.minimum), left_node, right_node)

    def update(self, version: int, index: int, value: int) -> int:
        """
        Return a new version with ``values[index]`` replaced by ``value``.

        >>> tree = PersistentSegmentTreeMin([5, 2])
        >>> updated_version = tree.update(0, 0, 1)
        >>> tree.query(updated_version, 0, 1), tree.query(0, 0, 1)
        (1, 2)
        >>> tree.update(2, 0, 3)
        Traceback (most recent call last):
        ...
        IndexError: version out of range
        >>> tree.update(0, 2, 3)
        Traceback (most recent call last):
        ...
        IndexError: index out of range
        """
        if version < 0 or version >= len(self.roots):
            raise IndexError("version out of range")
        if index < 0 or index >= self.n:
            raise IndexError("index out of range")

        new_root = self._update(self.roots[version], 0, self.n - 1, index, value)
        self.roots.append(new_root)
        return len(self.roots) - 1

    def _update(
        self, node: _Node, start: int, end: int, index: int, value: int
    ) -> _Node:
        """Copy the updated path and reuse each untouched child."""
        if start == end:
            return _Node(value)

        middle = (start + end) // 2
        assert node.left is not None and node.right is not None
        if index <= middle:
            new_left = self._update(node.left, start, middle, index, value)
            return _Node(
                min(new_left.minimum, node.right.minimum), new_left, node.right
            )

        new_right = self._update(node.right, middle + 1, end, index, value)
        return _Node(min(node.left.minimum, new_right.minimum), node.left, new_right)

    def query(self, version: int, left: int, right: int) -> int:
        """
        Return the minimum value in the inclusive range ``[left, right]``.

        >>> tree = PersistentSegmentTreeMin((4, 3, 7))
        >>> tree.query(0, 1, 2)
        3
        >>> tree.query(0, -1, 1)
        Traceback (most recent call last):
        ...
        IndexError: query bounds out of range
        >>> tree.query(0, 2, 1)
        Traceback (most recent call last):
        ...
        ValueError: left bound must not exceed right bound
        >>> tree.query(1, 0, 1)
        Traceback (most recent call last):
        ...
        IndexError: version out of range
        """
        if version < 0 or version >= len(self.roots):
            raise IndexError("version out of range")
        if left < 0 or right < 0 or left >= self.n or right >= self.n:
            raise IndexError("query bounds out of range")
        if left > right:
            raise ValueError("left bound must not exceed right bound")

        return self._query(self.roots[version], 0, self.n - 1, left, right)

    def _query(
        self, node: _Node, start: int, end: int, left: int, right: int
    ) -> int:
        """Return the minimum for a query known to be inside this segment."""
        if left <= start and end <= right:
            return node.minimum

        middle = (start + end) // 2
        assert node.left is not None and node.right is not None
        if right <= middle:
            return self._query(node.left, start, middle, left, right)
        if left > middle:
            return self._query(node.right, middle + 1, end, left, right)

        return min(
            self._query(node.left, start, middle, left, middle),
            self._query(node.right, middle + 1, end, middle + 1, right),
        )
