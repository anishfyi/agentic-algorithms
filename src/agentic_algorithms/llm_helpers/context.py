"""Context window management for LLM message lists."""

from __future__ import annotations

from agentic_algorithms.llm_helpers.tokens import estimate_tokens
from agentic_algorithms.types import Message, MessageRole


def prune_messages_by_token_budget(
    messages: list[Message],
    *,
    max_tokens: int,
    preserve_system: bool = True,
    preserve_last_user: bool = True,
) -> list[Message]:
    """Drop oldest non-protected messages until under token budget.

    Time O(n), space O(n).
    """
    if not messages:
        return []
    protected: set[int] = set()
    if preserve_system:
        for index, message in enumerate(messages):
            if message.role == MessageRole.SYSTEM:
                protected.add(index)
    if preserve_last_user:
        for index in range(len(messages) - 1, -1, -1):
            if messages[index].role == MessageRole.USER:
                protected.add(index)
                break

    selected = list(messages)
    while estimate_tokens(selected) > max_tokens and len(selected) > 1:
        drop_index = next(
            (index for index in range(len(selected)) if index not in protected),
            None,
        )
        if drop_index is None:
            break
        selected.pop(drop_index)
        protected = {index if index < drop_index else index - 1 for index in protected}
    return selected


def sliding_window_messages(
    messages: list[Message],
    *,
    max_messages: int,
) -> list[Message]:
    """Keep system messages and the most recent turns. Time O(n), space O(n)."""
    if len(messages) <= max_messages:
        return messages
    system_messages = [message for message in messages if message.role == MessageRole.SYSTEM]
    other = [message for message in messages if message.role != MessageRole.SYSTEM]
    keep = max(0, max_messages - len(system_messages))
    return [*system_messages, *other[-keep:]]


def summarize_trigger(messages: list[Message], *, token_threshold: int) -> bool:
    """Return True when conversation should be summarized before continuing."""
    return estimate_tokens(messages) >= token_threshold
