"""Trust calibration for agentic systems."""

from __future__ import annotations

import re


def transparency_checklist(response: str) -> dict[str, bool]:
    """Check whether an agent response includes trust-building elements."""
    return {
        "states_limits": bool(
            re.search(r"\b(i can't|i cannot|not sure|uncertain)\b", response, re.I)
        ),
        "cites_source": bool(
            re.search(r"\b(source|according to|based on|reference)\b", response, re.I)
        ),
        "explains_reasoning": bool(
            re.search(r"\bbecause\b|\btherefore\b|\bso that\b", response, re.I)
        ),
        "offers_next_step": bool(
            re.search(r"\bnext step\b|\byou can\b|\bwould you like\b", response, re.I)
        ),
    }


def agent_trust_score(response: str) -> float:
    """Composite trust score from transparency checklist. Time O(n)."""
    checks = transparency_checklist(response)
    return sum(1.0 for value in checks.values() if value) / len(checks)
