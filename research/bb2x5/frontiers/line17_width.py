#!/usr/bin/env python3
"""Time the first terminal input on shortened versions of line 17's 424-pair register."""
import argparse
import json
import math
from pathlib import Path
import subprocess
from statistics import linear_regression, median

from line17 import DATA, digits
from prior_frontier import marks_on_word

ROOT_WORD = bytes((0, 1, 0, 0))
SUFFIX_START = 403


def first_sweep(engine, cut, bits, slots):
    # Retain the physical prefix and the original last 21 pairs.
    register = DATA[:2 * cut] + DATA[2 * SUFFIX_START:]
    width = len(register) // 2

    def run(epochs, *mode):
        args = [str(engine), str(epochs), str(bits), str(slots), *mode]
        result = subprocess.run(args, input=register, text=True, capture_output=True)
        if result.returncode:
            raise ValueError(result.stderr.strip() or f'worker exited {result.returncode}')
        return result.stdout.strip()

    horizon = 10 ** math.ceil(width * math.log10(1.5))
    while True:
        found = run(horizon, 'first')
        if found != 'none':
            break
        horizon *= 10
    root = int(found)
    before, offset = divmod(root - 1, 4)
    rows = [tuple(map(int, row.split())) for row in run(before).splitlines()]
    if len(rows) != width or rows[-1][2] != 0:
        raise ValueError('first-hit search and previous sweep disagree')

    def prefix_output(length):
        word = ROOT_WORD[:length]
        for v, pending, *_ in rows[:cut]:
            _, word = marks_on_word((v, pending), word)
        return word

    preceding = len(prefix_output(offset))
    suffix_states = [(row[0], row[1]) for row in rows[cut:]]
    for j, bit in enumerate(prefix_output(offset + 1), 1):
        word = bytes((bit,))
        for index, state in enumerate(suffix_states):
            suffix_states[index], word = marks_on_word(state, word)
        if word:
            if j <= preceding:
                raise ValueError('first-hit root slot disagrees with forward replay')
            return dict(prefix_pairs=cut, register_pairs=width, first_root_slot=root,
                        first_sweep=before + 1, first_suffix_slot=rows[cut - 1][2] + j)
    raise ValueError('selected root slot never reached the terminal')


def summarize(path, validation=None):
    records = [json.loads(line) for line in path.read_text().splitlines()]
    widths = [r['register_pairs'] for r in records]
    clocks = [math.log10(r['first_sweep']) for r in records]
    geometric = math.log10(1.5)
    intercepts = [y - geometric * w for w, y in zip(widths, clocks)]
    fitted = median(intercepts)
    prediction = fitted + 424 * geometric
    print(f'Fixed transmission rate: log10 sweeps {prediction:.3f}, '
          f'log10 raw {math.log10(14) + 2 * prediction:.3f}')
    slope, intercept = linear_regression(widths, clocks)
    print(f'Fitted slope {slope:.6f}, '
          f'log10 raw {math.log10(14) + 2 * (intercept + 424 * slope):.3f}')
    early = [b for w, b in zip(widths, intercepts) if w <= 91]
    later = [b for w, b in zip(widths, intercepts) if w > 91]
    if early and later:
        ratios = [10**(b - median(early)) for b in later]
        print(f'Sweeps observed/predicted on {len(later)} larger registers: '
              f'{min(ratios):.2f} to {max(ratios):.2f}')
    if validation is not None:
        checks = [json.loads(line) for line in validation.read_text().splitlines()]
        for name, growth, center in [('fixed', geometric, fitted), ('fitted', slope, intercept)]:
            errors = [math.log10(r['first_sweep']) - center - growth * r['register_pairs']
                      for r in checks]
            print(f'{name}: median held-out multiplicative error '
                  f'{10**median(abs(e) for e in errors):.2f}x')
    ranks = sorted(r['first_suffix_slot'] for r in records)
    print(f'Suffix slots: min {ranks[0]}, median {median(ranks):g}, max {ranks[-1]}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--engine', type=Path)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--cuts', nargs='+', type=int)
    mode.add_argument('--summarize', type=Path, metavar='JSONL')
    parser.add_argument('--validation', type=Path, help='held-out width records for --summarize')
    parser.add_argument('--word-bits', type=int, default=2**28)
    parser.add_argument('--finite-slots', type=int, default=20_000_000_000)
    args = parser.parse_args()
    if args.summarize:
        summarize(args.summarize, args.validation)
        return
    if args.validation:
        parser.error('--validation requires --summarize')
    if not args.engine:
        parser.error('--cuts requires --engine')
    for c in args.cuts:
        if not 6 <= c <= SUFFIX_START or digits(DATA)[c-1][1]:
            parser.error('splice must begin with a clear incoming flag')
        print(json.dumps(first_sweep(args.engine.resolve(), c, args.word_bits, args.finite_slots)), flush=True)

if __name__ == '__main__':
    main()
