#!/usr/bin/env python3
"""Check the same-suffix scale family of #758 in LIFTS758.md.

Only the standard library is required. No step budget or heuristic is used.
"""
from fractions import Fraction

D = 13_959_275
OFFSET = 130_491_612
BASE_M = 292
PERIOD = 242_660
FINE = "BCBBCCBBJBCBBC"
COARSE = "L" * 8 + "J" + "L" * 5
H = (3**307 - 8_282_708_212) // D


def seed_at(m):
    numer = 3**(m + 15) - OFFSET
    z, remainder = divmod(numer, D)
    assert remainder == 0
    return z - 2 * m


def tail_states(p, z):
    """Unguarded affine fine-tail states, with P = 3^m and z = c + 2m."""
    a, c = 2 * p - 1, z - p + 1
    states = [(a, c)]
    for move in FINE:
        if move == "J":
            a, c = 3 * a + 2, c - a + 1
        else:
            offset = 2 if move == "B" else 4
            addition = 5 if move == "B" else 8
            a, c = a - c - offset, 3 * (c - 1) / 2 + addition
        states.append((a, c))
    return states


def gap(p, z):
    a, c = tail_states(Fraction(p), Fraction(z))[-1]
    return a - c - 3


def check_family():
    # The final gap is affine, so these three rational evaluations recover it.
    constant = gap(0, 0)
    p_slope = gap(1, 0) - constant
    z_slope = gap(0, 1) - constant
    assert -p_slope / z_slope == Fraction(3**15, D)
    assert -constant / z_slope == Fraction(-OFFSET, D)
    assert seed_at(BASE_M) == H
    assert pow(3, BASE_M + 15, D) == OFFSET % D
    assert PERIOD == 2**2 * 5 * 11 * 1103
    assert pow(3, PERIOD, D) == 1
    for prime in (2, 5, 11, 1103):
        assert all(prime % x for x in range(2, int(prime**0.5) + 1))
        assert pow(3, PERIOD // prime, D) != 1
    # Exclude an even seed: it would supply P_eff = 2*3^m in the same equation.
    assert D % 11 == 0 and pow(3, 5, 11) == 1 and pow(2, 5, 11) == 10
    assert OFFSET % 11 != 0

    p0 = 3**BASE_M
    def states_on_line(p):
        z = Fraction(3**15 * p - OFFSET, D)
        return tail_states(Fraction(p), z)

    base = states_on_line(p0)
    plus = states_on_line(p0 + D)
    for (a, c), (aa, cc), move in zip(base, plus, FINE + "D"):
        da, dc = aa - a, cc - c
        assert all(v.denominator == 1 for v in (a, c, da, dc))
        assert a >= 0 and c >= 0 and da >= 0 and dc >= 0
        if move == "B":
            assert c % 4 == 1 and a >= c + 2 and da >= dc
        elif move == "C":
            assert c % 4 == 3 and a >= c + 4 and da >= dc
        elif move == "J":
            assert a % 2 == c % 2 == 1 and a <= c and da <= dc
        else:
            assert c % 4 == 3 and a == c + 3 and da == dc
    # In the full progression, (P-P0)/D is a multiple of four. The tabulated
    # integral increments therefore preserve each parity/congruence above.
    assert pow(3, PERIOD, 4 * D) == 1
    # All m leading Js are legal iff c + 2*m >= 3^m (for m >= 1).
    assert 3**15 > D and (3**15 - D) * p0 > OFFSET


def start_tail(m, seed):
    p = 3**m
    if seed % 2:
        return 2 * p - 1, seed - p + 1 + 2 * m
    return 4 * p - 1, seed + 5 - 2 * p + 2 * m


def coarse_gap(m, seed):
    # Extend without guards, including to negative integers for bisection.
    a, c = start_tail(m, seed)
    for move in COARSE:
        if move == "L":
            q = (c + 1) // 4
            a, c = a - 4 * q - 3, 6 * q + 5
        else:
            a, c = 3 * a + 2, c - a + 1
    return a - c


def replay(m, seed):
    """Exact guard check of one candidate including its leading Js and final halt."""
    a, c = 1, seed
    if c % 2 == 0:
        if a > c:
            return False
        a, c = 3, c + 3  # rule I
    for _ in range(m):
        if a > c or a % 2 == 0 or c % 2 == 0:
            return False
        a, c = 3 * a + 2, c - a + 1
    assert (a, c) == start_tail(m, seed)
    for move in COARSE:
        if move == "L":
            q = (c + 1) // 4
            if c % 2 == 0 or a < 4 * q + 3:
                return False
            a, c = a - 4 * q - 3, 6 * q + 5
        else:
            if a > c or a % 2 == 0 or c % 2 == 0:
                return False
            a, c = 3 * a + 2, c - a + 1
    # c is odd; even/even termination is unreachable on this word.
    return (a == c + 1) or (c % 4 == 3 and a == c + 3)


def check_smaller():
    # The final leading J requires seed >= 3^m-2*m for odd entry and
    # >= 2*3^m-2*m-4 for even entry. Both bounds increase for m >= 1.
    nxt = BASE_M + 1
    assert min(3**nxt - 2*nxt, 2*3**nxt - 2*nxt - 4) > H
    roots = []
    for m in range(nxt):
        for parity in (0, 1):
            # On a fixed parity, a is nonincreasing and c nondecreasing as the
            # seed increases, through either *unguarded* L or J. Therefore all
            # terminal gaps 1..3 lie in the one interval found by bisection.
            lo, hi = 0, (H - parity) // 2 + 1
            while lo < hi:
                mid = (lo + hi) // 2
                if coarse_gap(m, 2 * mid + parity) <= 3:
                    hi = mid
                else:
                    lo = mid + 1
            seed = 2 * lo + parity
            while seed <= H and coarse_gap(m, seed) >= 1:
                if replay(m, seed):
                    roots.append((m, seed))
                seed += 2
    assert roots == [(BASE_M, H - 2), (BASE_M, H)]
    a0, c0 = start_tail(BASE_M, H - 2)
    a1, c1 = start_tail(BASE_M, H)
    assert a0 == a1 and (c0 + 1) // 4 == (c1 + 1) // 4


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run without -O to enable verification.")
    check_family()
    check_smaller()
    print("Fine suffix ending in D: odd seed exponents 292 + 242660*k; even seeds excluded.")
    print("Coarse suffix: the only halting seeds through H are H-2 and H.")
