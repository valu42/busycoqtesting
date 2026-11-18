#!/usr/bin/env python3
"""Replay the line 3 mixed-counter trajectory with an exact raw clock."""
import argparse
import json
import sys
from pathlib import Path

from checkpoints import ROOT, atomic_json, checksum, holdouts

sys.path.insert(0, str(ROOT))
from mixed_and_sweeps import MIX, TapeMachine, decode, next_zero

FORMAT = 'bb2x5-line3-timed-v1'


def snapshot(machine, checkpoints, status):
    left, right = min(machine.tape), max(machine.tape)
    word = ''.join(str(machine.tape.get(i, 0)) for i in range(left, right+1))
    return {'format': FORMAT, 'line': 3, 'machine': MIX, 'checkpoints': checkpoints,
            'steps_hex': hex(machine.steps), 'status': status, 'left': left,
            'word': word, 'head': machine.head, 'state': machine.state}


def blank():
    m = TapeMachine(MIX)
    for _ in range(5):
        if not m.step():
            raise ValueError('unexpected halt at initialization')
    if decode(m) != (1, 0, 0, 0):
        raise ValueError('line 3 blank initializer failed')
    return snapshot(m, 0, 'unknown')


def restore(p):
    word = p['word']
    raw = int(p['steps_hex'], 16)
    if (p['format'], p['line'], p['machine']) != (FORMAT, 3, holdouts()[2]) or p['machine'] != MIX:
        raise ValueError('wrong line 3 machine or format')
    if (not word or word.startswith('0') or word.endswith('0') or set(word) - set('01234')
            or p['state'] not in ('A', 'B') or type(p['head']) is not int
            or type(p['left']) is not int or type(p['checkpoints']) is not int
            or p['checkpoints'] < 0 or raw < 5 or abs(p['head']) > raw
            or (raw-p['head']) % 2 or p['left'] < -raw or p['left']+len(word)-1 > raw):
        raise ValueError('invalid line 3 saved configuration')
    m = TapeMachine(MIX, map(int, word), p['head'], p['left'])
    m.state, m.steps = p['state'], raw
    if p['status'] == 'unknown':
        normal = decode(m)
        if normal is None or normal[-1] != 0:
            raise ValueError('line 3 checkpoint is outside the zero-counter family')
    elif p['status'] != 'halt' or (m.state, m.tape.get(m.head, 0)) != ('A', 1):
        raise ValueError('invalid line 3 halt status')
    return m


def load(path):
    doc = json.loads(Path(path).read_text())
    if doc['sha256'] != checksum(doc['payload']):
        raise ValueError('line 3 checksum mismatch')
    restore(doc['payload'])
    return doc['payload']


def advance(p, target):
    m = restore(p)
    raw, completed, status = m.steps, p['checkpoints'], p['status']
    if target < completed:
        raise ValueError('target precedes checkpoint')
    while completed < target and status == 'unknown':
        normal, elapsed, _ = next_zero(m, exact=True)
        raw += elapsed
        if normal is None:
            status = 'halt'
        else:
            completed += 1
    m.steps = raw
    return snapshot(m, completed, status)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--checkpoints', type=int, required=True,
                        help='target number of zero-counter checkpoints after the five-step initializer')
    parser.add_argument('--resume', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    p = advance(load(args.resume) if args.resume else blank(), args.checkpoints)
    atomic_json(args.output, {'payload': p, 'sha256': checksum(p)})
    print(f"{p['checkpoints']} checkpoints, {p['steps_hex']} raw steps, {p['status']}.")


if __name__ == '__main__':
    main()
