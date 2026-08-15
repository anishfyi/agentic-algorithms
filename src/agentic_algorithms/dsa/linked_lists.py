"""Linked list algorithms."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ListNode:
    """Singly linked list node."""

    val: int = 0
    next: ListNode | None = None


def reverse_list(head: ListNode | None) -> ListNode | None:
    """Reverse a singly linked list.

    Time: O(n). Space: O(1).
    """
    prev: ListNode | None = None
    current = head
    while current:
        nxt = current.next
        current.next = prev
        prev = current
        current = nxt
    return prev


def merge_two_lists(list1: ListNode | None, list2: ListNode | None) -> ListNode | None:
    """Merge two sorted linked lists.

    Time: O(n + m). Space: O(1).
    """
    dummy = ListNode()
    tail = dummy
    while list1 and list2:
        if list1.val <= list2.val:
            tail.next = list1
            list1 = list1.next
        else:
            tail.next = list2
            list2 = list2.next
        tail = tail.next
    tail.next = list1 or list2
    return dummy.next


def has_cycle_floyd(head: ListNode | None) -> bool:
    """Detect cycle using Floyd's tortoise and hare.

    Time: O(n). Space: O(1).
    """
    slow = fast = head
    while fast and fast.next:
        slow = slow.next if slow else None
        fast = fast.next.next
        if slow is fast:
            return True
    return False


def find_cycle_start(head: ListNode | None) -> ListNode | None:
    """Return node where cycle begins, or None.

    Time: O(n). Space: O(1).
    """
    slow = fast = head
    while fast and fast.next:
        slow = slow.next if slow else None
        fast = fast.next.next
        if slow is fast:
            break
    else:
        return None
    slow = head
    while slow is not fast:
        slow = slow.next if slow else None
        fast = fast.next if fast else None
    return slow


def remove_nth_from_end(head: ListNode | None, n: int) -> ListNode | None:
    """Remove the nth node from the end of the list.

    Time: O(n). Space: O(1).
    """
    dummy = ListNode(next=head)
    fast: ListNode | None = dummy
    slow: ListNode | None = dummy
    for _ in range(n):
        fast = fast.next if fast else None
    while fast and fast.next:
        slow = slow.next if slow else None
        fast = fast.next
    if slow and slow.next:
        slow.next = slow.next.next
    return dummy.next


def reorder_list(head: ListNode | None) -> None:
    """Reorder list L0 -> L1 -> ... -> Ln-1 -> Ln to L0 -> Ln -> L1 -> Ln-1 -> ...

    Time: O(n). Space: O(1).
    """
    if not head or not head.next:
        return
    slow: ListNode | None = head
    fast: ListNode | None = head.next
    while fast and fast.next:
        slow = slow.next if slow else None
        fast = fast.next.next
    second = reverse_list(slow.next if slow else None)
    if slow:
        slow.next = None
    first = head
    while second:
        temp1 = first.next
        temp2 = second.next
        first.next = second
        second.next = temp1
        first = temp1 if temp1 else first
        second = temp2


def add_two_numbers(l1: ListNode | None, l2: ListNode | None) -> ListNode | None:
    """Add two numbers represented as linked lists (digits in reverse order).

    Time: O(max(n, m)). Space: O(max(n, m)).
    """
    dummy = ListNode()
    tail = dummy
    carry = 0
    while l1 or l2 or carry:
        total = carry
        if l1:
            total += l1.val
            l1 = l1.next
        if l2:
            total += l2.val
            l2 = l2.next
        carry, digit = divmod(total, 10)
        tail.next = ListNode(digit)
        tail = tail.next
    return dummy.next


def intersection_node(head_a: ListNode | None, head_b: ListNode | None) -> ListNode | None:
    """Return node where two linked lists intersect, or None.

    Time: O(n + m). Space: O(1).
    """
    if not head_a or not head_b:
        return None
    pointer_a: ListNode | None = head_a
    pointer_b: ListNode | None = head_b
    while pointer_a is not pointer_b:
        pointer_a = pointer_a.next if pointer_a else head_b
        pointer_b = pointer_b.next if pointer_b else head_a
    return pointer_a
