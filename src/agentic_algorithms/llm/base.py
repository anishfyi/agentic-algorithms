"""Provider-agnostic LLM interface."""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from pydantic import BaseModel, Field

from agentic_algorithms.types import Message, ToolCall


class LLMResponse(BaseModel):
    content: str = ""
    tool_calls: list[ToolCall] = Field(default_factory=list)
    raw: dict[str, Any] = Field(default_factory=dict)


@runtime_checkable
class LLMProvider(Protocol):
    async def complete(
        self,
        messages: list[Message],
        *,
        tools: list[dict[str, Any]] | None = None,
        temperature: float = 0.0,
        max_tokens: int | None = None,
    ) -> LLMResponse: ...

    def complete_sync(
        self,
        messages: list[Message],
        *,
        tools: list[dict[str, Any]] | None = None,
        temperature: float = 0.0,
        max_tokens: int | None = None,
    ) -> LLMResponse: ...


class MockProvider:
    """Deterministic provider for tests and offline examples."""

    def __init__(
        self,
        *,
        responses: list[LLMResponse] | None = None,
        default_response: str = "Done.",
    ) -> None:
        self._responses = list(responses or [])
        self._default_response = default_response
        self._index = 0

    async def complete(
        self,
        messages: list[Message],
        *,
        tools: list[dict[str, Any]] | None = None,
        temperature: float = 0.0,
        max_tokens: int | None = None,
    ) -> LLMResponse:
        _ = (messages, tools, temperature, max_tokens)
        return self._next()

    def complete_sync(
        self,
        messages: list[Message],
        *,
        tools: list[dict[str, Any]] | None = None,
        temperature: float = 0.0,
        max_tokens: int | None = None,
    ) -> LLMResponse:
        _ = (messages, tools, temperature, max_tokens)
        return self._next()

    def _next(self) -> LLMResponse:
        if self._index < len(self._responses):
            response = self._responses[self._index]
            self._index += 1
            return response
        return LLMResponse(content=self._default_response)
