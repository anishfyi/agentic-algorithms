#!/usr/bin/env python3
"""Generate psychology expansion modules + catalog entries (sales/marketing/X)."""

from __future__ import annotations

import json
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PSY = ROOT / "src" / "agentic_algorithms" / "psychology"
CATALOG = ROOT / "catalogs" / "psychology_algorithms.json"

MODULE_HEADER = '''\
"""{title}."""

from __future__ import annotations

import math
import re
from typing import Sequence

'''

# Each spec: (name, category, time, space, doc, body, use_case, returns, example)
SPECS: dict[str, list[tuple]] = {}


def _add(module: str, category: str, items: list[tuple]) -> None:
    SPECS.setdefault(module, []).extend(
        (name, category, time, space, doc, body, use_case, ret, example)
        for name, time, space, doc, body, use_case, ret, example in items
    )


_add(
    "twitter_x",
    "twitter_x",
    [
        (
            "hook_strength_score",
            "O(n)",
            "O(1)",
            "Score X post hook strength for scroll-stop. Time O(n).",
            '''\
_HOOK_PATTERNS = [
    (r"^\\d+\\s", 0.15),
    (r"\\b(how to|why|thread|mistake|secret|nobody)\\b", 0.2),
    (r"\\?$", 0.1),
    (r"\\b(i |we |my )", 0.05),
    (r"[!:]", 0.05),
]

def hook_strength_score(text: str) -> float:
    """Score X post hook strength for scroll-stop. Time O(n)."""
    head = text.strip().split("\\n", 1)[0][:280]
    if not head:
        return 0.0
    score = min(1.0, len(head) / 120.0 * 0.25)
    for pattern, weight in _HOOK_PATTERNS:
        if re.search(pattern, head, re.I):
            score += weight
    return min(1.0, score)
''',
            "Pick the strongest opener before posting a thread.",
            "float 0-1",
            'hook_strength_score("7 mistakes killing your X growth:")',
        ),
        (
            "thread_opener_variants",
            "O(n)",
            "O(k)",
            "Generate thread opener variants from a core claim. Time O(n).",
            '''\
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
''',
            "A/B test thread first tweets without rewriting from scratch.",
            "list[str]",
            'thread_opener_variants("consistency beats virality on X")',
        ),
        (
            "quote_tweet_angle",
            "O(1)",
            "O(1)",
            "Suggest quote-tweet framing angle. Time O(1).",
            '''\
def quote_tweet_angle(original_summary: str, *, stance: str = "add_value") -> str:
    """Suggest quote-tweet framing angle. Time O(1)."""
    angles = {
        "add_value": f"Adding context: {original_summary} — here is the tactical takeaway.",
        "respectful_disagree": f"Counterpoint on '{original_summary}': nuance matters because...",
        "amplify": f"This is underrated. {original_summary} — more people should see this.",
        "story": f"This matches what I saw building in public: {original_summary}",
    }
    return angles.get(stance, angles["add_value"])
''',
            "Quote-tweet with intent instead of empty praise.",
            "str",
            'quote_tweet_angle("ship daily", stance="add_value")',
        ),
        (
            "reply_value_score",
            "O(n)",
            "O(1)",
            "Score whether a reply adds value vs engagement bait. Time O(n).",
            '''\
_BAIT = [r"^\\s*(this|so true|facts|100%)\\s*!?$", r"^\\s*following\\s*$", r"^\\s*great post\\s*!?$"]
_VALUE = [r"\\bbecause\\b", r"\\btry\\b", r"\\bexample\\b", r"\\?"]

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
''',
            "Filter low-effort replies before posting.",
            "float 0-1",
            'reply_value_score("Try batching hooks on Sunday because Mon AM is noisy")',
        ),
        (
            "x_engagement_score",
            "O(n)",
            "O(1)",
            "Estimate algorithm-friendly engagement signals in copy. Time O(n).",
            '''\
def x_engagement_score(text: str) -> dict[str, float]:
    """Estimate algorithm-friendly engagement signals in copy. Time O(n)."""
    t = text.lower()
    return {
        "conversation": min(1.0, 0.2 * len(re.findall(r"\\?", text))),
        "save_worthy": 1.0 if re.search(r"\\b(thread|checklist|framework|steps)\\b", t) else 0.2,
        "reply_invite": 1.0 if re.search(r"\\b(what do you think|agree\\?|reply with)\\b", t) else 0.0,
        "share_hook": 1.0 if re.search(r"\\b(rt|repost|share)\\b", t) else 0.1,
    }
''',
            "Tune posts for replies and saves, not vanity likes.",
            "dict[str, float]",
            'x_engagement_score("Framework: 3 steps. What would you add?")',
        ),
        (
            "fomo_tweet_frame",
            "O(1)",
            "O(1)",
            "Ethical FOMO frame for time-bound offers on X. Time O(1).",
            '''\
def fomo_tweet_frame(offer: str, deadline: str, *, ethical: bool = True) -> str:
    """Ethical FOMO frame for time-bound offers on X. Time O(1)."""
    if ethical:
        return f"{offer} — closes {deadline}. No fake scarcity; link in bio if useful."
    return f"LAST CHANCE {offer}!!!"
''',
            "Announce real deadlines without dark patterns.",
            "str",
            'fomo_tweet_frame("Office hours", "Friday 5pm ET")',
        ),
        (
            "social_proof_tweet_line",
            "O(1)",
            "O(1)",
            "Social proof line for X without fabricated stats. Time O(1).",
            '''\
def social_proof_tweet_line(metric: str, *, qualifier: str = "founders") -> str:
    """Social proof line for X without fabricated stats. Time O(1)."""
    return f"Used by {qualifier} who {metric} — sharing what we learned publicly."
''',
            "Cite real traction patterns on X.",
            "str",
            'social_proof_tweet_line("shipped weekly for 6 months")',
        ),
        (
            "thread_cta_placement",
            "O(n)",
            "O(n)",
            "Place CTAs across thread tweets. Time O(n).",
            '''\
def thread_cta_placement(tweet_count: int, cta: str) -> dict[int, str]:
    """Place CTAs across thread tweets. Time O(n)."""
    if tweet_count < 1:
        return {}
    positions = {1: "Hook only — no CTA yet."}
    if tweet_count >= 3:
        positions[max(2, tweet_count // 2)] = f"Mid-thread value reminder. Soft CTA: {cta}"
    positions[tweet_count] = f"Final tweet CTA: {cta}"
    return positions
''',
            "Structure long threads with one clear close.",
            "dict[int, str]",
            'thread_cta_placement(5, "DM me PLAYBOOK")',
        ),
        (
            "bio_link_cta",
            "O(1)",
            "O(1)",
            "Bio link CTA optimized for X traffic. Time O(1).",
            '''\
def bio_link_cta(action: str, outcome: str) -> str:
    """Bio link CTA optimized for X traffic. Time O(1)."""
    return f"↓ {action} → {outcome}"
''',
            "Convert profile visits from threads.",
            "str",
            'bio_link_cta("Free playbook", "learn sales psychology in 10 min/day")',
        ),
        (
            "dm_permission_opener",
            "O(1)",
            "O(1)",
            "Permission-based cold DM opener for X. Time O(1).",
            '''\
def dm_permission_opener(context: str, ask: str) -> str:
    """Permission-based cold DM opener for X. Time O(1)."""
    return f"Saw your post on {context}. Open to a quick question about {ask}? Happy to share notes either way."
''',
            "Start DMs without spammy pitches.",
            "str",
            'dm_permission_opener("PLG onboarding", "activation metrics")',
        ),
        (
            "viral_loop_score",
            "O(n)",
            "O(1)",
            "Score creator viral loop completeness. Time O(n).",
            '''\
_LOOP_SIGNALS = ["share", "tag", "invite", "refer", "remix", "template", "challenge"]

def viral_loop_score(copy: str) -> float:
    """Score creator viral loop completeness. Time O(n)."""
    t = copy.lower()
    hits = sum(1 for word in _LOOP_SIGNALS if word in t)
    return min(1.0, hits / 3.0)
''',
            "Design posts that invite redistribution.",
            "float 0-1",
            'viral_loop_score("Tag a founder who needs this template")',
        ),
    ],
)

