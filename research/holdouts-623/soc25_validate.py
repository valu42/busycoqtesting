#!/usr/bin/env python3
"""Independent arithmetic/round checks for soc25_deque; optionally benchmark cpp_int.

Source recurrence: SOC25Iter.F in busycoq PR #40, commit
069dc1eb72df69dfa595f491b5c315c3ce424ac6. Testing is not a proof of native code.
"""
import argparse
import json
from pathlib import Path
import random
import subprocess


def split_low(x):
    if not x:
        return 0, 0
    h = (x & -x).bit_length()-1
    return x >> (h+1), h


def next_round(L, X):
    """Direct transcription using unbounded ints and Coq's truncated subtraction."""
    assert L >= 1 and 2 <= X < 1 << (L+1)
    if X == 1 << L:
        l = L-1
        a = l//2
        t = 5*a + (2 if l % 2 == 0 else 4)
        return l+3+t, ((1 << (l+2))+1)*(1 << t)+(0 if l % 2 == 0 else 1)
    m, h = split_low(X)
    k = max(0, (1 << L)-1 - ((1 << h)-1)*2)
    a = h//2
    if h % 2:
        return None if m else (L+1+5*a+3, (2*k+1) << (5*a+3))
    L1 = L+1+5*a
    k1 = max(0, ((2*k+1) << (5*a))-1)
    if not m:
        return L1, k1+2
    x, i = split_low(m)
    k1 = max(0, k1-2*((1 << i)-1))
    while True:
        a = i//2
        if i % 2 == 0:
            return L1+1+5*a+1, ((2*k1+1) << (5*a+1))+(2*x+1)
        L1 += 1+5*a+4
        k1 = max(0, ((2*k1+1) << (5*a+4))-1)
        if not x:
            return L1, k1+1
        x, i = split_low(x)
        k1 = max(0, k1-((1 << (i+1))-1))


def run(binary, *options):
    p = subprocess.run([str(binary), *map(str, options)], text=True,
                       capture_output=True, check=True, timeout=120)
    return json.loads(p.stdout)


def state(result):
    return result['L'], int(result['X_hex'], 16)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('binary', type=Path)
    parser.add_argument('--bigint', type=Path)
    args = parser.parse_args()
    binary = args.binary.resolve()
    cases = [(L, X, 1) for L in range(1, 13) for X in range(2, 1 << (L+1))]
    rng = random.Random(250040)
    cases.extend((L, rng.randrange(2, 1 << (L+1)), rng.randrange(1, 100))
                 for L in range(3, 20) for _ in range(100))
    batch = subprocess.run([str(binary), '--batch'], text=True, check=True,
                           capture_output=True, timeout=60,
                           input=''.join(f'{L} {X} {n}\n' for L, X, n in cases))
    lines = batch.stdout.splitlines()
    assert len(lines) == len(cases)
    halts = 0
    for (L, X, count), line in zip(cases, lines):
        expected = L, X
        for _ in range(count):
            expected = next_round(*expected)
            if expected is None:
                break
        got = None if line == 'HALT' else (int(line.split()[0]), int(line.split()[1], 16))
        assert got == expected, ((L, X, count), expected, got)
        halts += got is None
    arithmetic = run(binary, '--selftest')
    for start, initial in enumerate(((1, 2), (2, 4), (1, 3)), 1):
        expected = initial
        for _ in range(10000):
            expected = next_round(*expected)
            assert expected is not None
        assert state(run(binary, '--start', start, '--rounds', 10000, '--hex')) == expected
    limited = run(binary, '--max-bits', 8, '--hex')
    assert limited['status'] == 'space_limit' and limited['rounds'] == 1
    assert state(limited) == state(run(binary, '--rounds', 1, '--hex'))
    assert run(binary, '--seconds', '1e-9')['status'] == 'time_limit'
    for options in (('--start', '4'), ('--seconds', 'nan'), ('--rounds', '-1'),
                    ('--max-bits', '0')):
        assert subprocess.run([str(binary), *options], capture_output=True).returncode != 0
    for text in ('0 2 1\n', '3 1 1\n', '3 16 1\n', '3 6 -1\n', 'junk\n'):
        assert subprocess.run([str(binary), '--batch'], text=True, input=text,
                              capture_output=True).returncode != 0
    measurements = []
    if args.bigint:
        for start in (1, 2, 3):
            reference = run(args.bigint.resolve(), '--start', start, '--rounds', 100000, '--hex')
            fast = run(binary, '--start', start, '--rounds', 100000, '--hex')
            assert state(reference) == state(fast)
            measurements.append({'start': start, 'rounds': 100000,
                                 'bigint_seconds': reference['seconds'],
                                 'deque_seconds': fast['seconds'], 'L': fast['L'],
                                 'speed_ratio': reference['seconds']/fast['seconds']})
    print(json.dumps({'status': 'passed', 'round_cases': len(cases),
                      'halting_cases': halts, 'python_orbits': 3,
                      'python_rounds_per_orbit': 10000, 'arithmetic': arithmetic,
                      'compiled_comparisons': measurements}))


if __name__ == '__main__':
    main()
