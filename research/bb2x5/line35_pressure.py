"""Exact chronological debt of a synchronized suffix at a fixed right-index cut."""
import argparse
from pathlib import Path

from line35_band import load_checkpoint, pascal_at


def column(bits, index, period):
    """Subset-sum transform of the binomial coefficients, with addition modulo two."""
    word = bytearray(period)
    packed = bits.to_bytes((bits.bit_length() + 7) // 8, 'little')
    for degree in range(index + 1):
        position = index - degree
        if position // 8 < len(packed):
            word[degree] = (packed[position // 8] >> (position % 8)) & 1
    stride = 1
    while stride < period:
        for start in range(stride, period, 2 * stride):
            for t in range(start, start + stride):
                word[t] ^= word[t - stride]
        stride *= 2
    return word


def burst(bits, k, initial_neutral):
    """Return exact all-time bounds after confirming the starting center's phase."""
    p = k - 1
    if p < 2 or p & (p - 1):
        raise ValueError('choose k = 2**r + 1 with r >= 1')
    mask = (1 << (k + 1)) - 1
    bits &= mask
    period = 2 * p
    h = column(bits, k, period)
    lower = column(bits, k - 1, period)
    assert all(lower[t] ^ lower[t + p] for t in range(p))
    assert all(h[(t + 1) % period] == (h[t] ^ lower[t]) for t in range(period))
    # The current label of a just-joined center might predate its Pascal rule.
    # The perpetual certificate applies from the next update in that case.
    aligned = bool(h[0] and not h[-1]) == bool(initial_neutral)
    height = low = high = events = 0
    for t, bit in enumerate(h):
        event = int(bit and not h[t - 1])
        height += 4 * event - 1
        low = min(low, height)
        high = max(high, height)
        events += event
    assert height == 0 and events == period // 4 and high - low <= p + 1
    return period, events, high - low, aligned


def audit():
    # Check the transform, the arbitrary-initial-phase density bound and its sharpness.
    for k in range(1, 10):
        period = 1 << k.bit_length()
        weights = set()
        deviations = set()
        for a in range(1 << k):
            bits = 1 | (a << 1)
            h = column(bits, k, period)
            simple = bits
            for value in h:
                assert value == (simple >> k) & 1
                simple = (simple ^ (simple << 1)) & ((1 << (k + 1)) - 1)
            assert simple == bits
            weights.add(sum(x and not h[t-1] for t, x in enumerate(h)))
            if k in (3, 5, 9):
                deviations.add(burst(bits, k, bool(h[0] and not h[-1]))[2])
        if k == 1:
            assert weights == {period // 2}
        else:
            least = period >> (1 + (k - 1).bit_count())
            assert min(weights) == least and max(weights) == period // 2 - least
        if deviations:
            assert max(deviations) == k
    print('Pascal samples, extremal event counts, and sharp dyadic bounds checked through nine triples.')


def profile(path):
    record, band = load_checkpoint(path)
    bits = 1 | (band.nonopen << 1)
    # Inverse transport gives permanent coefficients relative to epoch five.
    base = pascal_at(bits, -((record['epoch'] - 5) // 2), band.count)
    assert pascal_at(base, (record['epoch'] - 5) // 2, band.count) == bits
    print('epoch', record['epoch'], 'covered triples', band.count)
    p = 2
    while p + 1 <= band.count:
        k = p + 1
        initial_neutral = (band.neutral >> (k - 1)) & 1
        period, count, spread, aligned = burst(bits, k, initial_neutral)
        first = record['epoch'] if aligned else record['epoch'] + 2
        print('triples', k, 'cells', 2 + 3*k, 'from odd epoch', first, 'period in pairs', period,
              'unit debts', count, 'sharp discrepancy', spread)
        p *= 2


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('checkpoint', nargs='?', type=Path)
    args = parser.parse_args()
    if not __debug__:
        parser.error('run with assertions enabled')
    audit()
    if args.checkpoint:
        profile(args.checkpoint)
