"""Estimate the #758 raw clock conditional on reaching A(1,H) from blank.

Run this file beside the other research/bb3x3 scripts. Each local clock is
exact. Weighting them to model the long, untraced orbit is heuristic.
"""
import argparse
from bisect import bisect_right
from decimal import Decimal
from random import Random

from after_fourth_758 import CHECKPOINT
from after_target_758 import CHECKPOINT as POST_TARGET
from check_bb33 import HALTING_TARGET, champion_step
from exact_fourth_758 import MERGER
from target_clock_758 import first_pass, follow
from timing_758 import branch_cost


def powers_through(limit):
    powers = [1]
    while powers[-1] < limit:
        powers.append(3 * powers[-1])
    return powers


def timed_reset(seed, powers):
    """Exact first return from A(1,seed), including the raw transition cost.

    A terminal branch returns None in the seed position. The powers list is a
    search accelerator only. Further powers are generated on demand.
    """
    half = 1 if seed % 2 else 2
    base = seed + 4 * (half - 1)
    elapsed = (14 * seed + 24) * (half - 1)
    k = bisect_right(powers, base // half) - 1
    power = powers[k]
    while 3 * half * power <= base + 2 * k + 2:
        k += 1
        power *= 3
    elapsed += (12 * half**2 * ((power**2 - 1) // 8)
                - 17 * half * ((power - 1) // 2)
                + (5 * base + 14) * k + 5 * k * (k - 1))
    a, c = 2 * half * power - 1, base + 2 * k + 1 - half * power
    for _ in range(5000):
        elapsed += branch_cost(a, c)
        nxt = champion_step(a, c)
        if nxt is None:
            return None, elapsed
        a, c = nxt
        if a == 1:
            return c, elapsed
    raise RuntimeError(f'Seed {seed} exceeded the limit of 5000 post-prefix calls.')


def local_rate(seed, powers, burn, keep):
    """Return the first new parity and the time per seed gained after burn-in."""
    first_parity = None
    start = None
    elapsed = 0
    for step in range(burn + keep):
        if step == burn:
            start = seed
        seed, clock = timed_reset(seed, powers)
        if seed is None:
            return None
        if step == 0:
            first_parity = seed % 2
        if step >= burn:
            elapsed += clock
    return first_parity, Decimal(elapsed) / (seed - start)


def estimate(lo, hi, strata, rng_seed, burn, keep):
    rng = Random(rng_seed)
    powers = powers_through(hi)
    elapsed = Decimal(0)
    even_weight = 2 if lo % 2 == 0 else 0  # twice the modeled even probability
    retries = 0
    for i in range(strata):
        left = lo + (hi - lo) * i // strata
        right = lo + (hi - lo) * (i + 1) // strata
        for _ in range(100):
            draw = rng.randrange(left, right)
            even = local_rate(draw + draw % 2, powers, burn, keep)
            odd = local_rate(draw + 1 - draw % 2, powers, burn, keep)
            if even is not None and odd is not None:
                break
            retries += 1
        else:
            raise ValueError(f'No surviving paired sample found in [{left}, {right}).')
        if even[0] == odd[0]:
            even_weight = 2 if even[0] == 0 else 0
        elif even[0] == 1:
            even_weight = 1
        rate = (even_weight * even[1] + (2 - even_weight) * odd[1]) / 2
        elapsed += (right - left) * rate
    return elapsed, retries


# Each row gives the seed and the exact cumulative raw time from A(1,3).
# The optional replay mode reconstructs them without quadrature.
SMALL_CHECKS = (
    (100_008, 32_247_774_174_667),
    (1_000_007, 27_810_930_125_361_618),
    (10_000_048, 23_644_585_702_717_369_942),
    (100_000_009, 21_383_779_029_167_874_368_822),
)


def audit(replay):
    powers = powers_through(HALTING_TARGET + 1)
    samples = [*range(3, 1000), HALTING_TARGET - 1, HALTING_TARGET, HALTING_TARGET + 1]
    for power in (3**12, 3**30, 3**170):
        samples.extend(power + delta for delta in range(-3, 4))
    for origin in samples:
        a, c = 1, origin
        elapsed = 0
        while True:
            elapsed += branch_cost(a, c)
            nxt = champion_step(a, c)
            if nxt is None:
                c = None
                break
            a, c = nxt
            if a == 1:
                break
        assert (c, elapsed) == timed_reset(origin, powers)
    if replay:
        seed, elapsed = 3, 0
        for target, expected in SMALL_CHECKS:
            while seed < target:
                seed, dt = timed_reset(seed, powers)
                assert seed is not None
                elapsed += dt
            assert (seed, elapsed) == (target, expected)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--strata', type=int, default=4096)
    parser.add_argument('--runs', type=int, default=3)
    parser.add_argument('--burn', type=int, default=8)
    parser.add_argument('--keep', type=int, default=16)
    parser.add_argument('--replay', action='store_true', help='recompute four small blank checkpoints')
    args = parser.parse_args()
    if min(args.strata, args.runs, args.burn, args.keep) < 1 or args.strata > 899_999:
        parser.error('Use positive arguments and at most 899999 strata.')
    if not __debug__:
        parser.error('Run without -O to enable the checks.')
    audit(args.replay)
    spans = [(f'small {i}', x, y, ty - tx)
             for i, ((x, tx), (y, ty)) in enumerate(zip(SMALL_CHECKS, SMALL_CHECKS[1:]), 1)]
    exit_seed, _, target_clock = first_pass(HALTING_TARGET + 906)
    _, tail = follow(exit_seed, {POST_TARGET: (0, 0)}, POST_TARGET)
    spans.extend([
        ('fourth crossing', MERGER, CHECKPOINT,
         12_009_315_348_729_165_034_617_066_232_977_846_431_994_862_719
         + 868_964_390_669_458_400_613_660_337_140_973_728_114_577_608),
        ('post-target escape', HALTING_TARGET + 906, POST_TARGET, target_clock + tail),
        ('candidate', CHECKPOINT, HALTING_TARGET, None),
    ])
    for name, lo, hi, exact in spans:
        print(name + (f' (exact {Decimal(exact):.7E})' if exact else ''), flush=True)
        for run in range(args.runs):
            clock, retries = estimate(lo, hi, args.strata, run, args.burn, args.keep)
            error = '' if exact is None else f' error {100 * (clock / exact - 1):+.4f}%'
            print(f'  run {run}: {clock:.7E}{error}, {retries} paired draws rejected', flush=True)


if __name__ == '__main__':
    main()
