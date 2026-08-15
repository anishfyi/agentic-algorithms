"""Tool definitions and registry."""

from __future__ import annotations

import inspect
import json
from collections.abc import Awaitable, Callable
from typing import Any, ParamSpec, TypeVar, get_type_hints

from pydantic import BaseModel, Field

from agentic_algorithms.types import ToolCall, ToolResult

P = ParamSpec("P")
R = TypeVar("R")

ToolHandler = Callable[..., Any | Awaitable[Any]]


class Tool(BaseModel):
    name: str
    description: str
    parameters: dict[str, Any] = Field(default_factory=dict)
    handler: ToolHandler = Field(exclude=True)

    model_config = {"arbitrary_types_allowed": True}

    def tool_schema(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
        }

    async def execute(self, call: ToolCall) -> ToolResult:
        try:
            if inspect.iscoroutinefunction(self.handler):
                output = await self.handler(**call.arguments)
            else:
                output = self.handler(**call.arguments)
            content = output if isinstance(output, str) else json.dumps(output, default=str)
            return ToolResult(tool_call_id=call.id, name=self.name, content=content)
        except Exception as exc:
            return ToolResult(
                tool_call_id=call.id,
                name=self.name,
                content=str(exc),
                is_error=True,
            )


class ToolRegistry:
    def __init__(self, tools: list[Tool] | None = None) -> None:
        self._tools: dict[str, Tool] = {}
        for item in tools or []:
            self.register(item)

    def register(self, tool: Tool) -> None:
        if tool.name in self._tools:
            msg = f"Tool already registered: {tool.name}"
            raise ValueError(msg)
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool | None:
        return self._tools.get(name)

    def schemas(self) -> list[dict[str, Any]]:
        return [tool.tool_schema() for tool in self._tools.values()]

    def names(self) -> list[str]:
        return list(self._tools.keys())

    async def execute(self, call: ToolCall) -> ToolResult:
        tool = self.get(call.name)
        if tool is None:
            return ToolResult(
                tool_call_id=call.id,
                name=call.name,
                content=f"Unknown tool: {call.name}",
                is_error=True,
            )
        return await tool.execute(call)


def _annotation_to_json_type(annotation: Any) -> str:
    if annotation in (str, inspect.Parameter.empty):
        return "string"
    if annotation is int:
        return "integer"
    if annotation is float:
        return "number"
    if annotation is bool:
        return "boolean"
    return "string"


def tool(
    *,
    name: str | None = None,
    description: str | None = None,
) -> Callable[[ToolHandler], Tool]:
    def decorator(func: ToolHandler) -> Tool:
        tool_name = name or func.__name__
        tool_description = description or (func.__doc__ or "").strip() or tool_name
        hints = get_type_hints(func)
        properties: dict[str, Any] = {}
        required: list[str] = []
        signature = inspect.signature(func)
        for param_name, param in signature.parameters.items():
            if param_name in {"self", "cls"}:
                continue
            properties[param_name] = {
                "type": _annotation_to_json_type(hints.get(param_name, str)),
                "description": param_name.replace("_", " "),
            }
            if param.default is inspect.Parameter.empty:
                required.append(param_name)
        parameters = {
            "type": "object",
            "properties": properties,
            "required": required,
        }
        return Tool(
            name=tool_name,
            description=tool_description,
            parameters=parameters,
            handler=func,
        )

    return decorator
