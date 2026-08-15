"""Tests for linked list algorithms."""

from __future__ import annotations

from agentic_algorithms.dsa.linked_lists import (
    ListNode,
    add_two_numbers,
    find_cycle_start,
    has_cycle_floyd,
    intersection_node,
    merge_two_lists,
    remove_nth_from_end,
    reverse_list,
)


def _to_list(head: ListNode | None) -> list[int]:
    values: list[int] = []
    while head:
        values.append(head.val)
        head = head.next
    return values


def _from_list(values: list[int]) -> ListNode | None:
    dummy = ListNode()
    tail = dummy
    for value in values:
        tail.next = ListNode(value)
        tail = tail.next
    return dummy.next


def test_reverse_list() -> None:
    assert _to_list(reverse_list(_from_list([1, 2, 3]))) == [3, 2, 1]


def test_merge_two_lists() -> None:
    merged = merge_two_lists(_from_list([1, 2, 4]), _from_list([1, 3, 4]))
    assert _to_list(merged) == [1, 1, 2, 3, 4, 4]


def test_cycle_detection() -> None:
    head = _from_list([3, 2, 0, -4])
    assert head and head.next and head.next.next
    tail = head.next.next
    tail.next = head.next
    assert has_cycle_floyd(head)
    assert find_cycle_start(head) is head.next


def test_remove_nth_from_end() -> None:
    head = remove_nth_from_end(_from_list([1, 2, 3, 4, 5]), 2)
    assert _to_list(head) == [1, 2, 3, 5]


def test_add_two_numbers() -> None:
    result = add_two_numbers(_from_list([2, 4, 3]), _from_list([5, 6, 4]))
    assert _to_list(result) == [7, 0, 8]


def test_intersection_node() -> None:
    shared = ListNode(8, ListNode(4, ListNode(5)))
    head_a = ListNode(3, ListNode(7, shared))
    head_b = ListNode(1, ListNode(9, shared))
    assert intersection_node(head_a, head_b) is shared
