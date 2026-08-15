"""Segment tree for range queries."""

from __future__ import annotations

from collections.abc import Callable
from typing import Literal

Operation = Literal["sum", "min"]


class SegmentTree:
    """Segment tree supporting range sum and range minimum queries.

    Build time: O(n). Query/update: O(log n). Space: O(n).
    """

    def __init__(self, nums: list[int], operation: Operation = "sum") -> None:
        self._operation = operation
        self._n = len(nums)
        size = 1
        while size < self._n:
            size <<= 1
        self._size = size
        if operation == "sum":
            self._identity: int | float = 0
            self._combine: Callable[[int | float, int | float], int | float] = lambda a, b: a + b
        else:
            self._identity = float("inf")
            self._combine = lambda a, b: min(a, b)
        self._tree: list[int | float] = [self._identity] * (2 * size)
        for i, value in enumerate(nums):
            self._tree[size + i] = value
        for i in range(size - 1, 0, -1):
            self._tree[i] = self._combine(self._tree[2 * i], self._tree[2 * i + 1])

    def update(self, index: int, value: int) -> None:
        """Point update at index."""
        pos = self._size + index
        self._tree[pos] = value
        pos //= 2
        while pos:
            self._tree[pos] = self._combine(self._tree[2 * pos], self._tree[2 * pos + 1])
            pos //= 2

    def query(self, left: int, right: int) -> int | float:
        """Inclusive range query on [left, right]."""
        left += self._size
        right += self._size
        result: int | float = self._identity
        while left <= right:
            if left % 2 == 1:
                result = self._combine(result, self._tree[left])
                left += 1
            if right % 2 == 0:
                result = self._combine(result, self._tree[right])
                right -= 1
            left //= 2
            right //= 2
        return result
