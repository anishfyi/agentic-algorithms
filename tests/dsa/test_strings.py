"""Tests for string algorithms."""

from __future__ import annotations

from agentic_algorithms.dsa import strings as str_alg


def test_is_palindrome() -> None:
    assert str_alg.is_palindrome("A man, a plan, a canal: Panama")


def test_longest_palindrome_expand() -> None:
    assert str_alg.longest_palindrome_expand("babad") in {"bab", "aba"}


def test_kmp_and_rabin_karp() -> None:
    assert str_alg.kmp_search("ababcababa", "aba") == [0, 5, 7]
    assert str_alg.rabin_karp("ababcababa", "aba") == [0, 5, 7]


def test_longest_common_prefix() -> None:
    assert str_alg.longest_common_prefix(["flower", "flow", "flight"]) == "fl"


def test_valid_parentheses() -> None:
    assert str_alg.valid_parentheses("()[]{}")
    assert not str_alg.valid_parentheses("(]")


def test_min_window_substring() -> None:
    assert str_alg.min_window_substring("ADOBECODEBANC", "ABC") == "BANC"


def test_group_anagrams() -> None:
    groups = str_alg.group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
    assert sorted(len(group) for group in groups) == [1, 2, 3]


def test_isomorphic_strings() -> None:
    assert str_alg.isomorphic_strings("egg", "add")
    assert not str_alg.isomorphic_strings("foo", "bar")


def test_edit_distance_and_lcs() -> None:
    assert str_alg.edit_distance_levenshtein("horse", "ros") == 3
    assert str_alg.longest_common_subsequence("abcde", "ace") == 3


def test_regex_wildcard_dp() -> None:
    assert str_alg.regex_wildcard_dp("aa", "a") is False
    assert str_alg.regex_wildcard_dp("aa", "*") is True
