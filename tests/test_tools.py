"""Tests for core types and tools."""

from __future__ import annotations

import pytest

from agentic_algorithms.tools import Tool, ToolRegistry, tool
from agentic_algorithms.types import ToolCall


@tool(description="Look up an account balance")
def get_balance(account_id: str) -> str:
    return f"balance:{account_id}:1000"


def test_tool_decorator_builds_schema() -> None:
    assert get_balance.name == "get_balance"
    assert "account_id" in get_balance.parameters["properties"]


@pytest.mark.asyncio
async def test_tool_registry_executes_handler() -> None:
    registry = ToolRegistry([get_balance])
    result = await registry.execute(
        ToolCall(id="1", name="get_balance", arguments={"account_id": "acct_123"})
    )
    assert result.content == "balance:acct_123:1000"
    assert not result.is_error


@pytest.mark.asyncio
async def test_unknown_tool_returns_error() -> None:
    registry = ToolRegistry()
    result = await registry.execute(ToolCall(id="1", name="missing", arguments={}))
    assert result.is_error


@pytest.mark.asyncio
async def test_async_tool_handler() -> None:
    async def fetch_rate(pair: str) -> str:
        return f"rate:{pair}:83.12"

    registry = ToolRegistry(
        [
            Tool(
                name="fetch_rate",
                description="Fetch FX rate",
                parameters={
                    "type": "object",
                    "properties": {"pair": {"type": "string"}},
                    "required": ["pair"],
                },
                handler=fetch_rate,
            )
        ]
    )
    result = await registry.execute(
        ToolCall(id="1", name="fetch_rate", arguments={"pair": "USDINR"})
    )
    assert result.content == "rate:USDINR:83.12"
