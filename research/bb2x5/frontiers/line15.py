#!/usr/bin/env python3
"""Time line 15 by exact first returns of seven-cell strips on the positive half."""
import argparse
import base64
import json
from pathlib import Path
import subprocess
import sys
import zlib

from checkpoints import atomic_json, checksum, holdouts
from longitudinal import Driver, parse

MACHINE = '1RB3RB1LA2LA3RA_1LB2RA4RB0LA---'
RULES = parse(MACHINE)
WIDTH = 7
FORMAT = 'bb2x5-line15-strips-v1'


class Guard(Exception):
    """A speculative strip failed; its predicted return cannot be committed."""


class PhysicalEvent(Exception):
    def __init__(self, state):
        self.state = state


class Left(Driver):
    line = 15
    machine = MACHINE
    prefix = 'BBBA'
    period = 'BABAABBABBABAAAB'
    transient = 9
    usual = 'A'

    def __init__(self):
        if holdouts()[14] != MACHINE:
            raise ValueError('line 15 machine identity mismatch')
        self.check_left(RULES, 1)

    def source(self, old, target):
        """Actual root entries, including the initial A and excluding the final reentry."""
        for n in range(self.excursions(old), self.excursions(target)):
            yield self.letter(n-1) if n else 'A'


def transfer(word, entries):
    """Interpret each seven-cell call, suspending at its right edge for an A reply."""
    cells = bytearray(word)
    outgoing = []
    steps = 0
    width = len(cells)
    if not width:
        raise ValueError('strip must contain at least one cell')
    for q in entries:
        x = 0
        start = steps
        while x >= 0:
            rule = RULES.get((q, cells[x]))
            if rule is None:
                raise Guard('candidate B4')
            cells[x], move, q = rule
            x += move
            steps += 1
            if x == width:
                outgoing.append(q)
                x, q = width-1, 'A'
            if steps-start >= 10000:
                raise Guard('strip first-exit work limit')
        if q != 'A':
            raise Guard('candidate strip returned B')
    return bytes(cells), ''.join(outgoing), steps


def reference(seed, entries):
    tape = bytearray(seed)
    cost = 0
    for index in range(0, 7 * (len(entries) + 1) + len(seed), WIDTH):
        if not entries:
            return bytes(tape), cost
        word = tape[index:index+WIDTH] or bytes(WIDTH)
        word, entries, raw = transfer(word, entries)
        tape[index:index+WIDTH] = word
        cost += raw
    raise Guard('reference strip depth budget')


def native(engine, seed, groups, entries, resume, audit=False):
    cmd = [str(Path(engine).resolve()), str(groups)]
    data = ''
    if resume:
        cmd.append('--resume-check-prefix' if audit else '--resume')
        data = '\n'.join(''.join(str(c) for c in seed[i:i+WIDTH])
                         for i in range(0, len(seed), WIDTH))
    elif audit:
        cmd.append('--check-prefix')
    run = subprocess.run(cmd, input=data, text=True, capture_output=True)
    if run.returncode:
        detail = run.stderr.strip()
        if detail.startswith(('candidate strip', 'undefined instruction inside', 'strip first-exit work limit')):
            raise Guard(detail)
        raise RuntimeError(detail or 'native strip worker failed')
    if audit and run.stderr:
        print(run.stderr.strip(), file=sys.stderr)
    tape = bytearray(seed)
    total = 0
    expected = entries
    for index, row in enumerate(run.stdout.splitlines()):
        word, num, elapsed, child = row.split()
        n, raw, emitted = int(num), int(elapsed), int(child)
        if (len(word) != WIDTH or set(word) - set('01234') or n < 1 or n != expected
                or emitted < 0 or raw < n + emitted or (raw - n - emitted) % 2):
            raise ValueError('invalid strip result')
        expected = emitted
        tape[WIDTH*index:WIDTH*(index+1)] = bytes(map(int, word))
        total += raw
    if expected:
        raise ValueError('incomplete strip result')
    return bytes(tape), total


