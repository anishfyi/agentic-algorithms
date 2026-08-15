"""Tests for memory helpers."""

from agentic_algorithms.memory import LongTermMemory, ShortTermMemory, cosine_similarity
from agentic_algorithms.types import Message, MessageRole


def test_short_term_memory_is_bounded() -> None:
    memory = ShortTermMemory(max_messages=2)
    memory.add(Message(role=MessageRole.USER, content="one"))
    memory.add(Message(role=MessageRole.USER, content="two"))
    memory.add(Message(role=MessageRole.USER, content="three"))
    snapshot = memory.snapshot()
    assert len(snapshot) == 2
    assert snapshot[0].content == "two"


def test_long_term_memory_search() -> None:
    memory = LongTermMemory()
    memory.remember("client:acme", "INR reporting, net-30 terms")
    memory.remember("client:beta", "USD reporting, prepaid")
    hits = memory.search("INR reporting")
    assert hits
    assert "acme" in hits[0]


def test_cosine_similarity() -> None:
    assert cosine_similarity([1.0, 0.0], [1.0, 0.0]) == 1.0
    assert cosine_similarity([1.0, 0.0], [0.0, 1.0]) == 0.0
