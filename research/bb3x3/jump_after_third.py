"""Exact two-return translation after the third #758 candidate has been bypassed."""
from math import comb
from check_bb33 import champion_step
from check_confluence import itinerary
from timing_758 import branch_cost

START = 3_335_436_339_933_383
PAIRS = 2_573_639_151_182
FINAL = 3_706_040_377_703_662
ELAPSED = 113_644_631_629_159_423_408_446_473_432_172_906_253_179_377


def timed_return(seed):
    a, c = 1, seed
    elapsed = 0
    # Odd seeds begin with J. Even seeds begin with I. Then both have
    # 31 J's, one bulk on c=3 mod 4, and the ordinary h-return.
    assert a <= c
    elapsed += branch_cost(a, c)
    a, c = champion_step(a, c)
    assert a in (3, 5) and c % 2
    for _ in range(31):
        assert a % 2 and a <= c
        elapsed += branch_cost(a, c)
        a, c = champion_step(a, c)
        assert a > 1
    assert c % 4 == 3 and a >= c + 4
    elapsed += branch_cost(a, c)
    a, c = champion_step(a, c)
    assert a % 2 == 0 and c % 2 and a <= c
    elapsed += branch_cost(a, c)
    a, c = champion_step(a, c)
    assert a == 1
    return c, elapsed


def pair(index):
    seed = START + 144*index
    middle, first = timed_return(seed)
    end, second = timed_return(middle)
    assert middle == seed + 71 and end == seed + 144
    return first + second


def verify():
    # The entire two-parity band from immediately above the candidate pair
    # through this end uses the same coarse word. Its bulk may use either
    # fine residue. This checks the separate absence of direct halting seeds.
    lower = 3_335_436_339_933_246
    upper = 3_706_040_377_703_612
    for parity in (0, 1):
        lo = lower + (parity-lower) % 2
        hi = upper - (upper-parity) % 2
        expected = ('J'*31 + 'LR', 142 if parity else 146)
        assert itinerary(lo) == itinerary(hi) == expected
    # For each row of seeds with stride 144, the first move gives fixed a
    # and c increasing by 144. The 31 J's preserve those differences.
    # The bulk sees the same c mod 4, decreases a by an extra 144 and
    # increases c by an extra 216. All physical guards are affine. Testing
    # both end seeds in the two rows establishes every intervening return.
    for i in (0, PAIRS-1):
        pair(i)
    end, final_clock = timed_return(START + 144*PAIRS)
    assert end == FINAL
    v0, v1, v2 = (pair(i) for i in range(3))
    # Every branch cost is quadratic in affine counters. The Newton differences
    # of the per-pair cost after order two vanish over the verified interval.
    elapsed = (PAIRS*v0 + comb(PAIRS, 2)*(v1-v0)
               + comb(PAIRS, 3)*(v2-2*v1+v0) + final_clock)
    assert elapsed == ELAPSED
    print(f"{2*PAIRS+1:,} first returns; c = {FINAL:,}; {elapsed:,} raw transitions")


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit("Run without -O to enable the checks.")
    verify()
