"""Persuasion principles with ethical guardrails."""

from __future__ import annotations

import re

_CIALDINI_SIGNALS = {
    "reciprocity": [r"\bfree\b", r"\bcomplimentary\b", r"\bincluded\b"],
    "scarcity": [r"\blimited\b", r"\bonly \d+ left\b", r"\bexpires\b", r"\blast chance\b"],
    "authority": [r"\bcertified\b", r"\bexpert\b", r"\bapproved by\b", r"\bcpa\b", r"\blicensed\b"],
    "consistency": [r"\byou already\b", r"\bcontinue\b", r"\bkeep your streak\b"],
    "liking": [r"\bwe're like you\b", r"\bfor people like you\b"],
    "consensus": [r"\b\d+% of\b", r"\bmost customers\b", r"\bothers also\b"],
}

_DARK_PATTERNS = [
    r"\bact now or lose\b",
    r"\bhidden fee\b",
    r"\bcan't cancel\b",
    r"\bguaranteed returns\b",
]


def cialdini_principle_score(text: str) -> dict[str, float]:
    """Score presence of Cialdini persuasion principles. Time O(n)."""
    scores: dict[str, float] = {}
    for principle, patterns in _CIALDINI_SIGNALS.items():
        hits = sum(1 for pattern in patterns if re.search(pattern, text, re.I))
        scores[principle] = min(1.0, hits / max(1, len(patterns)))
    return scores


def ethical_persuasion_check(text: str, *, domain: str = "general") -> list[str]:
    """Flag manipulative patterns; stricter for fintech. Time O(n)."""
    issues: list[str] = []
    for pattern in _DARK_PATTERNS:
        if re.search(pattern, text, re.I):
            issues.append(f"dark pattern detected: {pattern}")
    if domain in {"fintech", "accounting", "expense"}:
        scores = cialdini_principle_score(text)
        if scores.get("scarcity", 0) > 0.5:
            issues.append("scarcity framing may be inappropriate for regulated financial UX")
    return issues
