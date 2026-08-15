"""Tests for dynamic programming algorithms."""

from __future__ import annotations

from agentic_algorithms.dsa.dp import (
    climb_stairs,
    coin_change,
    coin_change_ways,
    house_robber,
    house_robber_circular,
    knapsack_01,
    longest_increasing_subsequence_nlogn,
    matrix_chain,
    max_square,
    palindrome_partitioning_min_cuts,
    unbounded_knapsack,
)


def test_coin_change() -> None:
    assert coin_change([1, 2, 5], 11) == 3
    assert coin_change_ways([1, 2, 5], 5) == 4


def test_climb_stairs() -> None:
    assert climb_stairs(5) == 8


def test_house_robber() -> None:
    assert house_robber([2, 7, 9, 3, 1]) == 12
    assert house_robber_circular([2, 3, 2]) == 3


def test_lis() -> None:
    assert longest_increasing_subsequence_nlogn([10, 9, 2, 5, 3, 7, 101, 18]) == 4


def test_matrix_chain() -> None:
    assert matrix_chain([10, 30, 5, 60, 20]) == 8500


def test_knapsack() -> None:
    assert knapsack_01([1, 2, 3], [6, 10, 12], 5) == 22
    assert unbounded_knapsack([1, 2, 3], [6, 10, 12], 5) == 30


def test_palindrome_partitioning() -> None:
    assert palindrome_partitioning_min_cuts("aab") == 1


def test_max_square() -> None:
    matrix = [
        ["1", "0", "1", "0", "0"],
        ["1", "0", "1", "1", "1"],
        ["1", "1", "1", "1", "1"],
        ["1", "0", "0", "1", "0"],
    ]
    assert max_square(matrix) == 4
