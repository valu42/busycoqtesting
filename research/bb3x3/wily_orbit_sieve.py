#!/usr/bin/env python3
"""Sieve the whole cyclic orbit on finite prefixes for Wily's sign-change inputs."""
import argparse
from bisect import bisect_left
from collections import Counter
from itertools import product

from wily_edge_stream import append_run, through
from wily_integer_map import START, image, inverse, terminal

# Two roots of the negative-to-positive input forest.
ROOTS = (-8, -16)
EXPECTED = {
    -325005293, -3758096386, -21701425901, -257634140162,
    -1948454754451451, -4323174695770738877, -4228484313993422914510738,
}
POSITIVE_ENTRANCE = 16472443404719956078


def prior_positive(n, limit):
    for steps in range(1, limit + 1):
        n = inverse(n)
        if n > 0:
            return steps, n
    raise RuntimeError("no positive predecessor within the specified bound")


class CarryPeriod:
    """Number of emissions and bit flips in any prefix of a compressed period."""
    def __init__(self, runs):
        self.ends = []
        self.offsets = []
        self.runs = runs
        size = emitted = flips = 0
        for mode, count in runs:
            self.offsets.append((emitted, flips))
            size += count
            self.ends.append(size)
            calls, parity = self.action(mode, count)
            emitted += calls
            flips ^= parity
        self.emitted = emitted
        self.flips = flips

    @staticmethod
    def action(mode, count):
        calls = count if mode in (1, 2) else (count + (mode == 0)) // 2
        return calls, 0 if mode == 2 else count % 2

    def prefix(self, count):
        if count == 0:
            return 0, 0
        i = bisect_left(self.ends, count)
        length = count - (self.ends[i - 1] if i else 0)
        calls, parity = self.action(self.runs[i][0], length)
        emitted, flips = self.offsets[i]
        return emitted + calls, flips ^ parity


# Layout of a pending forest constraint: n = offset + 2^shift * m, with m
# in the entire escape forest. A negative shift denotes an exact candidate.
def refine(shift, offset, numerator, width, bound):
    mask = (1 << width) - 1
    if shift < 0:
        if (offset - numerator) & mask == 0:
            yield shift, offset
        return
    bits = width - shift
    residue = (numerator - offset) >> shift
    while bits >= 2:
        if residue % 4 == 0:
            for root in ROOTS:
                candidate = offset + (root << shift)
                if candidate >= -bound and (candidate - numerator) & mask == 0:
                    yield -1, candidate
            return
        if residue % 4 == 2:
            constant, consumed = 6, 2
        else:
            constant, consumed = (-3 if residue % 4 == 3 else 9), 1
        offset += constant << shift
        shift += consumed
        residue = (residue - constant) >> consumed
        bits -= consumed
    # The largest even forest member is -8, and the largest odd one is -7.
    maximum = -8 if bits == 1 and residue % 2 == 0 else -7
    if offset + (maximum << shift) >= -bound:
        yield shift, offset


def sieve(bound_bits, precision, start=START):
    if not 1 <= bound_bits < precision:
        raise ValueError("precision must exceed a positive size bound")
    runs = [(0, 1)]
    # (physical binary prefix, events before its phase, phase, shift, offset)
    nodes = [(0, 0, 0, 0, 0)]
    seed_tail = start
    period = 1
    for width in range(1, precision + 1):
        digit = seed_tail % 2
        seed_tail = (seed_tail - 3 * digit) // 2
        previous = CarryPeriod(runs)
        new_runs, second_bit = through(runs, digit)
        assert second_bit == digit ^ previous.flips
        if previous.flips:
            other, restored = through(runs, second_bit)
            assert restored == digit
            for mode, count in other:
                append_run(new_runs, mode, count)
        children = []
        place = 1 << (width - 1)
        for prefix, index, phase, shift, offset in nodes:
            emitted, parity = previous.prefix(index)
            for half in range(previous.flips + 1):
                word = prefix + place * (digit ^ parity ^ half)
                for child_shift, child_offset in refine(shift, offset, 3 * word,
                                                         width, 1 << bound_bits):
                    children.append((word, emitted + half * previous.emitted,
                                     phase + half * period, child_shift, child_offset))
        nodes, runs = children, new_runs
        period <<= previous.flips
    assert all(shift < 0 for _, _, _, shift, _ in nodes)
    assert len({offset for *_, offset in nodes}) == len(nodes)
    return period, {offset: phase for _, _, phase, _, offset in nodes}


