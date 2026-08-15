"""Graph algorithms."""

from __future__ import annotations

from collections import deque
from heapq import heappop, heappush

from agentic_algorithms.dsa.union_find import UnionFind

Graph = dict[int, list[tuple[int, int]]]


def build_adjacency_list(
    n: int, edges: list[tuple[int, int]], directed: bool = False
) -> dict[int, list[int]]:
    """Build unweighted adjacency list from edge list.

    Time: O(n + e). Space: O(n + e).
    """
    graph: dict[int, list[int]] = {i: [] for i in range(n)}
    for u, v in edges:
        graph[u].append(v)
        if not directed:
            graph[v].append(u)
    return graph


def build_weighted_graph(
    n: int, edges: list[tuple[int, int, int]], directed: bool = False
) -> Graph:
    """Build weighted adjacency list from (u, v, weight) edges.

    Time: O(n + e). Space: O(n + e).
    """
    graph: Graph = {i: [] for i in range(n)}
    for u, v, weight in edges:
        graph[u].append((v, weight))
        if not directed:
            graph[v].append((u, weight))
    return graph


def bfs(graph: dict[int, list[int]], start: int) -> list[int]:
    """Breadth-first search traversal order from start.

    Time: O(V + E). Space: O(V).
    """
    visited: set[int] = {start}
    order: list[int] = []
    queue: deque[int] = deque([start])
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return order


def dfs(graph: dict[int, list[int]], start: int) -> list[int]:
    """Depth-first search traversal order from start (iterative).

    Time: O(V + E). Space: O(V).
    """
    visited: set[int] = set()
    order: list[int] = []
    stack = [start]
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        order.append(node)
        for neighbor in reversed(graph.get(node, [])):
            if neighbor not in visited:
                stack.append(neighbor)
    return order


def dijkstra(graph: Graph, start: int) -> list[float]:
    """Single-source shortest paths using Dijkstra's algorithm.

    Time: O((V + E) log V). Space: O(V).
    """
    n = len(graph)
    dist = [float("inf")] * n
    dist[start] = 0.0
    heap: list[tuple[float, int]] = [(0.0, start)]
    while heap:
        current_dist, node = heappop(heap)
        if current_dist > dist[node]:
            continue
        for neighbor, weight in graph.get(node, []):
            new_dist = current_dist + weight
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                heappush(heap, (new_dist, neighbor))
    return dist


def bellman_ford(n: int, edges: list[tuple[int, int, int]], start: int) -> list[float] | None:
    """Single-source shortest paths; return None if negative cycle exists.

    Time: O(V * E). Space: O(V).
    """
    dist = [float("inf")] * n
    dist[start] = 0.0
    for _ in range(n - 1):
        updated = False
        for u, v, weight in edges:
            if dist[u] != float("inf") and dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                updated = True
        if not updated:
            break
    for u, v, weight in edges:
        if dist[u] != float("inf") and dist[u] + weight < dist[v]:
            return None
    return dist


def floyd_warshall(dist: list[list[float]]) -> list[list[float]]:
    """All-pairs shortest paths in-place on distance matrix.

    Time: O(V^3). Space: O(V^2).
    """
    n = len(dist)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist


def topological_sort_kahn(n: int, edges: list[tuple[int, int]]) -> list[int] | None:
    """Topological sort using Kahn's algorithm; None if cycle exists.

    Time: O(V + E). Space: O(V + E).
    """
    indegree = [0] * n
    graph: dict[int, list[int]] = {i: [] for i in range(n)}
    for u, v in edges:
        graph[u].append(v)
        indegree[v] += 1
    queue: deque[int] = deque(i for i in range(n) if indegree[i] == 0)
    order: list[int] = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
    return order if len(order) == n else None