# Additional modules via compact generator for remaining functions
def _score_patterns(text: str, patterns: list[str], cap: int = 3) -> float:
    return min(1.0, sum(1 for p in patterns if re.search(p, text, re.I)) / cap)


def _simple_module(
    module: str,
    title: str,
    category: str,
    funcs: list[dict],
) -> None:
    for f in funcs:
        SPECS.setdefault(module, []).append(
            (
                f["name"],
                category,
                f.get("time", "O(n)"),
                f.get("space", "O(1)"),
                f["doc"],
                f["body"],
                f.get("use_case", ""),
                f.get("returns", "Any"),
                f.get("example", f'{f["name"]}(...)'),
            )
        )


_simple_module(
    "sales",
    "Sales psychology helpers",
    "sales",
    [
        {
            "name": "objection_reframe",
            "doc": "Reframe a sales objection into a learning question. Time O(1).",
            "body": '''\
def objection_reframe(objection: str) -> str:
    """Reframe a sales objection into a learning question. Time O(1)."""
    return f"When you say '{objection}', what outcome would need to be true for this to be a yes?"
''',
            "use_case": "Turn stalls into discovery on calls.",
            "returns": "str",
            "example": 'objection_reframe("too expensive")',
        },
        {
            "name": "spin_question_builder",
            "doc": "Build SPIN-style discovery question. Time O(1).",
            "body": '''\
def spin_question_builder(stage: str, topic: str) -> str:
    """Build SPIN-style discovery question. Time O(1)."""
    templates = {
        "situation": f"Walk me through how you handle {topic} today.",
        "problem": f"What breaks most often with {topic}?",
        "implication": f"If {topic} stays unsolved, what does that cost you this quarter?",
        "need_payoff": f"If we fixed {topic}, what would your team do with the time back?",
    }
    return templates.get(stage.lower(), templates["situation"])
''',
            "use_case": "Structured discovery without a script doc.",
            "returns": "str",
        },
        {
            "name": "discovery_gap_score",
            "doc": "Score how much discovery is missing from notes. Time O(n).",
            "body": '''\
_GAPS = [r"\\bbudget\\b", r"\\btimeline\\b", r"\\bdecision\\b", r"\\bpain\\b", r"\\bmetric\\b"]

def discovery_gap_score(notes: str) -> float:
    """Score how much discovery is missing from notes. Time O(n)."""
    covered = sum(1 for g in _GAPS if re.search(g, notes, re.I))
    return 1.0 - covered / len(_GAPS)
''',
            "returns": "float 0-1 (higher = more gaps)",
        },
        {
            "name": "follow_up_timing_days",
            "doc": "Suggest ethical follow-up delay in days. Time O(1).",
            "body": '''\
def follow_up_timing_days(stage: str) -> int:
    """Suggest ethical follow-up delay in days. Time O(1)."""
    return {"cold": 3, "demo": 2, "proposal": 1, "silent": 5}.get(stage.lower(), 3)
''',
        },
        {
            "name": "pipeline_stage_score",
            "doc": "Score deal health from stage signals. Time O(n).",
            "body": '''\
def pipeline_stage_score(signals: dict[str, bool]) -> float:
    """Score deal health from stage signals. Time O(n)."""
    weights = {"champion": 0.3, "economic_buyer_met": 0.25, "timeline": 0.2, "pain_quantified": 0.15, "next_step": 0.1}
    return min(1.0, sum(weights[k] for k, v in signals.items() if v and k in weights))
''',
        },
        {
            "name": "champion_enablement_brief",
            "doc": "One-pager brief for internal champion. Time O(1).",
            "body": '''\
def champion_enablement_brief(problem: str, proof: str, ask: str) -> str:
    """One-pager brief for internal champion. Time O(1)."""
    return f"Problem: {problem}\\nProof: {proof}\\nAsk: {ask}\\nRisk if we wait: status quo continues."
''',
        },
        {
            "name": "demo_story_arc",
            "doc": "Three-beat demo narrative arc. Time O(1).",
            "body": '''\
def demo_story_arc(pain: str, shift: str, proof: str) -> list[str]:
    """Three-beat demo narrative arc. Time O(1)."""
    return [f"Today: {pain}", f"Imagine: {shift}", f"Proof: {proof}"]
''',
        },
        {
            "name": "closing_language_check",
            "doc": "Flag pushy closing language. Time O(n).",
            "body": '''\
_PUSHY = [r"sign today", r"last chance", r"act now", r"limited seats"]

def closing_language_check(text: str) -> list[str]:
    """Flag pushy closing language. Time O(n)."""
    return [p for p in _PUSHY if re.search(p, text, re.I)]
''',
        },
    ],
)

_simple_module(
    "marketing",
    "Marketing psychology",
    "marketing",
    [
        {
            "name": "icp_fit_score",
            "doc": "Score ideal customer profile fit from text. Time O(n).",
            "body": '''\
def icp_fit_score(text: str, icp_keywords: Sequence[str]) -> float:
    """Score ideal customer profile fit from text. Time O(n)."""
    if not icp_keywords:
        return 0.0
    hits = sum(1 for k in icp_keywords if k.lower() in text.lower())
    return hits / len(icp_keywords)
''',
        },
        {
            "name": "value_prop_one_liner",
            "doc": "Compress value prop into one line. Time O(1).",
            "body": '''\
def value_prop_one_liner(audience: str, outcome: str, differentiator: str) -> str:
    """Compress value prop into one line. Time O(1)."""
    return f"For {audience} who need {outcome}, we {differentiator}."
''',
        },
        {
            "name": "positioning_statement",
            "doc": "Classic positioning statement template. Time O(1).",
            "body": '''\
def positioning_statement(category: str, audience: str, benefit: str, proof: str) -> str:
    """Classic positioning statement template. Time O(1)."""
    return f"The {category} for {audience} that {benefit}, unlike alternatives because {proof}."
''',
        },
        {
            "name": "competitor_diff_line",
            "doc": "Ethical competitor differentiation line. Time O(1).",
            "body": '''\
def competitor_diff_line(competitor: str, wedge: str) -> str:
    """Ethical competitor differentiation line. Time O(1)."""
    return f"Compared to {competitor}, we optimize for {wedge} — best when that is your bottleneck."
''',
        },
        {
            "name": "persona_pain_hook",
            "doc": "Pain-led hook for a persona. Time O(1).",
            "body": '''\
def persona_pain_hook(persona: str, pain: str) -> str:
    """Pain-led hook for a persona. Time O(1)."""
    return f"If you are a {persona} tired of {pain}, read this."
''',
        },
        {
            "name": "channel_message_fit",
            "doc": "Score message fit for a marketing channel. Time O(n).",
            "body": '''\
_CHANNEL = {
    "x": [r".{0,280}", r"\\?"],
    "email": [r"\\bdear\\b", r"\\bsubject\\b"],
    "linkedin": [r"\\bprofessional\\b", r"\\bcareer\\b"],
}

def channel_message_fit(message: str, channel: str) -> float:
    """Score message fit for a marketing channel. Time O(n)."""
    patterns = _CHANNEL.get(channel.lower(), [])
    if not patterns:
        return 0.5
    return min(1.0, sum(1 for p in patterns if re.search(p, message, re.I)) / len(patterns))
''',
        },
        {
            "name": "launch_sequence_plan",
            "doc": "Simple launch email/post sequence. Time O(n).",
            "body": '''\
def launch_sequence_plan(beat: str, channels: Sequence[str]) -> list[str]:
    """Simple launch email/post sequence. Time O(n)."""
    return [f"{ch}: {beat} — teaser" for ch in channels] + [f"{ch}: {beat} — launch" for ch in channels]
''',
        },
        {
            "name": "brand_promise_check",
            "doc": "Flag overpromising brand language. Time O(n).",
            "body": '''\
_OVER = [r"\\bguaranteed\\b", r"\\b#1\\b", r"\\bbest in the world\\b", r"\\bnever fail\\b"]

def brand_promise_check(copy: str) -> list[str]:
    """Flag overpromising brand language. Time O(n)."""
    return [p for p in _OVER if re.search(p, copy, re.I)]
''',
        },
    ],
)

