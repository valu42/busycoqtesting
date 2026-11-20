#!/usr/bin/env python3
"""Transport the ordinary-state entry test through a longer dyadic shadow.

No new high-pair angular exhaustion is used here.  The reverse-guard
calculation extends the physical interpretation of the p<=28 tail survey.
"""
from math import comb

from dyadic_guard_shadow_758 import guard_counts
from filtered_entry_758 import Membership, inverse_cylinder, launch_exponent, physical_return
from target_basin_758 import least_tail_margin, read_tails
from target_shadow_758 import C, D, POWER, horizon
from wider_even_entry_758 import (
    FAR, H, MAX_CALLS, MAX_H as RECTANGLE_H, NEAR, TRIM,
    verify as verify_rectangle,
)

MAX_R = 88
RECTANGLE_R = launch_exponent(RECTANGLE_H)[0]
MIN_JUMPS = 307-MAX_R
MAX_CUT = MAX_R+1
LAST_GUARD = MAX_CUT+188
SHADOW_UPPER = FAR+600
MIN_MASS = H-FAR
MAX_MASS = H-NEAR-TRIM
MAX_H = 2*(MIN_MASS//(2*3**MIN_JUMPS))


def classify_left(h):
    """Sufficient predicate; an inconclusive result makes no fate assertion."""
    if not isinstance(h, int) or h < 2 or h > MAX_H or h % 2:
        raise ValueError('h must be an even integer between 2 and MAX_H')
    r, denominator = launch_exponent(h)
    assert r <= MAX_R
    if r <= RECTANGLE_R:
        assert h <= RECTANGLE_H
        return Membership(True, 'complete rectangle', r, 0, 0)
    numerator, depth, pairs = D*h, 0, 0
    launch_denominator = denominator
    while True:
        assert 0 < numerator < denominator
        assert 3*numerator != denominator and 9*numerator != 5*denominator
        if denominator < 3*numerator and 9*numerator < 5*denominator:
            return Membership(True, 'ordinary return by the cut', r, depth, pairs)
        if depth >= r:
            assert depth in (r, r+1) and depth <= MAX_CUT
            assert numerator % launch_denominator == 0
            tail_numerator = numerator//launch_denominator
            assert denominator == launch_denominator*4**pairs
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
    if (not isinstance(h, int) or not isinstance(u, int)
            or h < 2 or h > MAX_H or h % 2 or u % 2
            or not MIN_MASS <= u <= MAX_MASS):
        return False
    return classify_left(h).accepted


def inconclusive_bound():
    """Count a covering family by binomial coefficients, not word enumeration."""
    cylinders = bound = 0
    for r in range(RECTANGLE_R+1, MAX_R+1):
        for p in range(29, (r+1)//2+1):
            n = r-p-1
            for extra, k in ((0, p-1), (1, p-2)):
                if not 0 <= k <= n:
                    continue
                count = comb(n, k)
                cylinders += count
                bound += count*(4**p//(2*D*3**extra)+1)
    return cylinders, bound


def boundary_checks():
    us = (MIN_MASS+MIN_MASS%2,
          2*((MIN_MASS+MAX_MASS)//4), MAX_MASS-MAX_MASS%2)
    hs = {2, RECTANGLE_H, RECTANGLE_H+2, MAX_H-2, MAX_H,
          2*(MAX_H//4)}
    # A covered p=28 cut, with its remaining angular direction near 1/4.
    word = 'P'+'J'*(MAX_R-56)+'P'*27
    a, p, m = inverse_cylinder(word)
    assert (p, m) == (28, MAX_R)
    hs.add(2*((a+4**(p-1))//(2*D)))
    # A high-pair cylinder ending at each possible cut depth.
    examples = []
    for m in (MAX_R, MAX_R+1):
        p = m//2
        jumps = m-2*p
        word = 'P'+'J'*jumps+'P'*(p-1)
        if m == MAX_R+1 and not word.endswith('P'):
            continue
        examples.append((word, m))
    for word, expected_m in examples:
        a, p, m = inverse_cylinder(word)
        assert m == expected_m and m in (MAX_R, MAX_R+1) and p >= 29
        scale = D*3**(m-MAX_R)
        low = 2*(a//(2*scale))
        high = 2*((a+4**p)//(2*scale))
        quarter = 2*((a+4**(p-1))//(2*scale))
        hs.update((low-2, low, low+2, quarter, high-2, high, high+2))
    hs = sorted(h for h in hs if 2 <= h <= MAX_H and not h%2)
    accepted = rejected = accepted_replays = rejected_replays = 0
    reasons = set()
    for h in hs:
        decision = classify_left(h)
        if decision.accepted:
            accepted += 1
            reasons.add(decision.reason)
            for u in us:
                assert accepts(h, u)
                physical_return(h, u)
                accepted_replays += 1
        else:
            rejected += 1
            assert decision.pairs >= 29 and not accepts(h, us[0])
            # These particular rejected cases also return; they supply no
            # universal conclusion for the rejected cylinders.
            physical_return(h, us[0])
            rejected_replays += 1
    assert reasons == {'complete rectangle', 'ordinary return by the cut', 'covered dyadic tail'}
    assert accepted and rejected
    assert not accepts(3, us[0]) and not accepts(2, us[0]+1)
    assert not accepts(MAX_H+2, us[0])
    print(f'Boundary checks: {accepted} accepted and {rejected} inconclusive h values; '
          f'{accepted_replays} accepted and {rejected_replays} inconclusive physical replays.')


def verify():
    verify_rectangle()
    assert MAX_H == 69_471_640_166_665_074_144_382_279_320_672_514
    assert MAX_H == 2*(3**MAX_R//(2*D))
    assert 3**MIN_JUMPS*MAX_H <= MIN_MASS
    assert 2*3**293 > MAX_MASS+2*293
    assert 0 < C < 594*D and NEAR+TRIM > 2*292
    initial = horizon(SHADOW_UPPER)
    assert MAX_CUT <= initial == 248
    assert min(3**MIN_JUMPS, 3**(307-initial-2)) > D*(FAR+2600)
    rows = list(guard_counts(MAX_R, SHADOW_UPPER, LAST_GUARD))
    assert rows and [row[0] for row in rows] == list(range(initial+1, LAST_GUARD+1))
    assert all(ancestors == 0 for _, _, ancestors in rows)
    assert rows[-1][:2] == (277, 256_653_068_233_911)
    margin = least_tail_margin(read_tails(28))
    assert POWER*margin > D*3**MAX_CUT*(FAR+2600)
    assert 307+1+243+2 == MAX_CALLS and 9*MAX_CALLS//2 == TRIM
    print(f'Extended physical shadow through depth {LAST_GUARD} at every r <= {MAX_R}; '
          f'the last guard has {rows[-1][1]:,} candidate distances and no cut ancestors.')
    cylinders, bound = inconclusive_bound()
    total = MAX_H//2
    masses = MAX_MASS//2-(MIN_MASS-1)//2
    assert 0 < bound < total
    print(f'Even h through {MAX_H:,}: at most {bound:,} of {total:,} left coordinates '
          f'are inconclusive, covered by {cylinders:,} symbolic cylinders.')
    print(f'At least {(total-bound)*masses:,} ordinary states are certified '
          f'to return inside the halting basin within {MAX_CALLS} calls.')
    boundary_checks()


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run without -O for verification.')
    verify()
