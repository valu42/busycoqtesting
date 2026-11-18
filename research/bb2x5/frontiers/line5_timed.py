#!/usr/bin/env python3
"""Exact raw clock for the A/B normal forms of BB(2,5) formal line 5."""
import argparse
import json
from pathlib import Path
import sys
import subprocess

from checkpoints import ROOT, atomic_json, checksum, holdouts
sys.path.insert(0, str(ROOT))
from arithmetic5 import MACHINE, State, a_repeat_count, scalar
from line4_cert import Lin, ZERO, verify_rule

FORMAT = 'bb2x5-line5-timed-v1'


def verify_local_rules():
    """Symbolically replay every timed rule at all natural parameter values."""
    if not __debug__:
        raise ValueError('symbolic rule verification requires Python assertions')
    if holdouts()[4] != MACHINE:
        raise ValueError('line 5 dataset identity mismatch')
    rules = {(q, s): row[3*s:3*s+3] for q, row in zip('AB', MACHINE.split('_')) for s in range(5)}
    for n in [Lin(0,i) for i in range(16)] + [Lin(1,16)]:
        k = n+4
        rows = [
            (([9,4,(1,k)], [1,9]), ([9,(1,k+2)], [9]), 2*k+3),
            (([1,(1,k)], [1,1,1,9]), ([1,(4,k),1,1,1,1], [9]), 2*k+15),
            (([1,(1,k)], [1,1,2]), ([1,(4,k-2),(1,ZERO+6)], [1,1]), 2*k+39),
            (([1,(1,k)], [1,2]), None, 2*k+5),
            (([9,(1,k)], [2]), ([9,(1,k-1)], [1,1]), ZERO+1),
            (([9,4,4,4,(1,n+3)], [1,1]), ([9,(1,n+8)], [1,1]), 6*n+42),
            (([1,(1,n+3)], [1,1]), ([1,(4,n+3),1,1,1], [1,1]), 2*n+24),
            (([1,4,(1,n+3)], [1,1]), ([1,(4,ZERO+4),1,1,1,1], [(1,n+2),2]), 5*n+72),
            (([1,4,4,(1,n+3)], [1,1]), ([1,(4,n+5),(1,ZERO+5)], [1,1]), 6*n+68),
        ]
        for start, end, time in rows:
            verify_rule(start, end, time, rules)
    verify_rule(([], []), ([1,(4,ZERO+4),1,1,1,1], [(1,ZERO+4),2]), ZERO+136, rules)


def step(state):
    """Return successor, raw cost and number of published events. None is a physical halt."""
    a, b = state.a, state.b
    if state.tag == 'A':
        k = a_repeat_count(a, b)
        if k:
            x = a+4
            y = x << k
            # One complete doubling costs 2x²−3x+3. Sum at x,2x,…,2^(k−1)x.
            cost = 2*((y-x)*(y+x)//3) - 3*(y-x) + 3*k
            return State('A', y-4, b-(y-x)+k), cost, k
        j = min(a, b)
        consumed = j*(2*j+9)
        if b == a+2:
            terminal = 4*a+47
        elif b == a+1:
            terminal = 4*a+13
        else:
            terminal = 1
        return scalar(state), consumed+terminal, 1
    q, residue = divmod(a, 3)
    k = b+5*q
    consumed = q*(15*q+6*b+27)
    terminal = (2*k+24, 5*k+72, 6*k+68)[residue]
    return scalar(state), consumed+terminal, 1


def blank():
    return {'format': FORMAT, 'line': 5, 'machine': MACHINE, 'family': 'A', 'a_hex': '0x4',
            'b_hex': '0x4', 'steps_hex': '0x88', 'rounds':0, 'events_hex':'0x0', 'status':'unknown'}


def load(path):
    doc = json.loads(Path(path).read_text())
    p = doc['payload']
    if doc['sha256'] != checksum(p) or set(p) != set(blank()):
        raise ValueError('invalid line 5 checkpoint')
    if (p['format'], p['machine'], p['line']) != (FORMAT, MACHINE, 5) or p['status'] not in ('halt','unknown'):
        raise ValueError('wrong line 5 checkpoint identity or status')
    state = State(p['family'], int(p['a_hex'],16), int(p['b_hex'],16))
    if type(p['rounds']) is not int or p['rounds'] < 0 or int(p['steps_hex'],16) < 136 or int(p['events_hex'],16) < p['rounds']:
        raise ValueError('invalid counters')
    if p['status'] == 'halt' and (state.tag != 'A' or state.b != state.a+1):
        raise ValueError('wrong halting predecessor')
    return p


def advance(p, rounds):
    state = State(p['family'], int(p['a_hex'],16), int(p['b_hex'],16))
    raw, events = int(p['steps_hex'],16), int(p['events_hex'],16)
    completed, status = p['rounds'], p['status']
    while completed < rounds and status == 'unknown':
        successor, elapsed, count = step(state)
        raw += elapsed
        events += count
        if successor is None:
            status = 'halt'
        else:
            completed += state.tag == 'B' and successor.tag == 'A'
            state = successor
    return {**p, 'family':state.tag, 'a_hex':hex(state.a), 'b_hex':hex(state.b),
            'steps_hex':hex(raw), 'rounds':completed, 'events_hex':hex(events), 'status':status}


def native(engine, rounds):
    result = subprocess.run([str(Path(engine).resolve()), str(rounds)], capture_output=True, text=True, check=True)
    status, completed, a, b, raw, events = result.stdout.split()
    completed = int(completed)
    if status not in ('halt', 'unknown') or not 0 <= completed <= rounds or (status == 'unknown' and completed != rounds):
        raise ValueError('unexpected native completion')
    a, b, raw, events = (int(item, 16) for item in (a, b, raw, events))
    if (status == 'unknown' and a != 4) or (status == 'halt' and b != a+1) or raw < 136 or events < completed:
        raise ValueError('invalid native result')
    return {**blank(), 'a_hex':hex(a), 'b_hex':hex(b), 'steps_hex':hex(raw),
            'rounds':completed, 'events_hex':hex(events), 'status':status}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rounds', type=int, required=True, help='absolute number of completed A(4,b) returns')
    parser.add_argument('--checkpoint', type=Path, required=True)
    parser.add_argument('--resume', type=Path)
    parser.add_argument('--engine', type=Path, help='optional GMP replay from blank, saving at the requested endpoint')
    parser.add_argument('--every', type=int, default=100)
    args = parser.parse_args()
    verify_local_rules()
    p = load(args.resume) if args.resume else blank()
    if args.rounds < p['rounds'] or args.every < 1:
        parser.error('invalid target or save interval')
    if args.engine:
        if args.resume:
            parser.error('the native replay starts from blank; omit --engine to continue a saved checkpoint')
        p = native(args.engine, args.rounds)
        atomic_json(args.checkpoint, {'payload':p, 'sha256':checksum(p)})
        print(f"{p['rounds']} returns, {int(p['steps_hex'],16).bit_length()} raw clock bits, {p['status']}.")
        return
    while True:
        p = advance(p, min(args.rounds, p['rounds']+args.every))
        atomic_json(args.checkpoint, {'payload':p, 'sha256':checksum(p)})
        print(f"{p['rounds']} returns, {int(p['steps_hex'],16).bit_length()} raw clock bits, {p['status']}.", flush=True)
        if p['status'] == 'halt' or p['rounds'] == args.rounds:
            return


if __name__ == '__main__':
    main()
