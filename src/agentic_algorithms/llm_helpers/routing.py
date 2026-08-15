"""Model routing and inference loop helpers."""

from __future__ import annotations

import re
from collections import Counter


def route_model_by_complexity(
    prompt: str,
    *,
    simple_model: str = "gpt-4o-mini",
    complex_model: str = "gpt-4o",
    token_threshold: int = 1500,
) -> str:
    """Route to a larger model when prompt complexity signals warrant it.

    Heuristics: length, code blocks, multi-step verbs, tool/schema mentions.
    Time O(n), space O(1).
    """
    score = 0
    if len(prompt) > token_threshold * 4:
        score += 2
    if "```" in prompt:
        score += 2
    if re.search(r"\b(refactor|architect|prove|optimize|migrate)\b", prompt, re.I):
        score += 2
    if re.search(r"\b(json schema|tool call|multi-?step)\b", prompt, re.I):
        score += 1
    return complex_model if score >= 3 else simple_model


def self_consistency_vote(answers: list[str]) -> str:
    """Majority vote across self-consistency samples. Time O(n), space O(n)."""
    if not answers:
        return ""
    normalized = [answer.strip().lower() for answer in answers]
    winner, _ = Counter(normalized).most_common(1)[0]
    for answer in answers:
        if answer.strip().lower() == winner:
            return answer
    return answers[0]


def reflexion_critique_prompt(task: str, answer: str) -> str:
    """Prompt template for self-critique before retry."""
    return (
        "You are a strict reviewer. Identify factual errors, missing steps, and unsafe actions.\n"
        f"Task:\n{task}\n\nAnswer:\n{answer}\n\n"
        "Write a short critique. If the answer is fine, say 'No issues.'"
    )
