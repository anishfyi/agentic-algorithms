"""Tests for segment tree."""

from __future__ import annotations

from agentic_algorithms.dsa.segments import SegmentTree


def test_segment_tree_sum() -> None:
    tree = SegmentTree([1, 3, 5, 7, 9, 11], operation="sum")
    assert tree.query(1, 3) == 15
    tree.update(1, 10)
    assert tree.query(1, 3) == 22


def test_segment_tree_min() -> None:
    tree = SegmentTree([3, 1, 4, 2], operation="min")
    assert tree.query(0, 3) == 1
