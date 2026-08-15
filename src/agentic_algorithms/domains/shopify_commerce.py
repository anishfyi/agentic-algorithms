"""Shopify commerce algorithms: webhooks, GIDs, cart, inventory, fees, rate limits."""

from __future__ import annotations

import base64
import hashlib
import hmac
import math
import re
import time
from typing import Any


_GID_RE = re.compile(r"^gid://shopify/([A-Za-z]+)/(\d+)$")


def verify_webhook_hmac(body: bytes, header_hmac: str, secret: str) -> bool:
    """Verify Shopify webhook HMAC-SHA256 signature. Time O(n), space O(1)."""
    digest = hmac.new(secret.encode(), body, hashlib.sha256).digest()
    expected = base64.b64encode(digest).decode()
    return hmac.compare_digest(expected, header_hmac)


def parse_shopify_gid(gid: str) -> tuple[str, int] | None:
    """Parse a Shopify global ID into resource type and numeric id. Time O(1), space O(1)."""
    match = _GID_RE.match(gid.strip())
    if not match:
        return None
    return match.group(1), int(match.group(2))


def merge_cart_lines(lines: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Merge cart lines by variant_id, summing quantities. Time O(n), space O(n)."""
    merged: dict[str, dict[str, Any]] = {}
    for line in lines:
        variant_id = str(line.get("variant_id", ""))
        if not variant_id:
            continue
        if variant_id not in merged:
            merged[variant_id] = {**line, "quantity": int(line.get("quantity", 0))}
        else:
            merged[variant_id]["quantity"] += int(line.get("quantity", 0))
    return list(merged.values())


def inventory_available(on_hand: int, committed: int, incoming: int = 0) -> int:
    """Compute sellable inventory (on hand minus committed plus incoming). Time O(1), space O(1)."""
    return max(0, on_hand - committed + incoming)


def shopify_transaction_fee(amount_minor: int, rate_bps: int, flat_minor: int = 0) -> int:
    """Compute payment processing fee in minor currency units. Time O(1), space O(1)."""
    if amount_minor <= 0:
        return 0
    percent_fee = math.ceil(amount_minor * rate_bps / 10_000)
    return percent_fee + flat_minor


def normalize_metafield_key(namespace: str, key: str) -> str:
    """Build canonical Shopify metafield key namespace.key. Time O(1), space O(1)."""
    ns = re.sub(r"[^a-z0-9_]", "_", namespace.lower().strip())
    k = re.sub(r"[^a-z0-9_]", "_", key.lower().strip())
    return f"{ns}.{k}"


def rate_limit_backoff_ms(attempt: int, *, base_ms: int = 500, cap_ms: int = 30_000) -> int:
    """Exponential backoff for Shopify REST/GraphQL 429 retries. Time O(1), space O(1)."""
    if attempt < 1:
        attempt = 1
    delay = min(cap_ms, base_ms * (2 ** (attempt - 1)))
    jitter = int(delay * 0.1)
    return delay + (attempt % (jitter + 1))


def storefront_product_url(shop_domain: str, handle: str) -> str:
    """Build canonical storefront product URL. Time O(1), space O(1)."""
    domain = shop_domain.removeprefix("https://").removeprefix("http://").rstrip("/")
    handle = handle.strip("/")
    return f"https://{domain}/products/{handle}"


def order_tags_from_risk(score: float, *, high: float = 0.75, medium: float = 0.45) -> list[str]:
    """Map fraud risk score to Shopify order tags. Time O(1), space O(1)."""
    if score >= high:
        return ["risk:high", "review-required"]
    if score >= medium:
        return ["risk:medium"]
    return ["risk:low"]
