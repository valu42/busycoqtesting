#!/usr/bin/env python3
"""Exact run-length sweeps on lines 29 (Bonus Cryptid) and 30 (Hydra)."""
import argparse
import json
from pathlib import Path
import sys

from checkpoints import ROOT, atomic_json, checksum, holdouts
sys.path.insert(0, str(ROOT))
from prior_sweeps import parse

MACHINES = {
    29: '1RB3RB---3LA1RA_2LA3RA4LB0LB1LB',
    30: '1RB3RB---3LA1RA_2LA3RA4LB0LB0LA',
}
FORMAT = 'bb2x5-hydra-v1'


def push(stack, digit, n=1):
    if not n or (not stack and digit == 0):
        return
    if stack and stack[-1][0] == digit:
        n += stack.pop()[1]
    stack.append((digit, n))


def pop(stack, n=1):
    """Remove n cells from the nearest run, or read implicit exterior zeros."""
    if not stack:
        return 0
    digit, length = stack.pop()
    if not 0 < n <= length:
        raise ValueError('move crosses a run boundary')
    push(stack, digit, length - n)
    return digit


class Machine:
    def __init__(self, line):
        self.line = line
        self.code = MACHINES[line]
        if holdouts()[line - 1] != self.code:
            raise ValueError('holdout encoding mismatch')
        self.rules = parse(self.code)
        self.state = 'A'
        self.steps = self.head = self.operations = 0
        # Nearest run last on each side. The right stack includes the scanned cell.
        self.left, self.right = [], []

    @property
    def digit(self):
        return self.right[-1][0] if self.right else 0

    def bulk_sweep(self):
        """Batch P(m,n) at A scanning 02, with a finite zero run beyond the 2."""
        if (len(self.right) < 3 or self.right[-2:] != [(2, 1), (0, 1)]
                or self.right[-3][0] != 0
                or (self.left and (len(self.left) != 1 or self.left[0][0] != 3))):
            return False
        stride = 3 if self.line == 29 else 2
        copies = self.right[-3][1] // stride
        if not copies:
            return False
        growth = stride + 1
        m = self.left[0][1] if self.left else 0
        # One pass does (12+stride) local instructions, a leftward scan of
        # m+growth threes and a three-instruction rightward shift per three.
        self.steps += copies * (12 + stride + 4*(m + growth)) + 2*growth*copies*(copies - 1)
        self.head += stride * copies
        del self.right[-2:]
        pop(self.right, stride * copies)
        push(self.right, 2)
        push(self.right, 0)
        push(self.left, 3, growth * copies)
        return True

    def step(self):
        """Apply a whole finite sweep, a run scan or one defined instruction."""
        rule = self.rules.get((self.state, self.digit))
        if rule is None:
            return False
        self.operations += 1
        if self.state == 'A' and self.digit == 0:
            if self.bulk_sweep():
                return True
            if len(self.right) >= 2 and self.right[-1] == (0, 1) and self.right[-2][0] == 3:
                # A scanning 03 becomes 3 followed by A scanning 0 in three instructions.
                self.right.pop()
                _, length = self.right.pop()
                push(self.right, 0)
                push(self.left, 3, length)
                self.head += length
                self.steps += 3 * length
                return True
        write, move, new_state = rule
        digit = self.digit
        n = 1
        if move == 1:
            if new_state == self.state and self.right:
                n = self.right[-1][1]
            pop(self.right, n)
            push(self.left, write, n)
        else:
            pop(self.right)
            if new_state == self.state and self.left and self.left[-1][0] == digit:
                n += self.left.pop()[1]
            push(self.right, write, n)
            push(self.right, pop(self.left))
        self.head += move * n
        self.steps += n
        self.state = new_state
        return True

    def advance(self, operations):
        if operations < self.operations:
            raise ValueError('target precedes checkpoint')
        while self.operations < operations and self.step():
            pass

    def payload(self):
        def encode(stack):
            return [[digit, hex(n)] for digit, n in stack]
        return {'format': FORMAT, 'line': self.line, 'machine': self.code,
                'operations': self.operations, 'steps_hex': hex(self.steps), 'head_hex': hex(self.head),
                'state': self.state, 'status': 'unknown' if (self.state, self.digit) in self.rules else 'halt',
                'left': encode(self.left), 'right': encode(self.right)}


def load(path, line):
    doc = json.loads(Path(path).read_text())
    p = doc['payload']
    machine = Machine(line)
    if doc['sha256'] != checksum(p):
        raise ValueError('invalid checkpoint checksum')
    machine.steps, machine.head = int(p['steps_hex'], 16), int(p['head_hex'], 16)
    machine.operations, machine.state = p['operations'], p['state']
    if (type(machine.operations) is not int or not 0 <= machine.operations <= machine.steps
            or machine.state not in ('A', 'B') or abs(machine.head) > machine.steps
            or (machine.steps - machine.head) % 2):
        raise ValueError('invalid head, state or counters')
    for side in ('left', 'right'):
        stack = getattr(machine, side)
        for digit, count in p[side]:
            n = int(count, 16)
            if type(digit) is not int or not 0 <= digit <= 4 or n <= 0:
                raise ValueError('invalid tape run')
            push(stack, digit, n)
    if machine.payload() != p:
        raise ValueError('noncanonical tape or wrong checkpoint identity/status')
    if (machine.head - sum(n for _, n in machine.left) < -machine.steps
            or machine.head + sum(n for _, n in machine.right) - 1 > machine.steps):
        raise ValueError('tape outside the reachable interval')
    return machine


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--line', type=int, choices=MACHINES, required=True)
    parser.add_argument('--operations', type=int, required=True, help='absolute number of acceleration operations')
    parser.add_argument('--resume', type=Path)
    parser.add_argument('--checkpoint', type=Path, required=True)
    args = parser.parse_args()
    machine = load(args.resume, args.line) if args.resume else Machine(args.line)
    machine.advance(args.operations)
    payload = machine.payload()
    atomic_json(args.checkpoint, {'payload': payload, 'sha256': checksum(payload)})
    print(f"Line {args.line}: {machine.operations} operations, {machine.steps.bit_length()} raw clock bits, {payload['status']}.")


if __name__ == '__main__':
    main()
