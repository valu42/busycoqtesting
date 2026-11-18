#!/usr/bin/env python3
"""Measure first-edge events in substituted sources for line 17's final 21 pairs."""
import argparse
from collections import Counter
from functools import lru_cache
import json
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory

from line17_edge import ROOT_PERIOD, initial
from line17 import DATA, periodic_marks
from prior_frontier import pulse_on_tail, T17


@lru_cache(maxsize=None)
def edge_return(row, special):
    """Replay the triggering input literally and run until A3 or exit at cell -32."""
    hit, row = pulse_on_tail(row, special)
    if not hit:
        raise ValueError('selected rank did not reach +12')
    tape = list(map(int, row))
    x, state = len(tape), 1
    for step in range(20_001):
        if x < 0:
            return 'exit_' + ('B' if state else 'A'), step, row
        if x == len(tape):
            tape.append(0)
        op = T17[state][tape[x]]
        if op is None:
            return 'halt', step, row
        tape[x], delta, state = op
        x += delta
    return 'censored', step, row


def literal_rank_check(word, phase, expected_rank, expected_row):
    """Replay full raw suffix requests from input 1 to the first right extension."""
    row, pending = DATA[2*403:]+'2', False
    for n in range(expected_rank):
        marked = bool(word[(phase+n) % len(word)])
        if pending and marked:
            raise ValueError('overlapping mark in literal replay')
        special = marked or pending
        pending = special and row[0] != '1'
        hit, row = pulse_on_tail(row, special)
        if hit:
            if n+1 == expected_rank and row == expected_row:
                return
            break
    raise ValueError('raw requests disagree with the transducer rank or tape')


def summarize(cut, word, engine, source, mark_count):
    source.write_bytes(word)
    locked = bytes(int(j in range(5, 6*mark_count, 6)) for j in range(1, 6*mark_count+3))
    if mark_count == 5:
        marks = [j for j, bit in enumerate(word) if bit]
        if not marks or min(y-x for x, y in zip(marks, marks[1:]+[marks[0]+len(word)])) < 4:
            raise ValueError('replacement source lacks the required cyclic four-slot spacing')
    output = subprocess.check_output([engine, DATA[2*403:], source, str(mark_count)], text=True)
    times, symbols, outcomes, halt_steps = [], Counter(), Counter(), Counter()
    distinguished = None
    examples = {}
    cyclic = word + word[:len(locked)-1]
    next_phase = cyclic.find(locked)
    for line in output.splitlines():
        phase, rank, symbol, row, special = line.split()
        if next_phase != int(phase):
            raise ValueError('matching cyclic phase skipped or duplicated')
        next_phase = cyclic.find(locked, next_phase+1)
        outcome, steps, suspended = edge_return(row, bool(int(special)))
        example = int(rank), int(phase), suspended
        if 'min' not in examples or example[0] < examples['min'][0]:
            examples['min'] = example
        if 'max' not in examples or example[0] > examples['max'][0]:
            examples['max'] = example
        if int(suspended[-13]) != int(symbol):
            raise ValueError('the physical symbol disagrees with cut-418 decision')
        times.append(int(rank))
        symbols[symbol] += 1
        outcomes[outcome] += 1
        if outcome == 'halt':
            halt_steps[steps] += 1
        if int(phase) == 0:
            examples['first'] = example
            distinguished = dict(slot=int(rank), symbol=int(symbol), outcome=outcome,
                                 steps_after_visit=steps, suspended=suspended)
    if next_phase != -1:
        raise ValueError('unprocessed cyclic phase')
    for rank, phase, suspended in set(examples.values()):
        literal_rank_check(word, phase, rank, suspended)
    times.sort()
    quantiles = {str(p): times[(p*len(times)+99)//100-1] for p in (5, 25, 50, 75, 95)} if times else {}
    return dict(cut=cut, prefix_marks=mark_count, prefix_slots=len(locked), period=len(word), matching_rotations=len(times), ranks=quantiles,
                min_rank=min(times, default=None), max_rank=max(times, default=None),
                symbols=dict(symbols), local_outcomes=dict(outcomes),
                local_halting_delays=dict(halt_steps), distinguished_phase=distinguished)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--engine', type=Path, required=True)
    parser.add_argument('--cuts', type=int, nargs='+', default=[53, 56, 59])
    parser.add_argument('--marks', type=int, choices=(4,5), nargs='+', default=[4,5])
    args = parser.parse_args()
    if any(cut < 40 or cut > 59 for cut in args.cuts):
        parser.error('supported shallow source cuts are 40–59')
    head, word = b'', ROOT_PERIOD
    with TemporaryDirectory() as folder:
        for cut in range(max(args.cuts)+1):
            if cut in args.cuts:
                if head:
                    raise ValueError('expected a pure periodic source')
                for mark_count in args.marks:
                    row = summarize(cut, word, args.engine.resolve(), Path(folder)/'period',mark_count)
                    print(json.dumps(row, sort_keys=True), flush=True)
            if cut < max(args.cuts):
                head, word = periodic_marks(initial(cut), head, word)


if __name__ == '__main__':
    main()
