"""Tests for union-find."""

from __future__ import annotations

from agentic_algorithms.dsa.union_find import UnionFind


def test_union_find() -> None:
    uf = UnionFind(5)
    assert uf.union(0, 1)
    assert uf.union(1, 2)
    assert uf.connected(0, 2)
    assert not uf.union(0, 2)
    assert uf.components == 3
