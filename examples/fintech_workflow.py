"""Fintech-oriented offline example using MockProvider."""

from __future__ import annotations

import asyncio

from agentic_algorithms import (
    Agent,
    AgentConfig,
    ApprovalDecision,
    ApprovalRequest,
    EvalCase,
    EvalHarness,
    EvalSuite,
    FanOut,
    Judge,
    MockProvider,
    ToolRegistry,
    tool,
)
from agentic_algorithms.human import ApprovalResponse
from agentic_algorithms.llm.base import LLMResponse
from agentic_algorithms.types import AgentResult, ToolCall


@tool(description="Fetch account balance in minor units")
def get_balance(account_id: str) -> str:
    balances = {"cash": 250000, "payables": 120000}
    return str(balances.get(account_id, 0))


@tool(description="Post a journal entry after approval")
def post_journal_entry(account: str, amount: int, memo: str) -> str:
    return f"posted {amount} to {account} ({memo})"


def approval_hook(request: ApprovalRequest) -> ApprovalResponse:
    if request.tool_call.name == "post_journal_entry":
        amount = int(request.tool_call.arguments.get("amount", 0))
        if amount > 100000:
            return ApprovalResponse(
                decision=ApprovalDecision.REJECT,
                reason="amount exceeds auto-approval threshold",
            )
    return ApprovalResponse(decision=ApprovalDecision.APPROVE)


async def build_agent() -> Agent:
    provider = MockProvider(
        responses=[
            LLMResponse(
                content="Fetching cash balance before posting.",
                tool_calls=[
                    ToolCall(
                        id="call_1",
                        name="get_balance",
                        arguments={"account_id": "cash"},
                    )
                ],
            ),
            LLMResponse(
                content="Posting accrual.",
                tool_calls=[
                    ToolCall(
                        id="call_2",
                        name="post_journal_entry",
                        arguments={
                            "account": "payables",
                            "amount": 50000,
                            "memo": "vendor accrual",
                        },
                    )
                ],
            ),
            LLMResponse(content="Accrual posted and verified."),
        ]
    )
    registry = ToolRegistry([get_balance, post_journal_entry])
    return Agent(
        provider=provider,
        tools=registry,
        config=AgentConfig(approval_hook=approval_hook),
    )


async def main() -> None:
    agent = await build_agent()
    agent.remember("policy:auto_approval_limit", "50000 minor units for journal entries")
    result = await agent.arun("Accrue vendor invoice for March utilities")
    print(result.output)

    async def worker_a() -> AgentResult:
        return AgentResult(output="matched 42 transactions", messages=[])

    async def worker_b() -> AgentResult:
        return AgentResult(output="matched 40 transactions with 2 exceptions", messages=[])

    fanout = FanOut()
    candidates = await fanout.arun([worker_a, worker_b])
    judge = Judge(provider=MockProvider(responses=[LLMResponse(content="Option 2")]))
    winner = await judge.arun("choose reconciliation result", candidates)
    print(winner.output)

    async def eval_runner(prompt: str) -> AgentResult:
        eval_agent = await build_agent()
        return await eval_agent.arun(prompt)

    harness = EvalHarness(runner=eval_runner)
    suite = EvalSuite(
        name="fintech-smoke",
        cases=[
            EvalCase(
                name="accrual completes",
                input="Accrue vendor invoice for March utilities",
                expected_contains=["Accrual posted"],
            )
        ],
    )
    eval_results = await harness.arun_suite(suite)
    print("eval passed:", all(result.passed for result in eval_results))


if __name__ == "__main__":
    asyncio.run(main())
