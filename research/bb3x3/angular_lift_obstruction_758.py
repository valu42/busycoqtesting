"""Audit possible lower-height angular transports of the secondary-cusp checkpoints."""
from math import gcd
from pathlib import Path

from check_bb33 import HALTING_TARGET, champion_step
from check_confluence import itinerary
from secondary_cusp_758 import gate_rows

HERE = Path(__file__).resolve().parent
P = 3**292
Y = 3**301 // 19171 + 4510976
REPRESENTATIVE = Y + 158145479878
MAX_DENOMINATOR = 10**18


def checkpoints():
    edges = {k: hi for k, _, hi in gate_rows()}
    seeds = []
    for filename in ('checkpoint_y_census_758.tsv', 'y_edge_bands_758.tsv'):
        for line in (HERE / filename).read_text().splitlines():
            row = tuple(map(int, line.split()))
            seeds.append(edges[row[0]] + row[-1])
    assert len(set(seeds)) == len(seeds) == 732
    return seeds


def minimum_launch_exponent(seed):
    b, k = (1, 292) if seed % 2 else (2, 291)
    h, u = b * 3**k, seed + 2*k + 4*(b-1)
    assert h <= u < 3*h
    numerator = h // gcd(h, u)
    result = 0
    while numerator % 3 == 0:
        numerator //= 3
        result += 1
    assert numerator == 1
    return result


def best_interior_error(h, u, limit):
    """Return (absolute numerator error, denominator) for the nearest strict direction."""
    if limit*h <= u:
        return abs(limit*h-u), limit
    if limit*(u-h) <= u:
        return abs(limit*(u-h)-u), limit

    # Adjacent fractions bracketing h/u, storing their positive errors
    # h*q_left-u*p_left and u*p_right-h*q_right. Their determinant is one.
    left_q, right_q = 1, 1
    left_err, right_err = h, u-h
    while left_q + right_q <= limit and left_err and right_err:
        if left_err >= right_err:
            steps = min(left_err // right_err, (limit-left_q) // right_q)
            left_q += steps * right_q
            left_err -= steps * right_err
        else:
            steps = min(right_err // left_err, (limit-right_q) // left_q)
            right_q += steps * left_q
            right_err -= steps * left_err
    if left_err * right_q <= right_err * left_q:
        return left_err, left_q
    return right_err, right_q


def smallest_guard_match(h, u, limit, allowance=18):
    """Least interior denominator up to limit with |h-u*p/q| <= allowance."""
    if (min(h, u-h)+allowance)*limit < u:
        return None
    left_q, right_q = 1, 1
    left_err, right_err = h, u-h
    while left_q + right_q <= limit:
        q = left_q + right_q
        error = left_err - right_err
        if abs(error) <= allowance*q:
            return q
        # Skip exactly the mediants still strictly to the same side of
        # the allowed interval. No skipped fraction satisfies its guard.
        if error > 0:
            steps = (left_err-allowance*left_q-1) // (right_err+allowance*right_q)
            left_q += steps * right_q
            left_err -= steps * right_err
        else:
            steps = (right_err-allowance*right_q-1) // (left_err+allowance*left_q)
            right_q += steps * left_q
            right_err -= steps * left_err
    return None


def check_minimum_search():
    for u in range(3,60):
        for h in range(1,u):
            for allowance in (0, 1):
                direct = next((q for q in range(2,32)
                               if any(abs(h*q-u*p) <= allowance*q
                                      for p in range(1,q))), None)
                assert smallest_guard_match(h, u, 31, allowance) == direct


def history(seeds, returns):
    calls, aligned, after = 0, 0, 0
    smallest_denom = None
    smallest_error = None
    guard_denominator = 2*Y
    for seed in seeds:
        a, c = 1, seed
        past_opening = False
        finished = 0
        while finished < returns:
            past_opening |= a > c
            if a % 2 and c % 2:
                h, u = (a+1)//2, (a+2*c-1)//2
                denom = u // gcd(h, u)
                if smallest_denom is None or denom < smallest_denom:
                    smallest_denom = denom
                aligned += 1
                if past_opening:
                    after += 1
                    match = smallest_guard_match(h, u, guard_denominator-1)
                    if match is not None:
                        guard_denominator = match
                    # If no interior fraction is close to either endpoint,
                    # its error is at least u/limit-min(h,u-h).
                    if (smallest_error is None or
                        (u-MAX_DENOMINATOR*min(h, u-h))*smallest_error[1] <
                        MAX_DENOMINATOR*smallest_error[0]):
                        err, q = best_interior_error(h, u, MAX_DENOMINATOR)
                        if smallest_error is None or err*smallest_error[1] < smallest_error[0]*q:
                            smallest_error = (err, q)
            pair = champion_step(a, c)
            if pair is None:
                raise AssertionError(f'halting excursion from {seed}')
            a, c = pair
            calls += 1
            if a == 1:
                finished += 1
                past_opening = False
    return calls, aligned, after, smallest_denom, smallest_error, guard_denominator


def check_target_direction():
    # The same metric detects the final odd-phase guard of both direct halters.
    for seed in (HALTING_TARGET-2, HALTING_TARGET):
        a, c = 1, seed
        for _ in range(305):
            a, c = champion_step(a, c)
        assert a % 2 and c % 2
        h, u = (a+1)//2, (a+2*c-1)//2
        assert 9*h-5*u == 34 and smallest_guard_match(h, u, 9) == 9
        assert champion_step(*champion_step(a, c)) is None


def main():
    check_minimum_search()
    check_target_direction()
    suffix, _ = itinerary(REPRESENTATIVE)
    assert 'J'+suffix == 'J'*292+'L'*8+'J'+'L'*716+'J'+'L'*20+'JLR'
    assert 3**293 > HALTING_TARGET + 10000 + 586
    assert 3**358 - 716 > 30_064 * 10**27 * HALTING_TARGET
    seeds = checkpoints()
    assert minimum_launch_exponent(REPRESENTATIVE) == 292
    assert min(map(minimum_launch_exponent, seeds)) == 285
    for name, starts, returns in (
            ('representative', [REPRESENTATIVE], 100),
            ('catalogs', seeds, 4)):
        calls, states, after, denominator, (error, q), guard_denominator = history(starts, returns)
        print(name, calls, states, after, denominator, error, q, guard_denominator, flush=True)
        expected = {
            'representative': (67050, 48200, 19050, 136, 224584707220898, 2187),
            'catalogs': (2510806, 1687303, 833068, 133, 695182660215218, 387420489),
        }[name]
        assert (calls, states, after, len(str(denominator))) == expected[:4]
        assert error * expected[5] == expected[4] * q
        guard_minima = {
            'representative': 7_338_499_478_584_705_329_266_844_575_071_286_432_531_794_360_058_779_537_191_734_415_176,
            'catalogs': 1_974_499_818_877_863_318_840_728_090_353_753_051_616_019_234_915_223_388_501_006_577_559,
        }
        assert guard_denominator == guard_minima[name]


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run with assertions enabled.')
    main()
