"""Cognitive load reduction for agent and product copy."""

from __future__ import annotations

import re


def readability_score(text: str) -> float:
    """Approximate readability 0..1 (higher is easier). Based on sentence/word length."""
    sentences = [part for part in re.split(r"[.!?]+", text) if part.strip()]
    words = re.findall(r"\b\w+\b", text)
    if not sentences or not words:
        return 0.0
    avg_sentence = len(words) / len(sentences)
    avg_word_len = sum(len(word) for word in words) / len(words)
    # Penalize long sentences and long words
    score = 1.0 - min(1.0, (avg_sentence - 12) / 30) - min(0.5, (avg_word_len - 4.5) / 10)
    return max(0.0, min(1.0, score))


def progressive_disclosure_plan(steps: list[str], *, batch_size: int = 3) -> list[list[str]]:
    """Batch complex instructions to reduce cognitive overload. Time O(n)."""
    if batch_size <= 0:
        return [steps]
    return [steps[index : index + batch_size] for index in range(0, len(steps), batch_size)]
