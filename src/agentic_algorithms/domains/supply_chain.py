"""Supply chain algorithms: inventory, forecasting, routing."""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class SkuLocation:
    sku: str
    location: str
    on_hand: int
    reserved: int
    inbound: int
    safety_hold: int = 0


def newsvendor_quantity(
    demand_quantiles: list[float],
    *,
    underage_cost: float,
    overage_cost: float,
) -> float:
    """Critical fractile order quantity from empirical demand sample.

    Q* = F^{-1}(Cu / (Cu + Co)). Time O(n log n) for sort, space O(1).
    """
    if not demand_quantiles:
        return 0.0
    critical = underage_cost / (underage_cost + overage_cost)
    sorted_demand = sorted(demand_quantiles)
    index = min(len(sorted_demand) - 1, int(math.ceil(critical * len(sorted_demand)) - 1))
    return sorted_demand[max(0, index)]


def safety_stock(
    demand_std: float,
    lead_time_periods: float,
    service_z: float,
) -> float:
    """Safety stock under normality assumption. Time O(1)."""
    return service_z * demand_std * math.sqrt(lead_time_periods)


def economic_order_quantity(
    annual_demand: float,
    order_cost: float,
    holding_cost_per_unit: float,
) -> float:
    """Classic EOQ. Time O(1)."""
    if holding_cost_per_unit <= 0:
        return 0.0
    return math.sqrt(2 * annual_demand * order_cost / holding_cost_per_unit)


def reorder_point(
    avg_demand_per_period: float,
    lead_time_periods: float,
    safety: float,
) -> float:
    """Reorder point = demand during lead time + safety stock. Time O(1)."""
    return avg_demand_per_period * lead_time_periods + safety


def atp_available(
    balance: SkuLocation,
    *,
    inbound_within_promise: int | None = None,
) -> int:
    """Available-to-promise inventory. Time O(1)."""
    inbound = balance.inbound if inbound_within_promise is None else inbound_within_promise
    return balance.on_hand - balance.reserved - balance.safety_hold + inbound


def allocate_inventory(
    pool: int,
    locations: list[tuple[str, int, float]],
) -> dict[str, int]:
    """Allocate shared pool by target gap weighted by underage cost.

    locations: (location_id, target_on_hand, underage_cost).
    Time O(n log n), space O(n).
    """
    allocation: dict[str, int] = {}
    remaining = pool
    gaps = []
    for location_id, target, underage in locations:
        gap = max(0, target)
        if gap > 0:
            gaps.append((underage, gap, location_id))
    gaps.sort(reverse=True)
    for _underage, gap, location_id in gaps:
        if remaining <= 0:
            allocation[location_id] = 0
            continue
        give = min(gap, remaining)
        allocation[location_id] = give
        remaining -= give
    return allocation


def exponential_smoothing_forecast(
    history: list[float],
    *,
    alpha: float,
) -> float:
    """Simple exponential smoothing one-step forecast. Time O(n), space O(1)."""
    if not history:
        return 0.0
    level = history[0]
    for value in history[1:]:
        level = alpha * value + (1 - alpha) * level
    return level


def moving_average_forecast(history: list[float], window: int) -> float:
    """Moving average forecast. Time O(window), space O(1)."""
    if not history:
        return 0.0
    sample = history[-window:]
    return sum(sample) / len(sample)


def vehicle_route_nearest_neighbor(
    depot: int,
    distances: list[list[float]],
) -> tuple[list[int], float]:
    """TSP heuristic via nearest neighbor. Time O(n^2), space O(n)."""
    n = len(distances)
    if n == 0:
        return [], 0.0
    unvisited = set(range(n)) - {depot}
    route = [depot]
    total = 0.0
    current = depot
    while unvisited:
        nearest = min(unvisited, key=lambda node: distances[current][node])
        total += distances[current][nearest]
        route.append(nearest)
        unvisited.remove(nearest)
        current = nearest
    total += distances[current][depot]
    route.append(depot)
    return route, total


def mrp_net_requirements(
    gross_requirements: list[int],
    scheduled_receipts: list[int],
    on_hand: int,
) -> list[int]:
    """Basic MRP net requirements by period. Time O(n), space O(n)."""
    net: list[int] = []
    projected = on_hand
    for period, gross in enumerate(gross_requirements):
        receipt = scheduled_receipts[period] if period < len(scheduled_receipts) else 0
        projected = projected + receipt - gross
        need = max(0, -projected)
        net.append(need)
        projected += need
    return net