# Continue with more modules - I'll add conversion, copywriting, learning, etc. in batches
# Due to length, use a helper to add pattern-based scorers

def _batch_scorers(
    module: str,
    category: str,
    items: list[tuple[str, str, list[str], str]],
) -> None:
    """items: name, doc, patterns, use_case"""
    for name, doc, patterns, use_case in items:
        const = f"_{name.upper()}_PATTERNS"
        body = f"""\
{const} = {patterns!r}

def {name}(text: str) -> float:
    \"\"\"{doc}\"\"\"
    if not text:
        return 0.0
    hits = sum(1 for p in {const} if re.search(p, text, re.I))
    return min(1.0, hits / max(1, len({const})))
"""
        SPECS.setdefault(module, []).append(
            (name, category, "O(n)", "O(1)", doc, body, use_case, "float 0-1", f"{name}(\"...\")")
        )


_batch_scorers(
    "conversion",
    "conversion",
    [
        ("cta_clarity_score", "Score CTA clarity in landing copy. Time O(n).", [r"\bstart\b", r"\btry\b", r"\bget\b", r"\bfree\b"], "Tune hero CTAs"),
        ("friction_point_score", "Score UX friction language in copy. Time O(n).", [r"\bwait\b", r"\bcomplicated\b", r"\bmanual\b", r"\bconfusing\b"], "Find copy that signals friction"),
        ("urgency_ethical_score", "Score ethical vs dark urgency. Time O(n).", [r"\breal deadline\b", r"\blimited\b", r"\bwhile supplies\b"], "Audit urgency claims"),
    ],
)

# Add remaining functions with inline bodies - conversion continued
_simple_module(
    "conversion",
    "Conversion psychology",
    "conversion",
    [
        {
            "name": "landing_hero_frame",
            "doc": "Hero section frame for landing pages. Time O(1).",
            "body": '''\
def landing_hero_frame(outcome: str, proof: str, cta: str) -> str:
    """Hero section frame for landing pages. Time O(1)."""
    return f"{outcome}\\n{proof}\\n→ {cta}"
''',
        },
        {
            "name": "form_field_reduction_plan",
            "doc": "Plan progressive form fields. Time O(n).",
            "body": '''\
def form_field_reduction_plan(fields: Sequence[str], *, max_initial: int = 3) -> list[list[str]]:
    """Plan progressive form fields. Time O(n)."""
    fields = list(fields)
    if len(fields) <= max_initial:
        return [fields]
    return [fields[:max_initial], fields[max_initial:]]
''',
            "space": "O(n)",
        },
        {
            "name": "micro_commitment_step",
            "doc": "Micro-commitment step before main CTA. Time O(1).",
            "body": '''\
def micro_commitment_step(small_action: str, benefit: str) -> str:
    """Micro-commitment step before main CTA. Time O(1)."""
    return f"First, {small_action} — takes 30 seconds and {benefit}."
''',
        },
    ],
)

_simple_module(
    "copywriting",
    "Copywriting psychology",
    "copywriting",
    [
        {
            "name": "headline_power_score",
            "doc": "Score headline punch. Time O(n).",
            "body": '''\
def headline_power_score(headline: str) -> float:
    """Score headline punch. Time O(n)."""
    score = 0.0
    if 6 <= len(headline.split()) <= 12:
        score += 0.3
    if re.search(r"\\b(how|why|new|secret|free)\\b", headline, re.I):
        score += 0.3
    if re.search(r"\\d", headline):
        score += 0.2
    return min(1.0, score + min(0.2, len(headline) / 80))
''',
        },
        {
            "name": "active_voice_ratio",
            "doc": "Estimate active vs passive voice ratio. Time O(n).",
            "body": '''\
def active_voice_ratio(text: str) -> float:
    """Estimate active vs passive voice ratio. Time O(n)."""
    passive = len(re.findall(r"\\b(is|are|was|were)\\s+\\w+ed\\b", text, re.I))
    active = len(re.findall(r"\\b(we|you|i)\\s+\\w+\\b", text, re.I))
    total = passive + active
    return active / total if total else 1.0
''',
        },
        {
            "name": "benefit_vs_feature_ratio",
            "doc": "Ratio of benefit to feature language. Time O(n).",
            "body": '''\
_BEN = [r"\\bsave\\b", r"\\bearn\\b", r"\\bfaster\\b", r"\\bconfident\\b", r"\\bgrow\\b"]
_FEAT = [r"\\bapi\\b", r"\\bdashboard\\b", r"\\bintegration\\b", r"\\bmodule\\b"]

def benefit_vs_feature_ratio(text: str) -> float:
    """Ratio of benefit to feature language. Time O(n)."""
    b = sum(1 for p in _BEN if re.search(p, text, re.I))
    f = sum(1 for p in _FEAT if re.search(p, text, re.I))
    return b / max(1, b + f)
''',
        },
        {
            "name": "curiosity_gap_line",
            "doc": "Curiosity gap line without clickbait. Time O(1).",
            "body": '''\
def curiosity_gap_line(topic: str, payoff: str) -> str:
    """Curiosity gap line without clickbait. Time O(1)."""
    return f"The part everyone skips about {topic} (and how it {payoff})."
''',
        },
        {
            "name": "specificity_score",
            "doc": "Score copy specificity via numbers and proper nouns. Time O(n).",
            "body": '''\
def specificity_score(text: str) -> float:
    """Score copy specificity via numbers and proper nouns. Time O(n)."""
    nums = len(re.findall(r"\\b\\d+[\\d.,%]*\\b", text))
    caps = len(re.findall(r"\\b[A-Z][a-z]+\\b", text))
    return min(1.0, (nums * 0.15 + caps * 0.05))
''',
        },
        {
            "name": "power_word_density",
            "doc": "Density of emotional power words. Time O(n).",
            "body": '''\
_POWER = ["proven", "instant", "exclusive", "trusted", "simple", "guaranteed"]

def power_word_density(text: str) -> float:
    """Density of emotional power words. Time O(n)."""
    words = text.lower().split()
    if not words:
        return 0.0
    hits = sum(1 for w in words if w.strip(".,!?") in _POWER)
    return hits / len(words)
''',
        },
    ],
)

