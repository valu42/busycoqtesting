#!/usr/bin/env python3
"""Explore TMs by memoizing execution inside recursively nested tape blocks.

This is an UNVERIFIED simulator, not a proof or certificate checker. A limit
means UNKNOWN. Halts and cycles are candidates requiring independent proof.
Each binary-tree node represents a finite block. A cached result records
execution from one boundary until exit or halt; untouched outer tape is never
read. Repeated complete local configurations detect cycles inside a block.

Counts describe completed top-level calls only. When a budget interrupts an
inner call, its partial progress is omitted and the last committed global
configuration remains the reported snapshot. Counts are not certified bounds.
Time is checked every 1,024 recursive calls. Memory is bounded by cache-miss
and node counts, not by a measured byte limit. AI-assisted research by Codex.
"""
import argparse
import itertools
import json
import math
import random
import time
from pathlib import Path


def parse(table):
    cells = table.strip().replace('_', '')
    if len(cells) != 36:
        raise ValueError('expected six binary states')
    result = []
    for i in range(0, 36, 3):
        item = cells[i:i+3]
        if item == '---':
            result.append(None)
        elif item[0] in '01' and item[1] in 'LR' and item[2] in 'ABCDEF':
            result.append((int(item[0]), int(item[1] == 'R'), ord(item[2])-65))
        else:
            raise ValueError('invalid transition ' + item)
    return result


class Budget(Exception):
    pass


class Cycle(Exception):
    pass


class Engine:
    def __init__(self, table, seconds=30, max_entries=500000):
        self.table = parse(table)
        self.deadline = time.monotonic() + seconds
        self.max_entries = max_entries
        self.children = [None, None]
        self.levels = [0, 0]
        self.popcounts = [0, 1]
        self.interned = {}
        self.cache = {}
        self.hits = self.misses = self.calls = 0
        self.zeroes = [0]

    def node(self, a, b):
        key = (a, b)
        got = self.interned.get(key)
        if got is not None:
            return got
        assert self.levels[a] == self.levels[b]
        if len(self.children) >= 4 * self.max_entries:
            raise Budget('node limit')
        got = len(self.children)
        self.interned[key] = got
        self.children.append(key)
        self.levels.append(self.levels[a] + 1)
        self.popcounts.append(self.popcounts[a] + self.popcounts[b])
        return got

    def zero(self, level):
        while len(self.zeroes) <= level:
            self.zeroes.append(self.node(self.zeroes[-1], self.zeroes[-1]))
        return self.zeroes[level]

    def from_bits(self, bits):
        if len(bits) == 1:
            return bits[0]
        mid = len(bits) // 2
        return self.node(self.from_bits(bits[:mid]), self.from_bits(bits[mid:]))

    def to_bits(self, node):
        if node < 2:
            return [node]
        a, b = self.children[node]
        return self.to_bits(a) + self.to_bits(b)

    def run(self, node, q, entry):
        """(new block, state, exit side or -1 for halt, steps, halt offset)."""
        self.calls += 1
        if self.calls % 1024 == 0 and time.monotonic() >= self.deadline:
            raise Budget('time limit')
        key = (node, q, entry)
        hit = self.cache.get(key)
        if hit is not None:
            self.hits += 1
            return hit
        self.misses += 1
        if self.misses > self.max_entries:
            raise Budget('entry limit')
        if node < 2:
            op = self.table[2*q + node]
            if op is None:
                answer = (node, q, -1, 0, 0)
            else:
                write, side, state = op
                answer = (write, state, side, 1, -1)
        else:
            children = list(self.children[node])
            child, steps, seen = entry, 0, set()
            while True:
                local = (*children, child, q, entry)
                if local in seen:
                    raise Cycle('repeated configuration in level ' + str(self.levels[node]))
                seen.add(local)
                new, q, side, count, pos = self.run(children[child], q, entry)
                children[child] = new
                steps += count
                if side == -1:
                    offset = child << (self.levels[node] - 1)
                    answer = (self.node(*children), q, -1, steps, pos + offset)
                    break
                if side == child:
                    answer = (self.node(*children), q, side, steps, -1)
                    break
                child, entry = 1-child, 1-side
        self.cache[key] = answer
        return answer


def raw_block(table, bits, q, entry):
    tape = list(bits)
    head = 0 if entry == 0 else len(tape)-1
    seen, steps = set(), 0
    while True:
        key = (tuple(tape), q, head)
        if key in seen:
            return 'cycle'
        seen.add(key)
        op = table[2*q + tape[head]]
        if op is None:
            return (tape, q, -1, steps, head)
        tape[head], side, q = op
        head += 2*side-1
        steps += 1
        if not 0 <= head < len(tape):
            return (tape, q, side, steps, -1)


