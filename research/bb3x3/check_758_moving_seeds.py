#!/usr/bin/env python3
"""Verify the first-return theorem in MOVING_SEEDS758.md (Python 3.10+)."""
from collections import Counter
from fractions import Fraction

from check_758_lifts import BASE_M, D, H, OFFSET, PERIOD, check_family, coarse_gap

COARSE = "LLJLLJLR"
WIDTH = 12_000_000
MOD = 256


def check_guards():
    # At entry after I J^(m-1), coefficients of Q = 3^(m-1) are
    # independent of delta in x=H_m+delta.
    a, c = Fraction(4), Fraction(3**16, D) - 2
    assert abs(3 - Fraction(OFFSET, D)) < 10
    for move in COARSE:
        assert min(a, c) > Fraction(9, 10)
        if move == "L":
            assert a - c > Fraction(9, 10)
            a, c = a - c, 3*c/2
        else:
            assert c - a > Fraction(9, 10)
            if move == "J":
                a, c = 3*a, c-a
    # For |delta| <= WIDTH + 2m + 31, the coordinate errors are initially
    # <= WIDTH + 2m + 41. Each L/J multiplies the error bound by at most
    # three and adds at most seven. Use the same upper bound at all stages.
    # Q triples per unit of m, while the positive error bound grows slower.
    initial_error = WIDTH + 2*BASE_M + 41
    error_bound = 3**len(COARSE) * (initial_error + 4)
    assert Fraction(9, 10)*3**(BASE_M - 1) > 2*error_bound + 10
    assert 3*(initial_error + 4) > initial_error + 6


def return_constant(m, b):
    """Exact first return of H_m - 2m - b, less H_m - b."""
    modulus = MOD
    q = pow(3, m-1, modulus)
    inv = pow(D, -1, modulus)
    a = (4*q - 1) % modulus
    c = ((3**16 * inv - 2)*q - OFFSET*inv - 2*m - b + 3) % modulus
    bulk_gain = 0
    for move in COARSE[:-1]:
        if move == "L":
            assert c % 2 == 1
            group = (c+1)//4
            bulk_gain += 5 if c % 4 == 1 else 9
            # Increasing c by the old modulus changes 6*group by 3*modulus/2.
            modulus //= 2
            a, c = (a-4*group-3) % modulus, (6*group+5) % modulus
        else:
            assert a % 2 == c % 2 == 1
            a, c = (3*a+2) % modulus, (c-a+1) % modulus
    assert a % 2 == 0 and c % 2 == 1
    # Mass gains: I costs 8, m-1 prefix Js plus 2 tail Js cost 4m+4,
    # all five bulk moves contribute bulk_gain, and the reset gains 5.
    return (17 + bulk_gain)//2


def verify():
    check_family()
    check_guards()
    assert tuple(coarse_gap(BASE_M, H+d) for d in (-4, -2, 0, 2)) == (7779, 3, 3, -5547)
    # H_m is always 1 mod 4. The two odd seeds reach identical states on
    # their first L because their second counters there are paired as 4q-1,4q+1.
    assert H % 4 == 1 and PERIOD % 4 == 0 and pow(3, PERIOD, 4*D) == 1
    # k -> k+64 leaves m and Q mod 256 unchanged.
    assert (PERIOD*64) % MOD == 0 and pow(3, PERIOD*64, MOD) == 1
    counts = Counter()
    for k in range(64):
        m = BASE_M + PERIOD*k
        hits = tuple(b for b in range(21, 34, 2)
                     if return_constant(m, b)-b in (-2, 0))
        counts[hits] += 1
    assert counts == {(25, 27): 32, (29, 31): 16, (25, 27, 29, 31): 16}
    # Every even seed at distance <= WIDTH below H_m overshoots once m is
    # in the progression from k=25 onward. This integer bound is exact.
    assert 2*(BASE_M+24*PERIOD)+21 <= WIDTH < 2*(BASE_M+25*PERIOD)+21
    return counts


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run without -O to enable verification.")
    print("Verified moving predecessor sets in 64 exponent classes:", dict(verify()))
