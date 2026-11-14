# primes_common.py - shared helpers used by every part of the Open Ended Lab
import math

REG_LAST3 = 154                       # last three digits of Reg# 235154
N = 2_000_000 + REG_LAST3 * 1000      # N = 2,154,000


def is_prime(n):
    """Trial division: test divisors only up to sqrt(n)."""
    if n < 2:
        return False
    if n < 4:
        return True            # 2 and 3
    if n % 2 == 0:
        return False
    for d in range(3, math.isqrt(n) + 1, 2):   # odd divisors up to sqrt(n)
        if n % d == 0:
            return False
    return True


def count_primes(lo, hi):
    """Count primes in the half-open range [lo, hi)."""
    c = 0
    for n in range(lo, hi):
        if is_prime(n):
            c += 1
    return c


def make_chunks(lo, hi, p):
    """Split [lo, hi) into p equal chunks (the last one takes any leftover)."""
    size = (hi - lo) // p
    chunks = []
    for i in range(p):
        a = lo + i * size
        b = hi if i == p - 1 else a + size
        chunks.append((a, b))
    return chunks
