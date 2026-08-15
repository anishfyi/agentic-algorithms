"""Retention psychology."""

from __future__ import annotations


def churn_risk_score(days_inactive: int, support_tickets: int, nps: int | None) -> float:
    """Score churn risk from usage signals. Time O(n)."""
    risk = min(1.0, days_inactive / 30.0) * 0.5
    risk += min(0.3, support_tickets * 0.1)
    if nps is not None and nps < 7:
        risk += 0.2
    return min(1.0, risk)


def win_back_subject_line(feature: str) -> str:
    """Win-back email subject line. Time O(1)."""
    return f"We saved your spot ,  new {feature} you asked for"


def habit_loop_design(cue: str, routine: str, reward: str) -> str:
    """Cue-routine-reward habit loop copy. Time O(1)."""
    return f"When {cue}, {routine} so you can {reward}."


def renewal_reminder_frame(value_received: str, renewal_date: str) -> str:
    """Renewal reminder with value recap. Time O(1)."""
    return f"You achieved {value_received}. Renew by {renewal_date} to keep momentum."


def expansion_upsell_timing(days_since_activation: int) -> bool:
    """Days until expansion upsell. Time O(1)."""
    return days_since_activation >= 14
