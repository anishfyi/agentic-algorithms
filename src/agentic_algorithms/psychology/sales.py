"""Sales psychology helpers."""

from __future__ import annotations

import math
import re
from typing import Sequence


def objection_reframe(objection: str) -> str:
    """Reframe a sales objection into a learning question. Time O(1)."""
    return f"When you say '{objection}', what outcome would need to be true for this to be a yes?"

def spin_question_builder(stage: str, topic: str) -> str:
    """Build SPIN-style discovery question. Time O(1)."""
    templates = {
        "situation": f"Walk me through how you handle {topic} today.",
        "problem": f"What breaks most often with {topic}?",
        "implication": f"If {topic} stays unsolved, what does that cost you this quarter?",
        "need_payoff": f"If we fixed {topic}, what would your team do with the time back?",
    }
    return templates.get(stage.lower(), templates["situation"])

_GAPS = [r"\bbudget\b", r"\btimeline\b", r"\bdecision\b", r"\bpain\b", r"\bmetric\b"]

def discovery_gap_score(notes: str) -> float:
    """Score how much discovery is missing from notes. Time O(n)."""
    covered = sum(1 for g in _GAPS if re.search(g, notes, re.I))
    return 1.0 - covered / len(_GAPS)

def follow_up_timing_days(stage: str) -> int:
    """Suggest ethical follow-up delay in days. Time O(1)."""
    return {"cold": 3, "demo": 2, "proposal": 1, "silent": 5}.get(stage.lower(), 3)

def pipeline_stage_score(signals: dict[str, bool]) -> float:
    """Score deal health from stage signals. Time O(n)."""
    weights = {"champion": 0.3, "economic_buyer_met": 0.25, "timeline": 0.2, "pain_quantified": 0.15, "next_step": 0.1}
    return min(1.0, sum(weights[k] for k, v in signals.items() if v and k in weights))

def champion_enablement_brief(problem: str, proof: str, ask: str) -> str:
    """One-pager brief for internal champion. Time O(1)."""
    return f"Problem: {problem}\nProof: {proof}\nAsk: {ask}\nRisk if we wait: status quo continues."

def demo_story_arc(pain: str, shift: str, proof: str) -> list[str]:
    """Three-beat demo narrative arc. Time O(1)."""
    return [f"Today: {pain}", f"Imagine: {shift}", f"Proof: {proof}"]

_PUSHY = [r"sign today", r"last chance", r"act now", r"limited seats"]

def closing_language_check(text: str) -> list[str]:
    """Flag pushy closing language. Time O(n)."""
    return [p for p in _PUSHY if re.search(p, text, re.I)]

def multi_threading_map(roles: Sequence[str]) -> dict[str, str]:
    """Map multi-threading stakeholders. Time O(n)."""
    return {r: f"Engage {r} with role-specific proof" for r in roles}

_RISK = [r"no budget", r"just browsing", r"next year", r"ghost"]

def deal_risk_flags(notes: str) -> list[str]:
    """Flag deal risk phrases in notes. Time O(n)."""
    return [p for p in _RISK if re.search(p, notes, re.I)]

