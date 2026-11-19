"""Enumerate #758 halts after an initial J-run and a single block of bulks.

Place next to check_bb33.py and check_small_right_758.py, or put their
directory on PYTHONPATH.  The optional censuses use the reference counter map.
"""

from argparse import ArgumentParser
from collections import Counter
from pathlib import Path

from check_bb33 import first_return
from check_small_right_758 import FINAL, GROUP, ODD, PERIOD, SCALE


def after_bulks(x, count):
    """Return the left-counter cost and the final right counter."""
    current, odds = x, 0
    for _ in range(count // GROUP):
        residue = current % PERIOD
        odds += ODD[residue]
        current = SCALE * (current // PERIOD) + FINAL[residue]
    for _ in range(count % GROUP):
        odds += current % 2
        current = 3 * current // 2
    previous = (2 * current + 1) // 3
    return 8 * (current - x) - 9 * count + 4 * odds, 6 * previous - 13


def pairs(exponent, multiple):
    power = multiple * 3**exponent
    left = 2 * power - 1
    p2, p3, count = 2, 3, 1
    while True:
        denominator = 12 * p3 - 8 * p2
        lower = (left * p2 + denominator - 1) // denominator
        upper = ((left + 9 * count) * p2 + 12 * p3) // denominator
        if upper < 3:
            return
        assert upper - lower <= 2
        for x in range(max(3, lower), upper + 1):
            cost, right = after_bulks(x, count)
            gap = left - cost - right
            if gap != 1 and (gap != 3 or right % 4 != 3):
                continue
            initial = 4 * (x - 3) - 1
            # The maximal-J boundary permits c0=1 with a single preimage,
            # or an unmatched upper endpoint. Neither occurs in this range.
            for c0 in (initial, initial + 2):
                if 1 <= c0 <= left - 1:
                    seed = power + c0 - 1 - 2 * exponent - 4 * (multiple == 2)
                    assert first_return(seed, batch=False) is None
                    yield count, seed
        p2 *= 4
        p3 *= 9
        count += 2


def census(q, distance):
    size = distance + 3
    hits = bytearray(size)
    best = streak = farthest = 0
    for i in reversed(range(size)):
        seed = q - distance + i
        successor = first_return(seed)
        if successor is not None:
            assert successor > seed
        if successor is None or (successor <= q + 2 and hits[successor - q + distance]):
            hits[i] = 1
            streak += 1
            best = max(best, streak)
            farthest = max(farthest, q - seed)
        else:
            streak = 0
    return sum(hits), best, farthest


def run(args):
    roots = []
    for exponent in range(20, 293):
        for multiple in (1, 2):
            seeds = list(pairs(exponent, multiple))
            assert len(seeds) % 2 == 0
            for (count, q), (other_count, sibling) in zip(seeds[::2], seeds[1::2]):
                assert (other_count, sibling) == (count, q + 2)
                roots.append((exponent, multiple, count, q))
    counts = Counter(count for _, _, count, _ in roots)
    assert counts == {1: 69, 5: 46, 7: 11, 9: 8, 11: 1, 13: 1}
    print(len(roots), "pairs; counts by bulk-run length:", sorted(counts.items()))
    if args.census:
        max_streak = max_distance = 0
        for exponent, multiple, count, q in roots:
            pop, streak, distance = census(q, 100000)
            max_streak = max(max_streak, streak)
            max_distance = max(max_distance, distance)
            print(exponent, multiple, count, pop, streak, distance, flush=True)
        assert (max_streak, max_distance) == (53, 67489)
    if args.futures:
        roots_file = args.table.read_text().splitlines()[1:]
        assert len(roots_file) == 546
        for row in roots_file:
            exponent, multiple, _, _, offset = map(int, row.split())
            seed = multiple * 3**exponent + offset
            for _ in range(8192):
                successor = first_return(seed)
                assert successor is not None and successor > seed
                seed = successor
            print(exponent, multiple, seed, flush=True)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--census", action="store_true")
    parser.add_argument("--futures", action="store_true")
    parser.add_argument("--table", type=Path, default=Path(__file__).with_name("power_gates_758.tsv"))
    run(parser.parse_args())
