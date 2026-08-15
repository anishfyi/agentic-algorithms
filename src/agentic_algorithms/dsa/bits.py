"""Bit manipulation algorithms."""

from __future__ import annotations


def count_bits(n: int) -> list[int]:
    """Return count of set bits for every number from 0 to n.

    Time: O(n). Space: O(n).
    """
    result = [0] * (n + 1)
    for i in range(1, n + 1):
        result[i] = result[i >> 1] + (i & 1)
    return result


def single_number_xor(nums: list[int]) -> int:
    """Return element that appears once when all others appear twice.

    Time: O(n). Space: O(1).
    """
    result = 0
    for value in nums:
        result ^= value
    return result


def power_of_two(n: int) -> bool:
    """Return True if n is a power of two.

    Time: O(1). Space: O(1).
    """
    return n > 0 and (n & (n - 1)) == 0


def subsets_bitmask(nums: list[int]) -> list[list[int]]:
    """Generate all subsets using bitmask enumeration.

    Time: O(n * 2^n). Space: O(n).
    """
    n = len(nums)
    result: list[list[int]] = []
    for mask in range(1 << n):
        subset = [nums[i] for i in range(n) if mask & (1 << i)]
        result.append(subset)
    return result
