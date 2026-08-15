"""Mathematical algorithms."""

from __future__ import annotations

import random


def gcd(a: int, b: int) -> int:
    """Greatest common divisor using Euclidean algorithm.

    Time: O(log min(a, b)). Space: O(1).
    """
    while b:
        a, b = b, a % b
    return abs(a)


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """Return (g, x, y) such that a*x + b*y = g = gcd(a, b).

    Time: O(log min(a, b)). Space: O(1).
    """
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t
    return old_r, old_s, old_t


def mod_pow(base: int, exponent: int, modulus: int) -> int:
    """Compute (base^exponent) % modulus using binary exponentiation.

    Time: O(log exponent). Space: O(1).
    """
    if modulus == 1:
        return 0
    result = 1
    base %= modulus
    while exponent > 0:
        if exponent & 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        exponent >>= 1
    return result


def sieve_primes(limit: int) -> list[int]:
    """Return all primes up to limit using Sieve of Eratosthenes.

    Time: O(n log log n). Space: O(n).
    """
    if limit < 2:
        return []
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            step = i
            start = i * i
            is_prime[start : limit + 1 : step] = [False] * len(range(start, limit + 1, step))
    return [i for i, prime in enumerate(is_prime) if prime]


def _miller_rabin_witness(n: int, a: int) -> bool:
    """Return True if a is a compositeness witness for n."""
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    x = mod_pow(a, d, n)
    if x == 1 or x == n - 1:
        return False
    for _ in range(s - 1):
        x = (x * x) % n
        if x == n - 1:
            return False
    return True


def is_prime_miller_rabin(n: int, rounds: int = 8) -> bool:
    """Primality test using Miller-Rabin (deterministic for 64-bit with default rounds).

    Time: O(k log^3 n). Space: O(1).
    """
    if n < 2:
        return False
    small_primes = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29}
    if n in small_primes:
        return True
    if n % 2 == 0:
        return False
    for _ in range(rounds):
        a = random.randrange(2, n - 1)
        if _miller_rabin_witness(n, a):
            return False
    return True


def factorial(n: int) -> int:
    """Compute n! iteratively.

    Time: O(n). Space: O(1).
    """
    if n < 0:
        raise ValueError("factorial undefined for negative integers")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def catalan(n: int) -> int:
    """Return nth Catalan number C_n.

    Time: O(n). Space: O(1).
    """
    if n < 0:
        raise ValueError("catalan undefined for negative integers")
    result = 1
    for k in range(1, n + 1):
        result = result * (n + k) // k
    return result // (n + 1)


def fibonacci_fast_doubling(n: int) -> int:
    """Return nth Fibonacci number using fast doubling.

    Time: O(log n). Space: O(log n).
    """

    def _fib(k: int) -> tuple[int, int]:
        if k == 0:
            return 0, 1
        a, b = _fib(k // 2)
        c = a * (2 * b - a)
        d = a * a + b * b
        if k % 2 == 0:
            return c, d
        return d, c + d

    return _fib(n)[0]
