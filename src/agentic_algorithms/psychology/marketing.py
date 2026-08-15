"""Marketing psychology."""

from __future__ import annotations

import re
from collections.abc import Sequence


def icp_fit_score(text: str, icp_keywords: Sequence[str]) -> float:
    """Score ideal customer profile fit from text. Time O(n)."""
    if not icp_keywords:
        return 0.0
    hits = sum(1 for k in icp_keywords if k.lower() in text.lower())
    return hits / len(icp_keywords)


def value_prop_one_liner(audience: str, outcome: str, differentiator: str) -> str:
    """Compress value prop into one line. Time O(1)."""
    return f"For {audience} who need {outcome}, we {differentiator}."


def positioning_statement(category: str, audience: str, benefit: str, proof: str) -> str:
    """Classic positioning statement template. Time O(1)."""
    return f"The {category} for {audience} that {benefit}, unlike alternatives because {proof}."


def competitor_diff_line(competitor: str, wedge: str) -> str:
    """Ethical competitor differentiation line. Time O(1)."""
    return (
        f"Compared to {competitor}, we optimize for {wedge} ,  best when that is your bottleneck."
    )


def persona_pain_hook(persona: str, pain: str) -> str:
    """Pain-led hook for a persona. Time O(1)."""
    return f"If you are a {persona} tired of {pain}, read this."


_CHANNEL = {
    "x": [r".{0,280}", r"\?"],
    "email": [r"\bdear\b", r"\bsubject\b"],
    "linkedin": [r"\bprofessional\b", r"\bcareer\b"],
}


def channel_message_fit(message: str, channel: str) -> float:
    """Score message fit for a marketing channel. Time O(n)."""
    patterns = _CHANNEL.get(channel.lower(), [])
    if not patterns:
        return 0.5
    return min(1.0, sum(1 for p in patterns if re.search(p, message, re.I)) / len(patterns))


def launch_sequence_plan(beat: str, channels: Sequence[str]) -> list[str]:
    """Simple launch email/post sequence. Time O(n)."""
    return [f"{ch}: {beat} ,  teaser" for ch in channels] + [
        f"{ch}: {beat} ,  launch" for ch in channels
    ]


_OVER = [r"\bguaranteed\b", r"\b#1\b", r"\bbest in the world\b", r"\bnever fail\b"]


def brand_promise_check(copy: str) -> list[str]:
    """Flag overpromising brand language. Time O(n)."""
    return [p for p in _OVER if re.search(p, copy, re.I)]


def newsletter_subject_score(subject: str) -> float:
    """Score newsletter subject line. Time O(n)."""
    score = 0.4 if 30 <= len(subject) <= 55 else 0.2
    if re.search(r"\b(you|your)\b", subject, re.I):
        score += 0.2
    if re.search(r"\d", subject):
        score += 0.15
    return min(1.0, score)


def newsletter_preview_text(hook: str) -> str:
    """Newsletter preview text line. Time O(1)."""
    return hook[:90]


def landing_social_proof_block(logos: Sequence[str], quote: str) -> str:
    """Social proof block for landing page. Time O(1)."""
    names = ", ".join(logos[:5])
    return f'Trusted by {names}\n"{quote}"'


def brand_voice_consistency_score(text: str, voice_keywords: Sequence[str]) -> float:
    """Score brand voice consistency. Time O(n)."""
    if not voice_keywords:
        return 0.0
    hits = sum(1 for k in voice_keywords if k.lower() in text.lower())
    return hits / len(voice_keywords)


def crisis_statement_frame(
    what_happened: str, what_we_are_doing: str, what_you_should_do: str
) -> str:
    """Crisis comms statement frame. Time O(1)."""
    return (
        f"What happened: {what_happened}\n"
        f"What we are doing: {what_we_are_doing}\n"
        f"What you should do: {what_you_should_do}"
    )


def influencer_fit_score(brand_values: Sequence[str], creator_bio: str) -> float:
    """Score influencer partnership fit. Time O(n)."""
    if not brand_values:
        return 0.0
    hits = sum(1 for v in brand_values if v.lower() in creator_bio.lower())
    return hits / len(brand_values)
