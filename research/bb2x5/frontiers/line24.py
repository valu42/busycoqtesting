#!/usr/bin/env python3
"""Run line 24 from its step-46 boundary, including physical B2 exceptions."""
import argparse
import json
from pathlib import Path

from checkpoints import checksum, holdouts
from longitudinal import CandidateUndefined, Driver, HALTED, resolve_candidate, save
from prior_sweeps import TapeMachine, parse

MACHINE = '1RB3LA1LA2RB2RA_2LA4RA3LB1RA---'
FORMAT = 'bb2x5-line24-sweeps-v1'


class Line24(Driver):
    line = 24
    machine = MACHINE
    # Trap B2 on the nonnegative half. Every remaining left move returns A.
    right_machine = '1RB3LA1LA2RB2RA_2LA4RA---1RA---'
    usual = 'A'
    first = 'AA'
    # Inputs at coordinate zero are AB, so the returns from the left are BA.
    prefix = ''
    period = 'BA'

    def __init__(self):
        actual = parse(self.machine)
        del actual['B', 2]
        if (holdouts()[23] != self.machine or parse(self.right_machine) != actual
                or any(q != 'A' for _, move, q in actual.values() if move == -1)):
            raise ValueError('line 24 guarded transition identity failed')

    def blank(self):
        """Replay the transient, including its early B return across coordinate zero."""
        tm = TapeMachine(self.machine)
        for _ in range(46):
            if not tm.step():
                raise ValueError('line 24 halted during setup')
        word = '1121331332'
        if ((tm.head, tm.state) != (0, 'A')
                or tm.tape != {i-4: int(c) for i, c in enumerate(word)}):
            raise ValueError('line 24 initial boundary mismatch')
        return {'format': FORMAT, 'machine': self.machine, 'line': 24,
                'groups': 0, 'steps': tm.steps, 'positive_tape': word[4:],
                'head': 0, 'state': 'A'}

    def left(self, excursions):
        """Time since the seed on the negative half; its tape in nearest-first blocks."""
        groups, half = divmod(excursions, 2)
        twos = 2 * groups + 1
        tail = (2, 4) if half else (1,)
        blocks = [(1, tuple((c,) for c in tail)), (twos, ((2,),)), (2, ((1,),))]
        return 6 * groups * (groups + 3) + half * (6 * groups + 9), blocks

    def load(self, path):
        doc = json.loads(Path(path).read_text())
        p = doc['payload']
        seed = self.blank()
        if (doc['sha256'] != checksum(p) or p.keys() != seed.keys()
                or any(p[k] != seed[k] for k in ('format', 'line', 'machine', 'head', 'state'))):
            raise ValueError('invalid line 24 checkpoint identity')
        groups, steps, tape = p['groups'], p['steps'], p['positive_tape']
        if (type(groups) is not int or groups < 0 or type(steps) is not int or steps % 2
                or steps < seed['steps'] + self.left(2 * groups)[0] + 2 * groups
                or not isinstance(tape, str) or len(tape) < len(seed['positive_tape'])
                or set(tape) - set('1234') or (groups == 0 and p != seed)):
            raise ValueError('invalid line 24 boundary')
        return p

    def run(self, state, target, engine, batch_size, word_bits, finite_slots, literal_work, progress):
        if target < state['groups'] or min(batch_size, literal_work) < 1 or word_bits < 16:
            raise ValueError('invalid sweep target or work budgets')
        while state['groups'] < target:
            groups = min(target - state['groups'], batch_size)
            try:
                state, _ = self.run_batch(engine, state, groups, word_bits, finite_slots=finite_slots)
            except CandidateUndefined:
                state = resolve_candidate(self, engine, state, groups, word_bits, literal_work,
                                          progress, finite_slots)
                if state['format'] == HALTED:
                    return state
            progress(state)
        return state


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--engine', type=Path, required=True, help='compiled longitudinal.cpp')
    parser.add_argument('--groups', type=int, required=True, help='absolute AB-pair target since the seed')
    parser.add_argument('--batch', type=int, default=2**26)
    parser.add_argument('--word-bits', type=int, default=2**20)
    parser.add_argument('--finite-slots', type=int, default=2**27)
    parser.add_argument('--literal-work', type=int, default=10**7)
    parser.add_argument('--resume', type=Path)
    parser.add_argument('--checkpoint', type=Path, required=True)
    args = parser.parse_args()
    try:
        driver = Line24()
        start = driver.load(args.resume) if args.resume else driver.blank()

        def output(payload):
            save(args.checkpoint, payload)

        state = driver.run(start, args.groups, args.engine, args.batch, args.word_bits,
                           args.finite_slots, args.literal_work, output)
        output(state)
        print(f"{state['format']}, step {state['steps']}, {state['state']} at {state['head']}")
    except (ValueError, KeyError, TypeError, RuntimeError, OSError) as error:
        parser.exit(2, f'Line 24 stopped: {error}\n')


if __name__ == '__main__':
    main()
