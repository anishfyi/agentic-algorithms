"""Multi-agent orchestration patterns."""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable, Sequence
from dataclasses import dataclass

from agentic_algorithms.llm.base import LLMProvider
from agentic_algorithms.types import AgentResult, Message, MessageRole


@dataclass
class FanOut:
    """Run the same task across multiple workers in parallel."""

    async def arun(
        self,
        workers: Sequence[Callable[[], Awaitable[AgentResult]]],
    ) -> list[AgentResult]:
        return list(await asyncio.gather(*[worker() for worker in workers]))

    def run(self, workers: Sequence[Callable[[], AgentResult]]) -> list[AgentResult]:
        async def _run_all() -> list[AgentResult]:
            async def _wrap(sync_worker: Callable[[], AgentResult]) -> AgentResult:
                return sync_worker()

            return list(await asyncio.gather(*[_wrap(worker) for worker in workers]))

        return asyncio.run(_run_all())


@dataclass
class Judge:
    """Pick the best candidate answer with an LLM judge."""

    provider: LLMProvider
    criteria: str = "Correctness, safety, and completeness for a fintech workflow."

    async def arun(self, task: str, candidates: Sequence[AgentResult]) -> AgentResult:
        if not candidates:
            msg = "Judge requires at least one candidate"
            raise ValueError(msg)
        if len(candidates) == 1:
            return candidates[0]

        options = []
        for index, candidate in enumerate(candidates, start=1):
            options.append(f"Option {index}:\n{candidate.output}")
        prompt = (
            f"Task:\n{task}\n\n"
            f"Criteria:\n{self.criteria}\n\n"
            + "\n\n".join(options)
            + "\n\nReply with only the winning option number."
        )
        response = await self.provider.complete(
            [Message(role=MessageRole.USER, content=prompt)],
            temperature=0.0,
        )
        winner = _parse_winner(response.content, len(candidates))
        chosen = candidates[winner - 1]
        chosen.metadata["judge_winner_index"] = winner
        chosen.metadata["judge_rationale"] = response.content
        return chosen

    def run(self, task: str, candidates: Sequence[AgentResult]) -> AgentResult:
        return asyncio.run(self.arun(task, candidates))


@dataclass
class Orchestrator:
    """Route a task to the best specialist agent."""

    provider: LLMProvider
    specialists: dict[str, Callable[[str], Awaitable[AgentResult]]]

    async def arun(self, task: str) -> AgentResult:
        route = await self._route(task)
        handler = self.specialists.get(route)
        if handler is None:
            msg = f"No specialist registered for route: {route}"
            raise KeyError(msg)
        result = await handler(task)
        result.metadata["route"] = route
        return result

    def run(self, task: str) -> AgentResult:
        return asyncio.run(self.arun(task))

    async def _route(self, task: str) -> str:
        options = ", ".join(self.specialists)
        prompt = (
            "Choose the best specialist for the task.\n"
            f"Specialists: {options}\n"
            f"Task: {task}\n"
            "Reply with only the specialist name."
        )
        response = await self.provider.complete(
            [Message(role=MessageRole.USER, content=prompt)],
            temperature=0.0,
        )
        choice = response.content.strip().lower()
        for name in self.specialists:
            if name.lower() in choice:
                return name
        return next(iter(self.specialists))


def _parse_winner(content: str, total: int) -> int:
    for token in content.replace(".", " ").split():
        if token.isdigit():
            value = int(token)
            if 1 <= value <= total:
                return value
    return 1
