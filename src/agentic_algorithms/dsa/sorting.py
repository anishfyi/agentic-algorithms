"""Sorting and binary search algorithms."""

from __future__ import annotations


def merge_sort(nums: list[int]) -> list[int]:
    """Sort array using merge sort.

    Time: O(n log n). Space: O(n).
    """
    if len(nums) <= 1:
        return nums[:]
    mid = len(nums) // 2
    left = merge_sort(nums[:mid])
    right = merge_sort(nums[mid:])
    return _merge(left, right)


def _merge(left: list[int], right: list[int]) -> list[int]:
    result: list[int] = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def quick_sort(nums: list[int]) -> list[int]:
    """Sort array using quick sort.

    Time: O(n log n) average, O(n^2) worst. Space: O(log n).
    """
    if len(nums) <= 1:
        return nums[:]
    pivot = nums[len(nums) // 2]
    left = [x for x in nums if x < pivot]
    middle = [x for x in nums if x == pivot]
    right = [x for x in nums if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)


def heap_sort(nums: list[int]) -> list[int]:
    """Sort array using heap sort.

    Time: O(n log n). Space: O(1) excluding output copy.
    """
    arr = nums[:]
    n = len(arr)

    def heapify(size: int, root: int) -> None:
        largest = root
        left = 2 * root + 1
        right = 2 * root + 2
        if left < size and arr[left] > arr[largest]:
            largest = left
        if right < size and arr[right] > arr[largest]:
            largest = right
        if largest != root:
            arr[root], arr[largest] = arr[largest], arr[root]
            heapify(size, largest)

    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i)
    for end in range(n - 1, 0, -1):
        arr[0], arr[end] = arr[end], arr[0]
        heapify(end, 0)
    return arr


def counting_sort(nums: list[int], max_value: int | None = None) -> list[int]:
    """Sort non-negative integers using counting sort.

    Time: O(n + k). Space: O(n + k).
    """
    if not nums:
        return []
    upper = max_value if max_value is not None else max(nums)
    counts = [0] * (upper + 1)
    for value in nums:
        counts[value] += 1
    result: list[int] = []
    for value, count in enumerate(counts):
        result.extend([value] * count)
    return result


def radix_sort(nums: list[int]) -> list[int]:
    """Sort non-negative integers using LSD radix sort (base 10).

    Time: O(d * n). Space: O(n + k).
    """
    if not nums:
        return []
    max_val = max(nums)
    exp = 1
    arr = nums[:]
    while max_val // exp > 0:
        buckets: list[list[int]] = [[] for _ in range(10)]
        for value in arr:
            digit = (value // exp) % 10
            buckets[digit].append(value)
        arr = [value for bucket in buckets for value in bucket]
        exp *= 10
    return arr


def binary_search(nums: list[int], target: int) -> int:
    """Return index of target or -1 if not found.

    Time: O(log n). Space: O(1).
    """
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1


def lower_bound(nums: list[int], target: int) -> int:
    """Return first index where nums[i] >= target.

    Time: O(log n). Space: O(1).
    """
    left, right = 0, len(nums)
    while left < right:
        mid = (left + right) // 2
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid
    return left


def upper_bound(nums: list[int], target: int) -> int:
    """Return first index where nums[i] > target.

    Time: O(log n). Space: O(1).
    """
    left, right = 0, len(nums)
    while left < right:
        mid = (left + right) // 2
        if nums[mid] <= target:
            left = mid + 1
        else:
            right = mid
    return left


def first_position(nums: list[int], target: int) -> int:
    """Return first index of target in sorted array, or -1.

    Time: O(log n). Space: O(1).
    """
    index = lower_bound(nums, target)
    return index if index < len(nums) and nums[index] == target else -1


def last_position(nums: list[int], target: int) -> int:
    """Return last index of target in sorted array, or -1.

    Time: O(log n). Space: O(1).
    """
    index = upper_bound(nums, target) - 1
    return index if index >= 0 and nums[index] == target else -1


def search_rotated_array(nums: list[int], target: int) -> int:
    """Search target in rotated sorted array with distinct elements.

    Time: O(log n). Space: O(1).
    """
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        if nums[left] <= nums[mid]:
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
    return -1
