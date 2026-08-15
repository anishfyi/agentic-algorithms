"""Tests for MST graph algorithms."""

from agentic_algorithms.dsa.graphs import kruskal_mst, prim_mst


def test_prim_mst() -> None:
    edges = [(0, 1, 1), (1, 2, 2), (0, 2, 3)]
    assert prim_mst(3, edges) == 3


def test_kruskal_mst() -> None:
    edges = [(0, 1, 1), (1, 2, 2), (0, 2, 3)]
    assert kruskal_mst(3, edges) == 3
