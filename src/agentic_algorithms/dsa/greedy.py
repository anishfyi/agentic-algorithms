"""Greedy algorithms."""

from __future__ import annotations

from collections import Counter


def activity_selection(start: list[int], end: list[int]) -> int:
    """Return maximum number of non-overlapping activities.

    Time: O(n log n). Space: O(n).
    """
    activities = sorted(zip(end, start, strict=True))
    count = 0
    last_end = float("-inf")
    for finish, begin in activities:
        if begin >= last_end:
            count += 1
            last_end = finish
    return count


def jump_game(nums: list[int]) -> bool:
    """Return True if last index is reachable from index 0.

    Time: O(n). Space: O(1).
    """
    farthest = 0
    for i, reach in enumerate(nums):
        if i > farthest:
            return False
        farthest = max(farthest, i + reach)
    return True


def gas_station(gas: list[int], cost: list[int]) -> int:
    """Return starting gas station index for circular tour, or -1.

    Time: O(n). Space: O(1).
    """
    total_tank = current_tank = 0
    start = 0
    for i in range(len(gas)):
        diff = gas[i] - cost[i]
        total_tank += diff
        current_tank += diff
        if current_tank < 0:
            start = i + 1
            current_tank = 0
    return start if total_tank >= 0 else -1


def partition_labels(s: str) -> list[int]:
    """Partition string into parts where each letter appears in at most one part.

    Time: O(n). Space: O(k).
    """
    last = {char: index for index, char in enumerate(s)}
    parts: list[int] = []
    start = end = 0
    for i, char in enumerate(s):
        end = max(end, last[char])
        if i == end:
            parts.append(end - start + 1)
            start = i + 1
    return parts


def task_scheduler(tasks: list[str], n: int) -> int:
    """Minimum time to complete tasks with cooldown n between identical tasks.

    Time: O(n). Space: O(k).
    """
    counts = Counter(tasks)
    max_count = max(counts.values())
    max_count_tasks = sum(1 for count in counts.values() if count == max_count)
    return max(len(tasks), (max_count - 1) * (n + 1) + max_count_tasks)
