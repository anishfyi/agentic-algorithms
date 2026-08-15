"""Learning acceleration psychology."""

from __future__ import annotations

import math
import re
from typing import Sequence


def spaced_repetition_interval_days(repetition: int, ease: float = 2.5) -> int:
    """Next review interval via SM-2-lite. Time O(1)."""
    if repetition <= 0:
        return 1
    return max(1, int(round((repetition ** 0.5) * ease)))

def micro_lesson_chunks(items: Sequence[str], *, chunk_size: int = 3) -> list[list[str]]:
    """Split content into micro-lessons. Time O(n)."""
    items = list(items)
    return [items[i : i + chunk_size] for i in range(0, len(items), chunk_size)]

def recall_prompt_generator(concept: str) -> str:
    """Generate active recall prompt. Time O(1)."""
    return f"Without looking: explain {concept} and one example from your work."

def interleaving_schedule(topics: Sequence[str], rounds: int = 2) -> list[str]:
    """Interleave topics for practice. Time O(n)."""
    out: list[str] = []
    for _ in range(rounds):
        out.extend(topics)
    return out

def elaboration_questions(concept: str) -> list[str]:
    """Elaborative interrogation questions. Time O(1)."""
    return [
        f"Why does {concept} work?",
        f"When would {concept} fail?",
        f"How is {concept} different from what you tried last month?",
    ]

def feynman_gap_score(explanation: str) -> float:
    """Score explanation gaps (jargon without definition). Time O(n)."""
    jargon = len(re.findall(r"\b[A-Z]{2,}\b", explanation))
    defines = len(re.findall(r"\bmeans\b|\bi\.e\.", explanation, re.I))
    return min(1.0, max(0.0, jargon * 0.2 - defines * 0.3))

def practice_problem_spacing(mastery: float) -> int:
    """Days between practice problems. Time O(1)."""
    return max(1, int(round(7 * (1.0 - min(1.0, mastery)))))

def mastery_threshold_check(correct: int, attempts: int, *, threshold: float = 0.8) -> bool:
    """Check if mastery threshold met. Time O(1)."""
    return attempts > 0 and (correct / attempts) >= threshold

def skill_stacking_path(skills: Sequence[str]) -> list[str]:
    """Order skills for compound learning. Time O(n)."""
    return list(skills)

def forgetting_curve_reminder(days_since_review: int) -> bool:
    """Days until forgetting curve reminder. Time O(1)."""
    return days_since_review >= 3

def lesson_prerequisite_check(completed: set[str], required: Sequence[str]) -> list[str]:
    """Check lesson prerequisites met. Time O(n)."""
    return [r for r in required if r not in completed]

