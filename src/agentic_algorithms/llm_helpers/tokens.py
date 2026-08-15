"""Token and cost estimation for LLM calls."""

from __future__ import annotations

from agentic_algorithms.types import Message


def estimate_tokens(messages: list[Message] | str) -> int:
    """Rough token estimate (~4 chars per token). Time O(n)."""
    if isinstance(messages, str):
        text = messages
    else:
        text = "\n".join(message.content for message in messages)
    return max(1, len(text) // 4)


def estimate_cost_usd(
    *,
    input_tokens: int,
    output_tokens: int,
    input_price_per_million: float,
    output_price_per_million: float,
) -> float:
    """Estimate USD cost from token counts and per-million pricing. Time O(1)."""
    input_cost = input_tokens * input_price_per_million / 1_000_000
    output_cost = output_tokens * output_price_per_million / 1_000_000
    return input_cost + output_cost
