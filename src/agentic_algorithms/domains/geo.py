"""GEO algorithms: distance, geohash, jurisdiction, zones."""

from __future__ import annotations

import math
from dataclasses import dataclass


def haversine_km(
    origin: tuple[float, float],
    destination: tuple[float, float],
) -> float:
    """Great-circle distance in kilometers. Time O(1)."""
    lat1, lon1 = math.radians(origin[0]), math.radians(origin[1])
    lat2, lon2 = math.radians(destination[0]), math.radians(destination[1])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 6371.0 * 2 * math.asin(math.sqrt(a))


_BASE32 = "0123456789bcdefghjkmnpqrstuvwxyz"


def geohash_encode(lat: float, lon: float, *, precision: int = 8) -> str:
    """Encode lat/lon to geohash string. Time O(precision), space O(precision)."""
    lat_range = [-90.0, 90.0]
    lon_range = [-180.0, 180.0]
    bits = 0
    bit_count = 0
    even = True
    geohash: list[str] = []
    while len(geohash) < precision:
        if even:
            mid = (lon_range[0] + lon_range[1]) / 2
            if lon >= mid:
                bits = (bits << 1) | 1
                lon_range[0] = mid
            else:
                bits <<= 1
                lon_range[1] = mid
        else:
            mid = (lat_range[0] + lat_range[1]) / 2
            if lat >= mid:
                bits = (bits << 1) | 1
                lat_range[0] = mid
            else:
                bits <<= 1
                lat_range[1] = mid
        even = not even
        bit_count += 1
        if bit_count == 5:
            geohash.append(_BASE32[bits])
            bits = 0
            bit_count = 0
    return "".join(geohash)


def point_in_polygon(point: tuple[float, float], polygon: list[tuple[float, float]]) -> bool:
    """Ray casting point-in-polygon test. Time O(v), space O(1)."""
    x, y = point
    inside = False
    n = len(polygon)
    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % n]
        if ((y1 > y) != (y2 > y)) and (x < (x2 - x1) * (y - y1) / (y2 - y1 + 1e-12) + x1):
            inside = not inside
    return inside


@dataclass(frozen=True)
class Jurisdiction:
    name: str
    polygon: list[tuple[float, float]]
    combined_tax_rate: float


def jurisdiction_rate_lookup(
    point: tuple[float, float],
    jurisdictions: list[Jurisdiction],
) -> Jurisdiction | None:
    """Rooftop geocode to jurisdiction polygon match. Time O(j * v)."""
    for jurisdiction in jurisdictions:
        if point_in_polygon(point, jurisdiction.polygon):
            return jurisdiction
    return None


@dataclass(frozen=True)
class Facility:
    facility_id: str
    lat: float
    lon: float


def nearest_facility(
    point: tuple[float, float],
    facilities: list[Facility],
) -> Facility | None:
    """Nearest facility by haversine distance. Time O(n), space O(1)."""
    if not facilities:
        return None
    return min(
        facilities,
        key=lambda facility: haversine_km(point, (facility.lat, facility.lon)),
    )


def delivery_zone_match(
    point: tuple[float, float],
    zones: dict[str, list[tuple[float, float]]],
) -> str | None:
    """Return delivery zone name containing point. Time O(z * v)."""
    for zone_name, polygon in zones.items():
        if point_in_polygon(point, polygon):
            return zone_name
    return None


def zip_centroid_fallback_rate(
    zip_code: str,
    zip_rates: dict[str, float],
    *,
    default_rate: float = 0.0,
) -> float:
    """ZIP-level tax rate fallback (estimate only, not legal-grade). Time O(1)."""
    return zip_rates.get(zip_code, default_rate)
