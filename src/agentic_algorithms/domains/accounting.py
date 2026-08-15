"""Accounting algorithms: double-entry, reconciliation, controls."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Literal

NormalBalance = Literal["debit", "credit"]


@dataclass(frozen=True)
class JournalLine:
    account: str
    debit_minor: int = 0
    credit_minor: int = 0


@dataclass
class JournalEntry:
    memo: str
    lines: list[JournalLine]
    source: str = "manual"


@dataclass
class AccountBalance:
    account: str
    debit_minor: int = 0
    credit_minor: int = 0
    normal_balance: NormalBalance = "debit"

    @property
    def balance_minor(self) -> int:
        if self.normal_balance == "debit":
            return self.debit_minor - self.credit_minor
        return self.credit_minor - self.debit_minor


def validate_journal_entry(entry: JournalEntry) -> list[str]:
    """Validate double-entry invariants. Time O(n), space O(1)."""
    errors: list[str] = []
    if not entry.lines:
        errors.append("journal entry must have at least one line")
        return errors
    debit_total = 0
    credit_total = 0
    for line in entry.lines:
        if line.debit_minor < 0 or line.credit_minor < 0:
            errors.append(f"negative amount on account {line.account}")
        if line.debit_minor > 0 and line.credit_minor > 0:
            errors.append(f"both debit and credit set on account {line.account}")
        if line.debit_minor == 0 and line.credit_minor == 0:
            errors.append(f"zero line on account {line.account}")
        debit_total += line.debit_minor
        credit_total += line.credit_minor
    if debit_total != credit_total:
        errors.append(f"unbalanced entry: debits {debit_total} != credits {credit_total}")
    return errors


def post_journal_entry(
    entry: JournalEntry,
    balances: dict[str, AccountBalance],
) -> dict[str, AccountBalance]:
    """Post a balanced entry to account balances. Time O(n), space O(n)."""
    errors = validate_journal_entry(entry)
    if errors:
        msg = "; ".join(errors)
        raise ValueError(msg)
    updated = {
        key: AccountBalance(
            account=value.account,
            debit_minor=value.debit_minor,
            credit_minor=value.credit_minor,
            normal_balance=value.normal_balance,
        )
        for key, value in balances.items()
    }
    for line in entry.lines:
        account = updated.setdefault(
            line.account,
            AccountBalance(account=line.account),
        )
        account.debit_minor += line.debit_minor
        account.credit_minor += line.credit_minor
    return updated


def compute_trial_balance(balances: dict[str, AccountBalance]) -> tuple[int, int]:
    """Return total debits and credits across accounts. Time O(n)."""
    debit_total = sum(account.debit_minor for account in balances.values())
    credit_total = sum(account.credit_minor for account in balances.values())
    return debit_total, credit_total


def reconcile_bank_transactions(
    ledger_amounts: list[int],
    bank_amounts: list[int],
    *,
    tolerance_minor: int = 0,
) -> tuple[list[tuple[int, int]], list[int], list[int]]:
    """Greedy bank reconciliation by exact amount match.

    Time O(n log n + m log m), space O(n + m).
    Returns (matched pairs as ledger_idx, bank_idx), unmatched ledger, unmatched bank.
    """
    ledger_sorted = sorted(enumerate(ledger_amounts), key=lambda item: item[1])
    bank_sorted = sorted(enumerate(bank_amounts), key=lambda item: item[1])
    matched: list[tuple[int, int]] = []
    used_bank: set[int] = set()
    li = 0
    for ledger_idx, ledger_amount in ledger_sorted:
        while li < len(bank_sorted):
            bank_idx, bank_amount = bank_sorted[li]
            if bank_idx in used_bank:
                li += 1
                continue
            if abs(ledger_amount - bank_amount) <= tolerance_minor:
                matched.append((ledger_idx, bank_idx))
                used_bank.add(bank_idx)
                li += 1
                break
            if bank_amount < ledger_amount:
                li += 1
                continue
            break
    unmatched_ledger = [
        amount
        for index, amount in enumerate(ledger_amounts)
        if index not in {pair[0] for pair in matched}
    ]
    unmatched_bank = [
        amount
        for index, amount in enumerate(bank_amounts)
        if index not in {pair[1] for pair in matched}
    ]
    return matched, unmatched_ledger, unmatched_bank


def benford_anomaly_score(amounts_minor: list[int]) -> float:
    """Benford's law deviation score for fraud screening. Time O(n), space O(1).

    Returns 0.0 (normal) to 1.0 (highly anomalous).
    """
    if len(amounts_minor) < 20:
        return 0.0
    benford_expected = {
        1: 0.301,
        2: 0.176,
        3: 0.125,
        4: 0.097,
        5: 0.079,
        6: 0.067,
        7: 0.058,
        8: 0.051,
        9: 0.046,
    }
    counts: defaultdict[int, int] = defaultdict(int)
    valid = 0
    for amount in amounts_minor:
        if amount <= 0:
            continue
        first = int(str(abs(amount)).lstrip("0")[0])
        if 1 <= first <= 9:
            counts[first] += 1
            valid += 1
    if valid == 0:
        return 0.0
    deviation = 0.0
    for digit, expected in benford_expected.items():
        observed = counts[digit] / valid
        deviation += abs(observed - expected)
    return min(1.0, deviation / 1.2)


def round_amount_anomaly_score(amounts_minor: list[int]) -> float:
    """Detect clustering on round dollar amounts. Time O(n), space O(1)."""
    if not amounts_minor:
        return 0.0
    roundish = sum(1 for amount in amounts_minor if amount % 10000 == 0)
    ratio = roundish / len(amounts_minor)
    return max(0.0, min(1.0, (ratio - 0.15) / 0.5))
