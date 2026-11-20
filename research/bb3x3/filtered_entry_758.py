#!/usr/bin/env python3
"""Check a finite angular membership test for ordinary target-band entry.

The universal result reuses the archived dyadic exhaustion through p=28 and
the enlarged rectangle's r=57 lattice certificate.  The tests below check
the new arithmetic bounds, combinatorial enclosure, and selected physical
boundary cases; they do not rerun either exhaustive enumeration.
"""
from dataclasses import dataclass
from math import comb

from check_bb33 import champion_step
from target_basin_758 import least_tail_margin, read_tails
from target_bridge_even_758 import (
    FAR, H, LAST_GUARD, MAX_CALLS, MAX_H as RECTANGLE_H, NEAR, UPPER_TRIM,
    verify as verify_rectangle,
)
from target_shadow_758 import C, D, POWER

MIN_MASS = H - FAR
MAX_MASS = H - NEAR - UPPER_TRIM
MIN_JUMPS = 248
MAX_R = 307 - MIN_JUMPS
MAX_CUT = MAX_R + 1
MAX_H = 2 * (MIN_MASS // (2 * 3**MIN_JUMPS))


@dataclass(frozen=True)
class Membership:
    accepted: bool
    reason: str
    r: int
    depth: int
    pairs: int


def launch_exponent(h):
    """Least r with 3**r > D*h; the physical launch has 307-r jumps."""
    r, power = 0, 1
    while power <= D*h:
        r, power = r+1, 3*power
    return r, power


def classify_left(h):
    """Classify an even h in the stated range, independent of the even mass.

    False means this sufficient test gives no decision.  In particular it
    does not assert a long excursion, a halt-free crossing, or nonhalting.
    """
    if not isinstance(h, int) or h < 2 or h > MAX_H or h % 2:
        raise ValueError('h must be an even integer between 2 and MAX_H')
    r, denominator = launch_exponent(h)
    assert r <= MAX_R
    if r <= 57:
        assert h <= RECTANGLE_H
        return Membership(True, 'enlarged rectangle', r, 0, 0)

    numerator, depth, pairs = D*h, 0, 0
    original_denominator = denominator
    while True:
        assert 0 < numerator < denominator
        assert 3*numerator != denominator and 9*numerator != 5*denominator
        if denominator < 3*numerator and 9*numerator < 5*denominator:
            return Membership(True, 'ordinary return by the cut', r, depth, pairs)
        if depth >= r:
            assert depth in (r, r+1) and depth <= MAX_CUT
            assert numerator % original_denominator == 0
            tail_numerator = numerator // original_denominator
            assert denominator == original_denominator * 4**pairs
            assert 0 < tail_numerator < 4**pairs and tail_numerator % 10 == 5
            return Membership(pairs <= 28,
                              'covered dyadic tail' if pairs <= 28 else 'unsettled high-pair cut',
                              r, depth, pairs)
        if 3*numerator < denominator:
            numerator, depth = 3*numerator, depth+1
        else:
            assert 9*numerator > 5*denominator
            numerator, denominator = 9*numerator-5*denominator, 4*denominator
            depth, pairs = depth+2, pairs+1


def accepts(h, u):
    """Sufficient halting predicate on odd/odd coordinates h=(a+1)/2, u.

    An even h and an even u give a=2*h-1 and c=u-h+1 both odd.
    """
    if (not isinstance(h, int) or not isinstance(u, int)
            or h < 2 or h > MAX_H or h % 2 or u % 2
            or not MIN_MASS <= u <= MAX_MASS):
        return False
    return classify_left(h).accepted


def high_pair_rows():
    """All still-unsettled first-cut types, without enumerating their words."""
    def choose(n, k):
        return comb(n, k) if 0 <= k <= n else 0
    rows = []
    for r in (58, 59):
        for p in range(29, (r+1)//2+1):
            for extra, count in (
                (0, choose(r-p-1, p-1)),
                (1, choose(r-p-1, p-2)),
            ):
                if count:
                    m = r+extra
                    per_cylinder = 4**p // (2*D*3**extra) + 1
                    rows.append((r, m, p, count, per_cylinder))
    return rows


def inverse_cylinder(word):
    """Return (A,p,m) for x_initial=(A+4**p*x_final)/3**m."""
    a, pairs, depth = 0, 0, 0
    for letter in word:
        if letter == 'J':
            a, depth = 3*a, depth+1
        else:
            assert letter == 'P'
            a = 9*a + 5*4**pairs
            pairs, depth = pairs+1, depth+2
    return a, pairs, depth


def physical_return(h, u):
    a, c = 2*h-1, u-h+1
    assert a % 2 and c % 2 and a > 1 and c > 0
    for calls in range(1, MAX_CALLS+1):
        result = champion_step(a, c)
        assert result is not None, (h, u, calls, 'halt before the promised reset')
        a, c = result
        if a == 1:
            assert H-FAR <= c <= H-NEAR and 0 < c-u <= UPPER_TRIM
            return calls
    raise AssertionError((h, u, 'no reset within the promised bound'))


def check_boundaries():
    """Exercise actual cut boundaries, not only typical interior states."""
    us = (MIN_MASS + MIN_MASS % 2,
          2*((MIN_MASS+MAX_MASS)//4),
          MAX_MASS - MAX_MASS % 2)
    hs = {2, 4, RECTANGLE_H, RECTANGLE_H+2, MAX_H-2, MAX_H,
          2*(MAX_H//4)}
    # A p=28 cut with tail near 1/4 exercises the dyadic certificate path.
    a, p, m = inverse_cylinder('PJJ'+'P'*27)
    assert (p, m) == (28, 58)
    hs.add(2*((a+4**(p-1))//(2*D)))
    # One representative of each of the five unsettled cylinder types.
    examples = (
        (58, 'P'*29),
        (58, 'PJ'+'P'*28),
        (59, 'PJ'+'P'*28),
        (59, 'PJJ'+'P'*28),
        (59, 'P'*30),
    )
    for r, word in examples:
        a, p, m = inverse_cylinder(word)
        assert m in (r, r+1) and p >= 29
        scale = D*3**(m-r)
        low = 2*(a//(2*scale))
        high = 2*((a+4**p)//(2*scale))
        middle = 2*((2*a+4**p)//(4*scale))
        hs.update((low-2, low, low+2, middle, high-2, high, high+2))
    hs = sorted(h for h in hs if 2 <= h <= MAX_H and h % 2 == 0)
    accepted = rejected = 0
    reasons = set()
    accepted_physical = rejected_physical = 0
    for h in hs:
        decision = classify_left(h)
        if decision.accepted:
            accepted += 1
            reasons.add(decision.reason)
            for u in us:
                assert accepts(h, u)
                physical_return(h, u)
                accepted_physical += 1
        else:
            rejected += 1
            assert decision.r in (58, 59) and decision.pairs >= 29
            # These selected rejected examples also return.  This checks the
            # distinction between an inconclusive predicate and nonhalting;
            # it is not used to enlarge the universally certified set.
            assert not accepts(h, us[0])
            physical_return(h, us[0])
            rejected_physical += 1
    assert reasons == {'enlarged rectangle', 'ordinary return by the cut', 'covered dyadic tail'}
    assert accepted and rejected
    assert not accepts(3, us[0]) and not accepts(2, us[0]+1)
    assert not accepts(MAX_H+2, us[0])
    print(f'Boundary checks: {accepted} accepted and {rejected} inconclusive left coordinates; '
          f'{accepted_physical} accepted and {rejected_physical} inconclusive physical replays.')


def verify():
    verify_rectangle()
    assert MAX_H == 1_012_257_878_130_399_645_022
    assert MIN_JUMPS == 248 and MAX_R == 59 and MAX_CUT == 60
    assert 3**MIN_JUMPS*MAX_H <= MIN_MASS
    assert 0 < C < 594*D and NEAR+UPPER_TRIM > 2*292
    assert 2*3**293 > MAX_MASS+2*293
    assert MAX_CUT+188 == LAST_GUARD == 248
    margin = FAR+2600
    assert min(3**MIN_JUMPS, 3**(307-LAST_GUARD-2)) > D*margin
    listed_margin = least_tail_margin(read_tails(28))
    assert POWER*listed_margin > D*3**MAX_CUT*margin
    assert 307+1+243+2 == MAX_CALLS and 9*MAX_CALLS//2 == UPPER_TRIM

    rows = high_pair_rows()
    assert [row[:4] for row in rows] == [
        (58,58,29,1), (58,59,29,28), (59,59,29,29),
        (59,60,29,406), (59,60,30,1),
    ]
    assert sum(row[3] for row in rows) == 465
    excluded_bound = sum(count*per for _, _, _, count, per in rows)
    assert excluded_bound == 1_817_019_372_897
    total_left = MAX_H//2
    allowed_masses = MAX_MASS//2 - (MIN_MASS-1)//2
    assert excluded_bound * 10**12 < 3591*total_left
    print(f'At most {excluded_bound:,} of {total_left:,} even left coordinates '
          'are inconclusive; the deterministic fraction is below 3.591e-9.')
    print(f'At least {(total_left-excluded_bound)*allowed_masses:,} ordinary states '
          f'are certified to return inside the halting basin within {MAX_CALLS} calls.')
    check_boundaries()


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run without -O for verification.')
    verify()
