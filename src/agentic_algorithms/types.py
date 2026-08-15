"""Shared types for agent loops and providers."""

from __future__ import annotations

import json
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class MessageRole(StrEnum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


class ToolCall(BaseModel):
    id: str
    name: str
    arguments: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def from_raw(cls, *, call_id: str, name: str, arguments: str | dict[str, Any]) -> ToolCall:
        if isinstance(arguments, str):
            parsed = json.loads(arguments) if arguments else {}
        else:
            parsed = arguments
        return cls(id=call_id, name=name, arguments=parsed)


class StopReason(StrEnum):
    COMPLETE = "complete"
    MAX_ITERATIONS = "max_iterations"
    TOOL_ERROR = "tool_error"
    APPROVAL_DENIED = "approval_denied"
    CANCELLED = "cancelled"


class Message(BaseModel):
    role: MessageRole
    content: str
    tool_call_id: str | None = None
    tool_calls: list[ToolCall] = Field(default_factory=list)
    name: str | None = None

    def to_provider_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {"role": self.role.value, "content": self.content}
        if self.tool_call_id is not None:
            payload["tool_call_id"] = self.tool_call_id
        if self.name is not None:
            payload["name"] = self.name
        if self.tool_calls:
            payload["tool_calls"] = [call.model_dump() for call in self.tool_calls]
        return payload


class ToolResult(BaseModel):
    tool_call_id: str
    name: str
    content: str
    is_error: bool = False


class AgentStep(BaseModel):
    iteration: int
    assistant_message: Message | None = None
    tool_calls: list[ToolCall] = Field(default_factory=list)
    tool_results: list[ToolResult] = Field(default_factory=list)
    stop_reason: StopReason | None = None


class AgentResult(BaseModel):
    output: str
    messages: list[Message]
    steps: list[AgentStep] = Field(default_factory=list)
    stop_reason: StopReason = StopReason.COMPLETE
    metadata: dict[str, Any] = Field(default_factory=dict)