def selftest(tables):
    rng = random.Random(623625)
    cases = cycles = integration = 0
    controls = ['1RA1RA_------_------_------_------_------',
                '1RB1RB_1LA1LA_------_------_------_------',
                '------_------_------_------_------_------']
    for table in controls + tables:
        engine = Engine(table, 60, 2000000)
        words = [bits for n in (1, 2, 4) for bits in itertools.product((0, 1), repeat=n)]
        words += [tuple(rng.randrange(2) for _ in range(8)) for _ in range(64)]
        for bits, q, entry in itertools.product(words, range(6), range(2)):
            expected = raw_block(engine.table, bits, q, entry)
            try:
                got = engine.run(engine.from_bits(bits), q, entry)
                got = (engine.to_bits(got[0]), *got[1:])
            except Cycle:
                got = 'cycle'
                cycles += 1
            assert got == expected, (table, bits, q, entry, got, expected)
            cases += 1
        # Independently check composition across block boundaries and the
        # complete global tape, including expansions into blank space.
        engine = Engine(table, 60, 2000000)
        level, size = 3, 8
        blank = current = engine.zero(level)
        left, right, raw_tape = [], [], set()
        q = entry = index = raw_q = raw_head = 0
        for _ in range(25):
            try:
                new, next_q, side, count, pos = engine.run(current, q, entry)
            except Cycle:
                break  # Local-cycle detection is covered by raw_block above.
            for _ in range(count):
                op = engine.table[2*raw_q + (raw_head in raw_tape)]
                assert op is not None
                write, direction, raw_q = op
                if write:
                    raw_tape.add(raw_head)
                else:
                    raw_tape.discard(raw_head)
                raw_head += 2*direction-1
            packed = left + [new] + list(reversed(right))
            actual_tape = {(index-len(left)+k)*size+j
                           for k, node in enumerate(packed)
                           for j, bit in enumerate(engine.to_bits(node)) if bit}
            expected_head = index*size + (pos if side == -1 else size if side else -1)
            assert (actual_tape, next_q, expected_head) == (raw_tape, raw_q, raw_head)
            integration += 1
            if side == -1:
                assert engine.table[2*raw_q + (raw_head in raw_tape)] is None
                break
            q, current = next_q, new
            if side:
                left.append(current)
                current = right.pop() if right else blank
            else:
                right.append(current)
                current = left.pop() if left else blank
            index += 2*side-1
            entry = 1-side
    return {'block_tests': cases, 'cycles': cycles, 'global_snapshots': integration}


def explore(table, level, seconds, entries, top_limit):
    start = time.monotonic()
    engine = Engine(table, seconds, entries)
    blank = current = engine.zero(level)
    left, right = [], []
    q = entry = index = steps = top = 0
    status, detail = 'unknown', 'top-level limit'
    partial = 0
    try:
        while top < top_limit:
            new, q2, side, count, pos = engine.run(current, q, entry)
            if side == -1:
                current, q, steps = new, q2, steps + count
                status, detail, partial = 'halt_candidate', 'needs independent certificate', pos
                break
            current, q, steps = new, q2, steps + count
            if side:
                left.append(current)
                current = right.pop() if right else blank
            else:
                right.append(current)
                current = left.pop() if left else blank
            index += 2*side-1
            entry = 1-side
            top += 1
    except Budget as e:
        detail = str(e)
    except Cycle as e:
        status, detail = 'cycle_candidate', str(e) + '; needs independent certificate'
    return {'machine': table, 'status': status, 'detail': detail,
            'level': level, 'elapsed': round(time.monotonic()-start, 3),
            'completed_steps_hex': hex(steps), 'completed_steps_bits': steps.bit_length(),
            'completed_blocks': top, 'block_index': index, 'entry': entry,
            'state': q, 'halt_offset': partial if status == 'halt_candidate' else None,
            'ones': sum(engine.popcounts[n] for n in left+right+[current]),
            'nodes': len(engine.children), 'cache_entries': len(engine.cache),
            'cache_hits': engine.hits, 'cache_misses': engine.misses,
            'stored_blocks': len(left)+len(right)+1}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('--indices', default='7,33,39,116,144,321,375,387,397,549')
    parser.add_argument('--level', type=int, default=8)
    parser.add_argument('--seconds', type=float, default=30)
    parser.add_argument('--entries', type=int, default=500000)
    parser.add_argument('--blocks', type=int, default=1000000)
    parser.add_argument('--selftest', action='store_true')
    args = parser.parse_args()
    if not 0 <= args.level <= 60:
        parser.error('--level must be between 0 and 60')
    if not math.isfinite(args.seconds) or args.seconds <= 0:
        parser.error('--seconds must be finite and positive')
    if args.entries < args.level+1 or args.blocks < 0:
        parser.error('--entries must exceed the level, and --blocks must be nonnegative')
    tables = [line.strip() for line in args.input.read_text().splitlines() if line.strip()]
    try:
        indices = [int(s) for s in args.indices.split(',')]
        if any(i < 1 or i > len(tables) for i in indices):
            raise ValueError('index out of range')
        for i in indices:
            parse(tables[i-1])
    except ValueError as e:
        parser.error(str(e))
    if args.selftest:
        print(json.dumps(selftest([tables[i-1] for i in indices])), flush=True)
    else:
        for index in indices:
            result = explore(tables[index-1], args.level, args.seconds, args.entries, args.blocks)
            result['index'] = index
            print(json.dumps(result), flush=True)


if __name__ == '__main__':
    main()
