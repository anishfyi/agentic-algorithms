"""String algorithms."""

from __future__ import annotations

from collections import Counter, defaultdict


def is_palindrome(s: str) -> bool:
    """Check if string is a palindrome (alphanumeric only, case insensitive).

    Time: O(n). Space: O(1).
    """
    left, right = 0, len(s) - 1
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True


def longest_palindrome_expand(s: str) -> str:
    """Return longest palindromic substring using center expansion.

    Time: O(n^2). Space: O(1).
    """
    if not s:
        return ""

    def expand(left: int, right: int) -> tuple[int, int]:
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return left + 1, right - 1

    best_start, best_end = 0, 0
    for center in range(len(s)):
        for left, right in (expand(center, center), expand(center, center + 1)):
            if right - left > best_end - best_start:
                best_start, best_end = left, right
    return s[best_start : best_end + 1]


def kmp_search(text: str, pattern: str) -> list[int]:
    """Return all start indices where pattern occurs in text using KMP.

    Time: O(n + m). Space: O(m).
    """
    if not pattern:
        return []

    def build_lps(p: str) -> list[int]:
        lps = [0] * len(p)
        length = 0
        i = 1
        while i < len(p):
            if p[i] == p[length]:
                length += 1
                lps[i] = length
                i += 1
            elif length:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
        return lps

    lps = build_lps(pattern)
    matches: list[int] = []
    i = j = 0
    while i < len(text):
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == len(pattern):
                matches.append(i - j)
                j = lps[j - 1]
        elif j:
            j = lps[j - 1]
        else:
            i += 1
    return matches


def rabin_karp(text: str, pattern: str, base: int = 256, mod: int = 1_000_000_007) -> list[int]:
    """Return match indices using Rabin-Karp rolling hash.

    Time: O(n + m) average. Space: O(1).
    """
    n, m = len(text), len(pattern)
    if m == 0 or m > n:
        return []

    pattern_hash = text_hash = 0
    highest = pow(base, m - 1, mod)
    matches: list[int] = []

    for i in range(m):
        pattern_hash = (pattern_hash * base + ord(pattern[i])) % mod
        text_hash = (text_hash * base + ord(text[i])) % mod

    for i in range(n - m + 1):
        if pattern_hash == text_hash and text[i : i + m] == pattern:
            matches.append(i)
        if i < n - m:
            text_hash = (text_hash - ord(text[i]) * highest) % mod
            text_hash = (text_hash * base + ord(text[i + m])) % mod
            text_hash = (text_hash + mod) % mod
    return matches


def longest_common_prefix(strs: list[str]) -> str:
    """Return longest common prefix among strings.

    Time: O(S) where S is sum of lengths. Space: O(1).
    """
    if not strs:
        return ""
    for i in range(len(strs[0])):
        char = strs[0][i]
        for s in strs[1:]:
            if i >= len(s) or s[i] != char:
                return strs[0][:i]
    return strs[0]


def valid_parentheses(s: str) -> bool:
    """Check if parentheses string is valid.

    Time: O(n). Space: O(n).
    """
    pairs = {")": "(", "]": "[", "}": "{"}
    stack: list[str] = []
    for char in s:
        if char in pairs:
            if not stack or stack.pop() != pairs[char]:
                return False
        else:
            stack.append(char)
    return not stack


def min_window_substring(s: str, t: str) -> str:
    """Return smallest substring of s containing all characters of t.

    Time: O(n). Space: O(k) where k is charset size.
    """
    if not t or not s:
        return ""
    need = Counter(t)
    missing = len(t)
    left = start = 0
    length = len(s) + 1

    for right, char in enumerate(s):
        if need[char] > 0:
            missing -= 1
        need[char] -= 1
        while missing == 0:
            if right - left + 1 < length:
                start = left
                length = right - left + 1
            need[s[left]] += 1
            if need[s[left]] > 0:
                missing += 1
            left += 1
    return "" if length == len(s) + 1 else s[start : start + length]


def group_anagrams(strs: list[str]) -> list[list[str]]:
    """Group strings that are anagrams of each other.

    Time: O(n * k log k) where k is max string length. Space: O(n * k).
    """
    groups: dict[tuple[str, ...], list[str]] = defaultdict(list)
    for s in strs:
        key = tuple(sorted(s))
        groups[key].append(s)
    return list(groups.values())


def isomorphic_strings(s: str, t: str) -> bool:
    """Check if s and t are isomorphic (character mapping preserves order).

    Time: O(n). Space: O(k).
    """
    if len(s) != len(t):
        return False
    s_to_t: dict[str, str] = {}
    t_to_s: dict[str, str] = {}
    for a, b in zip(s, t, strict=True):
        if a in s_to_t:
            if s_to_t[a] != b:
                return False
        else:
            s_to_t[a] = b
        if b in t_to_s:
            if t_to_s[b] != a:
                return False
        else:
            t_to_s[b] = a
    return True


def edit_distance_levenshtein(word1: str, word2: str) -> int:
    """Compute minimum edit distance (insert, delete, replace) between words.

    Time: O(m * n). Space: O(min(m, n)).
    """
    if len(word1) < len(word2):
        word1, word2 = word2, word1
    previous = list(range(len(word2) + 1))
    for i, c1 in enumerate(word1, start=1):
        current = [i]
        for j, c2 in enumerate(word2, start=1):
            insert_cost = current[j - 1] + 1
            delete_cost = previous[j] + 1
            replace_cost = previous[j - 1] + (c1 != c2)
            current.append(min(insert_cost, delete_cost, replace_cost))
        previous = current
    return previous[-1]


def longest_common_subsequence(text1: str, text2: str) -> int:
    """Return length of longest common subsequence.

    Time: O(m * n). Space: O(min(m, n)).
    """
    if len(text1) < len(text2):
        text1, text2 = text2, text1
    previous = [0] * (len(text2) + 1)
    for c1 in text1:
        current = [0]
        for j, c2 in enumerate(text2, start=1):
            if c1 == c2:
                current.append(previous[j - 1] + 1)
            else:
                current.append(max(previous[j], current[-1]))
        previous = current
    return previous[-1]


def regex_wildcard_dp(s: str, p: str) -> bool:
    """Match string s against pattern p where '?' matches any char and '*' matches any sequence.

    Time: O(m * n). Space: O(n).
    """
    m, n = len(s), len(p)
    dp = [False] * (n + 1)
    dp[0] = True
    for j in range(1, n + 1):
        if p[j - 1] == "*":
            dp[j] = dp[j - 1]

    for i in range(1, m + 1):
        prev = dp[0]
        dp[0] = False
        for j in range(1, n + 1):
            temp = dp[j]
            if p[j - 1] == "*":
                dp[j] = dp[j] or dp[j - 1]
            elif p[j - 1] == "?" or s[i - 1] == p[j - 1]:
                dp[j] = prev
            else:
                dp[j] = False
            prev = temp
    return dp[n]
