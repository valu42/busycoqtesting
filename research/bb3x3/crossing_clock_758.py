"""Raw-step bounds from timed common words along the certified blank crossings."""
from fractions import Fraction
from itertools import pairwise
from typing import NamedTuple

from angular_clock_758 import KNOTS, RATE, certify_potential, potential
from check_bb33 import champion_step
from check_power_crossings_758 import GATES, LEGS, read_report, windows
from exact_fourth_758 import MERGER
from fourth_clock_758 import timed_return, verify as verify_fourth_clock
from jump_after_third import ELAPSED, FINAL, START
from mass_clock_758 import raw_lower_bound

# The witness bounds in CROSSING_CLOCK_758.md apply even at new cuts.
REACH = 100_000
DENOMINATOR = 1058


class ReturnBounds(NamedTuple):
    min_cost: int
    max_cost: int
    min_gain: int
    max_gain: int


def common_rates(lo, hi, parity):
    """Enclose a first-return cost and seed gain on one parity of [lo,hi)."""
    left_c = lo + (parity - lo) % 2
    right_c = hi - 1 - (hi - 1 - parity) % 2
    if left_c > right_c or left_c < 3:
        return None
    left_a = right_a = 1
    low_cost = high_cost = low_charge = high_charge = 0
    for step in range(1000):
        assert left_a >= right_a and left_c <= right_c
        assert left_a % 2 == right_a % 2 and left_c % 2 == right_c % 2
        if step and right_a <= 1 <= left_a and left_a % 2:
            return None  # Possible intermediate first reset.
        if left_a <= left_c:
            reset = left_a % 2 == 0
            if reset:
                assert left_c % 2
                qlo = qhi = 5
            else:
                qlo = qhi = 4 if left_c % 2 else 8  # J or even-seed opening.
            small, large = right_a, left_a
        elif left_c % 2 and right_a >= 4 * ((right_c + 1) // 4) + 3:
            qlo, qhi = 5, 9
            small, large = left_c, right_c
            reset = False
        else:
            return None
        low_cost += 3 * small**2
        high_cost += 3 * large**2 + 30 * (left_a + 2 * right_c) + 65
        low_charge += qlo
        high_charge += qhi
        if reset:
            assert low_charge % 2 == high_charge % 2 == 0
            assert (high_charge - low_charge) % 4 == 0
            return ReturnBounds(low_cost, high_cost, low_charge // 2, high_charge // 2)
        left_a, left_c = champion_step(left_a, left_c)
        right_a, right_c = champion_step(right_a, right_c)
    return None


def potential_numerator(seed):
    w = 1 + 2 * seed
    return 11 * w**3 + DENOMINATOR * (9 * w**2 + 30 * w)


def segment_bounds(lo, hi, depth):
    """Return a raw lower bound, generic upper saving, and covered seed width."""
    even, odd = (common_rates(lo, hi, parity) for parity in (0, 1))
    if even is None or odd is None:
        if depth and hi - lo > 4 * REACH:
            mid = (lo + hi) // 2
            left = segment_bounds(lo, mid, depth - 1)
            right = segment_bounds(mid, hi, depth - 1)
            return tuple(a + b for a, b in zip(left, right))
        return 0, 0, 0

    # Mass charges 5 and 9 on L give the same output seed parity.
    rates = (even, odd)
    output = [(parity + row.min_gain) % 2 for parity, row in enumerate(rates)]
    overhead_cost = max(even.max_cost, odd.max_cost)
    overhead_gain = max(even.max_gain, odd.max_gain)
    if output == [0, 1]:
        overhead_cost = overhead_gain = 0  # Both parities loop.
    elif output == [1, 0]:
        # Alternating returns leave at most one unmatched member.
        rates = (ReturnBounds(*(a + b for a, b in zip(even, odd))),)
    else:
        rates = (rates[output[0]],)  # At most one transient before the loop.

    low_rate = min(Fraction(r.min_cost, r.max_gain) for r in rates)
    high_rate = max(Fraction(r.max_cost, r.min_gain) for r in rates)
    lower = low_rate * max(0, hi - lo - REACH - overhead_gain)
    upper = high_rate * (hi - lo + REACH) + overhead_cost
    generic = Fraction(potential_numerator(hi) - potential_numerator(lo + REACH),
                       DENOMINATOR)
    savings = generic - upper
    return lower // 1, max(0, savings // 1), hi - lo


def audit_intervals():
    checked = 0
    for lo in range(1000, 2000, 7):
        for parity in (0, 1):
            bounds = common_rates(lo, lo + 23, parity)
            if bounds is None:
                continue
            for seed in range(lo + (parity - lo) % 2, lo + 23, 2):
                nxt, cost = timed_return(seed)
                gain = nxt - seed
                assert bounds.min_cost <= cost <= bounds.max_cost
                assert bounds.min_gain <= gain <= bounds.max_gain
                assert (gain - bounds.min_gain) % 2 == 0
                checked += 1
    assert checked > 1000


def verify():
    certify_potential()
    assert RATE == Fraction(33, DENOMINATOR)
    assert KNOTS[0][:2] == (0, Fraction(1, 23))
    assert potential(0, 0) == 0 and potential(0, Fraction(1, 23)) > 0
    assert potential(1, 0) <= 0
    read_report()
    audit_intervals()
    assert FINAL <= LEGS['power33'][0]
    lower = raw_lower_bound(1 + 2 * START) + ELAPSED
    upper = 2 + potential_numerator(MERGER) // DENOMINATOR
    for leg in LEGS:
        grid = windows(leg)
        if leg in GATES:
            m, multiple, _, _ = GATES[leg]
            # Both ordinary gate words apply through this cut.
            end = multiple * 3**m - 2*m - (4 if multiple == 1 else 6)
            last = grid[-1][1]
            cuts = [*range(last, end, LEGS[leg][2]), end]
            grid += list(pairwise(cuts))
        span = 0
        for lo, hi in grid:
            local_lower, saving, width = segment_bounds(lo, hi, 8)
            lower += local_lower
            upper -= saving
            span += width
        print(f'{leg}: common words cover {span:,} of '
              f'{grid[-1][1] - grid[0][0]:,} seed units.', flush=True)
    _, old_clock = verify_fourth_clock()
    suffix = old_clock - raw_lower_bound(1 + 2 * MERGER)
    lower += suffix
    upper += suffix
    assert lower == 75_287_784_527_483_315_086_258_653_649_976_784_825_150_292_446
    assert upper == 111_828_955_391_337_651_168_241_433_086_744_445_106_293_997_533
    print(f'#758 raw clock at the checkpoint lies in [{lower:,}, {upper:,}].')
    return lower, upper


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run without -O to check assertions.')
    verify()
