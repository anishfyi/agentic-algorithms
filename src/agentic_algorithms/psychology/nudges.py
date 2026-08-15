"""Behavioral nudge templates."""

from __future__ import annotations


def default_option_label(action: str, *, recommended: bool = True) -> str:
    """Label a default option (libertarian paternalism). Time O(1)."""
    if recommended:
        return f"{action} (recommended)"
    return action


def social_proof_line(metric: str, *, audience: str = "customers") -> str:
    """Social proof line without fabricated statistics."""
    return f"Many {audience} choose this when {metric}."


def commitment_prompt(action: str, benefit: str) -> str:
    """Commitment/consistency nudge for voluntary opt-in."""
    return f"Want to commit to {action}? It helps you {benefit}. You can change this anytime."
