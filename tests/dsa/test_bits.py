"""Tests for bit manipulation algorithms."""

from __future__ import annotations

from agentic_algorithms.dsa.bits import (
    count_bits,
    power_of_two,
    single_number_xor,
    subsets_bitmask,
)


def test_count_bits() -> None:
    assert count_bits(5) == [0, 1, 1, 2, 1, 2]


def test_single_number_xor() -> None:
    assert single_number_xor([4, 1, 2, 1, 2]) == 4


def test_power_of_two() -> None:
    assert power_of_two(16)
    assert not power_of_two(18)


def test_subsets_bitmask() -> None:
    assert subsets_bitmask([1, 2]) == [[], [1], [2], [1, 2]]
