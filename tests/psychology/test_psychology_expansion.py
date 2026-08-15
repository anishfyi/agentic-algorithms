"""Tests for expanded psychology algorithms (sales, marketing, X)."""

from __future__ import annotations

import pytest

from agentic_algorithms.psychology import (
    ad_claim_compliance_check,
    ad_hook_variants,
    audience_warmth_score,
    charm_price,
    cold_dm_opener,
    cta_clarity_score,
    discovery_gap_score,
    dm_spam_risk_score,
    engagement_bait_detector,
    feynman_gap_score,
    follower_quality_score,
    hook_strength_score,
    icp_fit_score,
    influencer_fit_score,
    k_factor_estimate,
    meddic_qualification_score,
    micro_lesson_chunks,
    newsletter_subject_score,
    objection_reframe,
    plg_activation_score,
    reply_value_score,
    spaced_repetition_interval_days,
    spin_question_builder,
    thread_opener_variants,
    thread_structure_outline,
    tweet_readability_for_x,
    value_prop_one_liner,
    viral_loop_score,
    x_engagement_score,
)


@pytest.mark.parametrize(
    "text,min_score",
    [
        ("7 mistakes killing your X growth:", 0.25),
        ("How to write hooks that stop the scroll?", 0.3),
    ],
)
def test_hook_strength_score(text: str, min_score: float) -> None:
    assert hook_strength_score(text) >= min_score


def test_thread_opener_variants() -> None:
    variants = thread_opener_variants("consistency beats virality")
    assert len(variants) >= 2
    assert all("consistency" in v.lower() for v in variants)


def test_reply_value_score() -> None:
    assert reply_value_score("great post!") < 0.2
    assert reply_value_score("Try batching hooks because Mon AM is noisy") > 0.3


def test_x_engagement_score() -> None:
    scores = x_engagement_score("Framework with 3 steps. What would you add?")
    assert scores["conversation"] > 0
    assert scores["save_worthy"] > 0


def test_engagement_bait_detector() -> None:
    hits = engagement_bait_detector("Comment YES below for follow back")
    assert hits


def test_sales_discovery() -> None:
    assert "?" in objection_reframe("too expensive")
    assert "handle" in spin_question_builder("situation", "pipeline").lower()
    assert discovery_gap_score("no budget info") > 0.5


def test_marketing_basics() -> None:
    assert "founders" in value_prop_one_liner("founders", "grow", "ship faster").lower()
    assert icp_fit_score("b2b saas founders", ["saas", "founders"]) == 1.0
    assert influencer_fit_score(["authentic", "builder"], "authentic builder") == 1.0


def test_learning_acceleration() -> None:
    assert spaced_repetition_interval_days(1) >= 1
    chunks = micro_lesson_chunks(["a", "b", "c", "d"], chunk_size=2)
    assert chunks == [["a", "b"], ["c", "d"]]
    assert feynman_gap_score("We use API and SSO without definitions") > 0


def test_conversion_and_dm() -> None:
    assert cta_clarity_score("Start your free trial today") > 0
    assert dm_spam_risk_score("guaranteed money click here") >= 0.5
    assert "Noticed" in cold_dm_opener("your thread on PLG", "activation")


def test_growth_metrics() -> None:
    assert k_factor_estimate(2.0, 0.25) == 0.5
    assert viral_loop_score("share this template and tag a friend") > 0.5
    assert audience_warmth_score(50, 30, 20) > 0
    assert follower_quality_score(5.0, 100) > 0


def test_b2b_and_saas() -> None:
    score = meddic_qualification_score({"metrics": True, "champion": True})
    assert 0 < score < 1
    plg = plg_activation_score({"signup": True, "core_action": True})
    assert plg == 0.4


def test_pricing_and_newsletter() -> None:
    assert charm_price(29) >= 29
    assert newsletter_subject_score("3 tactics to grow your newsletter this week") > 0.5


def test_thread_structure_outline() -> None:
    outline = thread_structure_outline(["problem", "fix"])
    assert outline[0].startswith("1/")
    assert any("CTA" in line for line in outline)


def test_tweet_readability_for_x() -> None:
    assert tweet_readability_for_x("Short clear words win on X") > 0.5


def test_ads_compliance() -> None:
    assert ad_claim_compliance_check("guaranteed results with no risk")
    assert len(ad_hook_variants("onboarding", count=2)) == 2
