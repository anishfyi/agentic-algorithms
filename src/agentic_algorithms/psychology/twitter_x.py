"""X (Twitter) growth and engagement psychology."""

from __future__ import annotations

import re
from collections.abc import Sequence

_HOOK_PATTERNS = [
    (r"^\d+\s", 0.15),
    (r"\b(how to|why|thread|mistake|secret|nobody)\b", 0.2),
    (r"\?$", 0.1),
    (r"\b(i |we |my )", 0.05),
    (r"[!:]", 0.05),
]


def hook_strength_score(text: str) -> float:
    """Score X post hook strength for scroll-stop. Time O(n)."""
    head = text.strip().split("\n", 1)[0][:280]
    if not head:
        return 0.0
    score = min(1.0, len(head) / 120.0 * 0.25)
    for pattern, weight in _HOOK_PATTERNS:
        if re.search(pattern, head, re.I):
            score += weight
    return min(1.0, score)


def thread_opener_variants(claim: str, *, count: int = 3) -> list[str]:
    """Generate thread opener variants from a core claim. Time O(n)."""
    claim = claim.strip().rstrip(".")
    templates = [
        f"I studied {claim.lower()} for 30 days. Here is what actually works:",
        f"Most people get {claim.lower()} wrong. A short thread:",
        f"{claim}. Breakdown (save this):",
        f"Stop scrolling if {claim.lower()} matters to you.",
        f"Unpopular truth: {claim.lower()}.",
    ]
    return templates[: max(1, min(count, len(templates)))]


def quote_tweet_angle(original_summary: str, *, stance: str = "add_value") -> str:
    """Suggest quote-tweet framing angle. Time O(1)."""
    angles = {
        "add_value": f"Adding context: {original_summary} — here is the tactical takeaway.",
        "respectful_disagree": f"Counterpoint on '{original_summary}': nuance matters because...",
        "amplify": f"This is underrated. {original_summary} — more people should see this.",
        "story": f"This matches what I saw building in public: {original_summary}",
    }
    return angles.get(stance, angles["add_value"])


_BAIT = [r"^\s*(this|so true|facts|100%)\s*!?$", r"^\s*following\s*$", r"^\s*great post\s*!?$"]
_VALUE = [r"\bbecause\b", r"\btry\b", r"\bexample\b", r"\?"]


def reply_value_score(reply: str) -> float:
    """Score whether a reply adds value vs engagement bait. Time O(n)."""
    text = reply.strip()
    if not text:
        return 0.0
    if any(re.search(p, text, re.I) for p in _BAIT):
        return 0.1
    score = min(0.5, len(text) / 200.0)
    score += 0.15 * sum(1 for p in _VALUE if re.search(p, text, re.I))
    return min(1.0, score)


def x_engagement_score(text: str) -> dict[str, float]:
    """Estimate algorithm-friendly engagement signals in copy. Time O(n)."""
    t = text.lower()
    return {
        "conversation": min(1.0, 0.2 * len(re.findall(r"\?", text))),
        "save_worthy": 1.0 if re.search(r"\b(thread|checklist|framework|steps)\b", t) else 0.2,
        "reply_invite": 1.0 if re.search(r"\b(what do you think|agree\?|reply with)\b", t) else 0.0,
        "share_hook": 1.0 if re.search(r"\b(rt|repost|share)\b", t) else 0.1,
    }


def fomo_tweet_frame(offer: str, deadline: str, *, ethical: bool = True) -> str:
    """Ethical FOMO frame for time-bound offers on X. Time O(1)."""
    if ethical:
        return f"{offer} — closes {deadline}. No fake scarcity; link in bio if useful."
    return f"LAST CHANCE {offer}!!!"


def social_proof_tweet_line(metric: str, *, qualifier: str = "founders") -> str:
    """Social proof line for X without fabricated stats. Time O(1)."""
    return f"Used by {qualifier} who {metric} — sharing what we learned publicly."


def thread_cta_placement(tweet_count: int, cta: str) -> dict[int, str]:
    """Place CTAs across thread tweets. Time O(n)."""
    if tweet_count < 1:
        return {}
    positions = {1: "Hook only — no CTA yet."}
    if tweet_count >= 3:
        positions[max(2, tweet_count // 2)] = f"Mid-thread value reminder. Soft CTA: {cta}"
    positions[tweet_count] = f"Final tweet CTA: {cta}"
    return positions


def bio_link_cta(action: str, outcome: str) -> str:
    """Bio link CTA optimized for X traffic. Time O(1)."""
    return f"↓ {action} → {outcome}"


def dm_permission_opener(context: str, ask: str) -> str:
    """Permission-based cold DM opener for X. Time O(1)."""
    return (
        f"Saw your post on {context}. Open to a quick question about {ask}? "
        "Happy to share notes either way."
    )


_LOOP_SIGNALS = ["share", "tag", "invite", "refer", "remix", "template", "challenge"]


def viral_loop_score(copy: str) -> float:
    """Score creator viral loop completeness. Time O(n)."""
    t = copy.lower()
    hits = sum(1 for word in _LOOP_SIGNALS if word in t)
    return min(1.0, hits / 3.0)


_BAIT = [r"comment \w+ below", r"like if you agree", r"follow for follow", r"drop a \W"]


def engagement_bait_detector(text: str) -> list[str]:
    """Detect engagement bait patterns on X. Time O(n)."""
    return [p for p in _BAIT if re.search(p, text, re.I)]


def creator_flywheel_stage(followers: int, engagement_rate: float) -> str:
    """Map creator flywheel stage from metrics. Time O(1)."""
    if followers < 500:
        return "reply_guy_growth"
    if engagement_rate < 0.02:
        return "audience_quality_fix"
    return "productize_attention"


def thread_structure_outline(bullets: Sequence[str]) -> list[str]:
    """Outline thread structure from bullets. Time O(n)."""
    out = ["1/ Hook"]
    for i, b in enumerate(bullets, start=2):
        out.append(f"{i}/ {b}")
    out.append(f"{len(bullets) + 2}/ CTA + recap")
    return out


def tweet_readability_for_x(text: str) -> float:
    """Score tweet readability for X. Time O(n)."""
    words = text.split()
    if not words:
        return 0.0
    avg_len = sum(len(w) for w in words) / len(words)
    return max(0.0, 1.0 - max(0, avg_len - 5) * 0.1)
