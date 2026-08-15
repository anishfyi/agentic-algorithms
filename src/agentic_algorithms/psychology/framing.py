"""Framing algorithms for decision-support copy."""

from __future__ import annotations


def loss_aversion_frame(
    action: str,
    loss_if_skip: str,
    *,
    multiplier: float = 2.0,
) -> str:
    """Loss-framed message (Kahneman-Tversky style emphasis on avoiding loss)."""
    _ = multiplier  # reserved for weighted experiments
    return f"If you skip {action}, you risk {loss_if_skip}. Taking action now avoids that loss."


def gain_frame(action: str, benefit: str) -> str:
    """Gain-framed message emphasizing positive outcome."""
    return f"If you {action}, you can {benefit}."


def neutral_frame(action: str, fact: str) -> str:
    """Neutral, low-manipulation framing for regulated domains (fintech, health)."""
    return f"Option: {action}. Relevant fact: {fact}. You can proceed or decline."


def anchoring_adjust(
    anchor_value: float,
    target_value: float,
    *,
    dampening: float = 0.5,
) -> float:
    """Pull estimate toward target, reducing anchor pull. Time O(1)."""
    return anchor_value + dampening * (target_value - anchor_value)
