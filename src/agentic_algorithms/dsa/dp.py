"""Dynamic programming algorithms."""

from __future__ import annotations

from bisect import bisect_left


def coin_change(coins: list[int], amount: int) -> int:
    """Return minimum coins needed to make amount, or -1 if impossible.

    Time: O(amount * n). Space: O(amount).
    """
    dp = [amount + 1] * (amount + 1)
    dp[0] = 0
    for value in range(1, amount + 1):
        for coin in coins:
            if coin <= value:
                dp[value] = min(dp[value], dp[value - coin] + 1)
    return dp[amount] if dp[amount] <= amount else -1


def coin_change_ways(coins: list[int], amount: int) -> int:
    """Return number of ways to make amount using unlimited coins.

    Time: O(amount * n). Space: O(amount).
    """
    dp = [0] * (amount + 1)
    dp[0] = 1
    for coin in coins:
        for value in range(coin, amount + 1):
            dp[value] += dp[value - coin]
    return dp[amount]


def climb_stairs(n: int) -> int:
    """Return number of distinct ways to climb n stairs (1 or 2 steps).

    Time: O(n). Space: O(1).
    """
    if n <= 2:
        return n
    prev, curr = 1, 2
    for _ in range(3, n + 1):
        prev, curr = curr, prev + curr
    return curr


def house_robber(nums: list[int]) -> int:
    """Maximize robbery amount without robbing adjacent houses.

    Time: O(n). Space: O(1).
    """
    prev = curr = 0
    for value in nums:
        prev, curr = curr, max(curr, prev + value)
    return curr


def house_robber_circular(nums: list[int]) -> int:
    """House robber on circular street (first and last adjacent).

    Time: O(n). Space: O(1).
    """
    if len(nums) == 1:
        return nums[0]

    def rob_linear(houses: list[int]) -> int:
        return house_robber(houses)

    return max(rob_linear(nums[:-1]), rob_linear(nums[1:]))


def longest_increasing_subsequence_nlogn(nums: list[int]) -> int:
    """Return length of longest strictly increasing subsequence.

    Time: O(n log n). Space: O(n).
    """
    tails: list[int] = []
    for value in nums:
        index = bisect_left(tails, value)
        if index == len(tails):
            tails.append(value)
        else:
            tails[index] = value
    return len(tails)


def matrix_chain(dimensions: list[int]) -> int:
    """Return minimum scalar multiplications for matrix chain.

    dimensions has length n+1 for n matrices.

    Time: O(n^3). Space: O(n^2).
    """
    n = len(dimensions) - 1
    if n <= 1:
        return 0
    dp = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = min(
                dp[i][k] + dp[k + 1][j] + dimensions[i] * dimensions[k + 1] * dimensions[j + 1]
                for k in range(i, j)
            )
    return dp[0][n - 1]


def knapsack_01(weights: list[int], values: list[int], capacity: int) -> int:
    """0/1 knapsack maximum value.

    Time: O(n * W). Space: O(W).
    """
    dp = [0] * (capacity + 1)
    for weight, value in zip(weights, values, strict=True):
        for w in range(capacity, weight - 1, -1):
            dp[w] = max(dp[w], dp[w - weight] + value)
    return dp[capacity]


def unbounded_knapsack(weights: list[int], values: list[int], capacity: int) -> int:
    """Unbounded knapsack maximum value.

    Time: O(n * W). Space: O(W).
    """
    dp = [0] * (capacity + 1)
    for weight, value in zip(weights, values, strict=True):
        for w in range(weight, capacity + 1):
            dp[w] = max(dp[w], dp[w - weight] + value)
    return dp[capacity]


def palindrome_partitioning_min_cuts(s: str) -> int:
    """Return minimum cuts to partition s into palindromes.

    Time: O(n^2). Space: O(n^2).
    """
    n = len(s)
    is_palindrome = [[False] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            if s[i] == s[j] and (j - i < 2 or is_palindrome[i + 1][j - 1]):
                is_palindrome[i][j] = True
    cuts = [0] * n
    for j in range(n):
        if is_palindrome[0][j]:
            cuts[j] = 0
        else:
            cuts[j] = j
            for i in range(1, j + 1):
                if is_palindrome[i][j]:
                    cuts[j] = min(cuts[j], cuts[i - 1] + 1)
    return cuts[n - 1]


def max_square(matrix: list[list[str]]) -> int:
    """Return area of largest square of '1's in binary matrix.

    Time: O(m * n). Space: O(n).
    """
    if not matrix:
        return 0
    rows, cols = len(matrix), len(matrix[0])
    previous = [0] * (cols + 1)
    best = 0
    for r in range(rows):
        current = [0] * (cols + 1)
        for c in range(cols):
            if matrix[r][c] == "1":
                current[c + 1] = 1 + min(previous[c], previous[c + 1], current[c])
                best = max(best, current[c + 1])
        previous = current
    return best * best
