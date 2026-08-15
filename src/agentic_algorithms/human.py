"""Human-in-the-loop approval hooks."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field

from agentic_algorithms.types import Message, ToolCall


class ApprovalDecision(StrEnum):
    APPROVE = "approve"
    REJECT = "reject"
    EDIT = "edit"


class ApprovalRequest(BaseModel):
    tool_call: ToolCall
    messages: list[Message] = Field(default_factory=list)
    context: dict[str, Any] = Field(default_factory=dict)


class ApprovalResponse(BaseModel):
    decision: ApprovalDecision
    edited_arguments: dict[str, Any] | None = None
    reason: str | None = None


ToolApprovalHook = Callable[[ApprovalRequest], ApprovalResponse | Awaitable[ApprovalResponse]]


async def resolve_approval(
    hook: ToolApprovalHook | None,
    request: ApprovalRequest,
) -> ApprovalResponse:
    if hook is None:
        return ApprovalResponse(decision=ApprovalDecision.APPROVE)
    result = hook(request)
    if isinstance(result, ApprovalResponse):
        return result
    return await result


def auto_approve() -> ToolApprovalHook:
    def _approve(_: ApprovalRequest) -> ApprovalResponse:
        return ApprovalResponse(decision=ApprovalDecision.APPROVE)

    return _approve


def deny_tools(tool_names: set[str]) -> ToolApprovalHook:
    """Fail closed on sensitive fintech tools (payments, transfers, journal posts)."""

    def _hook(request: ApprovalRequest) -> ApprovalResponse:
        if request.tool_call.name in tool_names:
            return ApprovalResponse(
                decision=ApprovalDecision.REJECT,
                reason="manual review required",
            )
        return ApprovalResponse(decision=ApprovalDecision.APPROVE)

    return _hook
