"""Tests for human approval helpers and type helpers."""

import pytest

from agentic_algorithms.human import (
    ApprovalDecision,
    ApprovalRequest,
    auto_approve,
    deny_tools,
    resolve_approval,
)
from agentic_algorithms.types import Message, MessageRole, ToolCall


@pytest.mark.asyncio
async def test_resolve_approval_without_hook() -> None:
    response = await resolve_approval(
        None,
        ApprovalRequest(tool_call=ToolCall(id="1", name="transfer", arguments={})),
    )
    assert response.decision == ApprovalDecision.APPROVE


@pytest.mark.asyncio
async def test_deny_tools_blocks_sensitive_actions() -> None:
    hook = deny_tools({"transfer_funds"})
    response = await resolve_approval(
        hook,
        ApprovalRequest(tool_call=ToolCall(id="1", name="transfer_funds", arguments={})),
    )
    assert response.decision == ApprovalDecision.REJECT


def test_auto_approve_hook() -> None:
    hook = auto_approve()
    response = hook(ApprovalRequest(tool_call=ToolCall(id="1", name="lookup", arguments={})))
    assert response.decision == ApprovalDecision.APPROVE


def test_message_provider_dict_includes_tool_calls() -> None:
    message = Message(
        role=MessageRole.ASSISTANT,
        content="working",
        tool_calls=[ToolCall(id="1", name="lookup", arguments={"id": "acct"})],
    )
    payload = message.to_provider_dict()
    assert payload["tool_calls"][0]["name"] == "lookup"