_simple_module(
    "learning",
    "Learning acceleration psychology",
    "learning_acceleration",
    [
        {
            "name": "spaced_repetition_interval_days",
            "doc": "Next review interval via SM-2-lite. Time O(1).",
            "body": '''\
def spaced_repetition_interval_days(repetition: int, ease: float = 2.5) -> int:
    """Next review interval via SM-2-lite. Time O(1)."""
    if repetition <= 0:
        return 1
    return max(1, int(round((repetition ** 0.5) * ease)))
''',
        },
        {
            "name": "micro_lesson_chunks",
            "doc": "Split content into micro-lessons. Time O(n).",
            "body": '''\
def micro_lesson_chunks(items: Sequence[str], *, chunk_size: int = 3) -> list[list[str]]:
    """Split content into micro-lessons. Time O(n)."""
    items = list(items)
    return [items[i : i + chunk_size] for i in range(0, len(items), chunk_size)]
''',
            "space": "O(n)",
        },
        {
            "name": "recall_prompt_generator",
            "doc": "Generate active recall prompt. Time O(1).",
            "body": '''\
def recall_prompt_generator(concept: str) -> str:
    """Generate active recall prompt. Time O(1)."""
    return f"Without looking: explain {concept} and one example from your work."
''',
        },
        {
            "name": "interleaving_schedule",
            "doc": "Interleave topics for practice. Time O(n).",
            "body": '''\
def interleaving_schedule(topics: Sequence[str], rounds: int = 2) -> list[str]:
    """Interleave topics for practice. Time O(n)."""
    out: list[str] = []
    for _ in range(rounds):
        out.extend(topics)
    return out
''',
            "space": "O(n)",
        },
        {
            "name": "elaboration_questions",
            "doc": "Elaborative interrogation questions. Time O(1).",
            "body": '''\
def elaboration_questions(concept: str) -> list[str]:
    """Elaborative interrogation questions. Time O(1)."""
    return [
        f"Why does {concept} work?",
        f"When would {concept} fail?",
        f"How is {concept} different from what you tried last month?",
    ]
''',
            "space": "O(1)",
        },
        {
            "name": "feynman_gap_score",
            "doc": "Score explanation gaps (jargon without definition). Time O(n).",
            "body": '''\
def feynman_gap_score(explanation: str) -> float:
    """Score explanation gaps (jargon without definition). Time O(n)."""
    jargon = len(re.findall(r"\\b[A-Z]{2,}\\b", explanation))
    defines = len(re.findall(r"\\bmeans\\b|\\bi\\.e\\.", explanation, re.I))
    return min(1.0, max(0.0, jargon * 0.2 - defines * 0.3))
''',
        },
        {
            "name": "practice_problem_spacing",
            "doc": "Days between practice problems. Time O(1).",
            "body": '''\
def practice_problem_spacing(mastery: float) -> int:
    """Days between practice problems. Time O(1)."""
    return max(1, int(round(7 * (1.0 - min(1.0, mastery)))))
''',
        },
        {
            "name": "mastery_threshold_check",
            "doc": "Check if mastery threshold met. Time O(1).",
            "body": '''\
def mastery_threshold_check(correct: int, attempts: int, *, threshold: float = 0.8) -> bool:
    """Check if mastery threshold met. Time O(1)."""
    return attempts > 0 and (correct / attempts) >= threshold
''',
        },
        {
            "name": "skill_stacking_path",
            "doc": "Order skills for compound learning. Time O(n).",
            "body": '''\
def skill_stacking_path(skills: Sequence[str]) -> list[str]:
    """Order skills for compound learning. Time O(n)."""
    return list(skills)
''',
            "space": "O(n)",
        },
    ],
)

# More modules to reach 86 new - social_growth, pricing, onboarding, retention, virality, objection, dm, ads, b2b, saas

_simple_module("social_growth", "Social growth psychology", "social_growth", [
    {"name": "audience_warmth_score", "doc": "Score audience warmth from engagement history. Time O(n).", "body": '''\
def audience_warmth_score(replies: int, saves: int, profile_clicks: int) -> float:
    """Score audience warmth from engagement history. Time O(n)."""
    raw = replies * 0.4 + saves * 0.35 + profile_clicks * 0.25
    return min(1.0, raw / 100.0)
'''},
    {"name": "content_pillar_balance", "doc": "Balance content pillars. Time O(n).", "body": '''\
def content_pillar_balance(counts: dict[str, int]) -> dict[str, float]:
    """Balance content pillars. Time O(n)."""
    total = sum(counts.values()) or 1
    return {k: v / total for k, v in counts.items()}
''', "space": "O(n)"},
    {"name": "posting_cadence_plan", "doc": "Weekly posting cadence plan. Time O(1).", "body": '''\
def posting_cadence_plan(posts_per_week: int) -> list[str]:
    """Weekly posting cadence plan. Time O(1)."""
    days = ["Mon", "Wed", "Fri", "Sat", "Tue", "Thu", "Sun"]
    return [f"{days[i % 7]}: post slot {i+1}" for i in range(posts_per_week)]
''', "space": "O(k)"},
    {"name": "cross_post_adaptation", "doc": "Adapt X post for LinkedIn. Time O(n).", "body": '''\
def cross_post_adaptation(x_post: str) -> str:
    """Adapt X post for LinkedIn. Time O(n)."""
    expanded = x_post.replace("\\n", "\\n\\n")
    return f"{expanded}\\n\\nWhat's your experience?"
'''},
    {"name": "creator_collab_fit", "doc": "Score creator collaboration fit. Time O(n).", "body": '''\
def creator_collab_fit(your_topics: Sequence[str], their_topics: Sequence[str]) -> float:
    """Score creator collaboration fit. Time O(n)."""
    yours = {t.lower() for t in your_topics}
    overlap = sum(1 for t in their_topics if t.lower() in yours)
    return overlap / max(1, len(your_topics))
'''},
    {"name": "community_reply_priority", "doc": "Prioritize community replies. Time O(n log n).", "body": '''\
def community_reply_priority(threads: Sequence[tuple[str, int]]) -> list[str]:
    """Prioritize community replies. Time O(n log n)."""
    return [t for t, _ in sorted(threads, key=lambda x: x[1], reverse=True)]
''', "time": "O(n log n)", "space": "O(n)"},
])

