#!/usr/bin/env python3
"""Merge catalogs/*.json into a single web/data/algorithms.json for the Algorithm Atlas.

Usage:
    python scripts/build_algorithm_catalog.py

The output feeds web/app.js. Each entry keeps its catalog fields (name,
category, time, space, module, function) and gains:
    id          - unique slug used for hash deep links
    track       - one of: dsa, domain, llm, psychology
    description - first line of the function docstring
    source      - full Python source of the implementation
    viz         - visualizer key for the web UI
"""

from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src" / "agentic_algorithms"
CATALOGS = ROOT / "catalogs"
OUTPUT = ROOT / "web" / "data" / "algorithms.json"

TRACKS = {
    "algorithms.json": "dsa",
    "domain_algorithms.json": "domain",
    "llm_algorithms.json": "llm",
    "psychology_algorithms.json": "psychology",
    "shopify_commerce.json": "shopify_commerce",
}

EXPECTED_TOTAL = 331

REQUIRED_FIELDS = ("name", "category", "time", "space", "module", "function")

VIZ_BY_CATEGORY: dict[str, str] = {
    "arrays": "array",
    "sorting": "bars",
    "graphs": "graph",
    "trees": "tree",
    "strings": "string",
    "dp": "grid",
    "heap": "heap",
    "stacks_queues": "stack",
    "trie": "trie",
    "union_find": "sets",
    "segments": "intervals",
    "linked_lists": "linked",
    "bits": "bits",
    "greedy": "flow",
    "backtracking": "tree",
    "math": "curve",
    "accounting": "pipeline",
    "fintech": "pipeline",
    "expense": "pipeline",
    "ecommerce": "pipeline",
    "supply_chain": "pipeline",
    "search": "index",
    "geo": "map",
    "aeo": "map",
    "prompts": "blocks",
    "context": "blocks",
    "parsing": "blocks",
    "rag": "blocks",
    "routing": "blocks",
    "tokens": "blocks",
    "loops": "blocks",
    "biases": "signal",
    "framing": "signal",
    "persuasion": "signal",
    "trust": "signal",
    "nudges": "signal",
    "cognitive_load": "signal",
    "motivation": "signal",
    "sales": "signal",
    "marketing": "signal",
    "twitter_x": "signal",
    "social_growth": "signal",
    "conversion": "signal",
    "copywriting": "signal",
    "learning_acceleration": "signal",
    "spaced_learning": "signal",
    "pricing_psychology": "signal",
    "onboarding": "signal",
    "retention": "signal",
    "virality": "signal",
    "objection_handling": "signal",
    "dm_outreach": "signal",
    "ads_psychology": "signal",
    "b2b_selling": "signal",
    "saas_growth": "signal",
    "hook_writing": "signal",
    "thread_structure": "signal",
    "engagement_scoring": "signal",
    "audience_building": "signal",
    "influencer_fit": "signal",
    "brand_voice": "signal",
    "crisis_comms": "signal",
    "community": "signal",
    "newsletter": "signal",
    "landing_pages": "signal",
    "ecommerce_merch": "signal",
    "shopify_webhooks": "pipeline",
    "shopify_cart": "pipeline",
    "shopify_inventory": "pipeline",
    "shopify_payments": "pipeline",
    "shopify_data": "blocks",
    "shopify_api": "curve",
    "shopify_storefront": "pipeline",
    "shopify_orders": "signal",
}

_source_cache: dict[Path, tuple[str, ast.Module]] = {}


def slugify(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return slug or "algorithm"


def module_path(track: str, module: str) -> Path:
    if track == "dsa":
        return SRC / "dsa" / f"{module}.py"
    return SRC / Path(module.replace(".", "/")).with_suffix(".py")


def load_module(path: Path) -> tuple[str, ast.Module]:
    if path not in _source_cache:
        text = path.read_text(encoding="utf-8")
        _source_cache[path] = (text, ast.parse(text))
    return _source_cache[path]


def extract_function(path: Path, function: str) -> tuple[str, str, str]:
    text, tree = load_module(path)
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and node.name == function:
            source = ast.get_source_segment(text, node) or ""
            doc = ast.get_docstring(node) or ""
            description = doc.split("\n")[0].strip() if doc else ""
            signature = ""
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                signature = _function_signature(node)
            return description, source, signature
    return "", "", ""


def _function_signature(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    args: list[str] = []
    defaults_offset = len(node.args.args) - len(node.args.defaults)
    for index, arg in enumerate(node.args.args):
        if arg.arg in {"self", "cls"}:
            continue
        part = arg.arg
        if arg.annotation is not None:
            part += f": {ast.unparse(arg.annotation)}"
        default_index = index - defaults_offset
        if default_index >= 0:
            part += f" = {ast.unparse(node.args.defaults[default_index])}"
        args.append(part)
    if node.args.vararg:
        args.append(f"*{node.args.vararg.arg}")
    if node.args.kwarg:
        args.append(f"**{node.args.kwarg.arg}")
    ret = ast.unparse(node.returns) if node.returns else "None"
    return f"def {node.name}({', '.join(args)}) -> {ret}"


def main() -> int:
    algorithms: list[dict] = []
    seen_ids: set[str] = set()
    missing_source: list[str] = []

    for filename, track in TRACKS.items():
        path = CATALOGS / filename
        entries = json.loads(path.read_text(encoding="utf-8"))
        for entry in entries:
            missing = [f for f in REQUIRED_FIELDS if f not in entry]
            if missing:
                raise ValueError(f"{filename}: {entry.get('name')!r} missing {missing}")
            slug = slugify(entry["name"])
            if slug in seen_ids:
                raise ValueError(f"duplicate algorithm id: {slug}")
            seen_ids.add(slug)

            src_path = module_path(track, entry["module"])
            description, source, signature = extract_function(src_path, entry["function"])
            if not source:
                missing_source.append(entry["name"])

            algorithms.append(
                {
                    "id": slug,
                    "track": track,
                    "viz": VIZ_BY_CATEGORY.get(entry["category"], "curve"),
                    "description": description,
                    "source": source,
                    "signature": signature,
                    "use_case": entry.get("use_case", ""),
                    "returns": entry.get("returns", ""),
                    "example": entry.get("example", ""),
                    **entry,
                }
            )

    algorithms.sort(key=lambda a: (a["track"], a["category"], a["name"]))

    if len(algorithms) != EXPECTED_TOTAL:
        raise SystemExit(
            f"expected {EXPECTED_TOTAL} algorithms, got {len(algorithms)}; "
            "update EXPECTED_TOTAL if catalogs changed intentionally"
        )

    if missing_source:
        raise SystemExit(f"missing source for {len(missing_source)} functions: {missing_source[:5]}")

    payload = {
        "total": len(algorithms),
        "tracks": sorted(TRACKS.values()),
        "algorithms": algorithms,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    per_track = {t: sum(1 for a in algorithms if a["track"] == t) for t in TRACKS.values()}
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(algorithms)} algorithms")
    for track, count in per_track.items():
        print(f"  {track}: {count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
