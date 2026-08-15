"""Tests for multi-agent and evaluation modules."""

from __future__ import annotations

import pytest

from agentic_algorithms.eval import EvalCase, EvalHarness, EvalSuite
from agentic_algorithms.llm.base import LLMResponse, MockProvider
from agentic_algorithms.multi import FanOut, Judge, Orchestrator
from agentic_algorithms.types import AgentResult, StopReason


async def _candidate(output: str) -> AgentResult:
    return AgentResult(output=output, messages=[])


@pytest.mark.asyncio
async def test_fanout_runs_workers_in_parallel() -> None:
    fanout = FanOut()
    results = await fanout.arun(
        [
            lambda: _candidate("worker-a"),
            lambda: _candidate("worker-b"),
        ]
    )
    assert {result.output for result in results} == {"worker-a", "worker-b"}


@pytest.mark.asyncio
async def test_judge_picks_winner() -> None:
    provider = MockProvider(responses=[LLMResponse(content="Option 2")])
    judge = Judge(provider=provider)
    candidates = [
        AgentResult(output="unsafe transfer", messages=[]),
        AgentResult(output="verified transfer with approval trail", messages=[]),
    ]
    winner = await judge.arun("approve payout", candidates)
    assert winner.output.startswith("verified")


@pytest.mark.asyncio
async def test_orchestrator_routes_to_specialist() -> None:
    provider = MockProvider(responses=[LLMResponse(content="ledger")])
    orchestrator = Orchestrator(
        provider=provider,
        specialists={
            "ledger": lambda task: _candidate(f"ledger handled {task}"),
            "treasury": lambda task: _candidate(f"treasury handled {task}"),
        },
    )
    result = await orchestrator.arun("reconcile GL accounts")
    assert result.metadata["route"] == "ledger"
    assert "ledger handled" in result.output


@pytest.mark.asyncio
async def test_eval_harness_checks_expected_output() -> None:
    async def runner(prompt: str) -> AgentResult:
        return AgentResult(output=f"answer for {prompt}", messages=[])

    harness = EvalHarness(runner=runner)
    suite = EvalSuite(
        name="fintech-smoke",
        cases=[
            EvalCase(
                name="mentions prompt",
                input="close books",
                expected_contains=["answer for close books"],
            )
        ],
    )
    results = await harness.arun_suite(suite)
    assert results[0].passed


@pytest.mark.asyncio
async def test_eval_harness_fails_on_forbidden_text() -> None:
    async def runner(_: str) -> AgentResult:
        return AgentResult(output="transfer completed without approval", messages=[])

    harness = EvalHarness(runner=runner)
    result = await harness.arun_case(
        EvalCase(
            name="no unapproved transfer",
            input="send payout",
            expected_not_contains=["without approval"],
        )
    )
    assert not result.passed
    assert result.agent_result is not None
    assert result.agent_result.stop_reason == StopReason.COMPLETE
