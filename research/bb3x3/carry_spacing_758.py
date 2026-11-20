#!/usr/bin/env python3
"""Exact rational audit of the carry-spacing theorem in REINJECTION_758.md."""
from fractions import Fraction
RHO = Fraction(3, 2)


def v2(n):
    assert n > 0
    return (n & -n).bit_length() - 1


def T(n):
    assert n > 0
    return 3 * ((n + 1) // 2)


def psi_interval(n, depth):
    """Strict rational enclosure, from the proved bounded correction."""
    assert n > 0
    for _ in range(depth):
        n = T(n)
    scale = Fraction(2, 3) ** depth
    return scale * n, scale * (n + 3)


def gap_interval(n, depth):
    lo0, hi0 = psi_interval(n, depth)
    lo1, hi1 = psi_interval(n + 1, depth)
    return lo1 - hi0, hi1 - lo0


def spacing_audit():
    qs = set(range(1, 513))
    for r in range(41):
        for odd in (1, 3, 7, 11):
            q = (1 << r) * odd - 1
            if q > 0:
                qs.add(q)
    for q in sorted(qs):
        r = v2(q + 1)
        qr = 3**r * ((q + 1) // 2**r) - 1
        assert qr > 0 and qr % 2 == 0
        current = q
        for _ in range(r):
            assert current % 2 == 1
            assert T(3 * current) == T(3 * current + 1)
            assert T(3 * current + 2) == T(3 * current + 3)
            following = (3 * current + 1) // 2
            assert v2(following + 1) == v2(current + 1) - 1
            current = following
        assert current == qr
        assert T(3 * qr + 3) - T(3 * qr) == 6
        lo, hi = gap_interval(2 * q, r + 100)
        assert Fraction(4, 3) * Fraction(2, 3)**r < lo
        assert hi < 4 * Fraction(2, 3)**r
        assert T(2 * q - 1) == T(2 * q)
    return len(qs)


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run without -O for verification.")
    print("Verified exact carry spacing and sibling plateaus:", spacing_audit(), "classes.")
