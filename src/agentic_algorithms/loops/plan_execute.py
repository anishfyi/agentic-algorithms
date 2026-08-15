"""Plan-and-execute: decompose a goal into steps, then execute each step."""

from __future__ import annotations

import asyncio
import json
import re
from dataclasses import dataclass
from typing import Any

from agentic_algorithms.llm.base import LLMProvider
from agentic_algorithms.loops.react import ReActLoop
from agentic_algorithms.tools import ToolRegistry
from agentic_algorithms.types import AgentResult, AgentStep, Message, MessageRole, StopReason


@dataclass
class PlanExecuteLoop:
    provider: LLMProvider
    tools: ToolRegistry
    react: ReActLoop | None = None
    max_steps: int = 8
    temperature: float = 0.0

    def __post_init__(self) -> None:
        if self.react is None:
            self.react = ReActLoop(
                provider=self.provider,
                tools=self.tools,
                temperature=self.temperature,
            )

    async def arun(
        self,
        goal: str,
        *,
        context: list[Message] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> AgentResult:
        plan = await self._create_plan(goal, context=context or [])
        messages = list(context or [])
        messages.append(Message(role=MessageRole.USER, content=goal))
        combined_steps: list[AgentStep] = []
        outputs: list[str] = []

        react = self.react
        assert react is not None
        for index, step in enumerate(plan[: self.max_steps], start=1):
            step_prompt = (
                f"Execute plan step {index}/{len(plan)}.\n"
                f"Goal: {goal}\n"
                f"Step: {step}\n"
                f"Prior outputs:\n" + "\n".join(outputs[-3:])
            )
            step_messages = [
                *messages,
                Message(role=MessageRole.USER, content=step_prompt),
            ]
            result = await react.arun(step_messages, metadata={"plan_step": step})
            combined_steps.extend(result.steps)
            outputs.append(result.output)
            messages = result.messages

        final = outputs[-1] if outputs else ""
        return AgentResult(
            output=final,
            messages=messages,
            steps=combined_steps,
            stop_reason=StopReason.COMPLETE,
            metadata={**(metadata or {}), "plan": plan, "step_outputs": outputs},
        )

    def run(
        self,
        goal: str,
        *,
        context: list[Message] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> AgentResult:
        return asyncio.run(self.arun(goal, context=context, metadata=metadata))

    async def _create_plan(self, goal: str, *, context: list[Message]) -> list[str]:
        planner_messages = list(context)
        planner_messages.append(
            Message(
                role=MessageRole.SYSTEM,
                content=(
                    "You are a planning agent for regulated fintech workflows. "
                    "Return a JSON array of short, executable steps. "
                    "Prefer verification and approval checkpoints before money movement."
                ),
            )
        )
        planner_messages.append(
            Message(
                role=MessageRole.USER,
                content=f"Create a plan for:\n{goal}",
            )
        )
        response = await self.provider.complete(
            planner_messages,
            temperature=self.temperature,
        )
        return _parse_plan(response.content)


def _parse_plan(content: str) -> list[str]:
    fenced = re.search(r"```(?:json)?\s*(\[[\s\S]*?\])\s*```", content)
    candidate = fenced.group(1) if fenced else content.strip()
    try:
        parsed = json.loads(candidate)
        if isinstance(parsed, list):
            return [str(item) for item in parsed]
    except json.JSONDecodeError:
        pass
    lines = [line.strip("- ").strip() for line in content.splitlines() if line.strip()]
    return [line for line in lines if line]