_simple_module("pricing_psychology", "Pricing psychology", "pricing_psychology", [
    {"name": "charm_price", "doc": "Charm price ending in 9. Time O(1).", "body": '''\
def charm_price(amount: float) -> float:
    """Charm price ending in 9. Time O(1)."""
    base = int(amount)
    return float(base) + 0.99 if amount >= 10 else max(0.99, round(amount - 0.01, 2))
'''},
    {"name": "anchoring_tier_order", "doc": "Order tiers for anchoring effect. Time O(n).", "body": '''\
def anchoring_tier_order(tiers: Sequence[str]) -> list[str]:
    """Order tiers for anchoring effect. Time O(n)."""
    return sorted(tiers, reverse=True)
''', "space": "O(n)"},
    {"name": "decoy_tier_highlight", "doc": "Highlight target tier vs decoy. Time O(1).", "body": '''\
def decoy_tier_highlight(target: str, decoy: str) -> str:
    """Highlight target tier vs decoy. Time O(1)."""
    return f"Most teams pick {target} over {decoy} because ROI is clearer."
'''},
    {"name": "price_framing_monthly_vs_annual", "doc": "Frame annual vs monthly savings. Time O(1).", "body": '''\
def price_framing_monthly_vs_annual(monthly: float, annual: float) -> str:
    """Frame annual vs monthly savings. Time O(1)."""
    save = monthly * 12 - annual
    return f"Pay annually and save ${save:.0f} vs monthly."
'''},
    {"name": "payment_friction_score", "doc": "Score checkout friction copy. Time O(n).", "body": '''\
_FRICTION = [r"\\bcredit card required\\b", r"\\bannual only\\b", r"\\bcontact sales\\b"]

def payment_friction_score(copy: str) -> float:
    """Score checkout friction copy. Time O(n)."""
    return min(1.0, sum(1 for p in _FRICTION if re.search(p, copy, re.I)) / len(_FRICTION))
'''},
])

_simple_module("onboarding", "Onboarding psychology", "onboarding", [
    {"name": "aha_moment_checklist", "doc": "Checklist items before aha moment. Time O(n).", "body": '''\
def aha_moment_checklist(steps: Sequence[str]) -> list[str]:
    """Checklist items before aha moment. Time O(n)."""
    return [f"[ ] {s}" for s in steps]
''', "space": "O(n)"},
    {"name": "time_to_value_score", "doc": "Score time-to-value from step count. Time O(1).", "body": '''\
def time_to_value_score(steps_to_value: int) -> float:
    """Score time-to-value from step count. Time O(1)."""
    return max(0.0, 1.0 - (steps_to_value - 1) * 0.15)
'''},
    {"name": "setup_wizard_steps", "doc": "Chunk setup wizard steps. Time O(n).", "body": '''\
def setup_wizard_steps(tasks: Sequence[str], *, per_screen: int = 2) -> list[list[str]]:
    """Chunk setup wizard steps. Time O(n)."""
    tasks = list(tasks)
    return [tasks[i:i+per_screen] for i in range(0, len(tasks), per_screen)]
''', "space": "O(n)"},
    {"name": "activation_milestone_map", "doc": "Map user actions to activation milestones. Time O(n).", "body": '''\
def activation_milestone_map(actions: Sequence[str]) -> dict[str, str]:
    """Map user actions to activation milestones. Time O(n)."""
    return {a: f"Complete {a} to unlock next value" for a in actions}
''', "space": "O(n)"},
    {"name": "empty_state_copy", "doc": "Empty state copy with next action. Time O(1).", "body": '''\
def empty_state_copy(resource: str, first_action: str) -> str:
    """Empty state copy with next action. Time O(1)."""
    return f"No {resource} yet. {first_action} to see results here."
'''},
])

_simple_module("retention", "Retention psychology", "retention", [
    {"name": "churn_risk_score", "doc": "Score churn risk from usage signals. Time O(n).", "body": '''\
def churn_risk_score(days_inactive: int, support_tickets: int, nps: int | None) -> float:
    """Score churn risk from usage signals. Time O(n)."""
    risk = min(1.0, days_inactive / 30.0) * 0.5
    risk += min(0.3, support_tickets * 0.1)
    if nps is not None and nps < 7:
        risk += 0.2
    return min(1.0, risk)
'''},
    {"name": "win_back_subject_line", "doc": "Win-back email subject line. Time O(1).", "body": '''\
def win_back_subject_line(feature: str) -> str:
    """Win-back email subject line. Time O(1)."""
    return f"We saved your spot — new {feature} you asked for"
'''},
    {"name": "habit_loop_design", "doc": "Cue-routine-reward habit loop copy. Time O(1).", "body": '''\
def habit_loop_design(cue: str, routine: str, reward: str) -> str:
    """Cue-routine-reward habit loop copy. Time O(1)."""
    return f"When {cue}, {routine} so you can {reward}."
'''},
    {"name": "renewal_reminder_frame", "doc": "Renewal reminder with value recap. Time O(1).", "body": '''\
def renewal_reminder_frame(value_received: str, renewal_date: str) -> str:
    """Renewal reminder with value recap. Time O(1)."""
    return f"You achieved {value_received}. Renew by {renewal_date} to keep momentum."
'''},
    {"name": "expansion_upsell_timing", "doc": "Days until expansion upsell. Time O(1).", "body": '''\
def expansion_upsell_timing(days_since_activation: int) -> bool:
    """Days until expansion upsell. Time O(1)."""
    return days_since_activation >= 14
'''},
])

_simple_module("virality", "Virality psychology", "virality", [
    {"name": "shareability_score", "doc": "Score content shareability. Time O(n).", "body": '''\
def shareability_score(text: str) -> float:
    """Score content shareability. Time O(n)."""
    signals = [r"\\btemplate\\b", r"\\bcheatsheet\\b", r"\\bshare\\b", r"\\btag\\b"]
    return min(1.0, sum(1 for s in signals if re.search(s, text, re.I)) / len(signals))
'''},
    {"name": "referral_incentive_frame", "doc": "Referral incentive frame. Time O(1).", "body": '''\
def referral_incentive_frame(give: str, get: str) -> str:
    """Referral incentive frame. Time O(1)."""
    return f"Give {give}, get {get} — both sides win."
'''},
    {"name": "network_effect_pitch", "doc": "Network effect pitch line. Time O(1).", "body": '''\
def network_effect_pitch(audience: str, benefit: str) -> str:
    """Network effect pitch line. Time O(1)."""
    return f"The more {audience} join, the better {benefit} gets for everyone."
'''},
    {"name": "k_factor_estimate", "doc": "Estimate viral k-factor. Time O(1).", "body": '''\
def k_factor_estimate(invites_per_user: float, conversion_rate: float) -> float:
    """Estimate viral k-factor. Time O(1)."""
    return invites_per_user * conversion_rate
'''},
    {"name": "word_of_mouth_prompt", "doc": "Prompt satisfied users for referrals. Time O(1).", "body": '''\
def word_of_mouth_prompt(outcome: str) -> str:
    """Prompt satisfied users for referrals. Time O(1)."""
    return f"If {outcome} helped you, who else should know?"
'''},
])

_simple_module("objection_handling", "Objection handling", "objection_handling", [
    {"name": "price_objection_reframe", "doc": "Reframe price objection to ROI. Time O(1).", "body": '''\
def price_objection_reframe(cost: str, roi: str) -> str:
    """Reframe price objection to ROI. Time O(1)."""
    return f"If {cost} feels high, compare it to {roi} over 90 days."
'''},
    {"name": "timing_objection_response", "doc": "Response to timing objection. Time O(1).", "body": '''\
def timing_objection_response(cost_of_wait: str) -> str:
    """Response to timing objection. Time O(1)."""
    return f"What happens if we push this a quarter? {cost_of_wait}"
'''},
    {"name": "authority_objection_response", "doc": "Response when buyer lacks authority. Time O(1).", "body": '''\
def authority_objection_response(stakeholder: str, proof: str) -> str:
    """Response when buyer lacks authority. Time O(1)."""
    return f"Happy to equip you with {proof} for {stakeholder}."
'''},
    {"name": "need_objection_probe", "doc": "Probe need objection. Time O(1).", "body": '''\
def need_objection_probe(current_workflow: str) -> str:
    """Probe need objection. Time O(1)."""
    return f"What would have to break in {current_workflow} for this to become urgent?"
'''},
    {"name": "competitor_objection_matrix", "doc": "Map competitor objection to wedge. Time O(1).", "body": '''\
def competitor_objection_matrix(competitor: str, wedge: str) -> dict[str, str]:
    """Map competitor objection to wedge. Time O(1)."""
    return {"objection": f"We already use {competitor}", "wedge": wedge, "question": "Where does it fall short today?"}
''', "space": "O(1)"},
])

