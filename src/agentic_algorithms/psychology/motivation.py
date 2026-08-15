"""Self-Determination Theory tone scoring for agent voice."""

from __future__ import annotations

import re

_AUTONOMY = [r"\byou can choose\b", r"\boptional\b", r"\bif you want\b", r"\byour choice\b"]
_COMPETENCE = [
    r"\byou(?:'ve| have) (?:done|completed)\b",
    r"\bhere(?:'s| is) how\b",
    r"\bstep \d+\b",
]
_RELATEDNESS = [r"\bwe(?:'re| are) here to help\b", r"\blet's\b", r"\btogether\b"]


def sdt_tone_score(text: str) -> dict[str, float]:
    """Score autonomy, competence, and relatedness language (SDT). Time O(n)."""

    def _score(patterns: list[str]) -> float:
        hits = sum(1 for pattern in patterns if re.search(pattern, text, re.I))
        return min(1.0, hits / max(1, len(patterns)))

    return {
        "autonomy": _score(_AUTONOMY),
        "competence": _score(_COMPETENCE),
        "relatedness": _score(_RELATEDNESS),
    }
