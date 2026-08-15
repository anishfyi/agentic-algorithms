"""SaaS growth psychology."""

from __future__ import annotations

from collections.abc import Sequence


def plg_activation_score(events: dict[str, bool]) -> float:
    """PLG activation score from events. Time O(n)."""
    keys = ["signup", "first_project", "invite_teammate", "core_action", "return_day_7"]
    return sum(1 for k in keys if events.get(k)) / len(keys)


def freemium_limit_message(limit: str, upgrade_benefit: str) -> str:
    """Freemium limit upgrade message. Time O(1)."""
    return f"You hit {limit}. Upgrade to {upgrade_benefit}."


def upgrade_trigger_event(usage_ratio: float, *, threshold: float = 0.8) -> bool:
    """Suggest upgrade trigger from usage. Time O(1)."""
    return usage_ratio >= threshold


def usage_based_upsell_line(metric: str, headroom: str) -> str:
    """Usage-based upsell line. Time O(1)."""
    return f"You are at {metric}. Add {headroom} before workflow stalls."


def seat_expansion_probe(team_growth: str) -> str:
    """Probe for seat expansion. Time O(1)."""
    return f"As {team_growth}, want shared seats so nobody hits limits?"


def nrr_expansion_map(accounts: Sequence[str]) -> dict[str, str]:
    """Net revenue retention expansion map. Time O(n)."""
    return {a: "upsell + cross-sell review" for a in accounts}
