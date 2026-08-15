"""High-level Agent API."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from agentic_algorithms.human import ToolApprovalHook
from agentic_algorithms.llm.base import LLMProvider
from agentic_algorithms.loops.plan_execute import PlanExecuteLoop
from agentic_algorithms.loops.react import ReActLoop
from agentic_algorithms.memory import LongTermMemory, ShortTermMemory
from agentic_algorithms.tools import Tool, ToolRegistry
from agentic_algorithms.types import AgentResult, Message, MessageRole


class AgentMode(StrEnum):
    REACT = "react"
    PLAN_EXECUTE = "plan_execute"


@dataclass
class AgentConfig:
    system_prompt: str = (
        "You are a careful fintech operations agent. "
        "Verify amounts, accounts, and approvals before any money movement."
    )
    mode: AgentMode = AgentMode.REACT
    max_iterations: int = 12
    temperature: float = 0.0
    max_tokens: int | None = None
    approval_hook: ToolApprovalHook | None = None


@dataclass
class Agent:
    provider: LLMProvider
    tools: ToolRegistry = field(default_factory=ToolRegistry)
    config: AgentConfig = field(default_factory=AgentConfig)
    short_term_memory: ShortTermMemory = field(default_factory=ShortTermMemory)
    long_term_memory: LongTermMemory = field(default_factory=LongTermMemory)

    def __post_init__(self) -> None:
        self._react = ReActLoop(
            provider=self.provider,
            tools=self.tools,
            max_iterations=self.config.max_iterations,
            approval_hook=self.config.approval_hook,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
        )
        self._plan_execute = PlanExecuteLoop(
            provider=self.provider,
            tools=self.tools,
            react=self._react,
            temperature=self.config.temperature,
        )

    def add_tool(self, tool: Tool) -> None:
        self.tools.register(tool)

    def remember(self, key: str, value: str) -> None:
        self.long_term_memory.remember(key, value)

    async def arun(self, user_input: str, *, metadata: dict[str, Any] | None = None) -> AgentResult:
        messages = self._build_messages(user_input)
        if self.config.mode == AgentMode.PLAN_EXECUTE:
            result = await self._plan_execute.arun(user_input, context=messages, metadata=metadata)
        else:
            result = await self._react.arun(messages, metadata=metadata)
        self.short_term_memory.extend(result.messages)
        return result

    def run(self, user_input: str, *, metadata: dict[str, Any] | None = None) -> AgentResult:
        import asyncio

        return asyncio.run(self.arun(user_input, metadata=metadata))

    def _build_messages(self, user_input: str) -> list[Message]:
        messages: list[Message] = []
        if self.config.system_prompt:
            messages.append(Message(role=MessageRole.SYSTEM, content=self.config.system_prompt))
        memory_message = self.long_term_memory.as_system_context(user_input)
        if memory_message is not None:
            messages.append(memory_message)
        messages.extend(self.short_term_memory.snapshot())
        messages.append(Message(role=MessageRole.USER, content=user_input))
        return messages
