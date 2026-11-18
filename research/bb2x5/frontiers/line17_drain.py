#!/usr/bin/env python3
"""Certify future cut marks by completing only bursts already pending at a checkpoint."""
import argparse
import json
from pathlib import Path

from line17 import DATA, deepest_probe, digits, load, mark_image, mark_step
from line17_edge import cut53_period
from prior_frontier import marks_on_word


def drain_digit(state, incoming, next_input):
    """Finite known marks followed by zeros. Return future child marks and a lower bound."""
    # After these extra zeros, all bursts started in this prefix have finished.
    limit = (incoming[-1] if incoming else 0) + 3
    children = list(mark_image(incoming, limit, state))
    positions = set(incoming)
    v, pending = state
    count = 0
    literal = []
    for slot in range(1, limit + 1):
        v, pending, word = mark_step(v, pending, slot in positions)
        for bit in word:
            count += 1
            if bit:
                literal.append(count)
    if pending or literal != children:
        raise ValueError('burst timestamps disagree with the literal pulse table')

    # The first additional surviving mark has r>=1 and parent t>=next_input.
    # Every intervening extinguished mark can only increase the coefficient.
    v, pending = state
    coefficient = v - 1
    for t in ([1] if pending else []) + incoming:
        residue = (t + coefficient) % 3
        coefficient += 4 * (1 + residue)
    earliest = (next_input + coefficient + 5 + 2) // 3
    return children, earliest


def drain(checkpoint, cut=403):
    data = digits(checkpoint['register'])
    if not 0 <= cut <= len(data):
        raise ValueError('target cut outside the data register')
    # In the normalized source at root, the next sweep has its mark on slot 2.
    known, earliest = [], 2
    for i, (v, _) in enumerate(data[:cut]):
        state = v, data[i - 1][1] if i else 0
        known, earliest = drain_digit(state, known, earliest)
        if known:
            gap = 4 if 53 <= i + 1 <= 403 else 3
            earliest = max(earliest, known[-1] + gap)
    depth = deepest_probe(checkpoint['register'])
    untouched = depth is None or depth[0] < cut
    return dict(epochs=checkpoint['epochs'], cut=cut, cut_previously_untouched=untouched,
                future_mark_slots=known, next_additional_mark_at_or_after=earliest)


def check_short_prefixes():
    # Run seven real starting pairs slot by slot. From each of forty sweep
    # boundaries, compare the predicted prefix against another 800 real sweeps.
    data = digits(DATA)[:7]
    root_period = bytes((0, 1, 0, 0))
    for epochs in range(1, 41):
        before = root_period * epochs
        later = root_period * 800
        known, earliest = [], 2
        for i, (v, _) in enumerate(data):
            initial = (v, data[i - 1][1] if i else 0)
            boundary, before = marks_on_word(initial, before)
            _, later = marks_on_word(boundary, later)
            known, earliest = drain_digit(boundary, known, earliest)
            observed = [j for j, bit in enumerate(later, 1) if bit]
            assert observed[:len(known)] == known
            assert len(observed) > len(known) and observed[len(known)] >= earliest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('checkpoint', type=Path)
    parser.add_argument('--cut', type=int, default=403)
    args = parser.parse_args()
    if not __debug__:
        parser.error('the pulse verifier requires assertions')
    check_short_prefixes()
    # Four-slot separation is preserved by the homogeneous band. Check its base.
    period = cut53_period()
    marks = [j for j, bit in enumerate(period) if bit]
    assert min(b - a for a, b in zip(marks, marks[1:] + [marks[0] + len(period)])) == 4
    print(json.dumps(drain(load(args.checkpoint), args.cut), indent=2))


if __name__ == '__main__':
    main()
