"""OpenAI provider."""

from __future__ import annotations

import json
from typing import Any

from agentic_algorithms.llm.base import LLMResponse
from agentic_algorithms.types import Message, MessageRole, ToolCall


class OpenAIProvider:
    def __init__(
        self,
        *,
        model: str = "gpt-4o-mini",
        api_key: str | None = None,
        client: Any | None = None,
    ) -> None:
        if client is None:
            try:
                import openai
            except ImportError as exc:
                msg = "Install openai: pip install 'agentic-algorithms[openai]'"
                raise ImportError(msg) from exc
            self._client = openai.AsyncOpenAI(api_key=api_key)
            self._sync_client = openai.OpenAI(api_key=api_key)
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
        kwargs = _build_kwargs(
            model=self.model,
            messages=messages,
            tools=tools,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        response = await self._client.chat.completions.create(**kwargs)
        return _from_openai_response(response)

    def complete_sync(
        self,
        messages: list[Message],
        *,
        tools: list[dict[str, Any]] | None = None,
        temperature: float = 0.0,
        max_tokens: int | None = None,
    ) -> LLMResponse:
        kwargs = _build_kwargs(
            model=self.model,
            messages=messages,
            tools=tools,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        response = self._sync_client.chat.completions.create(**kwargs)
        return _from_openai_response(response)


def _build_kwargs(
    *,
    model: str,
    messages: list[Message],
    tools: list[dict[str, Any]] | None,
    temperature: float,
    max_tokens: int | None,
) -> dict[str, Any]:
    kwargs: dict[str, Any] = {
        "model": model,
        "messages": [_to_openai_message(message) for message in messages],
        "temperature": temperature,
    }
    if max_tokens is not None:
        kwargs["max_tokens"] = max_tokens
    if tools:
        kwargs["tools"] = [
            {
                "type": "function",
                "function": {
                    "name": tool["name"],
                    "description": tool["description"],
                    "parameters": tool["parameters"],
                },
            }
            for tool in tools
        ]
    return kwargs


def _to_openai_message(message: Message) -> dict[str, Any]:
    if message.role == MessageRole.TOOL:
        return {
            "role": "tool",
            "tool_call_id": message.tool_call_id,
            "content": message.content,
        }
    if message.role == MessageRole.ASSISTANT and message.tool_calls:
        return {
            "role": "assistant",
            "content": message.content or None,
            "tool_calls": [
                {
                    "id": call.id,
                    "type": "function",
                    "function": {
                        "name": call.name,
                        "arguments": json.dumps(call.arguments),
                    },
                }
                for call in message.tool_calls
            ],
        }
    return {"role": message.role.value, "content": message.content}


def _from_openai_response(response: Any) -> LLMResponse:
    choice = response.choices[0]
    message = choice.message
    tool_calls: list[ToolCall] = []
    if message.tool_calls:
        for call in message.tool_calls:
            tool_calls.append(
                ToolCall.from_raw(
                    call_id=call.id,
                    name=call.function.name,
                    arguments=call.function.arguments,
                )
            )
    return LLMResponse(
        content=message.content or "",
        tool_calls=tool_calls,
        raw={"id": response.id, "model": response.model},
    )
