#!/usr/bin/env python3
"""Replay an alternative right input from the saved line-15 blank configuration."""
import argparse
import base64
import json
from pathlib import Path
import zlib

from line15 import Left, MACHINE, load, transfer
from prior_sweeps import TapeMachine

FRINGE_INPUT = 'AAABABAABBBAB'


def mature_controls():
    """Verify each one-cell prescription, including intermediate silent calls."""
    for digit in (1, 2):
        for desired in 'AB':
            calls = ('A' if digit == 2 else '') + ('B' if desired == 'A' else 'A')
            cell, emitted, _ = transfer([digit], calls)
            if (cell, emitted) != (bytes([1 if desired == 'A' else 2]), desired):
                raise ValueError('mature control failed')


def forced_counts(mature, letters):
    """Count the constructed input exactly using two successive inverse images.

    One lift maps (a,b) to (2b + [digit=2] - [last=B], a) and flips
    the last letter. Two lifts double both counts and restore that letter.
    The additions from the inner and outer cells form binary integers.
    """
    a, b = letters.count('A'), letters.count('B')
    last = letters[-1]
    digits = mature[::-1]
    pairs = len(digits)//2
    if pairs:
        bits = bytes(ord('1') if digit == 2 else ord('0') for digit in digits[:2*pairs])
        power = 1 << pairs
        a = power*a + int(bits[1::2], 2) - (last == 'A')*(power-1)
        b = power*b + int(bits[::2], 2) - (last == 'B')*(power-1)
    if len(digits) % 2:
        a, b = 2*b + (digits[-1] == 2) - (last == 'B'), a
    return a, b


def verify(path):
    p = load(path)
    raw = zlib.decompress(base64.b64decode(p['positive_zlib_base64']))
    start = next((i for i, d in enumerate(raw) if d not in (1, 2)), len(raw))
    if raw[start:].rstrip(bytes([0])) != bytes([0, 1, 1, 1]):
        raise ValueError('checkpoint does not have the 0111 fringe')
    mature_controls()
    tm = TapeMachine(MACHINE, raw[start:])
    returned = []
    for i, q in enumerate(FRINGE_INPUT):
        tm.head, tm.state = 0, q
        while tm.head >= 0 and tm.step():
            if tm.steps > 121:
                raise ValueError('unexpected fringe timing')
        if tm.head < 0:
            returned.append(tm.state)
        elif i+1 != len(FRINGE_INPUT):
            raise ValueError('unexpected early fringe halt')
    if (returned, tm.steps, tm.head, tm.state, tm.tape.get(tm.head)) != (['A']*12, 121, 5, 'B', 4):
        raise ValueError('fringe did not reach its physical B4')
    a, b = forced_counts(raw[:start], FRINGE_INPUT)
    # The first input letter follows from the first demanded letter and the
    # initial symbol. This remains valid while the controlled child is active.
    first = FRINGE_INPUT[0]
    for digit in reversed(raw[:start]):
        first = 'A' if digit == 2 or first == 'B' else 'B'
    actual = next(Left().source(p['groups'], p['groups']+1))
    return {'groups': p['groups'], 'blank_steps': p['steps'], 'fringe_at': start,
            'controlled_fringe_calls': FRINGE_INPUT, 'fringe_steps': tm.steps,
            'controlled_halt_at': start+tm.head, 'constructed_root_calls_bits': (a+b).bit_length(),
            'constructed_first_entry': first, 'actual_next_entry': actual}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('checkpoint', type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(args.checkpoint), indent=2))
