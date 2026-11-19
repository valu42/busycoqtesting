#!/usr/bin/env python3
"""Exclude late physical guard ambiguities by reversing eligible dyadic directions."""
import argparse

from target_shadow_758 import D, HIGH, LOW, horizon

GUARDS = ((0, 0), (1, 1), (5, 2), (1, 0))  # numerator, exponent of three
GAP20_UPPER = 32_078_348_842_098_793_106


def reaches_cut(numerator, pairs, depth, r):
    """Can a reduced dyadic reach either possible cut by inverse jumps or pairs?"""
    while pairs >= 1 and 2*pairs <= depth:
        if depth < r:
            return False
        if depth <= r+1:
            return True
        if numerator % 3 == 0:
            numerator //= 3
            depth -= 1
        else:
            numerator += 5*4**(pairs-1)
            if numerator % 9:
                return False
            numerator //= 9
            pairs -= 1
            depth -= 2
    return False


def count_cut_ancestors(low, high, pairs, depth, r):
    """Count the eligible numerators in an interval having a reverse history."""
    low += (5-low) % 10
    high -= (high-5) % 10
    if low > high or depth < r or pairs < 1 or 2*pairs > depth:
        return 0
    if depth <= r+1:
        return (high-low)//10+1
    if low == high:
        return int(reaches_cut(low, pairs, depth, r))
    # The J and P forward images of integer numerators are disjoint modulo 3.
    total = count_cut_ancestors((low+2)//3, high//3, pairs, depth-1, r)
    if pairs >= 2:
        shift = 5*4**(pairs-1)
        total += count_cut_ancestors((low+shift+8)//9, (high+shift)//9,
                                     pairs-1, depth-2, r)
    return total


def guard_counts(r, upper, last):
    """Yield (depth, candidates, possible_cut_ancestors) for each new guard depth."""
    if not 2 <= r <= horizon(upper) or not LOW <= upper <= HIGH:
        raise ValueError('requires a physical target range with its cut already shadowed')
    if last+2 > 307:
        raise ValueError('the guard formula in this verifier requires last+2 <= 307')
    for depth in range(horizon(upper)+1, last+1):
        candidates = ancestors = 0
        for b, t in GUARDS:
            denominator = 3**t
            margin = D*(upper+2000) // 3**(307-depth-t)
            for pairs in range(1, depth//2+1):
                scale = 4**pairs
                # Inclusive interval; ceil(a/b) = -floor(-a/b) for integers.
                low = max(1, -((margin-b*scale)//denominator))
                high = min(scale-1, (b*scale+margin)//denominator)
                first = low + (5-low) % 10
                candidates += max(0, (high-first)//10+1)
                ancestors += count_cut_ancestors(low, high, pairs, depth, r)
        yield depth, candidates, ancestors


def verify_examples():
    # A surviving small forward itinerary reaches two cut choices under reversal.
    # Start at depth 9 with 1 pair and x=1/4. Multiples of five are only
    # needed by guard_counts; inverse functions also hold for this toy orbit.
    assert reaches_cut(27-20, 2, 12, 9)  # J then P, x becomes 7/16
    assert reaches_cut(27-20, 2, 12, 10)
    assert not reaches_cut(5, 2, 12, 9)  # neither inverse is integral
    # Compare whole-interval inversion with independent pointwise counts.
    for pairs in range(2, 7):
        for r in range(5, 12):
            depth = 2*pairs + r
            high = min(4**pairs-1, 1500)
            direct = sum(reaches_cut(n, pairs, depth, r) for n in range(5, high+1, 10))
            assert direct == count_cut_ancestors(1, high, pairs, depth, r)


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('run without -O for verification')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--r', type=int, default=62)
    parser.add_argument('--upper', type=int, default=GAP20_UPPER)
    parser.add_argument('--last', type=int, default=251)
    args = parser.parse_args()
    verify_examples()
    rows = list(guard_counts(args.r, args.upper, args.last))
    for depth, candidates, ancestors in rows:
        print(f'depth {depth}: {candidates} candidates, {ancestors} with a possible cut ancestor')
    if any(ancestors for _, _, ancestors in rows):
        raise SystemExit('candidate cut ancestors require separate verification')
    print(f'Physical shadow certified through depth {args.last} at r={args.r} for offsets up to {args.upper:,}.')
