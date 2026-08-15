"""Tests for domain-specific algorithms."""

from __future__ import annotations

from datetime import date, datetime, timedelta

from agentic_algorithms.domains.accounting import (
    JournalEntry,
    JournalLine,
    benford_anomaly_score,
    post_journal_entry,
    reconcile_bank_transactions,
    validate_journal_entry,
)
from agentic_algorithms.domains.aeo import AeoPageInput, aeo_page_score
from agentic_algorithms.domains.ecommerce import (
    epsilon_greedy_select,
    item_item_cf_scores,
    ndcg_at_k,
    recall_at_k,
    thompson_sampling_select,
)
from agentic_algorithms.domains.expense import (
    Expense,
    categorize_expense,
    detect_duplicate_expenses,
)
from agentic_algorithms.domains.fintech import (
    PaymentEvent,
    luhn_check,
    velocity_check,
)
from agentic_algorithms.domains.geo import (
    Facility,
    Jurisdiction,
    haversine_km,
    jurisdiction_rate_lookup,
    nearest_facility,
    point_in_polygon,
)
from agentic_algorithms.domains.search import SearchIndex, hybrid_search_rrf
from agentic_algorithms.domains.supply_chain import (
    SkuLocation,
    atp_available,
    newsvendor_quantity,
    safety_stock,
    vehicle_route_nearest_neighbor,
)


def test_double_entry_validation_and_posting() -> None:
    entry = JournalEntry(
        memo="sale",
        lines=[
            JournalLine(account="cash", debit_minor=1000),
            JournalLine(account="revenue", credit_minor=1000),
        ],
    )
    assert validate_journal_entry(entry) == []
    balances = post_journal_entry(entry, {})
    assert balances["cash"].balance_minor == 1000


def test_bank_reconciliation() -> None:
    matched, unmatched_l, unmatched_b = reconcile_bank_transactions([100, 200], [200, 100])
    assert len(matched) == 2
    assert not unmatched_l
    assert not unmatched_b


def test_benford_score() -> None:
    amounts = [12300, 15600, 18900, 11200, 14500] * 5
    assert 0.0 <= benford_anomaly_score(amounts) <= 1.0


def test_expense_categorization_and_duplicates() -> None:
    category, confidence = categorize_expense("Uber Trip", "airport ride")
    assert category == "travel"
    assert confidence > 0
    expenses = [
        Expense("1", "e1", 50000, "Uber", "travel", date(2026, 1, 1)),
        Expense("2", "e1", 50000, "Uber", "travel", date(2026, 1, 2)),
    ]
    assert detect_duplicate_expenses(expenses)


def test_fintech_velocity_and_luhn() -> None:
    now = datetime(2026, 1, 1, 12, 0, 0)
    events = [
        PaymentEvent("a1", 10000, now, "ben"),
        PaymentEvent("a1", 10000, now + timedelta(minutes=5), "ben"),
    ]
    assert not velocity_check(
        events, window=timedelta(hours=1), max_count=5, max_amount_minor=50000
    )
    assert luhn_check("4532015112830366")


def test_supply_chain_newsvendor_and_atp() -> None:
    qty = newsvendor_quantity([10, 12, 15, 20], underage_cost=5, overage_cost=2)
    assert qty > 0
    assert safety_stock(10, 2, 1.65) > 0
    balance = SkuLocation("sku", "wh", on_hand=100, reserved=20, inbound=10)
    assert atp_available(balance) == 90


def test_vehicle_routing() -> None:
    distances = [[0, 1, 2], [1, 0, 1], [2, 1, 0]]
    route, total = vehicle_route_nearest_neighbor(0, distances)
    assert route[0] == 0
    assert total >= 0


def test_ecommerce_metrics_and_cf() -> None:
    assert recall_at_k({"a", "b"}, ["a", "c", "b"], 2) == 0.5
    assert ndcg_at_k({"a": 3, "b": 1}, ["a", "b"], 2) > 0
    scores = item_item_cf_scores([("u1", "a"), ("u1", "b"), ("u2", "a")], "a")
    assert scores


def test_bandits() -> None:
    arms = ["low", "high"]
    rewards = {"low": [0.1, 0.2], "high": [0.8, 0.9]}
    assert epsilon_greedy_select(arms, rewards, epsilon=0.0) == "high"
    assert thompson_sampling_select(arms, {"low": 1, "high": 9}, {"low": 9, "high": 1}) == "high"


def test_search_bm25_and_rrf() -> None:
    index = SearchIndex()
    index.add("1", "python data structures algorithms")
    index.add("2", "accounting double entry ledger")
    results = index.search("algorithms python")
    assert results[0][0] == "1"
    fused = hybrid_search_rrf([["a", "b"], ["b", "c"]])
    assert fused[0][0] == "b"


def test_geo_distance_and_jurisdiction() -> None:
    delhi = (28.6139, 77.2090)
    gurgaon = (28.4595, 77.0266)
    assert haversine_km(delhi, gurgaon) > 0
    square = [(0, 0), (0, 1), (1, 1), (1, 0)]
    assert point_in_polygon((0.5, 0.5), square)
    jurisdiction = Jurisdiction("test", square, 0.08)
    assert jurisdiction_rate_lookup((0.5, 0.5), [jurisdiction]) == jurisdiction
    facility = nearest_facility((0.5, 0.5), [Facility("f1", 0.0, 0.0), Facility("f2", 1.0, 1.0)])
    assert facility is not None


def test_aeo_page_score() -> None:
    page = AeoPageInput(
        title="What is agentic accounting?",
        body="Agentic accounting is software that uses AI agents to automate bookkeeping tasks.",
        schema_types=["Article"],
        has_faq_section=True,
        author_credentials="CPA",
        last_updated_iso="2026-01-01",
    )
    scores = aeo_page_score(page, present_fields={"Article": {"headline", "author"}})
    assert 0.0 <= scores["overall"] <= 1.0
