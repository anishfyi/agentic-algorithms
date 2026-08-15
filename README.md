# agentic-algorithms

Algorithms, patterns, and reference implementations for building agentic systems **and**
classic data structures and algorithms with optimal complexity.

Python 3.12+. **Primary focus: give LLMs every helper they need**, plus psychology engineering for trustworthy agent UX. Also includes agent runtime, DSA, and domain verticals.

1. **LLM helpers** (`agentic_algorithms.llm_helpers`) — prompts, context budgeting, JSON parsing, RAG packing, routing, reflexion/self-consistency (`catalogs/llm_algorithms.json`)
2. **Psychology engineering** (`agentic_algorithms.psychology`) — biases, framing, persuasion ethics, trust, nudges, cognitive load (`catalogs/psychology_algorithms.json`)
3. **Agent runtime** (`Agent`, ReAct, plan-execute, multi-agent, memory, eval, approval hooks)
4. **DSA catalog** (`agentic_algorithms.dsa`) — 134+ optimal algorithms (`catalogs/algorithms.json`)
5. **Domain algorithms** (`agentic_algorithms.domains`) — supply chain, fintech, accounting, expense, commerce, search, GEO, AEO (`catalogs/domain_algorithms.json`)

Complements [first-principles](https://github.com/anishfyi/first-principles): theory and citations there, runnable code here.

## Algorithm Atlas

An interactive web UI for browsing all 198 algorithms: search, track and category filters, complexity at a glance, and hash deep links to every entry. Built from the machine-readable catalogs and deployed to GitHub Pages via `.github/workflows/pages.yml`.

```bash
python scripts/build_algorithm_catalog.py  # merges catalogs/*.json into web/data/algorithms.json
python -m http.server -d web 8000          # open http://localhost:8000
```

The build script is dependency-free (stdlib only) and fails if the merged total drifts from 198.

## Install

```bash
pip install agentic-algorithms
pip install "agentic-algorithms[all]"  # Anthropic + OpenAI providers
```

## LLM helpers quick start

```python
from agentic_algorithms.llm_helpers import (
    few_shot_prompt,
    chain_of_thought_wrap,
    prune_messages_by_token_budget,
    pack_rag_context,
    parse_structured_output,
    route_model_by_complexity,
)

prompt = chain_of_thought_wrap("Reconcile these two ledger balances")
model = route_model_by_complexity(prompt)  # simple vs complex routing
```

## Psychology engineering quick start

```python
from agentic_algorithms.psychology import (
    detect_overconfidence_markers,
    bias_mitigation_prompt,
    ethical_persuasion_check,
    agent_trust_score,
    neutral_frame,
)

copy = neutral_frame("approve this journal entry", "debits equal credits")
assert not ethical_persuasion_check(copy, domain="fintech")
system = bias_mitigation_prompt(detect_overconfidence_markers(agent_reply))
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

## Domain algorithms (supply chain, fintech, accounting, expense, commerce, search, GEO, AEO)

```python
from agentic_algorithms.domains import (
    validate_journal_entry,
    newsvendor_quantity,
    atp_available,
    categorize_expense,
    payment_risk_score,
    recall_at_k,
    thompson_sampling_select,
    SearchIndex,
    haversine_km,
    jurisdiction_rate_lookup,
    aeo_page_score,
)
```

| Domain | Algorithms |
|--------|------------|
| **accounting** | double-entry validation, posting, bank reconciliation, Benford anomaly |
| **expense** | categorization, duplicate detection, mileage, policy scoring |
| **fintech** | velocity limits, AML structuring, payment risk, amortization, Luhn |
| **supply_chain** | newsvendor, safety stock, EOQ, ATP, allocation, MRP, vehicle routing |
| **ecommerce** | recall/NDCG, item-item CF, Wide&Deep logit, DIN attention, bandits |
| **search** | BM25 index, TF-IDF, hybrid RRF fusion, faceted filter |
| **geo** | haversine, geohash, point-in-polygon, jurisdiction lookup, nearest facility |
| **aeo** | schema completeness, FAQ structure, citation density, snippet answerability, EEAT |

Domain index: [`catalogs/domain_algorithms.json`](catalogs/domain_algorithms.json) (34 entries).

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
python examples/llm_psychology_agent.py
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
