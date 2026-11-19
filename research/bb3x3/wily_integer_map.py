#!/usr/bin/env python3
"""Wily's exact single-generator integer map. Add --power 192 for the sign certificate."""
import argparse
from functools import lru_cache
from itertools import product

from check_bb33 import WILY, sweep
from wily_edge_stream import CHECKPOINTS, blank_checkpoint, period_through


@lru_cache(maxsize=65_536)
def image(n):
    """The virtual action of s0 on n/3. Domain: integers prime to 3."""
    if n % 3 == 0:
        raise ValueError("the virtual alternating-tail model requires 3 not to divide n")
    if n == -2:
        return -1
    if n % 8 == 0:
        return n + 21
    if n % 8 == 4:
        return n - 3
    if n % 4 == 2:
        return 3 + 4 * image((n - 6) // 4)
    if n % 4 == 3:
        return 2 * image((n + 3) // 2)
    return 2 * image((n - 9) // 2)


@lru_cache(maxsize=65_536)
def inverse(y):
    """Inverse permutation of the same integer domain."""
    if y % 3 == 0:
        raise ValueError("nonunit input")
    if y == -1:
        return -2
    if y % 8 == 1:
        return y + 3
    if y % 8 == 5:
        return y - 21
    if y % 4 == 3:
        return 4 * inverse((y - 3) // 4) + 6
    middle = inverse(y // 2)
    return 2 * middle + (-3 if middle % 2 else 9)


def canonical_bucket(n):
    """Smallest B of the right parity with -B <= n <= 2B-3."""
    minimum = -n if n < 0 else (n + 4) // 2
    size = 1 << (minimum - 1).bit_length()
    if (n + size) % 3:
        size *= 2
    return size


def encode(word):
    bucket = 1 << len(word)
    value = sum(bit << index for index, bit in enumerate(word))
    return 3 * value - bucket, bucket


def advance(n, bucket):
    """One actual s0 sweep, with its edge carry. None means no edge arrival."""
    value = image(n)
    if (value + bucket) % 3:
        return None, None, 1
    if value >= -bucket:
        return value, bucket, None
    if value >= -4 * bucket:
        return value, 4 * bucket, 3
    if value >= -7 * bucket:
        return value, 16 * bucket, 2
    assert -28 * bucket <= value <= -25 * bucket - 3
    return value + 26 * bucket, 2 * bucket, 0


def terminal(n):
    """Descend to the exceptional input -2 or a multiple of four."""
    while n != -2 and n % 4:
        if n % 4 == 2:
            n = (n - 6) // 4
        elif n % 4 == 3:
            n = (n + 3) // 2
        else:
            n = (n - 9) // 2
    return n


def check_slow_predecessors():
    # Invert the original bit table, independently of the scalar inverse.
    rules = [tuple(next((old, carry) for old, (written, carry) in enumerate(row)
                        if written == bit) for bit in (0, 1)) for row in WILY.rules]

    def through(period, initial):
        bit = initial
        output = []
        for _ in range(2):
            for carry in period:
                if carry != -1:
                    bit, carry = rules[carry][bit]
                output.append(carry)
            if bit == initial:
                return output
        raise AssertionError("two periods must restore the bit")

    period = [0]
    for bit in (1, 0, 0, 1, 1, 0):
        period = through(period, bit)
    assert period == [-1, -1, -1, 1, -1, 1, -1, 1]
    for k in range(1, 14):
        slots = [i + 1 for i, event in enumerate(period) if event != -1]
        expected = 2 * ((2**(k + 1) + 2) // 3)
        assert slots[0] == expected and len(slots) == 3
        assert all(event in (-1, 1) for event in period)
        n = 11 - 48 * 4**k
        assert image(n) > 0
        for _ in range(expected):
            assert n < 0
            n = inverse(n)
        assert n > 0
        following = through(through(period, 1), 0)
        assert [i + 1 for i, event in enumerate(following) if event != -1] == [
            slots[1], len(period) + slots[0], 2 * len(period)]
        period = following


def check_zero_reference_obstruction():
    # This sweep from the virtual past changes the infinite alternating tail.
    numerator, mode = 2_031_034_478, 0
    assert image(numerator) == -318_922_769
    for _ in range(30):
        bit = numerator % 2
        numerator = (numerator - 3 * bit) // 2
        _, mode = WILY.rules[mode][bit]
        assert mode != -1
    assert (numerator, mode) == (-1, 1)
    for target in ((-2, 0), (-1, 1)):
        bit = numerator % 2
        numerator = (numerator - 3 * bit) // 2
        _, mode = WILY.rules[mode][bit]
        assert (numerator, mode) == target

    word, n = (0,), START
    for width in range(30):
        expected = {0} if width == 0 else {1, 2} if width == 1 else {0, 1, 2, 3}
        assert set(word) == expected
        bit = n % 2
        word = period_through(word, bit)
        n = (n - 3 * bit) // 2


def check_periodic_family():
    first = tuple(int(bit) for bit in "0000000001101110101100001001100001")
    repeat = (1, 1) + first[1:]

    def extend(bits, word, copies, clock):
        for bit in bits:
            # The previously processed prefix first returns after clock steps.
            # The next cell doubles this period iff it flips an odd number
            # of times during its copies of the incoming primitive word.
            if (len(word) - word.count(2)) * copies % 2:
                copies *= 2
                clock *= 2
            outgoing = period_through(word, bit)
            copies, remainder = divmod((len(word) - word.count(3)) * copies, len(outgoing))
            assert remainder == 0
            word = outgoing
        return word, copies, clock

    result = extend(first, (0,), 1, 1)
    assert result == ((0, 1), 2, 4096)
    assert extend(repeat, *result) == ((0, 1), 2, 4096 * 2048)
    assert extend((0, 1), *result) == result

    size = 1 << len(first)
    value = 3 * sum(bit << i for i, bit in enumerate(first)) - 2 * size
    assert value == -7_328_996_864
    n = value
    flips = 0
    for t in range(1, 4097):
        following = image(n)
        flips += (n - following) % 3 != 0
        n = following
        assert (n == value) == (t == 4096)
    assert flips == 4


def check_small():
    # Independent comparison on all allocated words, including the bare edge.
    for width in range(13):
        for word in product((0, 1), repeat=width):
            n, bucket = encode(word)
            actual = sweep(WILY, word, 0)
            value, size, mode = advance(n, bucket)
            if actual is None:
                assert mode == 1 and terminal(n) == -2
            else:
                assert (value, size) == encode(actual)
                assert terminal(n) != -2
    for n in range(-100_000, 100_001):
        if n % 3 == 0:
            continue
        y = image(n)
        assert inverse(y) == n and image(inverse(n)) == n
        if n < 0:
            assert (y > 0) == (terminal(n) in (-8, -16))
        if n < 0 and y < 0 and n != -2:
            assert canonical_bucket(n) <= canonical_bucket(y)
        if n > 0 and y > 0:
            assert canonical_bucket(n) >= canonical_bucket(y)

    crossing_roots = {-8: (1, 1), -16: (1, 4), 1: (16, 1), 2: (64, 1), 5: (1, 2)}
    for origin, (numerator, denominator) in crossing_roots.items():
        frontier = [origin]
        for _ in range(10):
            following = []
            for n in frontier:
                assert canonical_bucket(image(n)) * denominator == canonical_bucket(n) * numerator
                following.extend(child for child in (4 * n + 6, 2 * n + (-3 if n % 2 else 9))
                                 if child * origin > 0)
            frontier = following

    # Every escape below this size has a positive predecessor before the
    # finite interval of possible negative preimages could repeat.
    for n in range(-5000, 0):
        if n % 3 == 0 or image(n) <= 0:
            continue
        bound = canonical_bucket(n)
        y = n
        for _ in range((bound + 2) // 3 + 2):
            y = inverse(y)
            if y > 0:
                break
            assert y >= -bound
        assert y > 0

    # Verify that each pair of chronological input sweeps agrees with s0 on
    # the nonempty tail after removing the two recurring zeros.
    word = WILY.seed
    for _ in range(4096):
        assert word[:2] == (0, 0)
        twice = sweep(WILY, sweep(WILY, word, 0), 1)
        if len(word) == 2:
            assert twice[2:] == (0, 0, 1, 1, 0, 0)
        else:
            assert twice[2:] == sweep(WILY, word[2:], 0)
        word = twice


# One s0 iteration equals two original Wily sweeps after the first pair.
START = -227_089_934_777_573_210_432
START_BUCKET = 1 << 69
START_ITERATION = 1_721_188


def replay_start():
    n, bucket = -28, 64
    corrections = []
    for index in range(1, START_ITERATION + 1):
        n, bucket, mode = advance(n, bucket)
        assert mode != 1
        if mode == 0:
            corrections.append((index, n, bucket))
    assert corrections == [(583, -318_922_769, 1 << 29)]
    assert (n, bucket, mode) == (START, START_BUCKET, 3)
    # Cross-check against the chronological event-stream method at the exact
    # same sweep boundary, including the two removed zeros.
    rounds = 2 + 2 * START_ITERATION
    suffix, _ = blank_checkpoint(rounds)
    assert suffix[:2] == (0, 0)
    assert encode(suffix[2:]) == (START, START_BUCKET)
    print(f"At sweep {rounds}: n = {n}, B = {bucket}")


def certify_negative(power):
    # A 3 extension creates 00. Its next input 0 traverses both fresh bits
    # in one sweep and reaches the next edge in mode 3.
    events = []
    suffix, _ = blank_checkpoint(1 << power,
                                 lambda width, mode, nex: events.append((width, mode, nex)))
    events = [event for event in events if event[0] >= 69]
    assert events and events[0][0] == 69
    for index, (width, mode, following) in enumerate(events):
        assert width == 69 + 2 * index and mode == 3
        assert following == 0 or (following is None and index == len(events) - 1)
    assert len(suffix) == 69 + 2 * len(events)
    assert suffix[-2:] == (0, 0)
    last, bucket = encode(suffix[2:])
    assert last <= -bucket // 4 - 3 and canonical_bucket(last) == bucket
    if power in CHECKPOINTS:
        assert len(suffix) == CHECKPOINTS[power][0]
    print(f"The two highest suffix bits stay 00 from sweep {2 + 2 * START_ITERATION} "
          f"through 2^{power}. Checked {len(events)} extensions.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--power", type=int, default=96)
    args = parser.parse_args()
    if not __debug__ or args.power < 22:
        parser.error("use assertions and an exponent of at least 22")
    check_small()
    check_slow_predecessors()
    check_periodic_family()
    check_zero_reference_obstruction()
    replay_start()
    certify_negative(args.power)
