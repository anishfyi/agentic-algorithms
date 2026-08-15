"""LLM helper algorithms: prompts, context, parsing, RAG, routing."""

from agentic_algorithms.llm_helpers.context import (
    prune_messages_by_token_budget,
    sliding_window_messages,
)
from agentic_algorithms.llm_helpers.loops import reflexion_critique_prompt, self_consistency_vote
from agentic_algorithms.llm_helpers.parsing import (
    extract_json_block,
    parse_structured_output,
    repair_json,
)
from agentic_algorithms.llm_helpers.prompts import (
    chain_of_thought_wrap,
    few_shot_prompt,
    reflexion_retry_prompt,
    system_prompt_compose,
)
from agentic_algorithms.llm_helpers.rag import chunk_text, pack_rag_context
from agentic_algorithms.llm_helpers.routing import route_model_by_complexity
from agentic_algorithms.llm_helpers.tokens import estimate_cost_usd, estimate_tokens

__all__ = [
    "chain_of_thought_wrap",
    "chunk_text",
    "estimate_cost_usd",
    "estimate_tokens",
    "extract_json_block",
    "few_shot_prompt",
    "pack_rag_context",
    "parse_structured_output",
    "prune_messages_by_token_budget",
    "reflexion_critique_prompt",
    "reflexion_retry_prompt",
    "repair_json",
    "route_model_by_complexity",
    "self_consistency_vote",
    "sliding_window_messages",
    "system_prompt_compose",
]
