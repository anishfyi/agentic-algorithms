"""Objection handling."""

from __future__ import annotations

import math
import re
from typing import Sequence


def price_objection_reframe(cost: str, roi: str) -> str:
    """Reframe price objection to ROI. Time O(1)."""
    return f"If {cost} feels high, compare it to {roi} over 90 days."

def timing_objection_response(cost_of_wait: str) -> str:
    """Response to timing objection. Time O(1)."""
    return f"What happens if we push this a quarter? {cost_of_wait}"

def authority_objection_response(stakeholder: str, proof: str) -> str:
    """Response when buyer lacks authority. Time O(1)."""
    return f"Happy to equip you with {proof} for {stakeholder}."

def need_objection_probe(current_workflow: str) -> str:
    """Probe need objection. Time O(1)."""
    return f"What would have to break in {current_workflow} for this to become urgent?"

def competitor_objection_matrix(competitor: str, wedge: str) -> dict[str, str]:
    """Map competitor objection to wedge. Time O(1)."""
    return {"objection": f"We already use {competitor}", "wedge": wedge, "question": "Where does it fall short today?"}

