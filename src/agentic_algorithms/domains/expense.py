"""Expense management algorithms."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from agentic_algorithms.domains.geo import haversine_km


@dataclass(frozen=True)
class Expense:
    expense_id: str
    employee_id: str
    amount_minor: int
    merchant: str
    category: str
    expense_date: date
    memo: str = ""


CATEGORY_KEYWORDS: dict[str, set[str]] = {
    "travel": {"uber", "ola", "flight", "airline", "hotel", "booking"},
    "meals": {"restaurant", "cafe", "swiggy", "zomato", "doordash"},
    "software": {"aws", "github", "notion", "slack", "saas", "subscription"},
    "office": {"staples", "furniture", "supplies"},
    "fuel": {"petrol", "diesel", "shell", "bp", "indianoil"},
}


def categorize_expense(merchant: str, memo: str = "") -> tuple[str, float]:
    """Rule-based expense categorization with confidence. Time O(k), space O(1)."""
    haystack = f"{merchant} {memo}".lower()
    best_category = "uncategorized"
    best_score = 0.0
    for category, keywords in CATEGORY_KEYWORDS.items():
        hits = sum(1 for keyword in keywords if keyword in haystack)
        score = hits / max(1, len(keywords))
        if score > best_score:
            best_score = score
            best_category = category
    return best_category, best_score


def detect_duplicate_expenses(
    expenses: list[Expense],
    *,
    amount_tolerance_minor: int = 0,
    day_window: int = 3,
) -> list[tuple[str, str]]:
    """Find likely duplicate expense pairs. Time O(n^2), space O(1)."""
    duplicates: list[tuple[str, str]] = []
    for i, left in enumerate(expenses):
        for right in expenses[i + 1 :]:
            if left.employee_id != right.employee_id:
                continue
            day_delta = abs((left.expense_date - right.expense_date).days)
            if day_delta > day_window:
                continue
            if abs(left.amount_minor - right.amount_minor) > amount_tolerance_minor:
                continue
            if left.merchant.lower() != right.merchant.lower():
                continue
            duplicates.append((left.expense_id, right.expense_id))
    return duplicates


def per_diem_check(
    *,
    amount_minor: int,
    days: int,
    daily_limit_minor: int,
) -> bool:
    """Return True if expense is within per-diem policy. Time O(1)."""
    if days <= 0:
        return False
    return amount_minor <= days * daily_limit_minor


def mileage_reimbursement(
    origin: tuple[float, float],
    destination: tuple[float, float],
    *,
    rate_per_km_minor: int,
) -> int:
    """Mileage reimbursement from lat/lon pairs. Time O(1)."""
    distance_km = haversine_km(origin, destination)
    return round(distance_km * rate_per_km_minor)


def policy_violation_score(
    expense: Expense,
    *,
    single_transaction_limit_minor: int,
    blocked_merchants: set[str] | None = None,
    allowed_categories: set[str] | None = None,
) -> float:
    """Score policy violations from 0 (ok) to 1 (severe). Time O(1)."""
    score = 0.0
    blocked = blocked_merchants or set()
    if expense.merchant.lower() in blocked:
        score = max(score, 1.0)
    if allowed_categories and expense.category not in allowed_categories:
        score = max(score, 0.7)
    if expense.amount_minor > single_transaction_limit_minor:
        overflow = expense.amount_minor / max(1, single_transaction_limit_minor)
        score = max(score, min(1.0, 0.5 + (overflow - 1) * 0.25))
    return score
