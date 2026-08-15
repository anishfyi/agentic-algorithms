"""Stack and queue algorithms."""

from __future__ import annotations

from collections import deque
from typing import Protocol


class MinStackProtocol(Protocol):
    def push(self, value: int) -> None: ...
    def pop(self) -> None: ...
    def top(self) -> int: ...
    def get_min(self) -> int: ...


def daily_temperatures(temperatures: list[int]) -> list[int]:
    """Monotonic decreasing stack. Time O(n), space O(n)."""
    answer = [0] * len(temperatures)
    stack: list[int] = []
    for index, temp in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < temp:
            prev = stack.pop()
            answer[prev] = index - prev
        stack.append(index)
    return answer


def largest_rectangle_histogram(heights: list[int]) -> int:
    """Monotonic increasing stack. Time O(n), space O(n)."""
    stack: list[int] = []
    best = 0
    heights = [*heights, 0]
    for index, height in enumerate(heights):
        while stack and heights[stack[-1]] > height:
            h = heights[stack.pop()]
            width = index if not stack else index - stack[-1] - 1
            best = max(best, h * width)
        stack.append(index)
    return best


def sliding_window_max(nums: list[int], k: int) -> list[int]:
    """Deque monotonic queue. Time O(n), space O(k)."""
    if k <= 0 or not nums:
        return []
    window: deque[int] = deque()
    result: list[int] = []
    for index, value in enumerate(nums):
        while window and nums[window[-1]] <= value:
            window.pop()
        window.append(index)
        if window[0] <= index - k:
            window.popleft()
        if index >= k - 1:
            result.append(nums[window[0]])
    return result


def evaluate_rpn(tokens: list[str]) -> int:
    """Stack evaluation. Time O(n), space O(n)."""
    stack: list[int] = []
    for token in tokens:
        if token == "+":
            right = stack.pop()
            left = stack.pop()
            stack.append(left + right)
        elif token == "-":
            right = stack.pop()
            left = stack.pop()
            stack.append(left - right)
        elif token == "*":
            right = stack.pop()
            left = stack.pop()
            stack.append(left * right)
        elif token == "/":
            right = stack.pop()
            left = stack.pop()
            stack.append(int(left / right))
        else:
            stack.append(int(token))
    return stack[0]


class MinStack:
    """Min stack with O(1) push, pop, top, and get_min."""

    def __init__(self) -> None:
        self._main: list[int] = []
        self._mins: list[int] = []

    def push(self, value: int) -> None:
        self._main.append(value)
        self._mins.append(value if not self._mins else min(value, self._mins[-1]))

    def pop(self) -> None:
        self._main.pop()
        self._mins.pop()

    def top(self) -> int:
        return self._main[-1]

    def get_min(self) -> int:
        return self._mins[-1]
