#!/usr/bin/env python3
"""Check the binary first-contact thresholds and the first f edge on the blank run."""
from itertools import product

from check_bb33 import H397, compressed_sweeps, sweep
from transitive_section_397 import propagate


def register(bits):
    """Bits are in head-facing order. Ignore a final unpaired bit."""
    value = width = 0
    active = True
    for i in range(0, len(bits) - 1, 2):
        first, second = bits[i:i + 2]
        if active:
            value += first << width
            width += 1
        active = first == second
    return value, width


def check_registers():
    for n in range(7):
        for pairs in product((0, 1), repeat=2 * n):
            value, width = register(pairs)
            work = list(pairs)
            for t in range(value + 1):
                outgoing = propagate(work, 0)
                if t < value:
                    assert outgoing == -1
                    assert register(work) == (value - t - 1, width)
                else:
                    expected = 0 if not pairs or pairs[-2] == pairs[-1] else 3
                    assert outgoing == expected
                    assert register(work) == ((1 << width) - 1, width)
            for tail in ((), (0,), (1,)):
                bits = pairs + tail
                for mode in range(6):
                    if not bits:
                        continue
                    if mode in (0, 3):
                        body, q = bits, 1 if mode == 0 else 2
                    else:
                        _, outgoing = H397.rules[mode][bits[0]]
                        q = {-1: 0, 0: 1, 3: 2}[outgoing]
                        body = bits[1:]
                    projected, _ = register(body)
                    danger = len(body) % 2 == 1 and body[-1] == 0 and q > projected
                    assert danger == (sweep(H397, bits, mode) is None)


def sparse_period(prefix, extra):
    """Build one period of (sweep offset, incoming carry) just past prefix[:29+extra]."""
    first = list(prefix[:29])
    events = []
    for t in range(1024):
        carry = propagate(first, H397.modes[t % 4])
        if carry != -1:
            events.append((t, carry))
    assert tuple(first) == prefix[:29]
    ordinary_phases = [((64 + t) % 1024, carry) for t, carry in events if carry in (0, 3)]
    assert ordinary_phases == [(769, 3), (961, 0)]
    assert sum(carry in (2, 4, 5) for _, carry in events) == 21
    period = 1024
    for initial in prefix[29:29 + extra]:
        bit = initial
        next_events = []
        for shift in (0, period):
            for t, mode in events:
                bit, carry = H397.rules[mode][bit]
                if carry != -1:
                    next_events.append((t + shift, carry))
        assert bit == initial
        events = next_events
        period *= 2
    return period, events


def check_first_f():
    # At this return all cells used for the static prefix are occupied.
    # Replaying two complete local periods per extra bit is enough by the
    # transitive-section theorem. Time labels retain the original sweep index.
    start = 64 + 64 * 1024
    cut = 29 + 16
    target = 926_416_354
    word = H397.seed
    counts = [0] * 6
    earlier_pair = []
    for t in range(start):
        bits = list(word)
        h = propagate(bits, H397.modes[t % 4])
        if h != -1:
            assert h in (1, 3)
            counts[h] += 1
            if 28_417 <= t <= 37_346:
                earlier_pair.append((t, h, len(word)))
            bits.extend(H397.extension[h])
        assert bits[-1] == 1
        word = tuple(bits)
    assert earlier_pair == [(28_417, 3, 65), (37_346, 3, 68)]
    period, events = sparse_period(word, cut - 29)
    bits = list(word[cut:])
    for base in range(start, target + 1, period):
        for offset, mode in events:
            t = base + offset
            if t > target:
                break
            h = propagate(bits, mode)
            if h == -1:
                assert bits[-1] == 1
                continue
            counts[h] += 1
            if h == 5:
                assert t == target and cut + len(bits) == 137
                assert counts[0] == counts[2] == counts[4] == 0
                print(f'First f at sweep index {t:,}, occupied suffix length 137.')
                print('Earlier b and d growths:', counts[1], counts[3])
                return
            assert h in (1, 3)
            bits.extend(H397.extension[h])
    raise AssertionError('missing f event')


def check_truncated_frontier():
    start, end = 636_770, 637_734
    blank = compressed_sweeps(H397, start)
    assert len(blank) == 91
    word = list(blank[:40])
    assert ''.join(map(str, word)) == '1100010001000000000110000001100000011001'
    fixed = word.copy()
    arrivals = []
    changes = []
    previous = tuple(word[-2:])
    for t in range(start, end + 1):
        mode = H397.modes[t % 4]
        h = propagate(fixed, mode)
        if h != -1:
            arrivals.append((t, h))
        h = propagate(word, mode)
        if h in (2, 4):
            assert t == end and h == 4
            break
        if h != -1:
            assert t == start and h == 3
            word.extend(H397.extension[h])
        current = tuple(word[-2:])
        if current != previous:
            changes.append((t, current))
        previous = current
    assert arrivals == [(636_770, 3), (636_865, 1), (637_354, 0),
                        (637_697, 2), (637_734, 3)]
    assert changes == [(637_354, (1, 1)), (637_697, (0, 0))]
    assert len(word) == 43
    print('The 40-bit truncation grows by d, loses its 01 cap, and halts by e.')


def check_paired_truncation():
    start, end = 9_288_449, 9_295_330
    original = compressed_sweeps(H397, start)
    assert len(original) == 101
    word = list(original[:47])
    assert ''.join(map(str, word)) == '00100010001000111000110100101100000011001011001'
    growths = []
    for t in range(start, end + 1):
        h = propagate(word, H397.modes[t % 4])
        if h == -1:
            continue
        growths.append((t, h, len(word)))
        if H397.extension[h] is None:
            break
        word.extend(H397.extension[h])
    assert growths == [(start, 3, 47), (9_289_186, 3, 50), (end, 4, 53)]
    assert [t % 1024 for t, _, _ in growths[:2]] == [28_417 % 1024, 37_346 % 1024]
    print('The 47-bit truncation reproduces the two d phases, then halts by e.')


if __name__ == '__main__':
    check_registers()
    check_first_f()
    check_truncated_frontier()
    check_paired_truncation()
