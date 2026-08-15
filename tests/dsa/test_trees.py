"""Tests for tree algorithms."""

from __future__ import annotations

from agentic_algorithms.dsa.trees import (
    TreeNode,
    build_from_preorder_inorder,
    deserialize,
    diameter,
    inorder_iterative,
    inorder_recursive,
    is_valid_bst,
    level_order,
    max_depth,
    path_sum,
    serialize,
)


def _sample_tree() -> TreeNode:
    return TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3, TreeNode(6), TreeNode(7)))


def test_traversals() -> None:
    root = _sample_tree()
    assert inorder_recursive(root) == [4, 2, 5, 1, 6, 3, 7]
    assert inorder_iterative(root) == [4, 2, 5, 1, 6, 3, 7]
    assert level_order(root) == [[1], [2, 3], [4, 5, 6, 7]]


def test_max_depth_and_diameter() -> None:
    root = _sample_tree()
    assert max_depth(root) == 3
    assert diameter(root) == 4


def test_is_valid_bst() -> None:
    valid = TreeNode(2, TreeNode(1), TreeNode(3))
    invalid = TreeNode(5, TreeNode(1), TreeNode(4, TreeNode(3), TreeNode(6)))
    assert is_valid_bst(valid)
    assert not is_valid_bst(invalid)


def test_serialize_deserialize() -> None:
    root = _sample_tree()
    data = serialize(root)
    restored = deserialize(data)
    assert serialize(restored) == data


def test_path_sum() -> None:
    root = TreeNode(5, TreeNode(4, TreeNode(11, TreeNode(7), TreeNode(2))), TreeNode(8))
    assert path_sum(root, 22)


def test_build_from_preorder_inorder() -> None:
    root = build_from_preorder_inorder([3, 9, 20, 15, 7], [9, 3, 15, 20, 7])
    assert inorder_recursive(root) == [9, 3, 15, 20, 7]
