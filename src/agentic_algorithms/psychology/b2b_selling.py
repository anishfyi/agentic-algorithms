"""B2B selling psychology."""

from __future__ import annotations


def meddic_qualification_score(flags: dict[str, bool]) -> float:
    """MEDDIC qualification score. Time O(n)."""
    keys = [
        "metrics",
        "economic_buyer",
        "decision_criteria",
        "decision_process",
        "identify_pain",
        "champion",
    ]
    return sum(1 for k in keys if flags.get(k)) / len(keys)


def economic_buyer_map(initiative: str, risk: str) -> str:
    """Map economic buyer concerns. Time O(1)."""
    return f"EB cares about {initiative} and de-risking {risk}."


def procurement_objection_prep(vendor_requirement: str, answer: str) -> str:
    """Prep for procurement objections. Time O(1)."""
    return f"When they ask about {vendor_requirement}: {answer}"


def pilot_success_criteria(metric: str, target: str, timeline: str) -> str:
    """Pilot success criteria statement. Time O(1)."""
    return f"Success = {metric} reaches {target} within {timeline}."


def security_review_brief(certifications: str, data_handling: str) -> str:
    """Security review brief for enterprise. Time O(1)."""
    return f"Certs: {certifications}. Data: {data_handling}."


def expansion_playbook_step(stage: str) -> str:
    """Expansion playbook next step. Time O(1)."""
    return {
        "land": "prove ROI in one team",
        "expand": "roll out to adjacent team",
        "renew": "document outcomes for procurement",
    }.get(stage, "review usage")
