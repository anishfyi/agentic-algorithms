"""LLM + psychology engineering example for agent builders."""

from __future__ import annotations

from agentic_algorithms import Agent, AgentConfig, MockProvider, tool
from agentic_algorithms.llm_helpers import (
    chain_of_thought_wrap,
    pack_rag_context,
    prune_messages_by_token_budget,
    system_prompt_compose,
)
from agentic_algorithms.psychology import (
    agent_trust_score,
    bias_mitigation_prompt,
    detect_overconfidence_markers,
    ethical_persuasion_check,
    neutral_frame,
)
from agentic_algorithms.types import Message, MessageRole


@tool(description="Summarize policy text for an employee")
def summarize_policy(section: str) -> str:
    return f"Policy section {section}: submit expenses within 30 days with receipts."


def build_system_prompt() -> str:
    base = system_prompt_compose(
        "You are a helpful expense policy assistant for a fintech company.",
        [
            "Use neutral framing for financial decisions.",
            "State uncertainty when policy is ambiguous.",
            "Never promise guaranteed outcomes.",
        ],
        output_format="Short answer, then one suggested next step.",
    )
    guardrails = bias_mitigation_prompt(["overconfidence"])
    return f"{base}\n\n{guardrails}"


def main() -> None:
    rag = pack_rag_context(
        "expense deadline",
        [("Employees must submit expenses within 30 days.", 0.95)],
    )
    user_task = chain_of_thought_wrap(
        f"Using this context:\n{rag}\n\nCan I submit last month's receipt?"
    )

    # Psychology pre-check on outbound copy template
    draft = neutral_frame("submit the receipt", "deadline is 30 days from transaction date")
    assert not ethical_persuasion_check(draft, domain="expense")

    agent = Agent(
        provider=MockProvider(),
        config=AgentConfig(system_prompt=build_system_prompt()),
    )
    agent.add_tool(summarize_policy)

    messages = [
        Message(role=MessageRole.SYSTEM, content=build_system_prompt()),
        Message(role=MessageRole.USER, content=user_task),
    ]
    pruned = prune_messages_by_token_budget(messages, max_tokens=2000)
    result = agent.run(pruned[-1].content)

    overconfidence = detect_overconfidence_markers(result.output)
    trust = agent_trust_score(result.output)
    print(result.output)
    print("overconfidence markers:", overconfidence)
    print("trust score:", round(trust, 2))


if __name__ == "__main__":
    main()
