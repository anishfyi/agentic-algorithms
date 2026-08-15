"""Tests for trie algorithms."""

from __future__ import annotations

from agentic_algorithms.dsa.trie import Trie, word_search_ii


def test_trie_operations() -> None:
    trie = Trie()
    trie.insert("apple")
    assert trie.search("apple")
    assert not trie.search("app")
    assert trie.starts_with("app")


def test_word_search_ii() -> None:
    board = [["o", "a", "a", "n"], ["e", "t", "a", "e"], ["i", "h", "k", "r"], ["i", "f", "l", "v"]]
    words = ["oath", "pea", "eat", "rain"]
    assert word_search_ii(board, words) == ["eat", "oath"]
