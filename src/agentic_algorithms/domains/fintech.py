"""Fintech algorithms: payments, risk, interest, validation."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass(frozen=True)
class PaymentEvent:
    account_id: str
    amount_minor: int
    timestamp: datetime
    beneficiary: str
    country: str = "IN"


def velocity_check(
    events: list[PaymentEvent],
    *,
    window: timedelta,
    max_count: int,
    max_amount_minor: int,
) -> bool:
    """Return True if velocity limits are exceeded. Time O(n), space O(1)."""
    if not events:
        return False
    latest = max(event.timestamp for event in events)
    cutoff = latest - window
    recent = [event for event in events if event.timestamp >= cutoff]
    if len(recent) > max_count:
        return True
    total = sum(event.amount_minor for event in recent)
    return total > max_amount_minor


def aml_structuring_score(
    events: list[PaymentEvent],
    *,
    reporting_threshold_minor: int,
    band_minor: int,
) -> float:
    """Detect smurfing/structuring patterns. Time O(n), space O(1)."""
    if not events:
        return 0.0
    near_threshold = sum(
        1
        for event in events
        if reporting_threshold_minor - band_minor <= event.amount_minor < reporting_threshold_minor
    )
    ratio = near_threshold / len(events)
    return min(1.0, ratio * 2.0)


def payment_risk_score(
    event: PaymentEvent,
    history: list[PaymentEvent],
    *,
    max_transfer_minor: int,
    allowed_countries: set[str] | None = None,
) -> float:
    """Composite payment risk score 0..1. Time O(n), space O(1)."""
    score = 0.0
    if event.amount_minor > max_transfer_minor:
        score = max(score, 0.8)
    if allowed_countries and event.country not in allowed_countries:
        score = max(score, 0.9)
    known_beneficiaries = {
        item.beneficiary for item in history if item.account_id == event.account_id
    }
    if (
        event.beneficiary not in known_beneficiaries
        and event.amount_minor > max_transfer_minor // 2
    ):
        score = max(score, 0.6)
    if velocity_check(
        [*history, event],
        window=timedelta(hours=1),
        max_count=5,
        max_amount_minor=max_transfer_minor,
    ):
        score = max(score, 0.85)
    return score


def simple_interest(principal_minor: int, annual_rate: float, days: int) -> int:
    """Simple interest accrual. Time O(1)."""
    return round(principal_minor * annual_rate * days / 365)


def compound_interest(principal_minor: int, annual_rate: float, periods: int) -> int:
    """Compound interest after n periods (annual compounding). Time O(1)."""
    return round(principal_minor * (1 + annual_rate) ** periods)


def amortization_schedule(
    principal_minor: int,
    annual_rate: float,
    months: int,
) -> list[dict[str, int]]:
    """Fixed-rate amortization schedule. Time O(months), space O(months)."""
    if months <= 0:
        return []
    monthly_rate = annual_rate / 12
    if monthly_rate == 0:
        payment = principal_minor // months
        balance = principal_minor
        schedule: list[dict[str, int]] = []
        for month in range(1, months + 1):
            principal_part = payment if month < months else balance
            schedule.append(
                {
                    "month": month,
                    "payment_minor": principal_part,
                    "interest_minor": 0,
                    "principal_minor": principal_part,
                    "balance_minor": balance - principal_part,
                }
            )
            balance -= principal_part
        return schedule
    payment = round(
        principal_minor
        * monthly_rate
        * (1 + monthly_rate) ** months
        / ((1 + monthly_rate) ** months - 1)
    )
    balance = principal_minor
    schedule = []
    for month in range(1, months + 1):
        interest = round(balance * monthly_rate)
        principal_part = payment - interest if month < months else balance
        payment_actual = principal_part + interest
        balance = max(0, balance - principal_part)
        schedule.append(
            {
                "month": month,
                "payment_minor": payment_actual,
                "interest_minor": interest,
                "principal_minor": principal_part,
                "balance_minor": balance,
            }
        )
    return schedule


def luhn_check(card_number: str) -> bool:
    """Luhn checksum for card validation. Time O(n), space O(1)."""
    digits = [int(char) for char in card_number if char.isdigit()]
    if len(digits) < 2:
        return False
    checksum = 0
    parity = len(digits) % 2
    for index, digit in enumerate(digits):
        if index % 2 == parity:
            digit *= 2
            if digit > 9:
                digit -= 9
        checksum += digit
    return checksum % 10 == 0


def ach_routing_checksum(routing_number: str) -> bool:
    """US ACH routing number checksum. Time O(1)."""
    if len(routing_number) != 9 or not routing_number.isdigit():
        return False
    digits = [int(char) for char in routing_number]
    total = (
        3 * (digits[0] + digits[3] + digits[6])
        + 7 * (digits[1] + digits[4] + digits[7])
        + (digits[2] + digits[5] + digits[8])
    )
    return total % 10 == 0
