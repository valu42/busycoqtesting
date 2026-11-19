#!/usr/bin/env python3
"""Check a strip at the left axis of the #758 halting interval."""
from bisect import bisect_right

from check_bb33 import HALTING_TARGET as H, POWERS_OF_THREE, champion_step
from scale_transport_758 import ordinary

LOWER = H - 11_177_976_427_786
UPPER = H - 3_403_055
MAX_LEFT = 2**26 - 1
RESONANT_LEFT = 28_730_581


def common_gain(small, large):
    """Bound the mass gain to a halt or a positive-time reset for this rectangle."""
    # A lies between small and large. Bound the odd right coordinate outwards
    # over the full mass interval, including opposite corners off the mass strip.
    low_right = (2*LOWER + 1 - large)//2
    low_right -= (low_right+1) % 2
    high_right = (2*UPPER + 2 - small)//2
    high_right += (high_right+1) % 2
    jumps = bisect_right(POWERS_OF_THREE, (2*low_right+large+1)//(large+1)) - 1
    assert jumps >= 0
    factor = POWERS_OF_THREE[jumps]

    def advance(left, right):
        return factor*(left+1)-1, right-(left+1)*((factor-1)//2)+2*jumps

    lower = advance(small, high_right)
    upper = advance(large, low_right)
    assert upper[1] >= 1
    gain = 4*jumps
    for _ in range(1000):
        first, lower = ordinary(*lower)
        second, upper = ordinary(*upper)
        if first != second or first == "E":
            return None
        if first == "stop":
            return gain+5
        gain += 4 if first == "J" else 9
    raise ValueError("shared-word budget exhausted")


def check():
    stack = [(1, MAX_LEFT)]
    leaves = exceptional = maximum_gain = 0
    unresolved = []
    while stack:
        low, high = stack.pop()
        gain = common_gain(low, high)
        if gain is not None:
            leaves += 1
            maximum_gain = max(maximum_gain, gain)
        elif low < high:
            middle = low + 2*((high-low)//4)
            stack.extend(((low,middle), (middle+2,high)))
        else:
            # Exactly the left coordinates produced by J^k from a reset.
            half = (low+1)//2
            while half % 3 == 0:
                half //= 3
            if half == 1:
                exceptional += 1
            else:
                unresolved.append(low)
    # No state in the strip of mass below 2H can have 293 earlier J's.
    assert 3**293 > H and 4*292 <= 2_000
    assert maximum_gain <= 2_000
    assert unresolved == [RESONANT_LEFT]
    assert (RESONANT_LEFT+1)*3**278 > 2*H
    print(f"{leaves:,} shared-word intervals, {exceptional} inverse-reset singletons, "
          f"maximum terminal mass gain {maximum_gain:,}. Remaining coordinate {unresolved[0]:,}.")


def central_crossing():
    """Trace the sole unclassified left coordinate directly at the central cut."""
    wall = 2*(H-10_000_000) + 1
    offsets = []
    for jumps in range(293):
        landed = []
        for mass in range(wall-4*jumps, wall+17-4*jumps):
            if (mass-RESONANT_LEFT) % 4 != 2:
                continue
            state = RESONANT_LEFT, (mass-RESONANT_LEFT)//2
            for _ in range(580):
                assert state is not None and state[0] != 1
                state = champion_step(*state)
            assert state is not None and state[0] == 1
            assert LOWER <= state[1] <= UPPER
            landed.append(H-state[1])
        if jumps == 0:
            assert landed == [9_998_782, 9_998_782, 9_998_776, 9_998_776, 9_998_778]
        offsets.extend(landed)
    assert (len(offsets), min(offsets), max(offsets)) == (1465, 9_998_776, 9_999_376)


def switch_count():
    """Combine the two axis strips with the independent exceptional-return lemma."""
    min_gain = 2*(UPPER-LOWER) - 10_007
    assert (2**24+8)*3**751 > (H+7)*2**751
    assert (RESONANT_LEFT+1)*3**278 > 2*H
    def maximum_gain(runs):
        return (runs//2)*(4*277+9*750) + (runs%2)*9*750
    assert maximum_gain(5_689_983_720) < min_gain <= maximum_gain(5_689_983_721)
    print("An escape requires at least 5,689,983,720 switches.")


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run without -O so verification checks execute.")
    check()
    central_crossing()
    switch_count()
