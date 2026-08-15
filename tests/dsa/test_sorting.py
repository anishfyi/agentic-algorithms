"""Tests for sorting and binary search."""

from __future__ import annotations

from agentic_algorithms.dsa.sorting import (
    binary_search,
    counting_sort,
    first_position,
    heap_sort,
    last_position,
    lower_bound,
    merge_sort,
    quick_sort,
    radix_sort,
    search_rotated_array,
    upper_bound,
)


def test_sorting_algorithms() -> None:
    nums = [5, 2, 9, 1, 5, 6]
    assert merge_sort(nums) == [1, 2, 5, 5, 6, 9]
    assert quick_sort(nums) == [1, 2, 5, 5, 6, 9]
    assert heap_sort(nums) == [1, 2, 5, 5, 6, 9]
    assert counting_sort([4, 2, 2, 8, 3, 3, 1]) == [1, 2, 2, 3, 3, 4, 8]
    assert radix_sort([170, 45, 75, 90, 802, 24, 2, 66]) == [2, 24, 45, 66, 75, 90, 170, 802]


def test_binary_search_variants() -> None:
    nums = [1, 2, 2, 2, 3, 4, 5]
    assert binary_search(nums, 3) == 4
    assert lower_bound(nums, 2) == 1
    assert upper_bound(nums, 2) == 4
    assert first_position(nums, 2) == 1
    assert last_position(nums, 2) == 3


def test_search_rotated_array() -> None:
    assert search_rotated_array([4, 5, 6, 7, 0, 1, 2], 0) == 4
