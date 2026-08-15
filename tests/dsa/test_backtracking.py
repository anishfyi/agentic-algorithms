"""Tests for backtracking algorithms."""

from __future__ import annotations

from agentic_algorithms.dsa.backtracking import (
    combination_sum,
    combinations,
    n_queens,
    permutations,
    subsets,
    word_search,
)


def test_permutations() -> None:
    expected = [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
    assert sorted(permutations([1, 2, 3])) == sorted(expected)


def test_combinations_and_subsets() -> None:
    assert combinations(4, 2) == [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]
    assert subsets([1, 2]) == [[], [1], [1, 2], [2]]


def test_combination_sum() -> None:
    result = combination_sum([2, 3, 6, 7], 7)
    assert [2, 2, 3] in result
    assert [7] in result


def test_n_queens() -> None:
    assert len(n_queens(4)) == 2


def test_word_search() -> None:
    board = [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]]
    assert word_search(board, "ABCCED")
