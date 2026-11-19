#!/usr/bin/env python3
"""Check exact near-wall consequences of the #758 two-counter model.

Place next to check_bb33.py. All computations use Python standard-library integers.
"""
from itertools import product
from random import Random

from check_bb33 import HALTING_TARGET, WALL_FAR, WALL_NEAR, champion_step


LOW = HALTING_TARGET - WALL_FAR
HIGH = HALTING_TARGET - WALL_NEAR
BASIN_LOW = HALTING_TARGET - 64_000_000


def exceptional_return():
    """Verify the whole rectangular range using the two extremal odd inputs."""
    # A(c+2,c), c=3 mod 4, has mass 3*c+2.
    first = (2 * LOW - 1 + 2) // 3  # ceil((2*LOW-1)/3)
    first += (3 - first) % 4
    last = (2 * HIGH - 1) // 3
    last -= (last - 3) % 4

    total, right = 0, 1
    for _ in range(785):
        q = (right + 1) // 4
        total, right = total + 4 * q + 3, 6 * q + 5
    assert total - 6 <= 2 * LOW + 1 <= 2 * HIGH + 1 <= total + right - 6
    assert total - 6 <= 2 * BASIN_LOW + 1

    # For all intermediate parameters c, coordinate a stays between the two
    # endpoints and the right counter is identical until one endpoint exits.
    for c in (first, last):
        assert c % 4 == 3 and 2 * LOW + 1 <= 3 * c + 2 <= 2 * HIGH + 1
        a, right = champion_step(c + 2, c)
        assert (a, right) == (3 * c + 8, 1)
        for _ in range(785):
            q = (right + 1) // 4
            assert a >= 4 * q + 3
            step = champion_step(a, right)
            assert step == (a - 4 * q - 3, 6 * q + 5)
            a, right = step
        assert a % 2 == 0 and right % 2 == 1 and a <= right
        checkpoint = champion_step(a, right)
        assert checkpoint == (1, (3 * c + 5_459) // 2)
        assert 1 + 2 * checkpoint[1] == (3 * c + 2) + 5_458
    print("All eligible exceptional inputs take 787 updates to A(1,(3*c+5459)/2).")


def crossing_length():
    """Necessary itinerary length for an infinite orbit to escape the basin."""
    width = HIGH - BASIN_LOW
    # From the first mass >= 2B+1 (at most 2B+9) to the first mass
    # > 2U+1-5458, all source states are inside the exceptional-return strip.
    min_gain = 2 * width - 5_465
    min_steps = (min_gain + 8) // 9
    assert min_steps == 13_465_381
    assert 9*13_465_988 < 2*width+3 <= 9*13_465_989
    # A J run triples a+1. A bulk run scales c+7 by at least 3/2.
    assert 3**292 <= HALTING_TARGET < 3**293
    assert 8*3**786 <= (HALTING_TARGET+7)*2**786
    assert 8*3**787 > (HALTING_TARGET+7)*2**787
    assert 12_491*(292+786) < min_steps
    print("An infinite blank orbit would need at least 24,982 switches in the halting interval.")


def lift(u0, word):
    """Produce integer d0 following word through iterations J or a pair bb."""
    # The composed inverse at a terminal x has the form (A*x+C)/M.
    u = u0 + sum(2 if branch == "J" else 5 for branch in word)
    terminal_u = u
    A, C, M = 1, 0, 1
    for branch in reversed(word):
        if branch == "J":
            u -= 2
            C += (u - 1) * M
            M *= 3
        elif branch == "B":
            u -= 5
            A, C, M = 4 * A, 4 * C - 20 * M, 9 * M
        else:
            raise ValueError(branch)
    assert u == u0
    residue = (-C * pow(A, -1, M)) % M
    lower = (terminal_u + 4) // 5
    x = lower + (residue - lower) % M
    assert 5 * x >= terminal_u and 4 * x <= terminal_u
    d0, remainder = divmod(A * x + C, M)
    assert remainder == 0
    return d0, x


def audit_word(u0, word):
    """Check the constructed representative on the original two-counter map."""
    d0, terminal = lift(u0, word)
    u, d = u0, d0
    for branch in word:
        a, c = 2 * u - 4 * d - 1, 2 * d + 1
        assert a > 1 and c > 1
        if branch == "J":
            assert a <= c
            nxt = champion_step(a, c)
            u, d = u + 2, 3 * d - u + 1
        else:
            assert d % 4 == 0 and 9 * d <= 2 * u - 12
            middle = champion_step(a, c)
            assert middle[0] > middle[1] + 1 and middle[1] % 4 == 1
            nxt = champion_step(*middle)
            u, d = u + 5, (9 * d + 20) // 4
        assert nxt == (2 * u - 4 * d - 1, 2 * d + 1)
    assert d == terminal
    return d0


def branching():
    u = LOW
    # Allow for ceiling/floor at endpoints for all terminal u>=LOW.
    assert u // 20 - 2 > 9**144 and u // (5 * 3**144) > 100
    seen = {audit_word(u, w) for w in product("JB", repeat=10)}
    assert len(seen) == 2**10
    rng = Random(758)
    words = ["J"*144, "B"*144, "JB"*72, "BJ"*72]
    words += [rng.choices("JB", k=144) for _ in range(128)]
    assert len({audit_word(u, w) for w in words}) == len(words)
    print("Witness construction checked on 1,024 ten-block and 132 144-block words.")


def survival_bound():
    """Audit the paired bulk forms and the bound on arbitrary odd cut states."""
    u = HALTING_TARGET - 10_000_000
    residues = ((5, 20), (9, 35), (7, 26), (7, 29))
    for d in range(64):
        a, c = 2 * u - 4 * d - 1, 2 * d + 1
        a, c = champion_step(*champion_step(a, c))
        increase, offset = residues[d % 4]
        assert (a + 2 * c - 1) // 2 == u + increase
        assert 4 * ((c - 1) // 2) == 9 * d + offset

    depth = 334
    # Each word gives a frozen interval, padded by 14 integer units at both ends.
    # A closed interval of length ell contains at most ell+1 integers.
    bound = u * 7**depth // (2 * 9**depth) + 29 * 2**depth
    count = (u + 1) // 2
    assert bound * 10**39 < 446 * count
    assert bound < 4_783 * 10**99
    # The first crossing ranges from M to M+8. An even mass may take one
    # compulsory bulk update to either W+5 or W+9, bounded above by M+16.
    high_bound = (u + 8) * 7**depth // (2 * 9**depth) + 29 * 2**depth
    assert 13 * high_bound < 6_218 * 10**100
    print("Fewer than 6.218e103 states on the entire central crossing can bypass the test.")


def recent_resets():
    """Exact image at the central cut for resets within 4,000 updates."""
    mass = 2 * (HALTING_TARGET - 10_000_000) + 1
    horizon = 4_000
    # Initial mass is 1+2*z and the mass increment is at most 9 per live update.
    first = (mass - 9 * horizon) // 2
    last = (mass - 2) // 2
    assert last - first + 1 == 18_000
    states = set()
    count = longest = 0
    for z in range(first, last + 1):
        a, c = 1, z
        for step_number in range(1, horizon + 1):
            result = champion_step(a, c)
            if result is None:
                break
            a, c = result
            if a + 2 * c >= mass:
                count += 1
                states.add((a, c))
                longest = max(longest, step_number)
                break
            if a == 1:
                break  # A later reset, itself in the search interval, owns the crossing.
    assert (count, len(states), longest) == (903, 745, 582)
    for a, c in states:
        for _ in range(horizon):
            if a == 1:
                assert LOW <= c <= HIGH
                break
            result = champion_step(a, c)
            if result is None:
                break
            a, c = result
        else:
            raise AssertionError("cut state did not reach a verified outcome")
    print("903 recent reset seeds cross in at most 582 updates, at 745 distinct states.")


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run without -O to enable verification.")
    recent_resets()
    exceptional_return()
    branching()
    survival_bound()
    crossing_length()
