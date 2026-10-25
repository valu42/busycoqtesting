#!/usr/bin/env python3
"""Independent arithmetic, ordinary-TM, and integration checks.

Run: python3 cubic_family_validate.py /path/to/cubic_family
Testing does not verify the native executable or a saved long run.
"""
import argparse
import itertools
import json
from pathlib import Path
import subprocess
import tempfile

MODELS = {
    35: (17, '1RB0LE_1LC1RA_1RA1LD_0LC0LA_0RE1RF_0RC---', (3, 0, 0)),
    269: (32, '1LB1LD_0RC1LA_1LA1RC_0LB1RE_1LF0RD_---0LE', (0, 1, 0)),
    494: (33, '1LB1RE_1LC1LA_0RD1LB_1RE1RD_1LF0RA_---0LE', (2, 2, 1)),
    138: (35, '1LB1LD_0RC1LA_1RA1RC_1LA1RE_1LF0RD_---0LE', (0, 1, 1)),
    409: (36, '1LB1LD_0RC1LA_0LA1RC_1LA1RE_1LF0RD_---0LE', (0, 0, 1)),
}


def next_triple(entry, triple):
    """Literal nat-pattern cases from CubicCap, with Python big integers."""
    a, b, c = triple
    divisor = 3 if entry == 35 else 2
    i = min(a // divisor, c)
    a, b, c = a-divisor*i, b+2*i, c-i
    if entry == 35:
        match (a, b, c):
            case (0, 0, 0): return a, b, c
            case (0, 0, 1) | (0, 1, 0): return 3, 0, 4
            case (0, 0, _) | (0, 1, _): return None
            case (0, _, 0): return 3+2*(b-2), 1, 1
            case (0, _, _): return 5+2*(b-2), 0, c-1
            case (1, _, 0): return 3, 0, 4+2*b
            case (1, _, 1): return 3+2*b, 1, 1
            case (1, _, _): return 5+2*b, 0, c-2
            case (2, _, 0): return 0, 1, 3+2*b
            case (2, _, _): return 0, 3+b, c-1
            case (_, _, 0): return 1+(a-3), 1, 3+2*b
            case _: return a, b, c
    if a == 1 and c == 0:
        return None
    if a >= 4:
        assert c == 0
        return a-4, 2, 1+b
    if entry == 269:
        match (a, c):
            case (0, 0): return 1+2*b, 1, 0
            case (0, 1): return 2+2*b, 1, 0
            case (0, _): return 2+2*b, 1, 1+(c-2)
            case (1, 1): return 3+2*b, 1, 0
            case (1, _): return 4+2*b, 1, c-2
            case (2, 0): return 2, 1, b
            case (3, 0): return 4, 1, b
    elif entry == 494:
        match (a, b, c):
            case (0, 0, 0): return 2, 2, 1
            case (0, _, 0): return 1+2*(b-1), 2, 1
            case (0, _, 1): return 2*b, 2, 1
            case (0, _, _): return 2+2*b, 2, c-2
            case (1, _, 1): return 1+2*b, 2, 1
            case (1, _, 2): return 2+2*b, 2, 1
            case (1, _, _): return 4+2*b, 2, c-3
            case (2, 0, 0): return 0, 2, 1
            case (2, _, 0): return 2, 2, b-1
            case (3, 0, 0): return 2, 2, 1
            case (3, _, 0): return 4, 2, b-1
    elif entry == 138:
        match (a, b, c):
            case (0, _, 0): return 1+2*b, 1, 1
            case (0, _, 1): return 2+2*b, 1, 1
            case (0, _, _): return 4+2*b, 0, 1+(c-2)
            case (1, _, 1): return 3+2*b, 1, 1
            case (1, _, 2): return 4+2*b, 1, 1
            case (1, _, _): return 6+2*b, 0, 1+(c-3)
            case (2, 0, 0): return 2, 1, 1
            case (2, _, 0): return 4, 0, 1+(b-1)
            case (3, 0, 0): return 4, 1, 1
            case (3, _, 0): return 6, 0, 1+(b-1)
    else:
        match (a, c):
            case (0, 0): return 1+2*b, 0, 1
            case (0, _): return 2+2*b, 0, 1+(c-1)
            case (1, 1): return 3+2*b, 0, 1
            case (1, _): return 4+2*b, 0, 1+(c-2)
            case (2, 0): return 2, 0, 1+b
            case (3, 0): return 4, 0, 1+b
    raise AssertionError((entry, a, b, c))


def config(entry, triple, head=-1):
    a, b, c = triple
    word = ([0]+[0, 1]*b+[1]*c if entry == 35 else [1, 1]*b+[1, 0]*c)
    tape = set(range(head-a+1, head+1))
    tape.update(head+1+i for i, bit in enumerate(word) if bit)
    return (4 if entry == 35 else 0 if entry == 494 else 3), head, tape


def raw_check(entry, source, target, blank=False):
    flat = MODELS[entry][1].replace('_', '')
    table = [None if flat[i:i+3] == '---' else
             (int(flat[i]), 1 if flat[i+1] == 'R' else -1, ord(flat[i+2])-65)
             for i in range(0, 36, 3)]
    q, head, tape = (0, 0, set()) if blank else config(entry, source)
    for steps in range(200001):
        if target is not None:
            tq, _, expected = config(entry, target, head)
            if q == tq and tape == expected:
                return steps
        op = table[2*q+(head in tape)]
        if op is None:
            assert target is None, (entry, source, target, steps)
            return steps
        write, direction, q = op
        if write:
            tape.add(head)
        else:
            tape.discard(head)
        head += direction
    raise AssertionError(('ordinary execution limit', entry, source, target))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('binary', type=Path)
    args = parser.parse_args()
    binary = str(args.binary.resolve())

    def run(entry, *opts):
        result = subprocess.run([binary, '--entry', str(entry), *map(str, opts)],
                                check=True, text=True, capture_output=True, timeout=120)
        return json.loads(result.stdout)

    def state(result):
        return result['iterations'], (result['a'], result['b'], result['c'])

    report = {'verified': False, 'models': []}
    for entry, (lemma, machine, initial) in MODELS.items():
        grid = list(itertools.product(range(13), range(7), range(13)))
        expected = [next_triple(entry, x) for x in grid]
        results = subprocess.run([binary, '--entry', str(entry), '--batch'],
                                 input=''.join(' '.join(map(str, x))+'\n' for x in grid),
                                 check=True, text=True, capture_output=True).stdout.splitlines()
        actual = [None if line == 'HALT' else tuple(map(int, line.split())) for line in results]
        assert actual == expected, entry
        raw_max = max(raw_check(entry, x, target) for x, target in zip(grid, expected))
        entry_steps = raw_check(entry, None, initial, blank=True)
        python_state = initial
        for _ in range(1000000):
            python_state = next_triple(entry, python_state)
            assert python_state is not None
        full = run(entry, '--iterations', 1000000, '--seconds', 30)
        assert state(full) == (1000000, python_state)
        assert state(run(entry, '--scalar', '--iterations', 1000000, '--seconds', 30)) == state(full)
        with tempfile.TemporaryDirectory(prefix='cubic-family-test-', dir=Path.cwd()) as directory:
            cp = Path(directory)/'state'
            run(entry, '--bits', 7, '--iterations', 543210, '--seconds', 30, '--checkpoint', cp)
            split = run(entry, '--bits', 13, '--iterations', 456790, '--seconds', 30,
                        '--resume', cp, '--checkpoint', cp)
            assert state(split) == state(full)
            assert state(run(entry, '--resume', cp, '--iterations', 0)) == state(full)
            halting = next(x for x, y in zip(grid, expected) if y is None)
            cp.write_text(f'cubic-family-v1\n{entry} {machine}\n'+
                          ' '.join(map(str, (*halting, 0, 0, 0)))+'\n')
            for budget in (0, 100):
                result = run(entry, '--resume', cp, '--iterations', budget)
                assert result['status'] == 'halt_candidate' and result['new_iterations'] == 0
            bad = f'cubic-family-v1\n{entry} {machine}\n0 0 0 10 11 0\n'
            for text in (bad, bad.replace('11', '-1'), bad+'trailing\n'):
                cp.write_text(text)
                result = subprocess.run([binary, '--entry', str(entry), '--resume', str(cp)],
                                        text=True, capture_output=True)
                assert result.returncode != 0
        report['models'].append(dict(entry=entry, lemma=f'WF{lemma}',
            arithmetic_cases=len(grid), ordinary_tm_cases=len(grid),
            halting_cases=sum(x is None for x in expected), max_raw_steps=raw_max,
            blank_entry_steps=entry_steps, python_orbit_iterations=1000000,
            checkpoint_resume='passed', terminal_controls='passed'))
    report['native_selftest'] = run(269, '--selftest')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
