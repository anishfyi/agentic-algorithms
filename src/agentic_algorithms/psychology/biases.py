"""Cognitive bias detection and mitigation for LLM agents."""

from __future__ import annotations

import re

_OVERCONFIDENCE_PATTERNS = [
    r"\b(definitely|certainly|always|never|guaranteed|100%)\b",
    r"\b(obviously|clearly|without doubt)\b",
]

_SYCOPHANCY_PATTERNS = [
    r"\bgreat question\b",
    r"\byou(?:'re| are) absolutely right\b",
    r"\bexcellent point\b",
    r"\bi completely agree\b",
]

_CONFIRMATION_PATTERNS = [
    r"\bas you (?:said|mentioned|know)\b",
    r"\bthat confirms\b",
]


def detect_overconfidence_markers(text: str) -> list[str]:
    """Flag absolute language that erodes calibrated trust. Time O(n)."""
    hits: list[str] = []
    for pattern in _OVERCONFIDENCE_PATTERNS:
        if re.search(pattern, text, flags=re.IGNORECASE):
            hits.append(pattern)
    return hits


def detect_sycophancy_markers(text: str) -> list[str]:
    """Flag agreeable filler that reduces honest pushback. Time O(n)."""
    hits: list[str] = []
    for pattern in _SYCOPHANCY_PATTERNS:
        if re.search(pattern, text, flags=re.IGNORECASE):
            hits.append(pattern)
    return hits


def detect_confirmation_bias_markers(text: str) -> list[str]:
    """Flag language that mirrors user belief without verification. Time O(n)."""
    return [pattern for pattern in _CONFIRMATION_PATTERNS if re.search(pattern, text, re.I)]


def bias_mitigation_prompt(detected: list[str]) -> str:
    """System addendum to reduce detected bias patterns in agent replies."""
    if not detected:
        return ""
    return (
        "Communication guardrails:\n"
        "- State uncertainty when evidence is incomplete.\n"
        "- Avoid absolute claims unless mathematically or logically provable.\n"
        "- Disagree respectfully when user assumptions conflict with data.\n"
        "- Prefer 'based on available data' over 'definitely'."
    )
