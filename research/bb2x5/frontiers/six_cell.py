#!/usr/bin/env python3
"""Use exact six-cell stride rules on lines 14, 16 or 28 and save a physical tape checkpoint."""
import argparse
import base64
import itertools
import json
from pathlib import Path
import subprocess
import zlib

from checkpoints import holdouts
import survey

WIDTH = 6
MACHINES = {n: m for n, m in enumerate(holdouts(), 1) if n in (14, 16, 28)}


def worker_input(machine, seed, target, work):
    if seed is None:
        return f'{machine} {target} {work} 0 0 0 0\n'
    cells = survey.verify_state(seed, machine)
    offset = seed['left'] % WIDTH
    start = seed['left'] - offset
    padded = bytes(offset) + cells
    padded += bytes(-len(padded) % WIDTH)
    words = zip(*[iter(padded)] * WIDTH)
    rows = [f"{machine} {target} {work} {seed['steps']} {seed['head']} "
            f"{'AB'.index(seed['state'])} {start}"]
    for word, group in itertools.groupby(words):
        value = sum(d * 5**j for j, d in enumerate(word))
        rows.append(f'{value} {sum(1 for _ in group)}')
    return '\n'.join(rows) + '\n'


def unpack(line, output):
    machine = MACHINES[line]
    rows = iter(output.splitlines())
    status, *numbers = next(rows).split()
    operations, steps, head, state, start = map(int, numbers)
    if status not in ('unknown', 'halt') or state not in (0, 1) or start % WIDTH:
        raise ValueError('invalid worker header')
    tape = bytearray()
    for row in rows:
        value, copies = map(int, row.split())
        if not (0 <= value < 5**WIDTH and copies > 0):
            raise ValueError('invalid worker tile')
        word = bytes(value // 5**j % 5 for j in range(WIDTH))
        tape.extend(word * copies)
    # A word at either end may contain blank padding. Window checkpoints
    # store exactly the interval between the outermost nonzero cells.
    cells = tape.lstrip(b'\0')
    left = start + len(tape) - len(cells)
    cells = cells.rstrip(b'\0')
    p = {'format': survey.FORMAT, 'line': line, 'machine': machine, 'steps': steps,
         'head': head, 'state': 'AB'[state], 'status': status, 'left': left if cells else 0,
         'cells': len(cells), 'tape_zlib_base64': base64.b64encode(zlib.compress(cells, 9)).decode()}
    survey.verify_state(p, machine)
    return p, operations


def advance(engine, line, seed, target, work):
    proc = subprocess.run([str(Path(engine).resolve())], text=True, capture_output=True,
                          input=worker_input(MACHINES[line], seed, target, work))
    if proc.returncode:
        raise RuntimeError(proc.stderr.strip() or 'six-cell worker failed')
    return unpack(line, proc.stdout)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--engine', required=True, type=Path)
    parser.add_argument('--line', required=True, type=int, choices=MACHINES)
    parser.add_argument('--target', required=True, type=int, help='absolute raw step target through 2^60')
    parser.add_argument('--work', type=int, default=10**10, help='maximum two-tile operations')
    parser.add_argument('--resume', type=Path)
    parser.add_argument('--checkpoint', required=True, type=Path)
    args = parser.parse_args()
    seed = survey.load(args.resume, args.line, MACHINES[args.line]) if args.resume else None
    state, used = advance(args.engine, args.line, seed, args.target, args.work)
    survey.save(args.checkpoint, state)
    print(json.dumps({'line': args.line, 'status': state['status'], 'steps': state['steps'], 'work': used}))


if __name__ == '__main__':
    main()