_simple_module("dm_outreach", "DM outreach psychology", "dm_outreach", [
    {"name": "cold_dm_opener", "doc": "Cold DM opener with relevance. Time O(1).", "body": '''\
def cold_dm_opener(trigger: str, relevance: str) -> str:
    """Cold DM opener with relevance. Time O(1)."""
    return f"Noticed {trigger}. We help with {relevance} — worth a 2-line overview?"
'''},
    {"name": "warm_dm_followup", "doc": "Warm DM follow-up after engagement. Time O(1).", "body": '''\
def warm_dm_followup(interaction: str, offer: str) -> str:
    """Warm DM follow-up after engagement. Time O(1)."""
    return f"Thanks for {interaction}. If useful, I can send {offer}."
'''},
    {"name": "dm_personalization_hooks", "doc": "Extract DM personalization hooks. Time O(n).", "body": '''\
def dm_personalization_hooks(bio: str, recent_post: str) -> list[str]:
    """Extract DM personalization hooks. Time O(n)."""
    hooks = []
    if bio.strip():
        hooks.append(bio.strip()[:80])
    if recent_post.strip():
        hooks.append(recent_post.strip()[:80])
    return hooks
''', "space": "O(n)"},
    {"name": "dm_spam_risk_score", "doc": "Score DM spam risk. Time O(n).", "body": '''\
_SPAM = [r"\\bguaranteed\\b", r"\\bclick here\\b", r"\\bmake money\\b", r"\\b100%\\b"]

def dm_spam_risk_score(message: str) -> float:
    """Score DM spam risk. Time O(n)."""
    return min(1.0, sum(1 for p in _SPAM if re.search(p, message, re.I)) / len(_SPAM))
'''},
    {"name": "conversation_to_call_bridge", "doc": "Bridge DM thread to call. Time O(1).", "body": '''\
def conversation_to_call_bridge(topic: str) -> str:
    """Bridge DM thread to call. Time O(1)."""
    return f"Happy to go deeper on {topic} — 15 min next week?"
'''},
])

_simple_module("ads_psychology", "Ads psychology", "ads_psychology", [
    {"name": "ad_hook_variants", "doc": "Generate ad hook variants. Time O(n).", "body": '''\
def ad_hook_variants(offer: str, *, count: int = 3) -> list[str]:
    """Generate ad hook variants. Time O(n)."""
    opts = [f"Stop wasting time on {offer}", f"{offer} without the guesswork", f"Founders use this for {offer}"]
    return opts[:count]
''', "space": "O(k)"},
    {"name": "scroll_stop_score", "doc": "Score ad scroll-stop power. Time O(n).", "body": '''\
def scroll_stop_score(headline: str) -> float:
    """Score ad scroll-stop power. Time O(n)."""
    return min(1.0, (0.3 if len(headline) < 60 else 0.1) + (0.3 if re.search(r"\\d", headline) else 0))
'''},
    {"name": "ad_frequency_fatigue_score", "doc": "Score ad fatigue from impressions. Time O(1).", "body": '''\
def ad_frequency_fatigue_score(impressions: int, *, threshold: int = 8) -> float:
    """Score ad fatigue from impressions. Time O(1)."""
    return min(1.0, impressions / threshold)
'''},
    {"name": "retargeting_message_tier", "doc": "Retargeting message by funnel tier. Time O(1).", "body": '''\
def retargeting_message_tier(tier: str, offer: str) -> str:
    """Retargeting message by funnel tier. Time O(1)."""
    tiers = {"aware": f"Still curious about {offer}?", "consider": f"Compare plans for {offer}", "cart": f"Finish setup for {offer}"}
    return tiers.get(tier.lower(), offer)
'''},
])

_simple_module("b2b_selling", "B2B selling psychology", "b2b_selling", [
    {"name": "meddic_qualification_score", "doc": "MEDDIC qualification score. Time O(n).", "body": '''\
def meddic_qualification_score(flags: dict[str, bool]) -> float:
    """MEDDIC qualification score. Time O(n)."""
    keys = ["metrics", "economic_buyer", "decision_criteria", "decision_process", "identify_pain", "champion"]
    return sum(1 for k in keys if flags.get(k)) / len(keys)
'''},
    {"name": "economic_buyer_map", "doc": "Map economic buyer concerns. Time O(1).", "body": '''\
def economic_buyer_map(initiative: str, risk: str) -> str:
    """Map economic buyer concerns. Time O(1)."""
    return f"EB cares about {initiative} and de-risking {risk}."
'''},
    {"name": "procurement_objection_prep", "doc": "Prep for procurement objections. Time O(1).", "body": '''\
def procurement_objection_prep(vendor_requirement: str, answer: str) -> str:
    """Prep for procurement objections. Time O(1)."""
    return f"When they ask about {vendor_requirement}: {answer}"
'''},
    {"name": "pilot_success_criteria", "doc": "Pilot success criteria statement. Time O(1).", "body": '''\
def pilot_success_criteria(metric: str, target: str, timeline: str) -> str:
    """Pilot success criteria statement. Time O(1)."""
    return f"Success = {metric} reaches {target} within {timeline}."
'''},
])

_simple_module("saas_growth", "SaaS growth psychology", "saas_growth", [
    {"name": "plg_activation_score", "doc": "PLG activation score from events. Time O(n).", "body": '''\
def plg_activation_score(events: dict[str, bool]) -> float:
    """PLG activation score from events. Time O(n)."""
    keys = ["signup", "first_project", "invite_teammate", "core_action", "return_day_7"]
    return sum(1 for k in keys if events.get(k)) / len(keys)
'''},
    {"name": "freemium_limit_message", "doc": "Freemium limit upgrade message. Time O(1).", "body": '''\
def freemium_limit_message(limit: str, upgrade_benefit: str) -> str:
    """Freemium limit upgrade message. Time O(1)."""
    return f"You hit {limit}. Upgrade to {upgrade_benefit}."
'''},
    {"name": "upgrade_trigger_event", "doc": "Suggest upgrade trigger from usage. Time O(1).", "body": '''\
def upgrade_trigger_event(usage_ratio: float, *, threshold: float = 0.8) -> bool:
    """Suggest upgrade trigger from usage. Time O(1)."""
    return usage_ratio >= threshold
'''},
    {"name": "usage_based_upsell_line", "doc": "Usage-based upsell line. Time O(1).", "body": '''\
def usage_based_upsell_line(metric: str, headroom: str) -> str:
    """Usage-based upsell line. Time O(1)."""
    return f"You are at {metric}. Add {headroom} before workflow stalls."
'''},
])

