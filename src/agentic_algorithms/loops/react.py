"""ReAct: reason and act until the model stops calling tools."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any

from agentic_algorithms.human import (
    ApprovalDecision,
    ApprovalRequest,
    ToolApprovalHook,
    resolve_approval,
)
from agentic_algorithms.llm.base import LLMProvider
from agentic_algorithms.tools import ToolRegistry
from agentic_algorithms.types import (
    AgentResult,
    AgentStep,
    Message,
    MessageRole,
    StopReason,
    ToolCall,
)


@dataclass
class ReActLoop:
    provider: LLMProvider
    tools: ToolRegistry
    max_iterations: int = 12
    approval_hook: ToolApprovalHook | None = None
    temperature: float = 0.0
    max_tokens: int | None = None

    async def arun(
        self,
        messages: list[Message],
        *,
        metadata: dict[str, Any] | None = None,
    ) -> AgentResult:
        working = list(messages)
        steps: list[AgentStep] = []
        stop_reason = StopReason.COMPLETE

        for iteration in range(1, self.max_iterations + 1):
            response = await self.provider.complete(
                working,
                tools=self.tools.schemas(),
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
            assistant = Message(
                role=MessageRole.ASSISTANT,
                content=response.content,
                tool_calls=response.tool_calls,
            )
            working.append(assistant)

            if not response.tool_calls:
                return AgentResult(
                    output=response.content,
                    messages=working,
                    steps=steps,
                    stop_reason=stop_reason,
                    metadata=metadata or {},
                )

            tool_results = []
            for call in response.tool_calls:
                approved_call, denied = await self._apply_approval(call, working)
                if denied:
                    stop_reason = StopReason.APPROVAL_DENIED
                    step = AgentStep(
                        iteration=iteration,
                        assistant_message=assistant,
                        tool_calls=[call],
                        stop_reason=stop_reason,
                    )
                    steps.append(step)
                    return AgentResult(
                        output=denied,
                        messages=working,
                        steps=steps,
                        stop_reason=stop_reason,
                        metadata=metadata or {},
                    )
                result = await self.tools.execute(approved_call)
                tool_results.append(result)
                working.append(
                    Message(
                        role=MessageRole.TOOL,
                        content=result.content,
                        tool_call_id=result.tool_call_id,
                        name=result.name,
                    )
                )
                if result.is_error:
                    stop_reason = StopReason.TOOL_ERROR

            steps.append(
                AgentStep(
                    iteration=iteration,
                    assistant_message=assistant,
                    tool_calls=response.tool_calls,
                    tool_results=tool_results,
                )
            )

        return AgentResult(
            output=working[-1].content,
            messages=working,
            steps=steps,
            stop_reason=StopReason.MAX_ITERATIONS,
            metadata=metadata or {},
        )

    def run(
        self,
        messages: list[Message],
        *,
        metadata: dict[str, Any] | None = None,
    ) -> AgentResult:
        return asyncio.run(self.arun(messages, metadata=metadata))

    async def _apply_approval(
        self,
        call: ToolCall,
        messages: list[Message],
    ) -> tuple[ToolCall, str | None]:
        response = await resolve_approval(
            self.approval_hook,
            ApprovalRequest(tool_call=call, messages=messages),
        )
        if response.decision == ApprovalDecision.REJECT:
            reason = response.reason or f"Tool call rejected: {call.name}"
            return call, reason
        if response.decision == ApprovalDecision.EDIT and response.edited_arguments is not None:
            return call.model_copy(update={"arguments": response.edited_arguments}), None
        return call, None
