#!/usr/bin/env python3
"""Recover the suspended data word and run the first excursion on width analogues."""
import argparse
import json
from pathlib import Path
import subprocess

from line17 import DATA
from line17_edge import ROOT_PERIOD
from prior_frontier import pulse_on_tail, T17
from line17_pile import exceptional_sweep


def run_variant(record, engine, word_bits, finite_slots):
    cut = record['prefix_pairs']
    if type(cut) is not int or not 6 <= cut <= 403 or DATA[2*cut-1] != '2':
        raise ValueError('expected a splice with a clear incoming flag')
    root = record['first_root_slot']
    if type(root) is not int or root < 1:
        raise ValueError('expected a positive root slot')
    register = DATA[:2*cut] + DATA[2*403:]
    completed_sweeps, offset = divmod(root-1, 4)
    rows = subprocess.check_output(
        [engine, str(completed_sweeps), str(word_bits), str(finite_slots)], input=register,
        text=True).splitlines()
    rows = [tuple(map(int, line.split())) for line in rows]
    if len(rows)*2 != len(register) or rows[-1][2] or rows[0][1]:
        raise ValueError('invalid pre-overflow sweep')
    flags = [row[1] for row in rows[1:]] + [int(register[-1]) - 2]
    tape = ''.join('102'[row[0]]+str(2+flag) for row, flag in zip(rows, flags))+'2'
    pre_sweep = tape[:-1]
    pending = False
    for slot, bit in enumerate(ROOT_PERIOD[:offset+1]):
        if bit and pending:
            raise ValueError('overlapping root mark')
        special = bool(bit or pending)
        pending = special and tape[0] != '1'
        hit, tape = pulse_on_tail(tape, special)
        if hit != (slot == offset):
            raise ValueError('literal timing does not match selected root slot')
    x = len(tape)
    state = 1
    cells = list(map(int, tape))
    for delay in range(100_001):
        if x < 0:
            status = 'exit_' + ('B' if state else 'A')
            break
        if x == len(cells):
            cells.append(0)
        op = T17[state][cells[x]]
        if op is None:
            status = 'halt'
            break
        if delay == 100_000:
            status = 'censored'
            break
        cells[x], direction, state = op
        x += direction
    embedded = {}
    full_status, elapsed, first_edge, head, width = exceptional_sweep(
        completed_sweeps, pre_sweep, tape, engine=engine,
        word_bits=word_bits, finite_slots=finite_slots, embedded_log=embedded)
    if (first_edge is None or elapsed-first_edge < delay or
            (status=='halt' and (full_status!='halt' or elapsed-first_edge!=delay))):
        raise ValueError('full trace and local edge return disagree')
    return dict(embedded_jump=embedded or None, full_outcome=full_status, full_delay_after_edge=elapsed-first_edge,
                edge_time_in_sweep=first_edge, new_register_width=width, terminal_head=head,
                prefix_pairs=cut, register_pairs=len(rows), first_root_slot=record['first_root_slot'],
                outcome=status, steps_after_visit=delay, exit_or_halt_relative_to_edge=x-len(tape))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('variants', type=Path)
    p.add_argument('--engine', required=True, type=Path)
    p.add_argument('--word-bits', type=int, default=2**28)
    p.add_argument('--finite-slots', type=int, default=100_000_000_000)
    args = p.parse_args()
    for line in args.variants.read_text().splitlines():
        print(json.dumps(run_variant(json.loads(line), args.engine.resolve(), args.word_bits,
                                     args.finite_slots)), flush=True)


if __name__=='__main__':
    main()
