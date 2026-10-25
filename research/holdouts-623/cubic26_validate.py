#!/usr/bin/env python3
"""Independent small-case TM checks and integration checks for cubic26_accel.

Usage: python3 cubic26_validate.py /path/to/cubic26_accel
This is testing, not formal verification of the native executable.
"""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

MACHINE = '1RB1LC_1LC1RD_1LA0LB_0RB1RE_1RF0RA_---0RC'
_flat = MACHINE.replace('_', '')
TABLE = [None if _flat[i:i+3] == '---' else
         (int(_flat[i]), 1 if _flat[i+1] == 'R' else -1, ord(_flat[i+2])-65)
         for i in range(0, 36, 3)]


def next_pair(a, b):
    """Different case ordering from C++; mirrors the Coq next function."""
    assert a >= 1 and b >= 2 and a+b >= 11
    if b <= a:
        if b == 2:
            return a-3, 7
        if b == 3:
            return None
        return a-b+1, 2*b+3
    gap = b-a
    if gap == 1:
        return 4, 2*a+4
    if gap == 2:
        return 1, 2*a+7
    if gap == 3 and a % 2:
        return 2*a+1, 9
    return (2*a+4, b-a-1) if a % 2 == 0 else (2*a+3, b-a)


def raw_check(a, b, target, blank=False):
    q, head, tape = ((0, 0, set()) if blank else
                     (2, 0, set(range(-a-1, -1)) | set(range(b))))
    for steps in range(200000):
        op = TABLE[2*q + (head in tape)]
        if op is None:
            assert target is None, (a, b, steps, target)
            return steps
        write, direction, q = op
        if write:
            tape.add(head)
        else:
            tape.discard(head)
        head += direction
        if q == 2 and target is not None:
            aa, bb = target
            expected = set(range(head-aa-1, head-1)) | set(range(head, head+bb))
            if tape == expected:
                return steps+1
    raise AssertionError(('ordinary execution limit', a, b, target))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('binary', type=Path)
    args = parser.parse_args()
    binary = str(args.binary.resolve())
    cases = halts = max_steps = 0
    for a in range(1, 50):
        for b in range(2, 60):
            if a+b < 11:
                continue
            target = next_pair(a, b)
            max_steps = max(max_steps, raw_check(a, b, target))
            cases += 1
            halts += target is None
    entry_steps = raw_check(0, 0, (2, 9), blank=True)

    def run(*options):
        result = subprocess.run([binary, *map(str, options)], check=True,
                                capture_output=True, text=True, timeout=120)
        return json.loads(result.stdout)

    def state(result):
        return result['iterations'], result['a'], result['b']

    native = run('--selftest')
    expected = (2, 9)
    for _ in range(1000000):
        expected = next_pair(*expected)
        assert expected is not None
    result = run('--iterations', 1000000, '--seconds', 30)
    assert state(result) == (1000000, *expected)
    assert state(run('--scalar', '--iterations', 1000000, '--seconds', 30)) == state(result)
    with tempfile.TemporaryDirectory(prefix='cubic26-validation-', dir=Path.cwd()) as directory:
        checkpoint = Path(directory)/'split.checkpoint'
        run('--bits', 11, '--iterations', 100000000, '--seconds', 30,
            '--checkpoint', checkpoint)
        split = run('--bits', 14, '--resume', checkpoint, '--iterations', 100000000,
                    '--seconds', 30, '--checkpoint', checkpoint)
        full = run('--iterations', 200000000, '--seconds', 30)
        assert state(split) == state(full)
        assert state(run('--resume', checkpoint, '--iterations', 0)) == state(full)
        invalid = Path(directory)/'invalid.checkpoint'
        valid_text = checkpoint.read_text()
        for content in (valid_text.replace(MACHINE, 'wrong machine'),
                        'cubic26-v1\n'+MACHINE+'\n-1 9 0 0 0 0 0\n',
                        valid_text+'trailing garbage\n'):
            invalid.write_text(content)
            failed = subprocess.run([binary, '--resume', str(invalid)], capture_output=True)
            assert failed.returncode != 0
        # Boundary controls: report a halt, and preserve a resumable checkpoint
        # when the native integer range is exhausted.
        invalid.write_text('cubic26-v1\n'+MACHINE+'\n8 3 0 0 0 0 0\n')
        assert run('--resume', invalid, '--iterations', 0)['status'] == 'halt_candidate'
        limit = (2**64-1)//8
        invalid.write_text(f'cubic26-v1\n{MACHINE}\n1 {limit-1} 0 0 0 0 0\n')
        stopped = run('--resume', invalid, '--checkpoint', invalid)
        assert stopped['status'] == 'integer_limit'
        assert state(run('--resume', invalid, '--iterations', 0)) == state(stopped)
    for options in (('--seconds', 'nan'), ('--bits', '25'), ('--iterations', '-1')):
        assert subprocess.run([binary, *options], capture_output=True).returncode != 0
    limited = run('--seconds', '0.000000001', '--iterations', 1000000)
    assert limited['status'] == 'time_limit' and limited['verified'] is False
    print(json.dumps({'status': 'passed', 'ordinary_TM_cases': cases,
                      'halting_cases': halts, 'max_raw_steps_per_case': max_steps,
                      'blank_entry_steps': entry_steps,
                      'python_orbit_iterations': 1000000,
                      'checkpoint_iterations': 200000000, 'native': native}))


if __name__ == '__main__':
    main()