# Add a few more to cross 86 new - engagement_bait_detector, learning spaced, newsletter, etc.
_simple_module("twitter_x", "X/Twitter growth", "twitter_x", [
    {"name": "engagement_bait_detector", "doc": "Detect engagement bait patterns on X. Time O(n).", "body": '''\
_BAIT = [r"comment \\w+ below", r"like if you agree", r"follow for follow", r"drop a \\W"]

def engagement_bait_detector(text: str) -> list[str]:
    """Detect engagement bait patterns on X. Time O(n)."""
    return [p for p in _BAIT if re.search(p, text, re.I)]
''', "returns": "list[str]"},
    {"name": "creator_flywheel_stage", "doc": "Map creator flywheel stage from metrics. Time O(1).", "body": '''\
def creator_flywheel_stage(followers: int, engagement_rate: float) -> str:
    """Map creator flywheel stage from metrics. Time O(1)."""
    if followers < 500:
        return "reply_guy_growth"
    if engagement_rate < 0.02:
        return "audience_quality_fix"
    return "productize_attention"
'''},
])

_simple_module("learning", "Learning", "spaced_learning", [
    {"name": "forgetting_curve_reminder", "doc": "Days until forgetting curve reminder. Time O(1).", "body": '''\
def forgetting_curve_reminder(days_since_review: int) -> bool:
    """Days until forgetting curve reminder. Time O(1)."""
    return days_since_review >= 3
'''},
])

_simple_module("marketing", "Marketing", "newsletter", [
    {"name": "newsletter_subject_score", "doc": "Score newsletter subject line. Time O(n).", "body": '''\
def newsletter_subject_score(subject: str) -> float:
    """Score newsletter subject line. Time O(n)."""
    score = 0.4 if 30 <= len(subject) <= 55 else 0.2
    if re.search(r"\\b(you|your)\\b", subject, re.I):
        score += 0.2
    if re.search(r"\\d", subject):
        score += 0.15
    return min(1.0, score)
'''},
    {"name": "newsletter_preview_text", "doc": "Newsletter preview text line. Time O(1).", "body": '''\
def newsletter_preview_text(hook: str) -> str:
    """Newsletter preview text line. Time O(1)."""
    return hook[:90]
'''},
])

_simple_module("marketing", "Marketing", "landing_pages", [
    {"name": "landing_social_proof_block", "doc": "Social proof block for landing page. Time O(1).", "body": '''\
def landing_social_proof_block(logos: Sequence[str], quote: str) -> str:
    """Social proof block for landing page. Time O(1)."""
    names = ", ".join(logos[:5])
    return f"Trusted by {names}\\n\\"{quote}\\""
'''},
])

_simple_module("sales", "Sales", "b2b_selling", [
    {"name": "multi_threading_map", "doc": "Map multi-threading stakeholders. Time O(n).", "body": '''\
def multi_threading_map(roles: Sequence[str]) -> dict[str, str]:
    """Map multi-threading stakeholders. Time O(n)."""
    return {r: f"Engage {r} with role-specific proof" for r in roles}
''', "space": "O(n)"},
])

_simple_module("conversion", "Conversion", "landing_pages", [
    {"name": "checkout_trust_badges", "doc": "Checkout trust badge copy. Time O(1).", "body": '''\
def checkout_trust_badges(guarantee: str) -> list[str]:
    """Checkout trust badge copy. Time O(1)."""
    return ["Secure checkout", guarantee, "Cancel anytime"]
''', "space": "O(k)"},
])

_simple_module("saas_growth", "SaaS", "saas_growth", [
    {"name": "seat_expansion_probe", "doc": "Probe for seat expansion. Time O(1).", "body": '''\
def seat_expansion_probe(team_growth: str) -> str:
    """Probe for seat expansion. Time O(1)."""
    return f"As {team_growth}, want shared seats so nobody hits limits?"
'''},
    {"name": "nrr_expansion_map", "doc": "Net revenue retention expansion map. Time O(n).", "body": '''\
def nrr_expansion_map(accounts: Sequence[str]) -> dict[str, str]:
    """Net revenue retention expansion map. Time O(n)."""
    return {a: "upsell + cross-sell review" for a in accounts}
''', "space": "O(n)"},
])

_simple_module("social_growth", "Social", "audience_building", [
    {"name": "follower_quality_score", "doc": "Score follower quality vs vanity. Time O(1).", "body": '''\
def follower_quality_score(replies_per_post: float, follower_count: int) -> float:
    """Score follower quality vs vanity. Time O(1)."""
    if follower_count <= 0:
        return 0.0
    ratio = replies_per_post / math.sqrt(follower_count)
    return min(1.0, ratio * 10)
'''},
    {"name": "growth_loop_map", "doc": "Map content growth loop steps. Time O(n).", "body": '''\
def growth_loop_map(steps: Sequence[str]) -> list[str]:
    """Map content growth loop steps. Time O(n)."""
    return [f"{i+1}. {s}" for i, s in enumerate(steps)]
''', "space": "O(n)"},
])

_simple_module("copywriting", "Copy", "hook_writing", [
    {"name": "rhythm_variation_score", "doc": "Score sentence rhythm variation. Time O(n).", "body": '''\
def rhythm_variation_score(text: str) -> float:
    """Score sentence rhythm variation. Time O(n)."""
    lengths = [len(s.split()) for s in re.split(r"[.!?]+", text) if s.strip()]
    if len(lengths) < 2:
        return 0.0
    avg = sum(lengths) / len(lengths)
    var = sum((l - avg) ** 2 for l in lengths) / len(lengths)
    return min(1.0, var / 20.0)
'''},
])

_simple_module("virality", "Virality", "ecommerce_merch", [
    {"name": "meme_template_fit", "doc": "Score meme template fit for merch marketing. Time O(n).", "body": '''\
def meme_template_fit(caption: str, brand_voice: str) -> float:
    """Score meme template fit for merch marketing. Time O(n)."""
    risky = len(re.findall(r"\\b(nsfw|politics)\\b", caption, re.I))
    on_brand = 1.0 if brand_voice.lower() in caption.lower() else 0.3
    return max(0.0, on_brand - risky * 0.5)
'''},
])

_simple_module("marketing", "Marketing", "brand_voice", [
    {"name": "brand_voice_consistency_score", "doc": "Score brand voice consistency. Time O(n).", "body": '''\
def brand_voice_consistency_score(text: str, voice_keywords: Sequence[str]) -> float:
    """Score brand voice consistency. Time O(n)."""
    if not voice_keywords:
        return 0.0
    hits = sum(1 for k in voice_keywords if k.lower() in text.lower())
    return hits / len(voice_keywords)
'''},
])

_simple_module("marketing", "Marketing", "crisis_comms", [
    {"name": "crisis_statement_frame", "doc": "Crisis comms statement frame. Time O(1).", "body": '''\
def crisis_statement_frame(what_happened: str, what_we_are_doing: str, what_you_should_do: str) -> str:
    """Crisis comms statement frame. Time O(1)."""
    return f"What happened: {what_happened}\\nWhat we are doing: {what_we_are_doing}\\nWhat you should do: {what_you_should_do}"
'''},
])

_simple_module("social_growth", "Social", "community", [
    {"name": "community_welcome_message", "doc": "Community welcome message. Time O(1).", "body": '''\
def community_welcome_message(name: str, norm: str) -> str:
    """Community welcome message. Time O(1)."""
    return f"Welcome {name}! Start by introducing yourself. House rule: {norm}."
'''},
])

