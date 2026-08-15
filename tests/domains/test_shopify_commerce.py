"""Tests for Shopify commerce domain algorithms."""

from __future__ import annotations

import base64
import hashlib
import hmac

from agentic_algorithms.domains.shopify_commerce import (
    inventory_available,
    merge_cart_lines,
    normalize_metafield_key,
    order_tags_from_risk,
    parse_shopify_gid,
    rate_limit_backoff_ms,
    shopify_transaction_fee,
    storefront_product_url,
    verify_webhook_hmac,
)


def test_verify_webhook_hmac_valid() -> None:
    secret = "shpss_test"
    body = b'{"id": 1}'
    digest = base64.b64encode(hmac.new(secret.encode(), body, hashlib.sha256).digest()).decode()
    assert verify_webhook_hmac(body, digest, secret)


def test_parse_shopify_gid() -> None:
    assert parse_shopify_gid("gid://shopify/Product/123") == ("Product", 123)
    assert parse_shopify_gid("invalid") is None


def test_merge_cart_lines() -> None:
    lines = [
        {"variant_id": 1, "quantity": 2},
        {"variant_id": 1, "quantity": 3},
        {"variant_id": 2, "quantity": 1},
    ]
    merged = merge_cart_lines(lines)
    assert len(merged) == 2
    assert merged[0]["quantity"] == 5


def test_inventory_and_fees() -> None:
    assert inventory_available(10, 3, 2) == 9
    assert shopify_transaction_fee(10_000, 290, 30) == 320


def test_helpers() -> None:
    assert normalize_metafield_key("Custom NS", "Color-Name") == "custom_ns.color_name"
    assert rate_limit_backoff_ms(3) >= 2000
    assert (
        storefront_product_url("demo.myshopify.com", "hoodie")
        == "https://demo.myshopify.com/products/hoodie"
    )
    assert order_tags_from_risk(0.9) == ["risk:high", "review-required"]
