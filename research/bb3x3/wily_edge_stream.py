#!/usr/bin/env python3
"""Exact Wily Coyote edge-stream certificates. Run with --power 192 for the long check."""
import argparse
import hashlib
from collections import deque
from itertools import product

from check_bb33 import WILY, compressed_sweeps, sweep


def append_run(runs, mode, count):
    """A run is constant in 1 or 2, or alternates between 0 and 3."""
    if count == 0:
        return
    if runs:
        previous, size = runs[-1]
        following = 3 - previous if previous in (0, 3) and size % 2 else previous
        if following == mode:
            runs[-1] = previous, size + count
            return
    runs.append((mode, count))


def prefix(runs, count):
    result = []
    for mode, size in runs:
        if count <= size:
            append_run(result, mode, count)
            break
        result.append((mode, size))
        count -= size
    return result


def drop_first(runs, cyclic):
    mode, size = runs[0]
    result = runs[1:]
    if size > 1:
        following = 3 - mode if mode in (0, 3) else mode
        result.insert(0, (following, size - 1))
    if cyclic:
        append_run(result, mode, 1)
    return result


def through(runs, bit):
    output = []
    for mode, count in runs:
        if mode == 1:
            append_run(output, 3 if bit == 0 else 0, count)
            bit ^= count % 2
        elif mode == 2:
            append_run(output, 2 if bit == 0 else 1, count)
        else:
            zeros = (count + (mode == 0)) // 2
            on_zero = bit if mode == 0 else 1 - bit
            append_run(output, 1 if on_zero == 0 else 2, zeros)
            bit ^= count % 2
    return output, bit


def length(runs):
    return sum(size for _, size in runs)


def blank_checkpoint(rounds):
    if rounds < 0:
        raise ValueError("negative sweep count")
    runs = [(0, 1), (1, 1)]
    remaining = rounds
    periodic = True
    suffix = []
    extensions = []
    pending = deque(WILY.seed)
    while remaining:
        if not pending:
            mode = runs[0][0]
            extensions.append((len(suffix), mode))
            extension = WILY.extension[mode]
            if extension is None:
                return None, extensions
            pending.extend(extension)
            runs = drop_first(runs, periodic)
            remaining -= 1

        bit = pending.popleft()
        if periodic:
            period = length(runs)
            if remaining <= period:
                runs = prefix(runs, remaining)
                periodic = False
        if periodic:
            complete, extra = divmod(remaining, period)
            first, middle = through(runs, bit)
            partial_start = middle if complete % 2 else bit
            tail, final = through(prefix(runs, extra), partial_start)
            # Only mode 3 disappears. Consequently output length per input
            # period is independent of the starting bit.
            remaining = complete * length(first) + length(tail)
            if middle != bit:
                second, _ = through(runs, middle)
                for mode, count in second:
                    append_run(first, mode, count)
            runs = first
            bit = final
        else:
            runs, bit = through(runs, bit)
            remaining = length(runs)
        suffix.append(bit)
    return tuple(suffix) + tuple(pending), extensions


