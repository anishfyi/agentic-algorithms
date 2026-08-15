"""Additional tests for sync paths and edge cases."""

from __future__ import annotations

import pytest

from agentic_algorithms.agent import Agent, AgentConfig
from agentic_algorithms.eval import EvalCase, EvalHarness, EvalSuite
from agentic_algorithms.llm.base import LLMResponse, MockProvider
from agentic_algorithms.loops.plan_execute import PlanExecuteLoop, _parse_plan
from agentic_algorithms.loops.react import ReActLoop
from agentic_algorithms.multi import FanOut, Judge, Orchestrator
from agentic_algorithms.tools import ToolRegistry
from agentic_algorithms.types import AgentResult, Message, MessageRole


def test_agent_sync_run() -> None:
    agent = Agent(provider=MockProvider(responses=[LLMResponse(content="sync ok")]))
    result = agent.run("close books")
    assert result.output == "sync ok"


def test_plan_execute_sync_run() -> None:
    provider = MockProvider(
        responses=[
            LLMResponse(content='["Step one", "Step two"]'),
            LLMResponse(content="done one"),
            LLMResponse(content="done two"),
        ]
    )
    loop = PlanExecuteLoop(provider=provider, tools=ToolRegistry())
    result = loop.run("quarter close")
    assert result.output == "done two"


def test_parse_plan_fallback_to_lines() -> None:
    plan = _parse_plan("1. Fetch balances\n2. Post accruals")
    assert plan == ["1. Fetch balances", "2. Post accruals"]


def test_fanout_sync_run() -> None:
    fanout = FanOut()
    results = fanout.run([lambda: AgentResult(output="a", messages=[])])
    assert results[0].output == "a"


def test_judge_sync_run() -> None:
    judge = Judge(provider=MockProvider(responses=[LLMResponse(content="1")]))
    winner = judge.run("pick", [AgentResult(output="only", messages=[])])
    assert winner.output == "only"


def test_orchestrator_sync_run() -> None:
    async def treasury_handler(task: str) -> AgentResult:
        return AgentResult(output=task, messages=[])

    orchestrator = Orchestrator(
        provider=MockProvider(responses=[LLMResponse(content="treasury")]),
        specialists={"treasury": treasury_handler},
    )
    result = orchestrator.run("fx hedge")
    assert result.output == "fx hedge"


@pytest.mark.asyncio
async def test_eval_llm_judge_path() -> None:
    async def runner(_: str) -> AgentResult:
        return AgentResult(output="verified payout with approval trail", messages=[])

    harness = EvalHarness(
        runner=runner,
        judge=MockProvider(responses=[LLMResponse(content="PASS looks safe")]),
        use_llm_judge=True,
    )
    result = await harness.arun_case(
        EvalCase(name="safe payout", input="send vendor payment", expected_contains=["verified"])
    )
    assert result.passed


def test_eval_harness_sync_helpers() -> None:
    async def runner(prompt: str) -> AgentResult:
        return AgentResult(output=prompt, messages=[])

    harness = EvalHarness(runner=runner)
    suite = harness.run_suite(
        EvalSuite(
            name="sync",
            cases=[EvalCase(name="echo", input="ping", expected_contains=["ping"])],
        )
    )
    assert suite[0].passed
    assert harness.run_case(EvalCase(name="echo", input="pong", expected_contains=["pong"])).passed


def test_react_sync_run() -> None:
    loop = ReActLoop(
        provider=MockProvider(responses=[LLMResponse(content="ok")]),
        tools=ToolRegistry(),
    )
    result = loop.run([Message(role=MessageRole.USER, content="ping")])
    assert result.output == "ok"


def test_agent_plan_execute_mode() -> None:
    provider = MockProvider(
        responses=[
            LLMResponse(content='["Review invoices"]'),
            LLMResponse(content="reviewed"),
        ]
    )
    agent = Agent(
        provider=provider,
        config=AgentConfig(mode="plan_execute"),
    )
    result = agent.run("month-end")
    assert result.output == "reviewed"