def periodic_exclusions():
    # Freeze the cycle summaries once. A target digit then determines whether
    # it must occur in the first or second traversal of the preceding cycle.
    seed, runs = START, [(0, 1)]
    levels = []
    for _ in range(40):
        bit = seed % 2
        seed = (seed - 3 * bit) // 2
        state = CarryPeriod(runs)
        levels.append((bit, state))
        first, middle = through(runs, bit)
        if state.flips:
            second, _ = through(runs, middle)
            for mode, count in second:
                append_run(first, mode, count)
        runs = first

    def first_missing(n):
        index = 0
        for width, (initial_bit, state) in enumerate(levels, 1):
            bit = n % 2
            n = (n - 3 * bit) // 2
            emitted, changes = state.prefix(index)
            half = bit ^ changes ^ initial_bit
            if half and not state.flips:
                return width
            index = emitted + half * state.emitted
        return None

    totals = Counter()
    for size in range(1, 13):
        for word in map(''.join, product("LS", repeat=size)):
            if any(word == word[:d] * (size // d)
                   for d in range(1, size) if size % d == 0):
                continue
            weight = size + word.count("L")
            # w contracts exactly 'weight' binary bits per repetition, so
            # 40 determined bits are independent of the arbitrary inner seed.
            n = -8
            for _ in range((40 + weight - 1) // weight):
                for letter in reversed(word):
                    n = 4*n + 6 if letter == "L" else 2*n + (-3 if n % 2 else 9)
            missing = first_missing(n)
            assert missing is not None
            copies = (missing + weight - 1) // weight
            totals[copies] += 1
            if copies > 2:
                assert word in {"L", "S", "LLS", "LSSSL"}
    assert sum(totals.values()) == 8032
    assert {n: totals[n] for n in (3, 7, 20)} == {3: 2, 7: 1, 20: 1}
    return totals


def checks():
    for n in range(-12000, 12001):
        if n % 3:
            assert inverse(image(n)) == image(inverse(n)) == n
    # Independent literal modular cycles, with no carry-stream compression.
    for seed in (START, -8, -16, -7, 5):
        for bits in (7, 10, 13, 16):
            bound = 1 << (bits - 2)
            modulus = 1 << bits
            x = seed % modulus
            phases = {}
            while x not in phases:
                phases[x] = len(phases)
                x = image(x if x % 3 else x + modulus) % modulus
            brute = {n: phases[n % modulus] for n in range(-bound, 0)
                     if n % 3 and image(n) > 0 and n % modulus in phases}
            assert sieve(bits - 2, bits, seed) == (len(phases), brute)
    assert prior_positive(START, 672030) == (672030, POSITIVE_ENTRANCE)
    assert image(POSITIVE_ENTRANCE) == -60830999776514433041


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--large", action="store_true", help="use the 2^160 bound at 320-bit precision")
    args = parser.parse_args()
    if not __debug__:
        parser.error("enable assertions")
    checks()
    print("Periodic outer words, by copies excluded:", dict(sorted(periodic_exclusions().items())))
    bound_bits, precision = (160, 320) if args.large else (100, 240)
    period, hits = sieve(bound_bits, precision)
    assert period == 1 << (137 if args.large else 103)
    assert set(hits) == EXPECTED
    for n, phase in sorted(hits.items()):
        assert terminal(n) in ROOTS and image(n) > 0
        if n % 3 == START % 3:
            steps, positive = prior_positive(n, 666233)
            assert positive != POSITIVE_ENTRANCE
            print(f"{n}: phase {phase - period}, previous positive {positive} at distance {steps}")
        else:
            print(f"{n}: phase {phase - period}, in residue class {n % 3} modulo 3")
    print(f"Exactly seven sign-escape inputs of magnitude at most 2^{bound_bits} "
          f"survive the entire cycle modulo 2^{precision}.")


if __name__ == "__main__":
    main()
