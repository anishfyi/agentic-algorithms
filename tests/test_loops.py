"""Tests for ReAct and plan-and-execute loops."""

from __future__ import annotations

import pytest

from agentic_algorithms.agent import Agent, AgentConfig, AgentMode
from agentic_algorithms.human import ApprovalDecision, ApprovalRequest, ApprovalResponse
from agentic_algorithms.llm.base import LLMResponse, MockProvider
from agentic_algorithms.loops.plan_execute import PlanExecuteLoop
from agentic_algorithms.loops.react import ReActLoop
from agentic_algorithms.tools import ToolRegistry, tool
from agentic_algorithms.types import Message, MessageRole, StopReason, ToolCall


@tool(description="Post a journal entry")
def post_journal_entry(account: str, amount: int) -> str:
    return f"posted {amount} to {account}"


@pytest.mark.asyncio
async def test_react_loop_completes_without_tools() -> None:
    provider = MockProvider(responses=[LLMResponse(content="Reconciled successfully.")])
    loop = ReActLoop(provider=provider, tools=ToolRegistry())
    result = await loop.arun([Message(role=MessageRole.USER, content="reconcile cash")])
    assert result.output == "Reconciled successfully."
    assert result.stop_reason == StopReason.COMPLETE


@pytest.mark.asyncio
async def test_react_loop_executes_tool_then_finishes() -> None:
    provider = MockProvider(
        responses=[
            LLMResponse(
                content="Checking balance",
                tool_calls=[
                    ToolCall(
                        id="call_1",
                        name="post_journal_entry",
                        arguments={"account": "cash", "amount": 100},
                    ),
                ],
            ),
            LLMResponse(content="Journal posted."),
        ]
    )
    loop = ReActLoop(provider=provider, tools=ToolRegistry([post_journal_entry]))
    result = await loop.arun([Message(role=MessageRole.USER, content="post entry")])
    assert "Journal posted." in result.output
    assert len(result.steps) == 1
    assert result.steps[0].tool_results[0].content == "posted 100 to cash"


@pytest.mark.asyncio
async def test_approval_hook_can_reject_tool() -> None:
    def reject_payments(request: ApprovalRequest) -> ApprovalResponse:
        if request.tool_call.name == "post_journal_entry":
            return ApprovalResponse(decision=ApprovalDecision.REJECT, reason="needs CFO sign-off")
        return ApprovalResponse(decision=ApprovalDecision.APPROVE)

    provider = MockProvider(
        responses=[
            LLMResponse(
                content="Posting",
                tool_calls=[
                    ToolCall(
                        id="call_1",
                        name="post_journal_entry",
                        arguments={"account": "cash", "amount": 100},
                    ),
                ],
            )
        ]
    )
    loop = ReActLoop(
        provider=provider,
        tools=ToolRegistry([post_journal_entry]),
        approval_hook=reject_payments,
    )
    result = await loop.arun([Message(role=MessageRole.USER, content="post entry")])
    assert result.stop_reason == StopReason.APPROVAL_DENIED
    assert "CFO" in result.output


@pytest.mark.asyncio
async def test_plan_execute_runs_multiple_steps() -> None:
    provider = MockProvider(
        responses=[
            LLMResponse(content='["Fetch balances", "Match transactions", "Prepare report"]'),
            LLMResponse(content="Balances fetched."),
            LLMResponse(content="Transactions matched."),
            LLMResponse(content="Report ready."),
        ]
    )
    loop = PlanExecuteLoop(provider=provider, tools=ToolRegistry())
    result = await loop.arun("month-end close")
    assert result.output == "Report ready."
    assert result.metadata["plan"] == ["Fetch balances", "Match transactions", "Prepare report"]


@pytest.mark.asyncio
async def test_agent_uses_long_term_memory() -> None:
    provider = MockProvider(responses=[LLMResponse(content="Using client context.")])
    agent = Agent(provider=provider, config=AgentConfig(mode=AgentMode.REACT))
    agent.remember("client:acme", "prefers INR reporting and T+1 settlement")
    result = await agent.arun("prepare settlement summary for Acme")
    assert any("client:acme" in message.content for message in result.messages)
