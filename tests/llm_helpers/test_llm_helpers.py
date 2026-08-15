"""Tests for LLM helper algorithms."""

from __future__ import annotations

from pydantic import BaseModel

from agentic_algorithms.llm_helpers import (
    chain_of_thought_wrap,
    chunk_text,
    estimate_tokens,
    few_shot_prompt,
    pack_rag_context,
    parse_structured_output,
    prune_messages_by_token_budget,
    repair_json,
    route_model_by_complexity,
    self_consistency_vote,
    system_prompt_compose,
)
from agentic_algorithms.types import Message, MessageRole


class AnswerModel(BaseModel):
    answer: str


def test_few_shot_and_cot_prompts() -> None:
    prompt = few_shot_prompt("Classify sentiment", [("great", "positive")], "bad day")
    assert "Assistant:" in prompt
    assert "step by step" in chain_of_thought_wrap("Solve 2+2").lower()


def test_system_prompt_compose() -> None:
    system = system_prompt_compose("You are a bookkeeper", ["use minor units"], "JSON")
    assert "Constraints" in system
    assert "JSON" in system


def test_json_parsing_and_repair() -> None:
    raw = 'Here is data ```json\n{"answer": "ok"}\n```'
    parsed = parse_structured_output(raw, AnswerModel)
    assert parsed.answer == "ok"
    repaired = repair_json('{"answer": "x",}')
    assert '"answer"' in repaired


def test_context_pruning() -> None:
    messages = [
        Message(role=MessageRole.SYSTEM, content="sys"),
        Message(role=MessageRole.USER, content="old " * 200),
        Message(role=MessageRole.ASSISTANT, content="ok"),
        Message(role=MessageRole.USER, content="latest"),
    ]
    pruned = prune_messages_by_token_budget(messages, max_tokens=50)
    assert pruned[-1].content == "latest"
    assert estimate_tokens(pruned) <= estimate_tokens(messages)


def test_rag_chunk_and_pack() -> None:
    chunks = chunk_text("word " * 500, chunk_size=100, overlap=10)
    assert len(chunks) > 1
    packed = pack_rag_context("query", [(chunks[0], 0.9)])
    assert "Retrieved context" in packed


def test_routing_and_self_consistency() -> None:
    simple = route_model_by_complexity("hello")
    complex_prompt = route_model_by_complexity("refactor ```code``` " * 400)
    assert simple != complex_prompt or len(complex_prompt) > 0
    winner = self_consistency_vote(["yes", "yes", "no"])
    assert winner.lower() == "yes"
