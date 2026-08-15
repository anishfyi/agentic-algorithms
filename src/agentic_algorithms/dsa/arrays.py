"""Array algorithms and utilities."""

from __future__ import annotations

from collections import defaultdict
from typing import TypeVar

T = TypeVar("T")


def two_sum(nums: list[int], target: int) -> list[int]:
    """Return indices of two numbers that add up to target.

    Time: O(n). Space: O(n).
    """
    seen: dict[int, int] = {}
    for i, value in enumerate(nums):
        complement = target - value
        if complement in seen:
            return [seen[complement], i]
        seen[value] = i
    return []


def three_sum(nums: list[int]) -> list[list[int]]:
    """Return all unique triplets that sum to zero.

    Time: O(n^2). Space: O(1) excluding output.
    """
    nums.sort()
    result: list[list[int]] = []
    n = len(nums)
    for i in range(n - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        left, right = i + 1, n - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if total == 0:
                result.append([nums[i], nums[left], nums[right]])
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                left += 1
                right -= 1
            elif total < 0:
                left += 1
            else:
                right -= 1
    return result


def max_subarray_kadane(nums: list[int]) -> int:
    """Return maximum subarray sum using Kadane's algorithm.

    Time: O(n). Space: O(1).
    """
    best = current = nums[0]
    for value in nums[1:]:
        current = max(value, current + value)
        best = max(best, current)
    return best


def max_subarray_kadane_with_indices(nums: list[int]) -> tuple[int, int, int]:
    """Return max subarray sum and its start/end indices (inclusive).

    Time: O(n). Space: O(1).
    """
    best_sum = current_sum = nums[0]
    start = end = temp_start = 0
    for i in range(1, len(nums)):
        if current_sum < 0:
            current_sum = nums[i]
            temp_start = i
        else:
            current_sum += nums[i]
        if current_sum > best_sum:
            best_sum = current_sum
            start = temp_start
            end = i
    return best_sum, start, end


def max_subarray_circular(nums: list[int]) -> int:
    """Return maximum subarray sum for a circular array.

    Time: O(n). Space: O(1).
    """
    total = sum(nums)
    max_kadane = max_subarray_kadane(nums)
    min_kadane = min_subarray_kadane(nums)
    if min_kadane == total:
        return max_kadane
    return max(max_kadane, total - min_kadane)


def min_subarray_kadane(nums: list[int]) -> int:
    """Return minimum subarray sum using Kadane's algorithm.

    Time: O(n). Space: O(1).
    """
    best = current = nums[0]
    for value in nums[1:]:
        current = min(value, current + value)
        best = min(best, current)
    return best


def product_except_self(nums: list[int]) -> list[int]:
    """Return array where output[i] is product of all elements except nums[i].

    Time: O(n). Space: O(1) excluding output.
    """
    n = len(nums)
    result = [1] * n
    prefix = 1
    for i in range(n):
        result[i] = prefix
        prefix *= nums[i]
    suffix = 1
    for i in range(n - 1, -1, -1):
        result[i] *= suffix
        suffix *= nums[i]
    return result


def rotate_array(nums: list[int], k: int) -> None:
    """Rotate array to the right by k steps in place.

    Time: O(n). Space: O(1).
    """
    n = len(nums)
    if n == 0:
        return
    k %= n

    def reverse(left: int, right: int) -> None:
        while left < right:
            nums[left], nums[right] = nums[right], nums[left]
            left += 1
            right -= 1

    reverse(0, n - 1)
    reverse(0, k - 1)
    reverse(k, n - 1)


def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    """Merge overlapping intervals.

    Time: O(n log n). Space: O(n).
    """
    if not intervals:
        return []
    intervals.sort(key=lambda item: item[0])
    merged: list[list[int]] = [intervals[0][:]]
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged


def insert_interval(intervals: list[list[int]], new_interval: list[int]) -> list[list[int]]:
    """Insert new interval and merge if necessary.

    Time: O(n). Space: O(n).
    """
    result: list[list[int]] = []
    start, end = new_interval
    i = 0
    n = len(intervals)
    while i < n and intervals[i][1] < start:
        result.append(intervals[i])
        i += 1
    while i < n and intervals[i][0] <= end:
        start = min(start, intervals[i][0])
        end = max(end, intervals[i][1])
        i += 1
    result.append([start, end])
    while i < n:
        result.append(intervals[i])
        i += 1
    return result


def find_duplicate_floyd(nums: list[int]) -> int:
    """Find duplicate in array of n+1 integers in range [1, n] using Floyd's cycle.

    Time: O(n). Space: O(1).
    """
    slow = fast = nums[0]
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break
    slow = nums[0]
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]
    return slow


