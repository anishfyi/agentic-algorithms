"""Virality psychology."""

from __future__ import annotations

import re


def shareability_score(text: str) -> float:
    """Score content shareability. Time O(n)."""
    signals = [r"\btemplate\b", r"\bcheatsheet\b", r"\bshare\b", r"\btag\b"]
    return min(1.0, sum(1 for s in signals if re.search(s, text, re.I)) / len(signals))


def referral_incentive_frame(give: str, get: str) -> str:
    """Referral incentive frame. Time O(1)."""
    return f"Give {give}, get {get} — both sides win."


def network_effect_pitch(audience: str, benefit: str) -> str:
    """Network effect pitch line. Time O(1)."""
    return f"The more {audience} join, the better {benefit} gets for everyone."


def k_factor_estimate(invites_per_user: float, conversion_rate: float) -> float:
    """Estimate viral k-factor. Time O(1)."""
    return invites_per_user * conversion_rate


def word_of_mouth_prompt(outcome: str) -> str:
    """Prompt satisfied users for referrals. Time O(1)."""
    return f"If {outcome} helped you, who else should know?"


def meme_template_fit(caption: str, brand_voice: str) -> float:
    """Score meme template fit for merch marketing. Time O(n)."""
    risky = len(re.findall(r"\b(nsfw|politics)\b", caption, re.I))
    on_brand = 1.0 if brand_voice.lower() in caption.lower() else 0.3
    return max(0.0, on_brand - risky * 0.5)
