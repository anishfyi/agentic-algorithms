"""Algorithms and patterns for building agentic systems."""

from agentic_algorithms.agent import Agent, AgentConfig
from agentic_algorithms.domains import (
    SearchIndex,
    aeo_page_score,
    atp_available,
    bm25_score,
    haversine_km,
    newsvendor_quantity,
    post_journal_entry,
    thompson_sampling_select,
    validate_journal_entry,
)
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
    "SearchIndex",
    "ShortTermMemory",
    "StopReason",
    "Tool",
    "ToolApprovalHook",
    "ToolCall",
    "ToolRegistry",
    "ToolResult",
    "aeo_page_score",
    "atp_available",
    "bm25_score",
    "haversine_km",
    "newsvendor_quantity",
    "post_journal_entry",
    "thompson_sampling_select",
    "tool",
    "validate_journal_entry",
]

__version__ = "0.1.0"
