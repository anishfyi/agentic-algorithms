"""Copywriting psychology."""

from __future__ import annotations

import math
import re
from typing import Sequence


def headline_power_score(headline: str) -> float:
    """Score headline punch. Time O(n)."""
    score = 0.0
    if 6 <= len(headline.split()) <= 12:
        score += 0.3
    if re.search(r"\b(how|why|new|secret|free)\b", headline, re.I):
        score += 0.3
    if re.search(r"\d", headline):
        score += 0.2
    return min(1.0, score + min(0.2, len(headline) / 80))

def active_voice_ratio(text: str) -> float:
    """Estimate active vs passive voice ratio. Time O(n)."""
    passive = len(re.findall(r"\b(is|are|was|were)\s+\w+ed\b", text, re.I))
    active = len(re.findall(r"\b(we|you|i)\s+\w+\b", text, re.I))
    total = passive + active
    return active / total if total else 1.0

_BEN = [r"\bsave\b", r"\bearn\b", r"\bfaster\b", r"\bconfident\b", r"\bgrow\b"]
_FEAT = [r"\bapi\b", r"\bdashboard\b", r"\bintegration\b", r"\bmodule\b"]

def benefit_vs_feature_ratio(text: str) -> float:
    """Ratio of benefit to feature language. Time O(n)."""
    b = sum(1 for p in _BEN if re.search(p, text, re.I))
    f = sum(1 for p in _FEAT if re.search(p, text, re.I))
    return b / max(1, b + f)

def curiosity_gap_line(topic: str, payoff: str) -> str:
    """Curiosity gap line without clickbait. Time O(1)."""
    return f"The part everyone skips about {topic} (and how it {payoff})."

def specificity_score(text: str) -> float:
    """Score copy specificity via numbers and proper nouns. Time O(n)."""
    nums = len(re.findall(r"\b\d+[\d.,%]*\b", text))
    caps = len(re.findall(r"\b[A-Z][a-z]+\b", text))
    return min(1.0, (nums * 0.15 + caps * 0.05))

_POWER = ["proven", "instant", "exclusive", "trusted", "simple", "guaranteed"]

def power_word_density(text: str) -> float:
    """Density of emotional power words. Time O(n)."""
    words = text.lower().split()
    if not words:
        return 0.0
    hits = sum(1 for w in words if w.strip(".,!?") in _POWER)
    return hits / len(words)

def rhythm_variation_score(text: str) -> float:
    """Score sentence rhythm variation. Time O(n)."""
    lengths = [len(s.split()) for s in re.split(r"[.!?]+", text) if s.strip()]
    if len(lengths) < 2:
        return 0.0
    avg = sum(lengths) / len(lengths)
    var = sum((l - avg) ** 2 for l in lengths) / len(lengths)
    return min(1.0, var / 20.0)

