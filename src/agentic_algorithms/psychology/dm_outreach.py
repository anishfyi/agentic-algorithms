"""DM outreach psychology."""

from __future__ import annotations

import math
import re
from typing import Sequence


def cold_dm_opener(trigger: str, relevance: str) -> str:
    """Cold DM opener with relevance. Time O(1)."""
    return f"Noticed {trigger}. We help with {relevance} — worth a 2-line overview?"

def warm_dm_followup(interaction: str, offer: str) -> str:
    """Warm DM follow-up after engagement. Time O(1)."""
    return f"Thanks for {interaction}. If useful, I can send {offer}."

def dm_personalization_hooks(bio: str, recent_post: str) -> list[str]:
    """Extract DM personalization hooks. Time O(n)."""
    hooks = []
    if bio.strip():
        hooks.append(bio.strip()[:80])
    if recent_post.strip():
        hooks.append(recent_post.strip()[:80])
    return hooks

_SPAM = [r"\bguaranteed\b", r"\bclick here\b", r"\bmake money\b", r"\b100%\b"]

def dm_spam_risk_score(message: str) -> float:
    """Score DM spam risk. Time O(n)."""
    return min(1.0, sum(1 for p in _SPAM if re.search(p, message, re.I)) / len(_SPAM))

def conversation_to_call_bridge(topic: str) -> str:
    """Bridge DM thread to call. Time O(1)."""
    return f"Happy to go deeper on {topic} — 15 min next week?"

def dm_opt_out_respect() -> str:
    """Respectful DM opt-out reply. Time O(1)."""
    return "Thanks for letting me know — won't follow up. Door's open if timing changes."