def trapping_rain_water(height: list[int]) -> int:
    """Compute trapped rainwater between bars.

    Time: O(n). Space: O(1).
    """
    left, right = 0, len(height) - 1
    left_max = right_max = water = 0
    while left < right:
        if height[left] < height[right]:
            left_max = max(left_max, height[left])
            water += left_max - height[left]
            left += 1
        else:
            right_max = max(right_max, height[right])
            water += right_max - height[right]
            right -= 1
    return water


def container_with_most_water(height: list[int]) -> int:
    """Return maximum water a container can store.

    Time: O(n). Space: O(1).
    """
    left, right = 0, len(height) - 1
    best = 0
    while left < right:
        width = right - left
        best = max(best, width * min(height[left], height[right]))
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    return best


def longest_consecutive(nums: list[int]) -> int:
    """Return length of longest consecutive elements sequence.

    Time: O(n). Space: O(n).
    """
    num_set = set(nums)
    best = 0
    for num in num_set:
        if num - 1 not in num_set:
            current = num
            length = 1
            while current + 1 in num_set:
                current += 1
                length += 1
            best = max(best, length)
    return best


def subarray_sum_equals_k(nums: list[int], k: int) -> int:
    """Count subarrays with sum equal to k.

    Time: O(n). Space: O(n).
    """
    counts: dict[int, int] = defaultdict(int)
    counts[0] = 1
    prefix = total = 0
    for value in nums:
        prefix += value
        total += counts[prefix - k]
        counts[prefix] += 1
    return total


def dutch_flag_sort(nums: list[int]) -> None:
    """Sort array of 0s, 1s, and 2s in place.

    Time: O(n). Space: O(1).
    """
    low, mid, high = 0, 0, len(nums) - 1
    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1


def next_permutation(nums: list[int]) -> None:
    """Rearrange nums into the lexicographically next greater permutation in place.

    Time: O(n). Space: O(1).
    """
    i = len(nums) - 2
    while i >= 0 and nums[i] >= nums[i + 1]:
        i -= 1
    if i >= 0:
        j = len(nums) - 1
        while nums[j] <= nums[i]:
            j -= 1
        nums[i], nums[j] = nums[j], nums[i]
    left, right = i + 1, len(nums) - 1
    while left < right:
        nums[left], nums[right] = nums[right], nums[left]
        left += 1
        right -= 1


def majority_element_boyer_moore(nums: list[int]) -> int:
    """Return element appearing more than n/2 times using Boyer-Moore voting.

    Time: O(n). Space: O(1).
    """
    candidate = count = 0
    for value in nums:
        if count == 0:
            candidate = value
        count += 1 if value == candidate else -1
    return candidate


def prefix_sum(nums: list[int]) -> list[int]:
    """Build prefix sum array where result[i] is sum of nums[0..i].

    Time: O(n). Space: O(n).
    """
    if not nums:
        return []
    result = [nums[0]]
    for i in range(1, len(nums)):
        result.append(result[-1] + nums[i])
    return result


def range_sum(prefix: list[int], left: int, right: int) -> int:
    """Return sum of original array from left to right inclusive using prefix sums.

    Time: O(1). Space: O(1).
    """
    if left == 0:
        return prefix[right]
    return prefix[right] - prefix[left - 1]
