"""Ads psychology."""

from __future__ import annotations

import re


def ad_hook_variants(offer: str, *, count: int = 3) -> list[str]:
    """Generate ad hook variants. Time O(n)."""
    opts = [
        f"Stop wasting time on {offer}",
        f"{offer} without the guesswork",
        f"Founders use this for {offer}",
    ]
    return opts[:count]


def scroll_stop_score(headline: str) -> float:
    """Score ad scroll-stop power. Time O(n)."""
    return min(
        1.0, (0.3 if len(headline) < 60 else 0.1) + (0.3 if re.search(r"\d", headline) else 0)
    )


def ad_frequency_fatigue_score(impressions: int, *, threshold: int = 8) -> float:
    """Score ad fatigue from impressions. Time O(1)."""
    return min(1.0, impressions / threshold)


def retargeting_message_tier(tier: str, offer: str) -> str:
    """Retargeting message by funnel tier. Time O(1)."""
    tiers = {
        "aware": f"Still curious about {offer}?",
        "consider": f"Compare plans for {offer}",
        "cart": f"Finish setup for {offer}",
    }
    return tiers.get(tier.lower(), offer)


_BAD = [r"\bguaranteed results\b", r"\bget rich\b", r"\bno risk\b"]


def ad_claim_compliance_check(copy: str) -> list[str]:
    """Flag non-compliant ad claims. Time O(n)."""
    return [p for p in _BAD if re.search(p, copy, re.I)]


def creative_angle_matrix(product: str) -> dict[str, str]:
    """Creative angle matrix for ads. Time O(1)."""
    return {
        "pain": f"Stop struggling with {product}",
        "gain": f"Get outcomes faster with {product}",
        "proof": f"See how teams use {product}",
    }
