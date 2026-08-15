"""Trie data structure and word search."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class TrieNode:
    """Trie node with children map and end-of-word flag."""

    children: dict[str, TrieNode] = field(default_factory=dict)
    is_end: bool = False


class Trie:
    """Prefix tree supporting insert, search, and starts_with.

    Time: O(m) per operation where m is key length. Space: O(total chars).
    """

    def __init__(self) -> None:
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """Insert word into trie."""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search(self, word: str) -> bool:
        """Return True if word exists in trie."""
        node = self._traverse(word)
        return node is not None and node.is_end

    def starts_with(self, prefix: str) -> bool:
        """Return True if any word starts with prefix."""
        return self._traverse(prefix) is not None

    def _traverse(self, key: str) -> TrieNode | None:
        node = self.root
        for char in key:
            if char not in node.children:
                return None
            node = node.children[char]
        return node


def word_search_ii(board: list[list[str]], words: list[str]) -> list[str]:
    """Find all words from list that exist in board (Word Search II).

    Time: O(m * n * 4^L) worst case with trie pruning. Space: O(total chars).
    """
    trie = Trie()
    for word in words:
        trie.insert(word)

    rows, cols = len(board), len(board[0])
    result: set[str] = set()

    def dfs(r: int, c: int, node: TrieNode, path: str) -> None:
        if node.is_end:
            result.add(path)
        if r < 0 or c < 0 or r >= rows or c >= cols:
            return
        char = board[r][c]
        if char not in node.children:
            return
        board[r][c] = "#"
        child = node.children[char]
        dfs(r + 1, c, child, path + char)
        dfs(r - 1, c, child, path + char)
        dfs(r, c + 1, child, path + char)
        dfs(r, c - 1, child, path + char)
        board[r][c] = char

    for r in range(rows):
        for c in range(cols):
            dfs(r, c, trie.root, "")
    return sorted(result)