def topological_sort_dfs(n: int, edges: list[tuple[int, int]]) -> list[int] | None:
    """Topological sort using DFS; None if cycle exists.

    Time: O(V + E). Space: O(V + E).
    """
    graph = build_adjacency_list(n, edges, directed=True)
    visited = [0] * n
    order: list[int] = []

    def dfs(node: int) -> bool:
        if visited[node] == 1:
            return False
        if visited[node] == 2:
            return True
        visited[node] = 1
        for neighbor in graph[node]:
            if not dfs(neighbor):
                return False
        visited[node] = 2
        order.append(node)
        return True

    for i in range(n):
        if visited[i] == 0 and not dfs(i):
            return None
    order.reverse()
    return order


def detect_cycle_directed(n: int, edges: list[tuple[int, int]]) -> bool:
    """Detect cycle in directed graph.

    Time: O(V + E). Space: O(V + E).
    """
    return topological_sort_kahn(n, edges) is None


def detect_cycle_undirected(n: int, edges: list[tuple[int, int]]) -> bool:
    """Detect cycle in undirected graph.

    Time: O(V + E) amortized. Space: O(V).
    """
    uf = UnionFind(n)
    return any(not uf.union(u, v) for u, v in edges)


def num_islands(grid: list[list[str]]) -> int:
    """Count islands of '1's in a 2D grid.

    Time: O(m * n). Space: O(m * n).
    """
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])
    count = 0

    def flood(r: int, c: int) -> None:
        if r < 0 or c < 0 or r >= rows or c >= cols or grid[r][c] != "1":
            return
        grid[r][c] = "0"
        flood(r + 1, c)
        flood(r - 1, c)
        flood(r, c + 1)
        flood(r, c - 1)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                count += 1
                flood(r, c)
    return count


def course_schedule(num_courses: int, prerequisites: list[list[int]]) -> bool:
    """Return True if all courses can be finished given prerequisites.

    Time: O(V + E). Space: O(V + E).
    """
    edges = [(pre, course) for course, pre in prerequisites]
    return topological_sort_kahn(num_courses, edges) is not None


def word_ladder(begin_word: str, end_word: str, word_list: list[str]) -> int:
    """Return shortest transformation sequence length, or 0 if impossible.

    Time: O(n * m^2) where m is word length. Space: O(n * m).
    """
    word_set = set(word_list)
    if end_word not in word_set:
        return 0
    queue: deque[tuple[str, int]] = deque([(begin_word, 1)])
    visited = {begin_word}
    while queue:
        word, length = queue.popleft()
        if word == end_word:
            return length
        chars = list(word)
        for i in range(len(chars)):
            original = chars[i]
            for code in range(ord("a"), ord("z") + 1):
                chars[i] = chr(code)
                candidate = "".join(chars)
                if candidate in word_set and candidate not in visited:
                    visited.add(candidate)
                    queue.append((candidate, length + 1))
            chars[i] = original
    return 0


def prim_mst(n: int, edges: list[tuple[int, int, int]]) -> int:
    """Minimum spanning tree weight via Prim's algorithm.

    Time: O(E log V). Space: O(V + E).
    """
    import heapq

    graph: dict[int, list[tuple[int, int]]] = {i: [] for i in range(n)}
    for u, v, weight in edges:
        graph[u].append((v, weight))
        graph[v].append((u, weight))
    visited = {0}
    heap: list[tuple[int, int]] = [(weight, node) for node, weight in graph[0]]
    heapq.heapify(heap)
    total = 0
    while heap and len(visited) < n:
        weight, node = heapq.heappop(heap)
        if node in visited:
            continue
        visited.add(node)
        total += weight
        for neighbor, edge_weight in graph[node]:
            if neighbor not in visited:
                heapq.heappush(heap, (edge_weight, neighbor))
    return total if len(visited) == n else -1


def kruskal_mst(n: int, edges: list[tuple[int, int, int]]) -> int:
    """Minimum spanning tree weight via Kruskal's algorithm.

    Time: O(E log E). Space: O(V).
    """
    from agentic_algorithms.dsa.union_find import UnionFind

    sorted_edges = sorted(edges, key=lambda item: item[2])
    uf = UnionFind(n)
    total = 0
    used = 0
    for u, v, weight in sorted_edges:
        if uf.union(u, v):
            total += weight
            used += 1
            if used == n - 1:
                break
    return total if used == n - 1 else -1
