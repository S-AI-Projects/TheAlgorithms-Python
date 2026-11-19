"""
Iterative Binary Tree Flattening Algorithm (Morris Traversal Style).

This module implements an in-place algorithm to flatten a binary tree into
a right-skewed linked list using right child pointers, adhering to pre-order
traversal order (root, left, right).

Unlike the recursive implementation in `flatten_binarytree_to_linkedlist.py`,
which requires O(h) call-stack space (where h is the tree height, up to O(n) in
skewed trees) and repeated subtree right-pointer traversals leading to O(n^2)
time in degenerate cases, this iterative Morris-style approach achieves:
- Time Complexity: O(n), where each tree edge is traversed at most twice.
- Auxiliary Space Complexity: O(1), modifying node pointers in-place without
  recursion, call stack frames, or auxiliary data structures.

References:
- https://www.geeksforgeeks.org/flatten-a-binary-tree-into-linked-list/
- https://leetcode.com/problems/flatten-binary-tree-to-linked-list/
"""

from __future__ import annotations

try:
    from data_structures.binary_tree.flatten_binarytree_to_linkedlist import (
        TreeNode,
        build_tree,
    )
    from data_structures.binary_tree.flatten_binarytree_to_linkedlist import (
        flatten as recursive_flatten,
    )
except ImportError:
    from flatten_binarytree_to_linkedlist import (  # type: ignore[no-redef]
        TreeNode,
        build_tree,
    )
    from flatten_binarytree_to_linkedlist import (  # type: ignore[no-redef]
        flatten as recursive_flatten,
    )

__all__ = [
    "TreeNode",
    "build_tree",
    "display_linked_list",
    "flatten",
    "flatten_iterative",
    "is_flattened",
    "recursive_flatten",
    "to_list",
]


def flatten(root: TreeNode | None) -> None:
    """
    Flatten a binary tree into a linked list in-place using an iterative
    Morris-style traversal with O(1) auxiliary space.

    The resulting linked list follows the tree's pre-order traversal sequence,
    where each node's left child is set to None and its right child points to
    the next node in the traversal.

    Parameters:
        root (TreeNode | None): The root of the binary tree to flatten.

    Raises:
        TypeError: If root is not a TreeNode instance or None.

    Examples:
        >>> tree_iterative = build_tree()
        >>> tree_recursive = build_tree()
        >>> flatten(tree_iterative)
        >>> recursive_flatten(tree_recursive)
        >>> to_list(tree_iterative) == to_list(tree_recursive)
        True
        >>> to_list(tree_iterative)
        [1, 2, 3, 4, 5, 6]
        >>> flatten(None)
        >>> single = TreeNode(42)
        >>> flatten(single)
        >>> to_list(single)
        [42]
        >>> left_tree = TreeNode(10)
        >>> left_tree.left = TreeNode(20)
        >>> left_tree.left.left = TreeNode(30)
        >>> left_tree_rec = TreeNode(10)
        >>> left_tree_rec.left = TreeNode(20)
        >>> left_tree_rec.left.left = TreeNode(30)
        >>> flatten(left_tree)
        >>> recursive_flatten(left_tree_rec)
        >>> to_list(left_tree) == to_list(left_tree_rec)
        True
        >>> to_list(left_tree)
        [10, 20, 30]
        >>> flatten("invalid_input")
        Traceback (most recent call last):
            ...
        TypeError: root must be a TreeNode instance or None
    """
    if root is not None and not isinstance(root, TreeNode):
        raise TypeError("root must be a TreeNode instance or None")

    curr = root
    while curr:
        if curr.left:
            # Find the in-order predecessor: rightmost node in curr's left subtree
            predecessor = curr.left
            while predecessor.right:
                predecessor = predecessor.right

            # Splice curr.right onto predecessor.right
            predecessor.right = curr.right

            # Move left child to right child and clear left pointer
            curr.right = curr.left
            curr.left = None

        # Advance along the right spine
        curr = curr.right


# Alias for explicit naming
flatten_iterative = flatten


def to_list(root: TreeNode | None) -> list[int]:
    """
    Convert a flattened binary tree (right-pointer chain) into a Python list of values.

    Parameters:
        root (TreeNode | None): The root of the flattened binary tree.

    Returns:
        list[int]: Node values in right-pointer sequence.

    Raises:
        TypeError: If root is not a TreeNode instance or None.

    Examples:
        >>> root = TreeNode(1)
        >>> root.right = TreeNode(2)
        >>> root.right.right = TreeNode(3)
        >>> to_list(root)
        [1, 2, 3]
        >>> to_list(None)
        []
        >>> to_list("invalid")
        Traceback (most recent call last):
            ...
        TypeError: root must be a TreeNode instance or None
    """
    if root is not None and not isinstance(root, TreeNode):
        raise TypeError("root must be a TreeNode instance or None")

    result: list[int] = []
    curr = root
    while curr:
        result.append(curr.data)
        curr = curr.right
    return result


def is_flattened(root: TreeNode | None) -> bool:
    """
    Verify whether the binary tree has been flattened so that every node's
    left pointer is None.

    Parameters:
        root (TreeNode | None): Root node to check.

    Returns:
        bool: True if every left pointer is None, False otherwise.

    Raises:
        TypeError: If root is not a TreeNode instance or None.

    Examples:
        >>> is_flattened(None)
        True
        >>> sample = build_tree()
        >>> is_flattened(sample)
        False
        >>> flatten(sample)
        >>> is_flattened(sample)
        True
        >>> is_flattened(123)
        Traceback (most recent call last):
            ...
        TypeError: root must be a TreeNode instance or None
    """
    if root is not None and not isinstance(root, TreeNode):
        raise TypeError("root must be a TreeNode instance or None")

    curr = root
    while curr:
        if curr.left is not None:
            return False
        curr = curr.right
    return True


def display_linked_list(root: TreeNode | None) -> None:
    """
    Display the flattened linked list to stdout.

    Parameters:
        root (TreeNode | None): The root of the flattened linked list.

    Raises:
        TypeError: If root is not a TreeNode instance or None.

    Examples:
        >>> root = TreeNode(1)
        >>> root.right = TreeNode(2)
        >>> root.right.right = TreeNode(3)
        >>> display_linked_list(root)
        1 2 3
        >>> display_linked_list(None)
        >>> display_linked_list(123)
        Traceback (most recent call last):
            ...
        TypeError: root must be a TreeNode instance or None
    """
    if root is not None and not isinstance(root, TreeNode):
        raise TypeError("root must be a TreeNode instance or None")

    current = root
    while current:
        if current.right is None:
            print(current.data, end="")
            break
        print(current.data, end=" ")
        current = current.right


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    print("Flattened Linked List (Iterative Morris):")
    sample_tree = build_tree()
    flatten(sample_tree)
    display_linked_list(sample_tree)
    print()
