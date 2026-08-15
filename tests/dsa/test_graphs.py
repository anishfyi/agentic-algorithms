"""Tests for graph algorithms."""

from __future__ import annotations

from agentic_algorithms.dsa.graphs import (
    bfs,
    build_adjacency_list,
    build_weighted_graph,
    course_schedule,
    detect_cycle_directed,
    detect_cycle_undirected,
    dfs,
    dijkstra,
    num_islands,
    topological_sort_kahn,
    word_ladder,
)


def test_bfs_dfs() -> None:
    graph = build_adjacency_list(4, [(0, 1), (0, 2), (1, 3), (2, 3)])
    assert bfs(graph, 0) == [0, 1, 2, 3]
    assert dfs(graph, 0) == [0, 1, 3, 2]


def test_dijkstra() -> None:
    graph = build_weighted_graph(3, [(0, 1, 4), (0, 2, 2), (1, 2, 1)])
    assert dijkstra(graph, 0) == [0.0, 3.0, 2.0]


def test_topological_sort_and_cycles() -> None:
    edges = [(5, 2), (5, 0), (4, 0), (4, 1), (2, 3), (3, 1)]
    order = topological_sort_kahn(6, edges)
    assert order is not None
    assert len(order) == 6
    assert detect_cycle_directed(2, [(0, 1), (1, 0)])
    assert detect_cycle_undirected(3, [(0, 1), (1, 2), (2, 0)])


def test_num_islands() -> None:
    grid = [
        ["1", "1", "0", "0", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "1", "0", "0"],
        ["0", "0", "0", "1", "1"],
    ]
    assert num_islands([row[:] for row in grid]) == 3


def test_course_schedule() -> None:
    assert course_schedule(2, [[1, 0]])
    assert not course_schedule(2, [[1, 0], [0, 1]])


def test_word_ladder() -> None:
    assert word_ladder("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]) == 5
