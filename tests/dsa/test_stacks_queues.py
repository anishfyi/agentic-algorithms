"""Tests for stack and queue algorithms."""

from agentic_algorithms.dsa.stacks_queues import (
    MinStack,
    daily_temperatures,
    evaluate_rpn,
    largest_rectangle_histogram,
    sliding_window_max,
)


def test_daily_temperatures() -> None:
    assert daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]) == [1, 1, 4, 2, 1, 1, 0, 0]


def test_largest_rectangle_histogram() -> None:
    assert largest_rectangle_histogram([2, 1, 5, 6, 2, 3]) == 10


def test_sliding_window_max() -> None:
    assert sliding_window_max([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]


def test_evaluate_rpn() -> None:
    assert evaluate_rpn(["2", "1", "+", "3", "*"]) == 9


def test_min_stack() -> None:
    stack = MinStack()
    stack.push(2)
    stack.push(1)
    assert stack.get_min() == 1
    stack.pop()
    assert stack.top() == 2
