"""Tests for heap algorithms."""

from __future__ import annotations

from agentic_algorithms.dsa.heap import MaxHeap, MedianFinder, MinHeap, kth_largest
from agentic_algorithms.dsa.linked_lists import ListNode


def _from_list(values: list[int]) -> ListNode | None:
    dummy = ListNode()
    tail = dummy
    for value in values:
        tail.next = ListNode(value)
        tail = tail.next
    return dummy.next


def test_min_max_heap() -> None:
    min_heap = MinHeap([3, 1, 4])
    assert min_heap.pop() == 1
    max_heap = MaxHeap([3, 1, 4])
    assert max_heap.pop() == 4


def test_kth_largest() -> None:
    assert kth_largest([3, 2, 1, 5, 6, 4], 2) == 5


def test_median_finder() -> None:
    finder = MedianFinder()
    for value in [1, 2, 3, 4]:
        finder.add_num(value)
    assert finder.find_median() == 2.5