def period_through(period, initial_bit):
    """Literal, phase-preserving action on one infinite periodic stream."""
    bit = initial_bit
    out = []
    for _ in range(2):
        for mode in period:
            bit, emitted = WILY.rules[mode][bit]
            if emitted != -1:
                out.append(emitted)
        if bit == initial_bit:
            break
    assert bit == initial_bit
    for size in range(1, len(out) + 1):
        if len(out) % size == 0 and out == out[:size] * (len(out) // size):
            return tuple(out[:size])
    return ()


def check_rotation_lift():
    blocks = ((3, 1, 2), (1, 1), (0, 3), (2, 3, 1), (3, 0, 3, 0))
    for target, block in zip(((0,), (1,), (2,), (3,), (3, 0)), blocks):
        first, second = 1, 0
        output = []
        for mode in block:
            first, carry = WILY.rules[mode][first]
            if carry != -1:
                second, carry = WILY.rules[carry][second]
            if carry != -1:
                output.append(carry)
        assert (first, second, tuple(output)) == (1, 0, target)

    def edge(word):
        extension = WILY.extension[word[0]]
        if extension is None:
            return None
        word = word[1:] + word[:1]
        for bit in extension:
            word = period_through(word, bit)
        return word

    for words in (
        ((3, 0, 3, 0, 0, 3, 3, 0, 3, 0), (3, 0, 2, 3, 0), (3, 0), (3, 0)),
        ((3, 0, 0, 3, 3, 0, 3, 0, 3, 0), (3, 1, 0, 3, 0), (1, 1, 2, 3, 0), None),
    ):
        assert all(edge(a) == b for a, b in zip(words, words[1:]))


def check_edge_certificate():
    safe = (2,)
    stop = (1,)
    forward = (0, 3)
    reverse = (3, 0)
    table = {
        stop: (reverse, forward),
        safe: (safe, stop),
        reverse: (safe, stop),
        forward: (stop, safe),
    }
    for word, children in table.items():
        assert tuple(period_through(word, bit) for bit in range(2)) == children
    for word, next_word in ((forward, safe), (safe, reverse), (reverse, reverse)):
        mode = word[0]
        rest = word[1:] + word[:1]
        for bit in WILY.extension[mode]:
            rest = period_through(rest, bit)
        assert rest == next_word
    assert WILY.extension[stop[0]] is None
    word = (0, 1)
    for bit in (0, 0, 0, 0, 0, 1, 0, 0):
        word = period_through(word, bit)
    assert word == safe

    # Check the run rules independent of periodic-stream algebra.
    for size in range(1, 9):
        for mode, initial in product(range(4), range(2)):
            stream = [mode if mode in (1, 2) or i % 2 == 0 else 3 - mode
                      for i in range(size)]
            bit = initial
            expected = []
            for event in stream:
                bit, emitted = WILY.rules[event][bit]
                if emitted != -1:
                    expected.append(emitted)
            got, final = through([(mode, size)], initial)
            runs = []
            for event in expected:
                append_run(runs, event, 1)
            assert (got, final) == (runs, bit)

    # Check at every chronological horizon, including a fresh-edge allocation.
    word = WILY.seed
    for n in range(1025):
        suffix, _ = blank_checkpoint(n)
        assert suffix == word
        word = sweep(WILY, word, WILY.modes[n % 2])
    for n in (2**16 + 1, 2**32):
        assert blank_checkpoint(n)[0] == compressed_sweeps(WILY, n)


CHECKPOINTS = {
    96: (291, "2227cc873414ca1f243bc4281e0fa4f472146fffaab72223428979796be99bd1"),
    128: (383, "0b594c2242ceba0cd1a6c4d5ac6bd0388906f2ae0916910db037518ab0f377b0"),
    192: (577, "567df9a7f34a5764e1a90917ef2f35cfbb4984790de9560d8310261718d0f2d6"),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--power", type=int, default=96)
    args = parser.parse_args()
    if not __debug__ or args.power < 0:
        parser.error("use assertions and a nonnegative exponent")
    check_edge_certificate()
    check_rotation_lift()
    rounds = 2**args.power
    suffix, extensions = blank_checkpoint(rounds)
    if suffix is None:
        print("Halting carry at suffix length", extensions[-1][0])
        return
    digest = hashlib.sha256(bytes(b + 48 for b in suffix)).hexdigest()
    if args.power in CHECKPOINTS:
        assert (len(suffix), digest) == CHECKPOINTS[args.power]
    print(f"2^{args.power} completed passes, {len(suffix)} suffix bits, SHA-256 {digest}")
    print("Raw transition lower bound per encoding:", rounds * (rounds + 1) // 2)
    print("Non-s3 extensions (suffix length, mode):",
          [(width, mode) for width, mode in extensions if mode != 3])


if __name__ == "__main__":
    main()
