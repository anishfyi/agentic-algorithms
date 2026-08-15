"""Tests for psychology engineering algorithms."""

from agentic_algorithms.psychology import (
    agent_trust_score,
    bias_mitigation_prompt,
    cialdini_principle_score,
    detect_overconfidence_markers,
    ethical_persuasion_check,
    gain_frame,
    loss_aversion_frame,
    progressive_disclosure_plan,
    readability_score,
    sdt_tone_score,
)


def test_bias_detection_and_mitigation() -> None:
    text = "This is definitely guaranteed to always work."
    assert detect_overconfidence_markers(text)
    prompt = bias_mitigation_prompt(["pattern"])
    assert "uncertainty" in prompt.lower()


def test_framing() -> None:
    assert "risk" in loss_aversion_frame("backup", "data loss").lower()
    assert "can" in gain_frame("enable alerts", "catch issues early").lower()


def test_persuasion_ethics() -> None:
    scores = cialdini_principle_score("Limited time offer expires today")
    assert scores["scarcity"] > 0
    issues = ethical_persuasion_check("guaranteed returns", domain="fintech")
    assert issues


def test_trust_and_sdt() -> None:
    response = "I'm not sure, but based on the ledger, you can review next step."
    assert agent_trust_score(response) > 0
    tone = sdt_tone_score("You can choose optional steps. Here's how. We're here to help.")
    assert tone["autonomy"] > 0


def test_cognitive_load() -> None:
    assert readability_score("Short sentence. Clear words.") > 0.5
    batches = progressive_disclosure_plan(["a", "b", "c", "d", "e"], batch_size=2)
    assert len(batches) == 3
