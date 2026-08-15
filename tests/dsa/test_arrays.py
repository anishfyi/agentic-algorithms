"""Tests for array algorithms."""

from __future__ import annotations

from agentic_algorithms.dsa import arrays as arr


def test_two_sum() -> None:
    assert arr.two_sum([2, 7, 11, 15], 9) == [0, 1]


def test_three_sum() -> None:
    result = arr.three_sum([-1, 0, 1, 2, -1, -4])
    assert [-1, -1, 2] in result
    assert [-1, 0, 1] in result


def test_kadane_variants() -> None:
    nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    assert arr.max_subarray_kadane(nums) == 6
    assert arr.max_subarray_kadane_with_indices(nums) == (6, 3, 6)
    assert arr.min_subarray_kadane(nums) == -5
    assert arr.max_subarray_circular([5, -3, 5]) == 10


def test_product_except_self() -> None:
    assert arr.product_except_self([1, 2, 3, 4]) == [24, 12, 8, 6]


def test_rotate_array() -> None:
    nums = [1, 2, 3, 4, 5, 6, 7]
    arr.rotate_array(nums, 3)
    assert nums == [5, 6, 7, 1, 2, 3, 4]


def test_intervals() -> None:
    assert arr.merge_intervals([[1, 3], [2, 6], [8, 10]]) == [[1, 6], [8, 10]]
    assert arr.insert_interval([[1, 3], [6, 9]], [2, 5]) == [[1, 5], [6, 9]]


def test_find_duplicate_floyd() -> None:
    assert arr.find_duplicate_floyd([1, 3, 4, 2, 2]) == 2


def test_trapping_and_container() -> None:
    assert arr.trapping_rain_water([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6
    assert arr.container_with_most_water([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49


def test_longest_consecutive() -> None:
    assert arr.longest_consecutive([100, 4, 200, 1, 3, 2]) == 4


def test_subarray_sum_equals_k() -> None:
    assert arr.subarray_sum_equals_k([1, 1, 1], 2) == 2


def test_dutch_flag_sort() -> None:
    nums = [2, 0, 2, 1, 1, 0]
    arr.dutch_flag_sort(nums)
    assert nums == [0, 0, 1, 1, 2, 2]


def test_next_permutation() -> None:
    nums = [1, 2, 3]
    arr.next_permutation(nums)
    assert nums == [1, 3, 2]


def test_majority_element() -> None:
    assert arr.majority_element_boyer_moore([3, 2, 3]) == 3


def test_prefix_sum_utilities() -> None:
    prefix = arr.prefix_sum([1, 2, 3, 4])
    assert prefix == [1, 3, 6, 10]
    assert arr.range_sum(prefix, 1, 3) == 9
