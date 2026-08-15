"""RAG helpers for LLM context packing."""

from __future__ import annotations

import re


def chunk_text(
    text: str,
    *,
    chunk_size: int = 800,
    overlap: int = 100,
) -> list[str]:
    """Split text into overlapping chunks for embedding/RAG. Time O(n), space O(chunks)."""
    if chunk_size <= 0:
        return [text]
    words = text.split()
    if not words:
        return []
    chunks: list[str] = []
    start = 0
    step = max(1, chunk_size - overlap)
    while start < len(words):
        piece = " ".join(words[start : start + chunk_size])
        chunks.append(piece)
        start += step
    return chunks


def pack_rag_context(
    query: str,
    chunks: list[tuple[str, float]],
    *,
    max_chars: int = 6000,
    header: str = "Retrieved context:",
) -> str:
    """Pack top-ranked chunks into a single context block for the LLM.

    chunks: (text, score) sorted by score descending.
    Time O(chunks), space O(output).
    """
    lines = [header, f"Query: {query}", ""]
    used = 0
    for index, (text, score) in enumerate(chunks, start=1):
        block = f"[{index}] (score={score:.3f})\n{text.strip()}\n"
        if used + len(block) > max_chars:
            break
        lines.append(block)
        used += len(block)
    return "\n".join(lines).strip()


def deduplicate_chunks(chunks: list[str], *, min_jaccard: float = 0.8) -> list[str]:
    """Remove near-duplicate chunks by token Jaccard similarity. Time O(n^2)."""
    unique: list[str] = []
    for chunk in chunks:
        tokens = set(re.findall(r"[a-z0-9]+", chunk.lower()))
        if any(
            _jaccard(tokens, set(re.findall(r"[a-z0-9]+", item.lower()))) >= min_jaccard
            for item in unique
        ):
            continue
        unique.append(chunk)
    return unique


def _jaccard(left: set[str], right: set[str]) -> float:
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)
