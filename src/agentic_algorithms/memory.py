"""Agent memory primitives."""

from __future__ import annotations

import math
import re
from collections import deque
from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Protocol

from agentic_algorithms.types import Message, MessageRole


class MemoryStore(Protocol):
    def remember(self, key: str, value: str) -> None: ...
    def recall(self, key: str) -> str | None: ...
    def search(self, query: str, *, limit: int = 5) -> list[str]: ...


@dataclass
class ShortTermMemory:
    """Bounded in-context message window."""

    max_messages: int = 40

    def __post_init__(self) -> None:
        self._messages: deque[Message] = deque(maxlen=self.max_messages)

    def add(self, message: Message) -> None:
        self._messages.append(message)

    def extend(self, messages: Iterable[Message]) -> None:
        for message in messages:
            self.add(message)

    def snapshot(self) -> list[Message]:
        return list(self._messages)

    def clear(self) -> None:
        self._messages.clear()


@dataclass
class LongTermMemory:
    """Keyword-retrieval memory store for durable facts."""

    _entries: dict[str, str] = field(default_factory=dict)

    def remember(self, key: str, value: str) -> None:
        self._entries[key.strip().lower()] = value

    def recall(self, key: str) -> str | None:
        return self._entries.get(key.strip().lower())

    def search(self, query: str, *, limit: int = 5) -> list[str]:
        tokens = _tokenize(query)
        if not tokens:
            return []
        scored: list[tuple[float, str]] = []
        for key, value in self._entries.items():
            haystack = f"{key} {value}".lower()
            score = sum(1.0 for token in tokens if token in haystack)
            if score > 0:
                scored.append((score, f"{key}: {value}"))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [value for _, value in scored[:limit]]

    def as_system_context(self, query: str) -> Message | None:
        hits = self.search(query, limit=5)
        if not hits:
            return None
        body = "\n".join(f"- {hit}" for hit in hits)
        return Message(
            role=MessageRole.SYSTEM,
            content=f"Relevant memory:\n{body}",
        )


def _tokenize(text: str) -> list[str]:
    return [token for token in re.split(r"[^a-z0-9]+", text.lower()) if len(token) > 2]


def cosine_similarity(left: list[float], right: list[float]) -> float:
    if not left or not right or len(left) != len(right):
        return 0.0
    dot = sum(a * b for a, b in zip(left, right, strict=True))
    left_norm = math.sqrt(sum(value * value for value in left))
    right_norm = math.sqrt(sum(value * value for value in right))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return dot / (left_norm * right_norm)
