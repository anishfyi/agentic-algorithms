"""Tests for LLM providers."""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

from agentic_algorithms.llm.anthropic import AnthropicProvider
from agentic_algorithms.llm.base import LLMResponse, MockProvider
from agentic_algorithms.llm.openai import OpenAIProvider
from agentic_algorithms.types import Message, MessageRole, ToolCall


@pytest.mark.asyncio
async def test_mock_provider_returns_sequential_responses() -> None:
    provider = MockProvider(responses=[LLMResponse(content="first"), LLMResponse(content="second")])
    first = await provider.complete([Message(role=MessageRole.USER, content="hi")])
    second = await provider.complete([Message(role=MessageRole.USER, content="again")])
    assert first.content == "first"
    assert second.content == "second"


def test_mock_provider_sync_path() -> None:
    provider = MockProvider(responses=[LLMResponse(content="sync")])
    response = provider.complete_sync([Message(role=MessageRole.USER, content="hi")])
    assert response.content == "sync"


@pytest.mark.asyncio
async def test_anthropic_provider_parses_tool_use() -> None:
    fake_response = SimpleNamespace(
        id="msg_1",
        model="claude-test",
        content=[
            SimpleNamespace(type="text", text="Checking balance"),
            SimpleNamespace(
                type="tool_use",
                id="tool_1",
                name="get_balance",
                input={"account_id": "cash"},
            ),
        ],
    )

    class FakeMessages:
        async def create(self, **_: Any) -> Any:
            return fake_response

    class FakeClient:
        messages = FakeMessages()

    provider = AnthropicProvider(client=FakeClient())
    response = await provider.complete([Message(role=MessageRole.USER, content="balance?")])
    assert response.content == "Checking balance"
    assert response.tool_calls[0].name == "get_balance"


def test_anthropic_provider_sync_path() -> None:
    fake_response = SimpleNamespace(
        id="msg_1",
        model="claude-test",
        content=[SimpleNamespace(type="text", text="sync ok")],
    )

    class FakeMessages:
        def create(self, **_: Any) -> Any:
            return fake_response

    class FakeClient:
        messages = FakeMessages()

    provider = AnthropicProvider(client=FakeClient())
    response = provider.complete_sync([Message(role=MessageRole.USER, content="hi")])
    assert response.content == "sync ok"


@pytest.mark.asyncio
async def test_anthropic_provider_handles_tool_and_system_messages() -> None:
    fake_response = SimpleNamespace(
        id="msg_2",
        model="claude-test",
        content=[SimpleNamespace(type="text", text="done")],
    )

    class FakeMessages:
        async def create(self, **kwargs: Any) -> Any:
            assert kwargs["system"] == "follow policy"
            assert kwargs["messages"][0]["content"][0]["type"] == "tool_result"
            return fake_response

    provider = AnthropicProvider(client=SimpleNamespace(messages=FakeMessages()))
    response = await provider.complete(
        [
            Message(role=MessageRole.SYSTEM, content="follow policy"),
            Message(role=MessageRole.TOOL, content="250000", tool_call_id="tool_1"),
            Message(role=MessageRole.USER, content="next"),
        ]
    )
    assert response.content == "done"


@pytest.mark.asyncio
async def test_openai_provider_parses_tool_calls() -> None:
    fake_response = SimpleNamespace(
        id="chat_1",
        model="gpt-test",
        choices=[
            SimpleNamespace(
                message=SimpleNamespace(
                    content="posting",
                    tool_calls=[
                        SimpleNamespace(
                            id="call_1",
                            function=SimpleNamespace(
                                name="post_journal_entry",
                                arguments='{"account": "cash", "amount": 100}',
                            ),
                        )
                    ],
                )
            )
        ],
    )

    class FakeCompletions:
        async def create(self, **_: Any) -> Any:
            return fake_response

    class FakeClient:
        chat = SimpleNamespace(completions=FakeCompletions())

    provider = OpenAIProvider(client=FakeClient())
    response = await provider.complete([Message(role=MessageRole.USER, content="post")])
    assert response.tool_calls == [
        ToolCall(
            id="call_1", name="post_journal_entry", arguments={"account": "cash", "amount": 100}
        )
    ]


@pytest.mark.asyncio
async def test_openai_provider_handles_tool_message() -> None:
    fake_response = SimpleNamespace(
        id="chat_2",
        model="gpt-test",
        choices=[SimpleNamespace(message=SimpleNamespace(content="ok", tool_calls=None))],
    )

    class FakeCompletions:
        async def create(self, **kwargs: Any) -> Any:
            assert kwargs["messages"][0]["role"] == "tool"
            return fake_response

    provider = OpenAIProvider(
        client=SimpleNamespace(chat=SimpleNamespace(completions=FakeCompletions()))
    )
    response = await provider.complete(
        [Message(role=MessageRole.TOOL, content="done", tool_call_id="call_1")]
    )
    assert response.content == "ok"


def test_openai_provider_sync_path() -> None:
    fake_response = SimpleNamespace(
        id="chat_1",
        model="gpt-test",
        choices=[SimpleNamespace(message=SimpleNamespace(content="done", tool_calls=None))],
    )

    class FakeCompletions:
        def create(self, **_: Any) -> Any:
            return fake_response

    provider = OpenAIProvider(
        client=SimpleNamespace(chat=SimpleNamespace(completions=FakeCompletions()))
    )
    response = provider.complete_sync([Message(role=MessageRole.USER, content="hi")])
    assert response.content == "done"
