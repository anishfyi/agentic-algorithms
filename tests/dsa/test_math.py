"""Tests for math algorithms."""

from __future__ import annotations

from agentic_algorithms.dsa.math import (
    catalan,
    extended_gcd,
    factorial,
    fibonacci_fast_doubling,
    gcd,
    is_prime_miller_rabin,
    mod_pow,
    sieve_primes,
)


def test_gcd_and_extended_gcd() -> None:
    assert gcd(48, 18) == 6
    g, x, y = extended_gcd(30, 12)
    assert g == 6
    assert 30 * x + 12 * y == 6


def test_mod_pow() -> None:
    assert mod_pow(2, 10, 1000) == 24


def test_sieve_and_primes() -> None:
    assert sieve_primes(10) == [2, 3, 5, 7]
    assert is_prime_miller_rabin(97)
    assert not is_prime_miller_rabin(91)


def test_factorial_catalan_fibonacci() -> None:
    assert factorial(5) == 120
    assert catalan(3) == 5
    assert fibonacci_fast_doubling(10) == 55