_simple_module("ads_psychology", "Ads", "ads_psychology", [
    {"name": "ad_claim_compliance_check", "doc": "Flag non-compliant ad claims. Time O(n).", "body": '''\
_BAD = [r"\\bguaranteed results\\b", r"\\bget rich\\b", r"\\bno risk\\b"]

def ad_claim_compliance_check(copy: str) -> list[str]:
    """Flag non-compliant ad claims. Time O(n)."""
    return [p for p in _BAD if re.search(p, copy, re.I)]
''', "returns": "list[str]"},
    {"name": "creative_angle_matrix", "doc": "Creative angle matrix for ads. Time O(1).", "body": '''\
def creative_angle_matrix(product: str) -> dict[str, str]:
    """Creative angle matrix for ads. Time O(1)."""
    return {"pain": f"Stop struggling with {product}", "gain": f"Get outcomes faster with {product}", "proof": f"See how teams use {product}"}
''', "space": "O(1)"},
])

_simple_module("b2b_selling", "B2B", "b2b_selling", [
    {"name": "security_review_brief", "doc": "Security review brief for enterprise. Time O(1).", "body": '''\
def security_review_brief(certifications: str, data_handling: str) -> str:
    """Security review brief for enterprise. Time O(1)."""
    return f"Certs: {certifications}. Data: {data_handling}."
'''},
    {"name": "expansion_playbook_step", "doc": "Expansion playbook next step. Time O(1).", "body": '''\
def expansion_playbook_step(stage: str) -> str:
    """Expansion playbook next step. Time O(1)."""
    return {"land": "prove ROI in one team", "expand": "roll out to adjacent team", "renew": "document outcomes for procurement"}.get(stage, "review usage")
'''},
])

_simple_module("dm_outreach", "DM", "dm_outreach", [
    {"name": "dm_opt_out_respect", "doc": "Respectful DM opt-out reply. Time O(1).", "body": '''\
def dm_opt_out_respect() -> str:
    """Respectful DM opt-out reply. Time O(1)."""
    return "Thanks for letting me know — won't follow up. Door's open if timing changes."
'''},
])

_simple_module("conversion", "Conversion", "conversion", [
    {"name": "social_proof_placement", "doc": "Where to place social proof on page. Time O(1).", "body": '''\
def social_proof_placement(section: str) -> str:
    """Where to place social proof on page. Time O(1)."""
    return {"hero": "logo strip under headline", "pricing": "testimonial beside tier", "checkout": "trust badges"}.get(section, "near CTA")
'''},
])

_simple_module("sales", "Sales", "sales", [
    {"name": "deal_risk_flags", "doc": "Flag deal risk phrases in notes. Time O(n).", "body": '''\
_RISK = [r"no budget", r"just browsing", r"next year", r"ghost"]

def deal_risk_flags(notes: str) -> list[str]:
    """Flag deal risk phrases in notes. Time O(n)."""
    return [p for p in _RISK if re.search(p, notes, re.I)]
''', "returns": "list[str]"},
])

_simple_module("learning", "Learning", "learning_acceleration", [
    {"name": "lesson_prerequisite_check", "doc": "Check lesson prerequisites met. Time O(n).", "body": '''\
def lesson_prerequisite_check(completed: set[str], required: Sequence[str]) -> list[str]:
    """Check lesson prerequisites met. Time O(n)."""
    return [r for r in required if r not in completed]
''', "space": "O(n)", "returns": "list[str]"},
])

_simple_module("twitter_x", "X", "thread_structure", [
    {"name": "thread_structure_outline", "doc": "Outline thread structure from bullets. Time O(n).", "body": '''\
def thread_structure_outline(bullets: Sequence[str]) -> list[str]:
    """Outline thread structure from bullets. Time O(n)."""
    out = ["1/ Hook"]
    for i, b in enumerate(bullets, start=2):
        out.append(f"{i}/ {b}")
    out.append(f"{len(bullets)+2}/ CTA + recap")
    return out
''', "space": "O(n)"},
])

_simple_module("twitter_x", "X", "engagement_scoring", [
    {"name": "tweet_readability_for_x", "doc": "Score tweet readability for X. Time O(n).", "body": '''\
def tweet_readability_for_x(text: str) -> float:
    """Score tweet readability for X. Time O(n)."""
    words = text.split()
    if not words:
        return 0.0
    avg_len = sum(len(w) for w in words) / len(words)
    return max(0.0, 1.0 - max(0, avg_len - 5) * 0.1)
'''},
])

_simple_module("marketing", "Marketing", "influencer_fit", [
    {"name": "influencer_fit_score", "doc": "Score influencer partnership fit. Time O(n).", "body": '''\
def influencer_fit_score(brand_values: Sequence[str], creator_bio: str) -> float:
    """Score influencer partnership fit. Time O(n)."""
    if not brand_values:
        return 0.0
    hits = sum(1 for v in brand_values if v.lower() in creator_bio.lower())
    return hits / len(brand_values)
'''},
])

MODULE_TITLES = {
    "twitter_x": "X (Twitter) growth and engagement psychology",
    "sales": "Sales psychology helpers",
    "marketing": "Marketing psychology",
    "conversion": "Conversion psychology",
    "copywriting": "Copywriting psychology",
    "learning": "Learning acceleration psychology",
    "social_growth": "Social growth psychology",
    "pricing_psychology": "Pricing psychology",
    "onboarding": "Onboarding psychology",
    "retention": "Retention psychology",
    "virality": "Virality psychology",
    "objection_handling": "Objection handling",
    "dm_outreach": "DM outreach psychology",
    "ads_psychology": "Ads psychology",
    "b2b_selling": "B2B selling psychology",
    "saas_growth": "SaaS growth psychology",
}


def write_modules() -> list[str]:
    new_names: list[str] = []
    for module, items in SPECS.items():
        title = MODULE_TITLES.get(module, module.replace("_", " ").title())
        parts = [MODULE_HEADER.format(title=title)]
        seen: set[str] = set()
        for name, *_rest in items:
            if name in seen:
                continue
            seen.add(name)
            body = _rest[4]
            parts.append(textwrap.dedent(body).strip() + "\n")
            new_names.append(name)
        path = PSY / f"{module}.py"
        path.write_text("\n".join(parts) + "\n", encoding="utf-8")
        print(f"wrote {path.name}: {len(seen)} functions")
    return new_names


def build_catalog(existing: list[dict], new_names: list[str]) -> list[dict]:
    existing_names = {e["name"] for e in existing}
    out = list(existing)
    for module, items in SPECS.items():
        mod_path = f"psychology.{module}"
        seen: set[str] = set()
        for name, category, time, space, doc, _body, use_case, ret, example in items:
            if name in seen or name in existing_names:
                continue
            seen.add(name)
            out.append(
                {
                    "name": name,
                    "category": category,
                    "time": time,
                    "space": space,
                    "module": mod_path,
                    "function": name,
                    "use_case": use_case,
                    "returns": ret,
                    "example": example,
                }
            )
    return out


def main() -> None:
    existing = json.loads(CATALOG.read_text(encoding="utf-8"))
    new_names = write_modules()
    catalog = build_catalog(existing, new_names)
    new_count = len(catalog) - len(existing)
    print(f"catalog: {len(existing)} -> {len(catalog)} (+{new_count})")
    CATALOG.write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
