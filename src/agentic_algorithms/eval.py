"""Built-in evaluation harness for agent workflows."""

from __future__ import annotations

import asyncio
import re
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel, Field

from agentic_algorithms.llm.base import LLMProvider
from agentic_algorithms.types import AgentResult, Message, MessageRole


class EvalCase(BaseModel):
    name: str
    input: str
    expected_contains: list[str] = Field(default_factory=list)
    expected_not_contains: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class EvalSuite(BaseModel):
    name: str
    cases: list[EvalCase] = Field(default_factory=list)


class EvalResult(BaseModel):
    case: EvalCase
    passed: bool
    output: str
    failures: list[str] = Field(default_factory=list)
    agent_result: AgentResult | None = None


@dataclass
class EvalHarness:
    runner: Callable[[str], Awaitable[AgentResult]]
    judge: LLMProvider | None = None
    use_llm_judge: bool = False

    async def arun_suite(self, suite: EvalSuite) -> list[EvalResult]:
        results: list[EvalResult] = []
        for case in suite.cases:
            results.append(await self.arun_case(case))
        return results

    def run_suite(self, suite: EvalSuite) -> list[EvalResult]:
        return asyncio.run(self.arun_suite(suite))

    async def arun_case(self, case: EvalCase) -> EvalResult:
        agent_result = await self.runner(case.input)
        failures = _rule_failures(case, agent_result.output)
        if self.use_llm_judge and self.judge is not None and not failures:
            llm_passed, reason = await _llm_judge(self.judge, case, agent_result.output)
            if not llm_passed:
                failures.append(reason or "LLM judge rejected the answer")
        return EvalResult(
            case=case,
            passed=not failures,
            output=agent_result.output,
            failures=failures,
            agent_result=agent_result,
        )

    def run_case(self, case: EvalCase) -> EvalResult:
        return asyncio.run(self.arun_case(case))


def _rule_failures(case: EvalCase, output: str) -> list[str]:
    failures: list[str] = []
    normalized = output.lower()
    for needle in case.expected_contains:
        if needle.lower() not in normalized:
            failures.append(f"missing expected text: {needle}")
    for needle in case.expected_not_contains:
        if needle.lower() in normalized:
            failures.append(f"forbidden text present: {needle}")
    return failures


async def _llm_judge(provider: LLMProvider, case: EvalCase, output: str) -> tuple[bool, str | None]:
    prompt = (
        "Grade the agent answer for a fintech workflow.\n"
        f"Task: {case.input}\n"
        f"Answer: {output}\n"
        "Reply PASS or FAIL on the first line, then one sentence of rationale."
    )
    response = await provider.complete([Message(role=MessageRole.USER, content=prompt)])
    first_line = response.content.strip().splitlines()[0] if response.content else "FAIL"
    passed = bool(re.search(r"\bpass\b", first_line, flags=re.IGNORECASE))
    return passed, response.content
