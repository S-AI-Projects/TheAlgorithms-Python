"""Iterative (stack-based) algorithm to merge two binary trees.

Problem Description:
Given two binary trees, return the merged tree.
The rule for merging is that if two nodes overlap, then put the value sum
of both nodes as the new value of the merged node. Otherwise, the non-null
node will be used as the node of the new tree.

Reference:
https://leetcode.com/problems/merge-two-binary-trees/
"""

from __future__ import annotations


class Node:
    """A binary tree node with an integer value and left/right child pointers."""

    def __init__(self, value: int = 0) -> None:
        self.value = value
        self.left: Node | None = None
        self.right: Node | None = None


def merge_two_binary_trees_iterative(
    tree1: Node | None, tree2: Node | None
) -> Node | None:
    """Return the root node of the merged binary tree using an explicit stack.

    If two nodes overlap, their values are summed in tree1.
    If tree1 lacks a subtree where tree2 has one, tree2's subtree is attached.
    The merge modifies tree1 in-place and returns its root.

    >>> tree1 = Node(5)
    >>> tree1.left = Node(6)
    >>> tree1.right = Node(7)
    >>> tree1.left.left = Node(2)
    >>> tree2 = Node(4)
    >>> tree2.left = Node(5)
    >>> tree2.right = Node(8)
    >>> tree2.left.right = Node(1)
    >>> tree2.right.right = Node(4)
    >>> merged_tree = merge_two_binary_trees_iterative(tree1, tree2)
    >>> print_preorder(merged_tree)
    9
    11
    2
    1
    15
    4

    Verify identical pre-order traversal with recursive implementation:
    >>> from data_structures.binary_tree.merge_two_binary_trees import (
    ...     merge_two_binary_trees as recursive_merge,
    ... )
    >>> t1_rec = Node(5)
    >>> t1_rec.left = Node(6)
    >>> t1_rec.right = Node(7)
    >>> t1_rec.left.left = Node(2)
    >>> t2_rec = Node(4)
    >>> t2_rec.left = Node(5)
    >>> t2_rec.right = Node(8)
    >>> t2_rec.left.right = Node(1)
    >>> t2_rec.right.right = Node(4)
    >>> rec_merged = recursive_merge(t1_rec, t2_rec)
    >>> get_preorder(merged_tree) == get_preorder(rec_merged)
    True

    Empty tree cases:
    >>> merge_two_binary_trees_iterative(None, None) is None
    True
    >>> single = Node(42)
    >>> merge_two_binary_trees_iterative(single, None) is single
    True
    >>> merge_two_binary_trees_iterative(None, single) is single
    True

    Invalid input validation:
    >>> merge_two_binary_trees_iterative("not a node", None)
    Traceback (most recent call last):
        ...
    TypeError: tree1 must be an instance of Node or None, got str
    >>> merge_two_binary_trees_iterative(None, [1, 2, 3])
    Traceback (most recent call last):
        ...
    TypeError: tree2 must be an instance of Node or None, got list
    """
    if tree1 is not None and not isinstance(tree1, Node):
        msg = f"tree1 must be an instance of Node or None, got {type(tree1).__name__}"
        raise TypeError(msg)
    if tree2 is not None and not isinstance(tree2, Node):
        msg = f"tree2 must be an instance of Node or None, got {type(tree2).__name__}"
        raise TypeError(msg)

    if tree1 is None:
        return tree2
    if tree2 is None:
        return tree1

    stack: list[tuple[Node, Node]] = [(tree1, tree2)]
    while stack:
        node1, node2 = stack.pop()
        node1.value += node2.value

        # Push right before left so left is processed first (pre-order traversal)
        if node1.right is not None and node2.right is not None:
            stack.append((node1.right, node2.right))
        elif node1.right is None:
            node1.right = node2.right

        if node1.left is not None and node2.left is not None:
            stack.append((node1.left, node2.left))
        elif node1.left is None:
            node1.left = node2.left

    return tree1


def get_preorder(root: Node | None) -> list[int]:
    """Return pre-order traversal of the tree as a list of integers.

    >>> root = Node(1)
    >>> root.left = Node(2)
    >>> root.right = Node(3)
    >>> get_preorder(root)
    [1, 2, 3]
    >>> get_preorder(None)
    []
    """
    if root is None:
        return []
    result = [root.value]
    result.extend(get_preorder(root.left))
    result.extend(get_preorder(root.right))
    return result


def print_preorder(root: Node | None) -> None:
    """Print pre-order traversal values line by line.

    >>> root = Node(1)
    >>> root.left = Node(2)
    >>> root.right = Node(3)
    >>> print_preorder(root)
    1
    2
    3
    >>> print_preorder(None)
    """
    if root is not None:
        print(root.value)
        print_preorder(root.left)
        print_preorder(root.right)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
