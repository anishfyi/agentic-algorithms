"""Conversion psychology."""

from __future__ import annotations

import math
import re
from typing import Sequence


_CTA_PATTERNS = [r"\bstart\b", r"\btry\b", r"\bget\b", r"\bfree\b"]

def cta_clarity_score(text: str) -> float:
    """Score CTA clarity in landing copy. Time O(n)."""
    if not text:
        return 0.0
    hits = sum(1 for p in _CTA_PATTERNS if re.search(p, text, re.I))
    return min(1.0, hits / max(1, len(_CTA_PATTERNS)))

_FRICTION_PATTERNS = [r"\bwait\b", r"\bcomplicated\b", r"\bmanual\b", r"\bconfusing\b"]

def friction_point_score(text: str) -> float:
    """Score UX friction language in copy. Time O(n)."""
    if not text:
        return 0.0
    hits = sum(1 for p in _FRICTION_PATTERNS if re.search(p, text, re.I))
    return min(1.0, hits / max(1, len(_FRICTION_PATTERNS)))

_URGENCY_PATTERNS = [r"\breal deadline\b", r"\blimited\b", r"\bwhile supplies\b"]

def urgency_ethical_score(text: str) -> float:
    """Score ethical vs dark urgency. Time O(n)."""
    if not text:
        return 0.0
    hits = sum(1 for p in _URGENCY_PATTERNS if re.search(p, text, re.I))
    return min(1.0, hits / max(1, len(_URGENCY_PATTERNS)))

def landing_hero_frame(outcome: str, proof: str, cta: str) -> str:
    """Hero section frame for landing pages. Time O(1)."""
    return f"{outcome}\n{proof}\n→ {cta}"

def form_field_reduction_plan(fields: Sequence[str], *, max_initial: int = 3) -> list[list[str]]:
    """Plan progressive form fields. Time O(n)."""
    fields = list(fields)
    if len(fields) <= max_initial:
        return [fields]
    return [fields[:max_initial], fields[max_initial:]]

def micro_commitment_step(small_action: str, benefit: str) -> str:
    """Micro-commitment step before main CTA. Time O(1)."""
    return f"First, {small_action} — takes 30 seconds and {benefit}."

def checkout_trust_badges(guarantee: str) -> list[str]:
    """Checkout trust badge copy. Time O(1)."""
    return ["Secure checkout", guarantee, "Cancel anytime"]

def social_proof_placement(section: str) -> str:
    """Where to place social proof on page. Time O(1)."""
    return {"hero": "logo strip under headline", "pricing": "testimonial beside tier", "checkout": "trust badges"}.get(section, "near CTA")

