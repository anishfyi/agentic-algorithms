"""Anthropic Claude provider."""

from __future__ import annotations

import json
from typing import Any

from agentic_algorithms.llm.base import LLMResponse
from agentic_algorithms.types import Message, MessageRole, ToolCall


class AnthropicProvider:
    def __init__(
        self,
        *,
        model: str = "claude-sonnet-4-20250514",
        api_key: str | None = None,
        client: Any | None = None,
    ) -> None:
        if client is None:
            try:
                import anthropic
            except ImportError as exc:
                msg = "Install anthropic: pip install 'agentic-algorithms[anthropic]'"
                raise ImportError(msg) from exc
            self._client = anthropic.AsyncAnthropic(api_key=api_key)
            self._sync_client = anthropic.Anthropic(api_key=api_key)
        else:
            self._client = client
            self._sync_client = client
        self.model = model

    async def complete(
        self,
        messages: list[Message],
        *,
        tools: list[dict[str, Any]] | None = None,
        temperature: float = 0.0,
        max_tokens: int | None = None,
    ) -> LLMResponse:
        system, anthropic_messages = _split_messages(messages)
        kwargs: dict[str, Any] = {
            "model": self.model,
            "messages": anthropic_messages,
            "temperature": temperature,
            "max_tokens": max_tokens or 4096,
        }
        if system:
            kwargs["system"] = system
        if tools:
            kwargs["tools"] = [_to_anthropic_tool(tool) for tool in tools]
        response = await self._client.messages.create(**kwargs)
        return _from_anthropic_response(response)

    def complete_sync(
        self,
        messages: list[Message],
        *,
        tools: list[dict[str, Any]] | None = None,
        temperature: float = 0.0,
        max_tokens: int | None = None,
    ) -> LLMResponse:
        system, anthropic_messages = _split_messages(messages)
        kwargs: dict[str, Any] = {
            "model": self.model,
            "messages": anthropic_messages,
            "temperature": temperature,
            "max_tokens": max_tokens or 4096,
        }
        if system:
            kwargs["system"] = system
        if tools:
            kwargs["tools"] = [_to_anthropic_tool(tool) for tool in tools]
        response = self._sync_client.messages.create(**kwargs)
        return _from_anthropic_response(response)


def _split_messages(messages: list[Message]) -> tuple[str | None, list[dict[str, Any]]]:
    system_parts: list[str] = []
    converted: list[dict[str, Any]] = []
    for message in messages:
        if message.role == MessageRole.SYSTEM:
            system_parts.append(message.content)
            continue
        if message.role == MessageRole.TOOL:
            converted.append(
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": message.tool_call_id,
                            "content": message.content,
                        }
                    ],
                }
            )
            continue
        if message.role == MessageRole.ASSISTANT and message.tool_calls:
            content: list[dict[str, Any]] = []
            if message.content:
                content.append({"type": "text", "text": message.content})
            for call in message.tool_calls:
                content.append(
                    {
                        "type": "tool_use",
                        "id": call.id,
                        "name": call.name,
                        "input": call.arguments,
                    }
                )
            converted.append({"role": "assistant", "content": content})
            continue
        converted.append({"role": message.role.value, "content": message.content})
    system = "\n\n".join(system_parts) if system_parts else None
    return system, converted


def _to_anthropic_tool(tool: dict[str, Any]) -> dict[str, Any]:
    return {
        "name": tool["name"],
        "description": tool["description"],
        "input_schema": tool["parameters"],
    }


def _from_anthropic_response(response: Any) -> LLMResponse:
    text_parts: list[str] = []
    tool_calls: list[ToolCall] = []
    for block in response.content:
        block_type = getattr(block, "type", None)
        if block_type == "text":
            text_parts.append(block.text)
        elif block_type == "tool_use":
            tool_calls.append(ToolCall(id=block.id, name=block.name, arguments=dict(block.input)))
    return LLMResponse(
        content="".join(text_parts),
        tool_calls=tool_calls,
        raw={"id": response.id, "model": response.model},
    )


def _serialize_tool_arguments(arguments: dict[str, Any]) -> str:
    return json.dumps(arguments)
