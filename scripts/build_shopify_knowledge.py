#!/usr/bin/env python3
"""Build Shopify commerce knowledge JSON for the Algorithm Atlas UI.

Reads the curl_reap-scraped corpus from anish-shopify and emits a compact,
searchable index with exact DOM citations back to Shopify FAQ divs.

Usage:
    python scripts/build_shopify_knowledge.py
    SHOPIFY_CORPUS=/path/to/chunks.jsonl python scripts/build_shopify_knowledge.py
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CORPUS = ROOT.parent / "anish-shopify" / "knowledge" / "corpus" / "chunks.jsonl"
OUTPUT = ROOT / "web" / "data" / "shopify_commerce.json"
MAX_CONTENT = 1200
MAX_DOCS = 2000


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "doc"


def truncate(text: str, limit: int) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    if len(text) <= limit:
        return text
    return text[: limit - 1] + "…"


def load_chunks(path: Path) -> list[dict]:
    if not path.exists():
        raise SystemExit(f"corpus not found: {path}\nRun the scraper in anish-shopify/knowledge first.")
    rows: list[dict] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def chunk_to_doc(row: dict) -> dict:
    heading = row.get("heading") or row.get("page_title") or "Untitled"
    content = row.get("answer") or row.get("content") or ""
    citation = row.get("citation") or {}
    element_id = citation.get("element_id", "")
    slug = slugify(f"{row.get('page_url', '')}-{element_id or heading}")
    return {
        "id": f"shopify-doc--{slug}",
        "kind": "doc",
        "track": "shopify_commerce",
        "name": heading,
        "title": heading,
        "category": row.get("source_type", "help"),
        "block_type": row.get("block_type", "section"),
        "source_domain": row.get("source_domain", ""),
        "page_url": row.get("page_url", ""),
        "page_title": row.get("page_title", ""),
        "description": truncate(content, 220),
        "content": truncate(content, MAX_CONTENT),
        "citation": citation,
        "chunk_id": row.get("chunk_id", ""),
        "viz": "pipeline",
        "time": "",
        "space": "",
        "module": "",
        "function": "",
        "source": "",
    }


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--allow-missing", action="store_true")
    args = parser.parse_args()

    corpus_path = Path(os.environ.get("SHOPIFY_CORPUS", DEFAULT_CORPUS))
    if not corpus_path.exists():
        if args.allow_missing:
            payload = {"version": "1.0.0", "corpus_total": 0, "exported": 0, "faq_count": 0, "docs": []}
            OUTPUT.parent.mkdir(parents=True, exist_ok=True)
            OUTPUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
            print(f"wrote empty {OUTPUT.relative_to(ROOT)} (corpus missing)")
            return 0
        raise SystemExit(f"corpus not found: {corpus_path}\nRun the scraper in anish-shopify/knowledge first.")

    rows = load_chunks(corpus_path)

    # Prefer FAQ chunks, then sections; cap for UI bundle size
    faq_rows = [r for r in rows if r.get("block_type") == "faq"]
    other_rows = [r for r in rows if r.get("block_type") != "faq"]
    ordered = faq_rows + other_rows
    if len(ordered) > MAX_DOCS:
        ordered = ordered[:MAX_DOCS]

    docs = [chunk_to_doc(row) for row in ordered]
    faq_count = sum(1 for d in docs if d["block_type"] == "faq")

    payload = {
        "version": "1.0.0",
        "corpus_path": str(corpus_path),
        "corpus_total": len(rows),
        "exported": len(docs),
        "faq_count": faq_count,
        "scraped_at": rows[-1].get("scraped_at") if rows else None,
        "docs": docs,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(docs)} docs ({faq_count} FAQ) from {len(rows)} corpus chunks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
