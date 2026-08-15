"""Algorithms and patterns for building agentic systems."""

from agentic_algorithms.agent import Agent, AgentConfig
from agentic_algorithms.eval import EvalCase, EvalHarness, EvalResult, EvalSuite
from agentic_algorithms.human import ApprovalDecision, ApprovalRequest, ToolApprovalHook
from agentic_algorithms.llm import AnthropicProvider, MockProvider, OpenAIProvider
from agentic_algorithms.loops import PlanExecuteLoop, ReActLoop
from agentic_algorithms.memory import LongTermMemory, MemoryStore, ShortTermMemory
from agentic_algorithms.multi import FanOut, Judge, Orchestrator
from agentic_algorithms.tools import Tool, ToolRegistry, tool
from agentic_algorithms.types import (
    AgentResult,
    AgentStep,
    Message,
    MessageRole,
    StopReason,
    ToolCall,
    ToolResult,
)

__all__ = [
    "Agent",
    "AgentConfig",
    "AgentResult",
    "AgentStep",
    "AnthropicProvider",
    "ApprovalDecision",
    "ApprovalRequest",
    "EvalCase",
    "EvalHarness",
    "EvalResult",
    "EvalSuite",
    "FanOut",
    "Judge",
    "LongTermMemory",
    "MemoryStore",
    "Message",
    "MessageRole",
    "MockProvider",
    "OpenAIProvider",
    "Orchestrator",
    "PlanExecuteLoop",
    "ReActLoop",
    "ShortTermMemory",
    "StopReason",
    "Tool",
    "ToolApprovalHook",
    "ToolCall",
    "ToolRegistry",
    "ToolResult",
    "tool",
]

__version__ = "0.1.0"
