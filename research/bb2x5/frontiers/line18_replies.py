#!/usr/bin/env python3
"""Audit A replies at the batch boundaries used by line 18's suffix simulator."""
import argparse
import json
from pathlib import Path

from checkpoints import atomic_json
from line18 import MACHINE, Suffix, advance, blank_entry, load
from prior_sweeps import TapeMachine


def witness(before, after, entry, state, elapsed):
    """Replay the literal excursion and keep precisely the cells it touched."""
    tm = TapeMachine(MACHINE, before[:entry + elapsed], head=entry)
    tm.state = state
    right = entry
    while tm.head >= 0:
        right = max(right, tm.head)
        if tm.steps >= elapsed or not tm.step():
            raise ValueError('literal A witness failed to replay')
    span = right + 1
    initial = bytes(before[:span]).ljust(span, b'\x00')
    final = bytes(tm.tape.get(i, 0) for i in range(span))
    if tm.steps != elapsed or tm.state != 'A' or final != after[:span]:
        raise ValueError('literal A witness has inconsistent tape, control or clock')
    return {'entry_offset': entry, 'entry_state': state, 'steps': elapsed,
            'before': ''.join(map(str, initial)), 'after': ''.join(map(str, final))}


class ObservedSuffix(Suffix):
    def literal(self, pos, state, left):
        before, raw = self.cells[left:], self.steps
        reply = super().literal(pos, state, left)
        if reply == 'A':
            self.last_a = witness(before, self.cells[left:], pos-left, state, self.steps-raw)
        return reply

    def batch(self, pos, count):
        done, reply = yield from super().batch(pos, count)
        if reply == 'A':
            self.events.append({'offset': pos, 'completed_before_A_hex': hex(done), **self.last_a})
        return done, reply


def audit(start, epochs, limit=10**7):
    """Count batch exceptions on a contiguous interval of completed records."""
    if epochs < 1 or limit < 1:
        raise ValueError('positive epoch and work budgets required')
    suffix = ObservedSuffix(start['suffix'], limit)
    first = start['record']
    samples = {}
    number = records_with_a = 0
    for k in range(first, first + epochs):
        suffix.events = []
        suffix.epoch(k)
        number += len(suffix.events)
        records_with_a += bool(suffix.events)
        for event in suffix.events:
            at = {'record': k, 'coordinate': k+3+event['offset'], **event}
            kind = 'first_zero_cell' if event['before'] == '0' else 'first_occupied_strip'
            samples.setdefault(kind, at)
            if 'nearest_cut' not in samples or event['offset'] < samples['nearest_cut']['offset']:
                samples['nearest_cut'] = at
    return {'machine': MACHINE, 'first_record': first, 'epochs': epochs,
            'outer_A_requests_returning_B': epochs,
            'outer_B_requests_returning_B_hex': hex(((1 << epochs)-1) << (first-1)),
            'internal_A_replies_at_batch_boundaries': number, 'epochs_with_internal_A': records_with_a,
            'witnesses': samples}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--from-record', type=int, required=True)
    p.add_argument('--epochs', type=int, required=True)
    p.add_argument('--resume', type=Path, help='optional checkpoint at or before --from-record')
    p.add_argument('--output', type=Path)
    args = p.parse_args()
    start = advance(load(args.resume) if args.resume else blank_entry(), args.from_record)
    doc = audit(start, args.epochs)
    if args.output:
        atomic_json(args.output, doc)
    else:
        print(json.dumps(doc, indent=2))


if __name__ == '__main__':
    main()
