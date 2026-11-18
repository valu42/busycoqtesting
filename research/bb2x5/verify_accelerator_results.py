#!/usr/bin/env python3
"""Recheck saved accelerator states, including literal continuation replay.

python3 verify_accelerator_results.py
python3 verify_accelerator_results.py --replay-line5

The optional full line-5 replay uses the pre-existing A-phase formula and scalar
B rules, with no new B batching. Checksums are not reachability certificates.
"""
import argparse
import json
from pathlib import Path

import arithmetic5
from exact_blocks import Engine, Run
from prior_sweeps import TapeMachine, largest_repeat, published_return

RESULTS = Path(__file__).with_name('accelerator-results')


def check_blocks():
    report = json.loads((RESULTS / 'deep.json').read_text())
    for record in report['records']:
        document = json.loads((RESULTS / record['checkpoint']).read_text())
        engine = Engine(record['machine'])
        run = Run.restore(engine, document)
        if run.checkpoint(engine) != document:
            raise AssertionError('checkpoint roundtrip mismatch')
        if document['sha256'] != record['checkpoint_sha256']:
            raise AssertionError('report/checkpoint checksum mismatch')
        if run.steps != int(record['steps'], 0) or run.status != 'running':
            raise AssertionError('report/checkpoint state mismatch')
        literal = TapeMachine(run.encoding)
        literal.head, literal.state = run.head, chr(65 + run.state)
        literal.tape = run.sparse_tape(engine)
        previous_steps = run.steps
        for _ in range(100):
            run.advance(engine)
        for _ in range(run.steps - previous_steps):
            if not literal.step():
                raise AssertionError('literal continuation halted early')
        if (literal.state, literal.head, literal.tape) != (
                chr(65 + run.state), run.head, run.sparse_tape(engine)):
            raise AssertionError('literal continuation differs')
        print(f"Line {record['line']}: checkpoint reload and 100 further block "
              f"exits match {run.steps - previous_steps} literal defined steps.")


def check_arithmetic(replay):
    report = json.loads((RESULTS / 'arithmetic5-results.json').read_text())
    saved = arithmetic5.load(RESULTS / report['checkpoint'])
    expected = report['checkpoint_result']
    if (saved.rounds, saved.macro_events, saved.accelerated_operations,
            saved.state.tag, saved.state.a, saved.state.b.bit_length(), saved.halted) != (
            expected['rounds'], expected['macro_events'], expected['accelerated_operations'],
            'A', expected['a'], expected['b_bits'], False):
        raise AssertionError('arithmetic report/checkpoint mismatch')
    print(f'Line 5: exact {saved.rounds}-round checkpoint loaded.')
    if not replay:
        return
    # Independent older implementation: A doubling, then one B rule at a time.
    b, events = 4, 0
    for _ in range(saved.rounds):
        k = largest_repeat(b)
        state = published_return('A', 8 * (1 << k) - 4,
                                 b - 8 * ((1 << k) - 1) + k)
        events += k + 1
        if state is None:
            raise AssertionError('older recurrence reached a halt')
        b_events = 0
        while state[0] == 'B':
            state = published_return(*state)
            events += 1
            b_events += 1
            if b_events > 1_000_000:
                raise RuntimeError('independent B-phase work budget exhausted')
        tag, a, b = state
        if (tag, a) != ('A', 4):
            raise AssertionError('unexpected old recurrence normal form')
    if (b, events) != (saved.state.b, saved.macro_events):
        raise AssertionError('older recurrence differs from saved result')
    print(f'Line 5: all {saved.rounds} rounds and {events} macro events match '
          'the older A formula plus scalar B recurrence; complete integer equal.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--replay-line5', action='store_true')
    args = parser.parse_args()
    check_blocks()
    check_arithmetic(args.replay_line5)


if __name__ == '__main__':
    main()
