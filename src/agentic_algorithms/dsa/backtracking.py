"""Backtracking algorithms."""

from __future__ import annotations


def permutations(nums: list[int]) -> list[list[int]]:
    """Return all permutations of nums.

    Time: O(n * n!). Space: O(n).
    """
    result: list[list[int]] = []

    def backtrack(path: list[int], remaining: list[int]) -> None:
        if not remaining:
            result.append(path[:])
            return
        for i, value in enumerate(remaining):
            path.append(value)
            backtrack(path, remaining[:i] + remaining[i + 1 :])
            path.pop()

    backtrack([], nums)
    return result


def combinations(n: int, k: int) -> list[list[int]]:
    """Return all combinations of k numbers chosen from 1..n.

    Time: O(C(n,k) * k). Space: O(k).
    """
    result: list[list[int]] = []

    def backtrack(start: int, path: list[int]) -> None:
        if len(path) == k:
            result.append(path[:])
            return
        need = k - len(path)
        for value in range(start, n - need + 2):
            path.append(value)
            backtrack(value + 1, path)
            path.pop()

    backtrack(1, [])
    return result


def subsets(nums: list[int]) -> list[list[int]]:
    """Return all subsets of nums.

    Time: O(n * 2^n). Space: O(n).
    """
    result: list[list[int]] = []

    def backtrack(start: int, path: list[int]) -> None:
        result.append(path[:])
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()

    backtrack(0, [])
    return result


def combination_sum(candidates: list[int], target: int) -> list[list[int]]:
    """Return combinations where chosen numbers sum to target (reuse allowed).

    Time: O(2^t) worst case. Space: O(target).
    """
    candidates.sort()
    result: list[list[int]] = []

    def backtrack(start: int, remaining: int, path: list[int]) -> None:
        if remaining == 0:
            result.append(path[:])
            return
        for i in range(start, len(candidates)):
            value = candidates[i]
            if value > remaining:
                break
            path.append(value)
            backtrack(i, remaining - value, path)
            path.pop()

    backtrack(0, target, [])
    return result


def n_queens(n: int) -> list[list[str]]:
    """Return all distinct n-queens solutions as board strings.

    Time: O(n!). Space: O(n^2).
    """
    result: list[list[str]] = []
    cols: set[int] = set()
    diag1: set[int] = set()
    diag2: set[int] = set()
    board = [-1] * n

    def backtrack(row: int) -> None:
        if row == n:
            result.append(["." * col + "Q" + "." * (n - col - 1) for col in board])
            return
        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            board[row] = col
            backtrack(row + 1)
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)

    backtrack(0)
    return result


def sudoku_solver(board: list[list[str]]) -> bool:
    """Solve 9x9 Sudoku in place; return True if solvable.

    Time: O(9^m) worst case. Space: O(81).
    """
    rows: list[set[str]] = [set() for _ in range(9)]
    cols: list[set[str]] = [set() for _ in range(9)]
    boxes: list[set[str]] = [set() for _ in range(9)]
    empty: list[tuple[int, int]] = []

    for r in range(9):
        for c in range(9):
            value = board[r][c]
            if value == ".":
                empty.append((r, c))
            else:
                rows[r].add(value)
                cols[c].add(value)
                boxes[(r // 3) * 3 + c // 3].add(value)

    def backtrack(index: int) -> bool:
        if index == len(empty):
            return True
        r, c = empty[index]
        box = (r // 3) * 3 + c // 3
        for digit in map(str, range(1, 10)):
            if digit in rows[r] or digit in cols[c] or digit in boxes[box]:
                continue
            board[r][c] = digit
            rows[r].add(digit)
            cols[c].add(digit)
            boxes[box].add(digit)
            if backtrack(index + 1):
                return True
            board[r][c] = "."
            rows[r].remove(digit)
            cols[c].remove(digit)
            boxes[box].remove(digit)
        return False

    return backtrack(0)


def word_search(board: list[list[str]], word: str) -> bool:
    """Return True if word exists in grid using adjacent cells.

    Time: O(m * n * 4^L). Space: O(L).
    """
    rows, cols = len(board), len(board[0])

    def dfs(r: int, c: int, index: int) -> bool:
        if index == len(word):
            return True
        if r < 0 or c < 0 or r >= rows or c >= cols or board[r][c] != word[index]:
            return False
        temp = board[r][c]
        board[r][c] = "#"
        found = (
            dfs(r + 1, c, index + 1)
            or dfs(r - 1, c, index + 1)
            or dfs(r, c + 1, index + 1)
            or dfs(r, c - 1, index + 1)
        )
        board[r][c] = temp
        return found

    for r in range(rows):
        for c in range(cols):
            if dfs(r, c, 0):
                return True
    return False
