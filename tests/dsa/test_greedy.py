"""Tests for greedy algorithms."""

from __future__ import annotations

from agentic_algorithms.dsa.greedy import (
    activity_selection,
    gas_station,
    jump_game,
    partition_labels,
    task_scheduler,
)


def test_activity_selection() -> None:
    assert activity_selection([1, 2, 3], [3, 4, 5]) == 2


def test_jump_game() -> None:
    assert jump_game([2, 3, 1, 1, 4])
    assert not jump_game([3, 2, 1, 0, 4])


def test_gas_station() -> None:
    assert gas_station([1, 2, 3, 4, 5], [3, 4, 5, 1, 2]) == 3


def test_partition_labels() -> None:
    assert partition_labels("ababcbacadefegdehijhklij") == [9, 7, 8]


def test_task_scheduler() -> None:
    assert task_scheduler(["A", "A", "A", "B", "B", "B"], 2) == 8
