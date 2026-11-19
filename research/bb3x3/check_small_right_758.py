"""Verify the small-right-counter strip across the full #758 reset basin."""
from argparse import ArgumentParser
from functools import lru_cache

from check_bb33 import HALTING_TARGET as H, WALL_NEAR, champion_step


B, U = H-11_177_976_427_786, H-WALL_NEAR
LOW_MASS, HIGH_MASS = 2*B+1, 2*U+1
GROUP = 12
PERIOD = 1 << GROUP
SCALE = 3**GROUP


def bulk_table():
    final, odd = [], []
    for residue in range(PERIOD):
        x, count = residue, 0
        for _ in range(GROUP):
            count += x % 2
            x = 3*x//2
        final.append(x)
        odd.append(count)
    return final, odd


FINAL, ODD = bulk_table()


@lru_cache(maxsize=8192)
def launch(c, groups):
    """Unchecked positive bulk run; the caller proves the total decrement fits."""
    assert groups > 0
    initial = (c+1)//4 + 3
    x, odds = initial, 0
    for _ in range(groups):
        residue = x & (PERIOD-1)
        odds += ODD[residue]
        x = SCALE*(x >> GROUP) + FINAL[residue]
    cost = 8*(x-initial) - 9*groups*GROUP + 4*odds
    # Invert x_n=floor(3*x_(n-1)/2) on its image.
    previous = (2*x+1)//3
    return cost, 6*previous-13


def certify_interval(lo, hi):
    """Return the largest call count across the two parities, or zero to split."""
    # Choose a long initial bulk batch. Its legality is checked below by an
    # exact inequality; this estimate only affects computational cost.
    groups = (LOW_MASS.bit_length()-hi.bit_length()-7)*1709//(1000*GROUP)
    lower_cost, smaller_c = launch(lo, groups)
    upper_cost, larger_c = launch(hi, groups)
    largest_a = HIGH_MASS-2*lo-lower_cost
    smallest_a = LOW_MASS-2*hi-upper_cost
    # The decrements are positive and increase with initial c. The smallest
    # starting a covers the largest total, hence each individual guard holds.
    assert smallest_a >= 0
    longest = 0
    for parity in (0,1):
        high_a = largest_a-(HIGH_MASS-parity)%2
        low_a = smallest_a+(parity-LOW_MASS)%2
        left_c, right_c = smaller_c, larger_c
        calls = groups*GROUP
        while calls < 2000:
            left_q, right_q = (left_c+1)//4, (right_c+1)//4
            if low_a >= 4*right_q+3:
                high_a, left_c = high_a-4*left_q-3, 6*left_q+5
                low_a, right_c = low_a-4*right_q-3, 6*right_q+5
            elif high_a >= 4*left_q+3:
                return 0
            elif high_a%2 == 0:
                # Every state is even and nonbulk: its next instruction either
                # halts or returns to a=1, increasing the mass by exactly five.
                longest = max(longest, calls+1)
                break
            elif high_a <= left_c:
                high_a, left_c = 3*high_a+2, left_c-high_a+1
                low_a, right_c = 3*low_a+2, right_c-low_a+1
            else:
                return 0
            calls += 1
        else:
            return 0
    return longest


def cover(bits):
    pending = [(1, (1<<bits)-1)]
    nodes = leaves = longest = 0
    while pending:
        lo, hi = pending.pop()
        nodes += 1
        calls = certify_interval(lo,hi)
        if calls:
            leaves += 1
            longest = max(longest, calls)
        else:
            if lo == hi:
                raise ValueError(f"unresolved right counter {lo}")
            mid = lo+2*((hi-lo)//4)
            pending.extend(((mid+2,hi),(lo,mid)))
    return nodes, leaves, longest


def audit():
    # Independent scalar check of every low-bit group entry, at positive
    # states, for one and two consecutive groups.
    for residue in range(PERIOD):
        c = 4*(PERIOD+residue-3)+1
        a = 10**20
        state = a,c
        for groups in (1,2):
            for _ in range(GROUP):
                state = champion_step(*state)
            cost, right = launch(c,groups)
            assert state == (a-cost,right)
    # A near-axis state inside the untrimmed band can return *above* U.
    mass = HIGH_MASS-5448
    state = mass-2,1
    for _ in range(785):
        state = champion_step(*state)
        assert state is not None and state[0] != 1
    assert champion_step(*state) == (1,U+1)
    assert (2**24+8)*3**750 <= (H+7)*2**750
    assert (2**24+8)*3**751 > (H+7)*2**751


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run without -O to retain the verification checks.")
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--bits", type=int, default=24, choices=range(1,25),
                        help="cover all positive odd c below 2^bits (default 24)")
    args = parser.parse_args()
    audit()
    nodes, leaves, calls = cover(args.bits)
    if args.bits == 24:
        assert (nodes,leaves,calls) == (1_077_697,538_849,844)
    print(f"{nodes:,} nodes and {leaves:,} certified leaves, at most {calls} calls.")
    print(f"Top clearance for a return in the basin: {9*(calls-1)+5:,} mass units.")
