#!/usr/bin/env python3
"""Time line 9's left sweeps and batch the BBA requests at coordinate 2."""
import argparse
import json
from pathlib import Path
import sys

from checkpoints import ROOT, atomic_json, checksum, holdouts

sys.path.insert(0, str(ROOT))
from prior_sweeps import parse

MACHINE = '1RB---4RB2RB4LA_2LB3LA3LB0RA0RB'
RULES = parse(MACHINE)
FORMAT = 'bb2x5-line9-sweeps-v1'
EMPTY, A, B = range(3)


class ExceptionalCall(Exception):
    """The ordinary cell table does not describe A on a virgin zero."""


class WordBudget(Exception):
    """The shared word dictionary needs to be cleared."""


class Words:
    """Interned concatenations of A/B requests, with exact expanded lengths."""
    def __init__(self, limit):
        self.nodes = [None, None, None]
        self.length = [0, 1, 1]
        self.intern = {}
        self.images = {}
        self.limit = limit

    def join(self, left, right):
        if not left or not right:
            return left or right
        pair = (left, right)
        if pair not in self.intern:
            if len(self.nodes) >= self.limit:
                raise WordBudget
            self.intern[pair] = len(self.nodes)
            self.nodes.append(pair)
            self.length.append(self.length[left] + self.length[right])
        return self.intern[pair]

    def transmit(self, node, digit):
        """Return (final digit, ordered child requests), conditional on B replies."""
        if node == A:
            if digit == 0:
                raise ExceptionalCall
            return (2, self.join(B, B)) if digit == 2 else (3, B)
        if node == B:
            if digit == 0:
                return 2, EMPTY
            return (3, EMPTY) if digit == 2 else (2, A)
        key = (node, digit)
        if key not in self.images:
            left, right = self.nodes[node]
            middle, first = self.transmit(left, digit)
            final, second = self.transmit(right, middle)
            self.images[key] = final, self.join(first, second)
        return self.images[key]

    def batch(self, suffix, power):
        """Apply 2^power BBA cycles, committing only if every cell succeeds."""
        requests = self.join(self.join(B, B), A)
        for _ in range(power):
            requests = self.join(requests, requests)
        cost = self.length[requests]
        result = []
        while requests:
            i = len(result)
            digit = suffix[i] if i < len(suffix) else 0
            final, requests = self.transmit(requests, digit)
            result.append(final)
            cost += 2 * self.length[requests]
        return result + suffix[len(result):], cost


def literal_cycle(suffix, limit=1_000_000):
    """Resolve a cycle containing exceptional child replies directly at the cut."""
    tape = suffix.copy()
    steps = 0
    for state in 'BBA':
        pos = 0
        while pos >= 0:
            if pos == len(tape):
                tape.append(0)
            if steps >= limit:
                raise RuntimeError('literal suffix work limit reached')
            rule = RULES.get((state, tape[pos]))
            if rule is None:
                raise RuntimeError(f'undefined {state}{tape[pos]} at coordinate {pos+2} '
                                   f'after {steps} suffix steps in this cycle')
            tape[pos], move, state = rule
            pos += move
            steps += 1
        if state != 'B':
            raise RuntimeError('A returned across coordinate 2; the sweep reduction stopped')
    if any(digit not in (2, 3) for digit in tape):
        raise RuntimeError('the next suffix falls outside the 2/3 cell table')
    return tape, steps


def prefix_steps(cycles):
    # Startup takes 3 steps. Each n from 1 to 2*cycles contributes 3*n+4.
    return 3 + 6*cycles*cycles + 11*cycles


def checkpoint(cycles, suffix, steps):
    return {'format': FORMAT, 'line': 9, 'machine': MACHINE, 'cycles': cycles,
            'steps': steps, 'head': -(2*cycles+1), 'state': 'A',
            'suffix_at_2': ''.join(map(str, suffix))}


def load(path):
    doc = json.loads(Path(path).read_text())
    p = doc['payload']
    cycles, steps = p['cycles'], p['steps']
    if (doc['sha256'] != checksum(p) or p['format'] != FORMAT or p['line'] != 9
            or p['machine'] != MACHINE or holdouts()[8] != MACHINE
            or type(cycles) is not int or cycles < 0 or type(steps) is not int
            or steps < prefix_steps(cycles) + 3*cycles or (steps-p['head']) % 2
            or p['state'] != 'A' or p['head'] != -(2*cycles+1)
            or not isinstance(p['suffix_at_2'], str) or set(p['suffix_at_2']) - set('23')
            or (cycles == 0 and (steps != 3 or p['suffix_at_2']))):
        raise ValueError('invalid line 9 checkpoint')
    return p


def advance(goal, start=None, node_limit=100_000):
    if start is None:
        start = checkpoint(0, [], 3)
    done = start['cycles']
    if goal < done or node_limit < 32:
        raise ValueError('require cycles >= starting count and node limit >= 32')
    suffix = list(map(int, start['suffix_at_2']))
    cost = start['steps'] - prefix_steps(done)
    words = Words(node_limit)
    power = 0
    while done < goal:
        power = min(power, (goal-done).bit_length()-1)
        try:
            suffix, delta = words.batch(suffix, power)
        except (WordBudget, ExceptionalCall) as error:
            if isinstance(error, WordBudget):
                words = Words(node_limit)
            if power:
                power -= 1
                continue
            suffix, delta = literal_cycle(suffix)
        done += 1 << power
        cost += delta
        power += 1
    return checkpoint(done, suffix, prefix_steps(done) + cost)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cycles', type=int, required=True, help='absolute number of BBA cycles')
    parser.add_argument('--resume', type=Path)
    parser.add_argument('--checkpoint', type=Path, required=True)
    parser.add_argument('--node-limit', type=int, default=100_000)
    args = parser.parse_args()
    if holdouts()[8] != MACHINE:
        parser.exit(2, 'line 9 identity mismatch\n')
    try:
        p = advance(args.cycles, load(args.resume) if args.resume else None, args.node_limit)
        atomic_json(args.checkpoint, {'payload': p, 'sha256': checksum(p)})
        print(f"{p['cycles']} cycles, {p['steps']} raw steps, head {p['head']}")
    except (KeyError, OSError, RuntimeError, ValueError) as error:
        parser.exit(2, f'Line 9 stopped: {error}\n')


if __name__ == '__main__':
    main()