def physical(left, old, target, seed, work, right_before):
    """Resolve a failed one-period guard in physical order on the original tape."""
    tape = bytearray(seed)
    steps = 0
    for n, q in enumerate(left.source(old, target), left.excursions(old)):
        x = 0
        while x >= 0:
            if x == len(tape):
                tape.extend(bytes(WIDTH))
            rule = RULES.get((q, tape[x]))
            if rule is None:
                break
            if steps >= work:
                raise RuntimeError('physical positive-side work budget')
            tape[x], move, q = rule
            x += move
            steps += 1
        if x >= 0 or q != 'A':
            negative = left.left(n)[0]
            positive = right_before + steps
            raise PhysicalEvent({'format': 'bb2x5-line15-event-v1', 'machine': MACHINE, 'line': 15,
                                 'event': 'halt' if x >= 0 else 'B return to negative half',
                                 'completed_negative_returns': n, 'head': x, 'state': q,
                                 'steps': negative+positive, 'negative_steps': negative,
                                 'positive_steps': positive, 'positive_cells': len(tape),
                                 'positive_zlib_base64': base64.b64encode(zlib.compress(tape, 9)).decode()})
    return bytes(tape), steps


def boundary(driver, groups, cells, right):
    left = driver.left(driver.excursions(groups))[0]
    return {'format': FORMAT, 'machine': MACHINE, 'line': 15, 'groups': groups,
            'head': 0, 'state': driver.period[-1] if groups else 'A',
            'steps': left + right, 'negative_steps': left, 'positive_steps': right,
            'positive_cells': cells}


def payload(driver, groups, tape, right):
    return {**boundary(driver, groups, len(tape), right),
            'positive_zlib_base64': base64.b64encode(zlib.compress(tape, 9)).decode()}


def load(path):
    doc = json.loads(Path(path).read_text())
    p = doc['payload']
    if doc['sha256'] != checksum(p):
        raise ValueError('checksum mismatch')
    g, right = p['groups'], p['positive_steps']
    tape = zlib.decompress(base64.b64decode(p['positive_zlib_base64'], validate=True))
    left = Left()
    if (type(g) != int or g < 0 or type(right) != int or right < left.excursions(g)
            or (max(tape, default=0) > 4) or len(tape) % WIDTH or bool(tape) != bool(g)
            or p['steps'] % 2 or (g == 0 and right != 0)
            or p != {**boundary(left, g, len(tape), right), 'positive_zlib_base64': p['positive_zlib_base64']}):
        raise ValueError('invalid line 15 boundary')
    return p


def advance(driver, engine, old, target, seed, work, right_before, audit=False):
    delta = target - old
    if delta < 1:
        raise ValueError('target must follow the starting group')
    try:
        if engine:
            n = driver.excursions(target) - driver.excursions(old)
            return native(engine, seed, delta, n, bool(old), audit)
        return reference(seed, ''.join(driver.source(old, target)))
    except Guard as candidate:
        if audit:
            raise RuntimeError(f'prefix audit stopped at {candidate}') from candidate
        if delta == 1:
            return physical(driver, old, target, seed, work, right_before)
    mid = old + delta // 2
    tape, cost = advance(driver, engine, old, mid, seed, work, right_before)
    tape, more = advance(driver, engine, mid, target, tape, work, right_before+cost)
    return tape, cost + more


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--engine', type=Path, help='compiled line15_stream.cpp; otherwise interpret strips in Python')
    parser.add_argument('--groups', type=int, required=True, help='absolute number of complete negative-driver periods')
    parser.add_argument('--resume', type=Path)
    parser.add_argument('--check-prefix', action='store_true',
                        help='audit incoming startup letters; a resumed seed must have already passed this check')
    parser.add_argument('--checkpoint', type=Path, required=True)
    parser.add_argument('--literal-work', type=int, default=10**7)
    args = parser.parse_args()
    try:
        driver = Left()
        if args.check_prefix and not args.engine:
            raise ValueError('prefix audit requires the native strip worker')
        state = load(args.resume) if args.resume else payload(driver, 0, b'', 0)
        if args.groups < state['groups'] or args.literal_work < 1:
            raise ValueError('invalid target or work budget')
        if args.groups > state['groups']:
            tape = zlib.decompress(base64.b64decode(state['positive_zlib_base64']))
            tape, cost = advance(driver, args.engine, state['groups'], args.groups, tape,
                                 args.literal_work, state['positive_steps'], args.check_prefix)
            state = payload(driver, args.groups, tape, state['positive_steps'] + cost)
        atomic_json(args.checkpoint, {'payload': state, 'sha256': checksum(state)})
        print(f"{state['groups']} groups, {state['steps']} steps, {state['positive_cells']} stored nonnegative cells")
    except PhysicalEvent as event:
        state = event.state
        atomic_json(args.checkpoint, {'payload': state, 'sha256': checksum(state)})
        print(f"{state['event']} at step {state['steps']}, {state['state']} at {state['head']}")
    except (OSError, ValueError, RuntimeError, KeyError, TypeError, zlib.error) as error:
        parser.exit(2, f'Line 15 stopped: {error}\n')


if __name__ == '__main__':
    main()
