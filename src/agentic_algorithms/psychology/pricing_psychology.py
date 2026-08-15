"""Pricing psychology."""

from __future__ import annotations

import math
import re
from typing import Sequence


def charm_price(amount: float) -> float:
    """Charm price ending in 9. Time O(1)."""
    base = int(amount)
    return float(base) + 0.99 if amount >= 10 else max(0.99, round(amount - 0.01, 2))

def anchoring_tier_order(tiers: Sequence[str]) -> list[str]:
    """Order tiers for anchoring effect. Time O(n)."""
    return sorted(tiers, reverse=True)

def decoy_tier_highlight(target: str, decoy: str) -> str:
    """Highlight target tier vs decoy. Time O(1)."""
    return f"Most teams pick {target} over {decoy} because ROI is clearer."

def price_framing_monthly_vs_annual(monthly: float, annual: float) -> str:
    """Frame annual vs monthly savings. Time O(1)."""
    save = monthly * 12 - annual
    return f"Pay annually and save ${save:.0f} vs monthly."

_FRICTION = [r"\bcredit card required\b", r"\bannual only\b", r"\bcontact sales\b"]

def payment_friction_score(copy: str) -> float:
    """Score checkout friction copy. Time O(n)."""
    return min(1.0, sum(1 for p in _FRICTION if re.search(p, copy, re.I)) / len(_FRICTION))

