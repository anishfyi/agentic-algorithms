"""Prompt engineering helpers for LLM calls."""

from __future__ import annotations

from typing import Any


def few_shot_prompt(
    instruction: str,
    examples: list[tuple[str, str]],
    query: str,
) -> str:
    """Build a few-shot prompt. Time O(examples), space O(output)."""
    blocks = [instruction.strip(), ""]
    for user, assistant in examples:
        blocks.append(f"User: {user}")
        blocks.append(f"Assistant: {assistant}")
        blocks.append("")
    blocks.append(f"User: {query}")
    blocks.append("Assistant:")
    return "\n".join(blocks)


def chain_of_thought_wrap(task: str) -> str:
    """Wrap a task with explicit step-by-step reasoning instructions."""
    return (
        f"{task.strip()}\n\n"
        "Think step by step. Show your reasoning briefly, then give the final answer "
        "on a line starting with 'Answer:'."
    )


def system_prompt_compose(
    role: str,
    constraints: list[str],
    output_format: str | None = None,
) -> str:
    """Compose a structured system prompt from role + constraints."""
    lines = [role.strip(), "", "Constraints:"]
    lines.extend(f"- {item}" for item in constraints)
    if output_format:
        lines.extend(["", "Output format:", output_format.strip()])
    return "\n".join(lines)


def reflexion_retry_prompt(task: str, prior_answer: str, critique: str) -> str:
    """Reflexion-style retry prompt after verbal critique [Shinn2023]."""
    return (
        f"Task:\n{task}\n\n"
        f"Your prior answer:\n{prior_answer}\n\n"
        f"Critique:\n{critique}\n\n"
        "Revise your answer. Fix the critique. Keep what was correct."
    )


def tool_use_reminder(tools: list[str]) -> str:
    """Nudge the model toward explicit tool selection when appropriate."""
    tool_list = ", ".join(tools)
    return (
        "You may call tools when needed. Available tools: "
        f"{tool_list}. Prefer tools for factual lookups and calculations."
    )


def json_output_instruction(schema_hint: dict[str, Any]) -> str:
    """Instruction block for JSON-only structured output."""
    keys = ", ".join(schema_hint.keys())
    return f"Respond with valid JSON only. Required keys: {keys}. No markdown fences."
