"""Social growth psychology."""

from __future__ import annotations

import math
from collections.abc import Sequence


def audience_warmth_score(replies: int, saves: int, profile_clicks: int) -> float:
    """Score audience warmth from engagement history. Time O(n)."""
    raw = replies * 0.4 + saves * 0.35 + profile_clicks * 0.25
    return min(1.0, raw / 100.0)


def content_pillar_balance(counts: dict[str, int]) -> dict[str, float]:
    """Balance content pillars. Time O(n)."""
    total = sum(counts.values()) or 1
    return {k: v / total for k, v in counts.items()}


def posting_cadence_plan(posts_per_week: int) -> list[str]:
    """Weekly posting cadence plan. Time O(1)."""
    days = ["Mon", "Wed", "Fri", "Sat", "Tue", "Thu", "Sun"]
    return [f"{days[i % 7]}: post slot {i + 1}" for i in range(posts_per_week)]


def cross_post_adaptation(x_post: str) -> str:
    """Adapt X post for LinkedIn. Time O(n)."""
    expanded = x_post.replace("\n", "\n\n")
    return f"{expanded}\n\nWhat's your experience?"


def creator_collab_fit(your_topics: Sequence[str], their_topics: Sequence[str]) -> float:
    """Score creator collaboration fit. Time O(n)."""
    yours = {t.lower() for t in your_topics}
    overlap = sum(1 for t in their_topics if t.lower() in yours)
    return overlap / max(1, len(your_topics))


def community_reply_priority(threads: Sequence[tuple[str, int]]) -> list[str]:
    """Prioritize community replies. Time O(n log n)."""
    return [t for t, _ in sorted(threads, key=lambda x: x[1], reverse=True)]


def follower_quality_score(replies_per_post: float, follower_count: int) -> float:
    """Score follower quality vs vanity. Time O(1)."""
    if follower_count <= 0:
        return 0.0
    ratio = replies_per_post / math.sqrt(follower_count)
    return min(1.0, ratio * 10)


def growth_loop_map(steps: Sequence[str]) -> list[str]:
    """Map content growth loop steps. Time O(n)."""
    return [f"{i + 1}. {s}" for i, s in enumerate(steps)]


def community_welcome_message(name: str, norm: str) -> str:
    """Community welcome message. Time O(1)."""
    return f"Welcome {name}! Start by introducing yourself. House rule: {norm}."
