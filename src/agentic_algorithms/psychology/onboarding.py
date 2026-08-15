"""Onboarding psychology."""

from __future__ import annotations

import math
import re
from typing import Sequence


def aha_moment_checklist(steps: Sequence[str]) -> list[str]:
    """Checklist items before aha moment. Time O(n)."""
    return [f"[ ] {s}" for s in steps]

def time_to_value_score(steps_to_value: int) -> float:
    """Score time-to-value from step count. Time O(1)."""
    return max(0.0, 1.0 - (steps_to_value - 1) * 0.15)

def setup_wizard_steps(tasks: Sequence[str], *, per_screen: int = 2) -> list[list[str]]:
    """Chunk setup wizard steps. Time O(n)."""
    tasks = list(tasks)
    return [tasks[i:i+per_screen] for i in range(0, len(tasks), per_screen)]

def activation_milestone_map(actions: Sequence[str]) -> dict[str, str]:
    """Map user actions to activation milestones. Time O(n)."""
    return {a: f"Complete {a} to unlock next value" for a in actions}

def empty_state_copy(resource: str, first_action: str) -> str:
    """Empty state copy with next action. Time O(1)."""
    return f"No {resource} yet. {first_action} to see results here."

