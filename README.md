# agentic-algorithms

Algorithms, patterns, and reference implementations for building agentic systems **and**
classic data structures and algorithms with optimal complexity.

Python 3.12+. Two libraries in one package:

1. **Agent runtime** (`Agent`, ReAct, plan-execute, multi-agent, memory, eval, approval hooks)
2. **DSA catalog** (`agentic_algorithms.dsa`) with **134+ optimal algorithms** indexed in `catalogs/algorithms.json`

Complements [first-principles](https://github.com/anishfyi/first-principles): theory and citations there, runnable code here.

## Install

```bash
pip install agentic-algorithms
pip install "agentic-algorithms[all]"  # Anthropic + OpenAI providers
```

## Agent quick start

```python
from agentic_algorithms import Agent, AgentConfig, MockProvider, tool

@tool(description="Fetch account balance in minor units")
def get_balance(account_id: str) -> str:
    return "250000"

agent = Agent(provider=MockProvider(), config=AgentConfig())
agent.add_tool(get_balance)
print(agent.run("What is the cash balance?").output)
```

## DSA quick start

```python
from agentic_algorithms.dsa import two_sum, dijkstra, kmp_search, UnionFind, SegmentTree

print(two_sum([2, 7, 11, 15], 9))           # [0, 1]
print(kmp_search("ababcabc", "abc"))        # [2, 5]
```

## DSA categories (optimal implementations)

| Category | Examples |
|----------|----------|
| **arrays** | two_sum, Kadane, Dutch flag, rain water, intervals |
| **strings** | KMP, Rabin-Karp, LCS, edit distance, min window |
| **linked lists** | reverse, cycle detection, merge, reorder |
| **trees** | traversals, BST, LCA, serialize, diameter |
| **graphs** | BFS/DFS, Dijkstra, Bellman-Ford, Floyd-Warshall, MST, topo sort |
| **sorting** | merge, quick, heap, counting, radix, binary search variants |
| **heap** | MinHeap, kth largest, merge k lists, median stream |
| **dp** | coin change, knapsack, LIS, matrix chain |
| **greedy** | activity selection, jump game, task scheduler |
| **backtracking** | permutations, n-queens, sudoku, word search |
| **math** | gcd, sieve, Miller-Rabin, fast Fibonacci |
| **bits** | popcount table, XOR tricks, bitmask subsets |
| **trie** | prefix tree, word search II |
| **union find** | path compression + union by rank |
| **segments** | segment tree range sum/min |
| **stacks_queues** | monotonic stack, sliding window max, RPN |

Full index: [`catalogs/algorithms.json`](catalogs/algorithms.json) (machine-readable, 134 entries).

## Agent patterns

| Module | Pattern |
|--------|---------|
| `loops.react` | ReAct tool loop |
| `loops.plan_execute` | Plan then execute |
| `multi` | Fan-out, judge, orchestrator |
| `memory` | Short and long-term memory |
| `human` | Approval hooks before tool calls |
| `eval` | Task suites + optional LLM judge |

## Examples

```bash
python examples/fintech_workflow.py
```

## Development

```bash
pip install -e ".[dev]"
ruff check src tests examples
mypy
pytest --cov=agentic_algorithms
```

## Release

Tag `v*` to publish to PyPI via GitHub Actions.

## License

MIT. See [LICENSE](LICENSE).
