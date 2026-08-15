"""Heap data structures and algorithms."""

from __future__ import annotations

from heapq import heapify, heappop, heappush

from agentic_algorithms.dsa.linked_lists import ListNode


class MinHeap:
    """Binary min-heap supporting push, pop, and peek.

    Time: O(log n) push/pop, O(1) peek. Space: O(n).
    """

    def __init__(self, values: list[int] | None = None) -> None:
        self._data = list(values or [])
        heapify(self._data)

    def push(self, value: int) -> None:
        """Insert value into heap."""
        heappush(self._data, value)

    def pop(self) -> int:
        """Remove and return minimum element."""
        return heappop(self._data)

    def peek(self) -> int:
        """Return minimum element without removing it."""
        return self._data[0]

    def __len__(self) -> int:
        return len(self._data)

    def __bool__(self) -> bool:
        return bool(self._data)


class MaxHeap:
    """Binary max-heap via negation wrapper around MinHeap.

    Time: O(log n) push/pop, O(1) peek. Space: O(n).
    """

    def __init__(self, values: list[int] | None = None) -> None:
        self._heap = MinHeap([-v for v in values] if values else [])

    def push(self, value: int) -> None:
        self._heap.push(-value)

    def pop(self) -> int:
        return -self._heap.pop()

    def peek(self) -> int:
        return -self._heap.peek()

    def __len__(self) -> int:
        return len(self._heap)

    def __bool__(self) -> bool:
        return bool(self._heap)


def kth_largest(nums: list[int], k: int) -> int:
    """Return k-th largest element using a size-k min heap.

    Time: O(n log k). Space: O(k).
    """
    heap = MinHeap(nums[:k])
    for value in nums[k:]:
        if value > heap.peek():
            heap.pop()
            heap.push(value)
    return heap.peek()


def merge_k_sorted_lists(lists: list[ListNode | None]) -> ListNode | None:
    """Merge k sorted linked lists.

    Time: O(n log k). Space: O(k).
    """
    heap: list[tuple[int, int, ListNode]] = []
    for index, node in enumerate(lists):
        if node:
            heappush(heap, (node.val, index, node))
    dummy = ListNode()
    tail = dummy
    while heap:
        _, index, node = heappop(heap)
        tail.next = node
        tail = tail.next
        if node.next:
            heappush(heap, (node.next.val, index, node.next))
    return dummy.next


class MedianFinder:
    """Maintain median of a data stream using two heaps.

    Time: O(log n) add_num, O(1) find_median. Space: O(n).
    """

    def __init__(self) -> None:
        self._low = MaxHeap()
        self._high = MinHeap()

    def add_num(self, num: int) -> None:
        """Add integer to the stream."""
        self._low.push(num)
        self._high.push(self._low.pop())
        if len(self._low) < len(self._high):
            self._low.push(self._high.pop())

    def find_median(self) -> float:
        """Return current median."""
        if len(self._low) > len(self._high):
            return float(self._low.peek())
        return (self._low.peek() + self._high.peek()) / 2.0
