#!/usr/bin/env python3
"""Exact reusable block-exit simulation for finite-state, finite-symbol TMs.

Each cached answer is a finite computation on an immutable tape block, stopping
at its first exit, undefined instruction, or repeated complete local state.
Recursive answers compose smaller answers; no fitted or extrapolated rule is
used. Resource exhaustion is UNKNOWN, never a decision. Python 3.10+, stdlib.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
import os
import tempfile
from pathlib import Path
import re
import time


class ResourceLimit(RuntimeError):
    pass


def integer_text(value: int) -> str:
    """JSON-safe exact integer; hex avoids Python's decimal digit ceiling."""
    return str(value) if value.bit_length() < 12000 else hex(value)


def read_integer(value: str) -> int:
    return int(value, 16 if value.startswith(('0x', '-0x')) else 10)


def parse_machine(encoding: str):
    rows = encoding.split('_')
    states, symbols = len(rows), len(rows[0]) // 3
    if not states or not symbols or any(len(r) != 3 * symbols for r in rows):
        raise ValueError('inconsistent transition table')
    rules = {}
    for state, row in enumerate(rows):
        for symbol in range(symbols):
            token = row[3 * symbol:3 * symbol + 3]
            if token == '---':
                continue
            if not re.fullmatch(r'[0-9][LR][A-Z]', token):
                raise ValueError(f'invalid transition {token!r}')
            write, move, target = int(token[0]), (-1 if token[1] == 'L' else 1), ord(token[2]) - 65
            if write >= symbols or target >= states:
                raise ValueError('transition outside table alphabet/state set')
            rules[state, symbol] = write, move, target
    return rules, states, symbols


@dataclass(frozen=True)
class Answer:
    node: int
    state: int
    position: int  # -1 or block size on exit; otherwise the scanned cell
    steps: int
    status: str = 'exit'
    period: int = 0  # positive only for a witnessed confined loop


class Blocks:
    """Hash-consed complete binary words; leaves are alphabet symbols."""
    def __init__(self, symbols: int, max_nodes: int = 1_000_000):
        self.symbols = symbols
        self.nodes: list[tuple[int, int] | None] = [None] * symbols
        self.levels = [0] * symbols
        self.is_zero = [i == 0 for i in range(symbols)]
        self.intern = {}
        self.max_nodes = max_nodes
        self.zeros = [0]

    def pair(self, left: int, right: int) -> int:
        if self.levels[left] != self.levels[right]:
            raise ValueError('unequal subtree sizes')
        key = left, right
        if key in self.intern:
            return self.intern[key]
        if len(self.nodes) >= self.max_nodes:
            raise ResourceLimit('node budget')
        node = len(self.nodes)
        self.nodes.append(key)
        self.levels.append(self.levels[left] + 1)
        self.is_zero.append(self.is_zero[left] and self.is_zero[right])
        self.intern[key] = node
        return node

    def zero(self, level: int) -> int:
        while len(self.zeros) <= level:
            self.zeros.append(self.pair(self.zeros[-1], self.zeros[-1]))
        return self.zeros[level]

    def word(self, values) -> int:
        values = list(values)
        if not values or len(values) & (len(values) - 1):
            raise ValueError('word length must be a positive power of two')
        if any(v < 0 or v >= self.symbols for v in values):
            raise ValueError('symbol outside alphabet')
        while len(values) > 1:
            values = [self.pair(values[i], values[i+1]) for i in range(0, len(values), 2)]
        return values[0]

    def symbol_at(self, node: int, position: int) -> int:
        if not 0 <= position < (1 << self.levels[node]):
            raise ValueError('position outside block')
        while self.levels[node]:
            half = 1 << (self.levels[node] - 1)
            left, right = self.nodes[node]
            node = right if position >= half else left
            position %= half
        return node

    def nonzero(self, node: int, start: int = 0):
        """Yield exact sparse tape cells. Intended only for bounded validation."""
        level = self.levels[node]
        if self.is_zero[node]:
            return
        if level == 0:
            yield start, node
        else:
            left, right = self.nodes[node]
            yield from self.nonzero(left, start)
            yield from self.nonzero(right, start + (1 << (level - 1)))


class Engine:
    def __init__(self, encoding: str, *, max_work: int = 1_000_000,
                 max_nodes: int = 1_000_000, max_cache: int = 1_000_000,
                 seconds: float | None = None):
        self.encoding = encoding
        self.rules, self.states, symbols = parse_machine(encoding)
        self.blocks = Blocks(symbols, max_nodes)
        self.cache: dict[tuple[int, int, int], Answer] = {}
        self.max_work, self.max_cache = max_work, max_cache
        self.work = self.hits = self.misses = 0
        self.deadline = None if seconds is None else time.monotonic() + seconds

    def check_budget(self):
        if self.work >= self.max_work:
            raise ResourceLimit('work budget')
        if self.deadline is not None and time.monotonic() >= self.deadline:
            raise ResourceLimit('time budget')

    def exit(self, node: int, state: int, side: int) -> Answer:
        """Enter at the left (0) or right (1) edge; answer at first exit."""
        if side not in (0, 1) or not 0 <= state < self.states:
            raise ValueError('invalid entry')
        key = node, state, side
        self.check_budget()
        self.work += 1
        known = self.cache.get(key)
        if known is not None:
            self.hits += 1
            return known
        self.misses += 1
        level = self.blocks.levels[node]
        if not level:
            rule = self.rules.get((state, node))
            if rule is None:
                result = Answer(node, state, 0, 0, 'halt')
            else:
                write, move, target = rule
                result = Answer(write, target, move, 1)
        else:
            children = list(self.blocks.nodes[node])
            half = 1 << (level - 1)
            child, entry = side, side
            elapsed, seen = 0, {}
            while True:
                self.check_budget()
                self.work += 1
                local = children[0], children[1], state, child, entry
                if local in seen:
                    whole = self.blocks.pair(*children)
                    position = child * half + (half - 1 if entry else 0)
                    result = Answer(whole, state, position, elapsed, 'loop', elapsed - seen[local])
                    break
                seen[local] = elapsed
                answer = self.exit(children[child], state, entry)
                children[child] = answer.node
                state, elapsed = answer.state, elapsed + answer.steps
                if answer.status != 'exit':
                    result = Answer(self.blocks.pair(*children), state,
                                    child * half + answer.position, elapsed,
                                    answer.status, answer.period)
                    break
                direction = 0 if answer.position == -1 else 1
                if child == direction:
                    result = Answer(self.blocks.pair(*children), state,
                                    -1 if direction == 0 else 2 * half, elapsed)
                    break
                child, entry = direction, 1 - direction
        if len(self.cache) >= self.max_cache:
            raise ResourceLimit('cache budget')
        self.cache[key] = result
        return result


@dataclass
class Run:
    encoding: str
    level: int
    blocks: dict[int, int]
    index: int = 0
    side: int = 0
    state: int = 0
    steps: int = 0
    macros: int = 0
    status: str = 'running'
    position: int | None = None
    period: int = 0

    @classmethod
    def blank(cls, engine: Engine, level: int):
        if not 0 <= level <= 60:
            raise ValueError('level must be between 0 and 60')
        return cls(engine.encoding, level, {})

    @property
    def head(self):
        offset = self.position if self.position is not None else ((1 << self.level) - 1 if self.side else 0)
        return self.index * (1 << self.level) + offset

    def advance(self, engine: Engine):
        if self.status != 'running':
            return
        if self.encoding != engine.encoding:
            raise ValueError('machine mismatch')
        zero = engine.blocks.zero(self.level)
        answer = engine.exit(self.blocks.get(self.index, zero), self.state, self.side)
        # Commit only complete outer answers: a budget failure leaves the run intact.
        if answer.node == zero:
            self.blocks.pop(self.index, None)
        else:
            self.blocks[self.index] = answer.node
        self.steps += answer.steps
        self.macros += 1
        self.state = answer.state
        if answer.status == 'exit':
            direction = -1 if answer.position == -1 else 1
            self.index += direction
            self.side = 1 if direction == -1 else 0
        else:
            self.status, self.position, self.period = answer.status, answer.position, answer.period

    def sparse_tape(self, engine: Engine):
        return dict(cell for index, node in self.blocks.items()
                    for cell in engine.blocks.nonzero(node, index * (1 << self.level)))

    def checkpoint(self, engine: Engine):
        # Only reachable tape DAG nodes, not transient nodes or summary cache.
        ids = {i: i for i in range(engine.blocks.symbols)}
        pairs = []
        def visit(node):
            if node not in ids:
                left, right = engine.blocks.nodes[node]
                pair = [visit(left), visit(right)]
                ids[node] = engine.blocks.symbols + len(pairs)
                pairs.append(pair)
            return ids[node]
        tape = [[integer_text(index), visit(node)] for index, node in sorted(self.blocks.items())]
        payload = {'format': 'bb-exact-blocks-v1', 'machine': self.encoding,
                   'level': self.level, 'pairs': pairs, 'tape': tape,
                   'index': integer_text(self.index), 'side': self.side, 'state': self.state,
                   'steps': integer_text(self.steps), 'macros': integer_text(self.macros),
                   'status': self.status, 'position': self.position, 'period': integer_text(self.period)}
        canonical = json.dumps(payload, sort_keys=True, separators=(',', ':')).encode()
        return {'sha256': hashlib.sha256(canonical).hexdigest(), 'payload': payload}

    @classmethod
    def restore(cls, engine: Engine, document):
        """Load a checkpoint from a trusted run; checksum is not provenance proof."""
        p = document['payload']
        canonical = json.dumps(p, sort_keys=True, separators=(',', ':')).encode()
        if hashlib.sha256(canonical).hexdigest() != document['sha256']:
            raise ValueError('checkpoint checksum mismatch')
        if p['format'] != 'bb-exact-blocks-v1' or p['machine'] != engine.encoding:
            raise ValueError('checkpoint format/machine mismatch')
        level = p['level']
        if not isinstance(level, int) or not 0 <= level <= 60:
            raise ValueError('invalid checkpoint level')
        refs = list(range(engine.blocks.symbols))
        for pair in p['pairs']:
            if len(pair) != 2 or any(not isinstance(x, int) or not 0 <= x < len(refs) for x in pair):
                raise ValueError('invalid DAG reference')
            refs.append(engine.blocks.pair(refs[pair[0]], refs[pair[1]]))
        tape = {}
        for index, ref in p['tape']:
            if not isinstance(ref, int) or not 0 <= ref < len(refs):
                raise ValueError('invalid tape node')
            node, index = refs[ref], read_integer(index)
            if engine.blocks.levels[node] != level or index in tape:
                raise ValueError('invalid block level/duplicate index')
            tape[index] = node
        run = cls(p['machine'], level, tape, read_integer(p['index']), p['side'], p['state'],
                  read_integer(p['steps']), read_integer(p['macros']), p['status'], p['position'], read_integer(p['period']))
        if run.side not in (0, 1) or not 0 <= run.state < engine.states or run.steps < 0 or run.macros < 0 or run.period < 0:
            raise ValueError('invalid checkpoint state/counters')
        if run.status not in ('running', 'halt', 'loop'):
            raise ValueError('invalid checkpoint status')
        if run.status == 'running':
            if run.position is not None or run.period:
                raise ValueError('invalid running checkpoint')
        elif not isinstance(run.position, int) or not 0 <= run.position < 1 << level:
            raise ValueError('invalid stopped checkpoint position')
        if (run.status == 'loop') != (run.period > 0):
            raise ValueError('invalid loop period')
        if run.status == 'halt':
            node = run.blocks.get(run.index)
            symbol = 0 if node is None else engine.blocks.symbol_at(node, run.position)
            if (run.state, symbol) in engine.rules:
                raise ValueError('halt checkpoint scans a defined instruction')
        return run


def save_checkpoint(run: Run, engine: Engine, path: Path):
    """Atomically replace a checkpoint, preserving the previous file on failure."""
    path = Path(path)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8',
                                         dir=path.parent, prefix=path.name + '.',
                                         suffix='.tmp', delete=False) as output:
            temporary = Path(output.name)
            json.dump(run.checkpoint(engine), output, indent=2)
            output.write('\n')
            output.flush()
            os.fsync(output.fileno())
        os.replace(temporary, path)
        temporary = None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    choice = parser.add_mutually_exclusive_group(required=True)
    choice.add_argument('--line', type=int, help='one-based line in the 37 holdout file')
    choice.add_argument('--machine', help='transition encoding')
    choice.add_argument('--resume', type=Path, help='full-state checkpoint JSON')
    parser.add_argument('--level', type=int, default=8, help='block width is 2**level (default 8)')
    parser.add_argument('--macros', type=int, default=10000, help='additional outer block exits')
    parser.add_argument('--work', type=int, default=1000000, help='summary invocations plus child-composition iterations')
    parser.add_argument('--nodes', type=int, default=1000000)
    parser.add_argument('--cache', type=int, default=1000000)
    parser.add_argument('--seconds', type=float)
    parser.add_argument('--checkpoint', type=Path)
    args = parser.parse_args()
    document = None
    if args.resume:
        try:
            document = json.loads(args.resume.read_text())
            encoding = document['payload']['machine']
        except (OSError, ValueError, KeyError, TypeError) as error:
            parser.error(f'invalid checkpoint: {error}')
    elif args.line is not None:
        machines = Path(__file__).with_name('BB2x5_Rocq_holdouts_37.txt').read_text().splitlines()
        if not 1 <= args.line <= len(machines):
            parser.error('line outside holdout file')
        encoding = machines[args.line-1]
    else:
        encoding = args.machine
    if min(args.macros, args.work, args.nodes, args.cache) < 0 or (args.seconds is not None and args.seconds < 0):
        parser.error('budgets must be nonnegative')
    try:
        engine = Engine(encoding, max_work=args.work, max_nodes=args.nodes, max_cache=args.cache, seconds=args.seconds)
        run = Run.restore(engine, document) if document is not None else Run.blank(engine, args.level)
    except (ResourceLimit, ValueError, KeyError, TypeError, AttributeError) as error:
        parser.error(str(error))
    reason = 'macro budget'
    started = time.monotonic()
    try:
        for _ in range(args.macros):
            run.advance(engine)
            if run.status != 'running':
                reason = run.status
                break
    except ResourceLimit as error:
        reason = str(error)
    if args.checkpoint:
        try:
            save_checkpoint(run, engine, args.checkpoint)
        except OSError as error:
            parser.error(f'cannot save checkpoint: {error}')
    result = {'machine': encoding, 'status': 'unknown' if run.status == 'running' else run.status,
              'reason': reason, 'steps': integer_text(run.steps), 'head': integer_text(run.head),
              'state': chr(65+run.state), 'macros': integer_text(run.macros), 'block_level': run.level,
              'loop_period': integer_text(run.period), 'work': engine.work, 'misses': engine.misses, 'hits': engine.hits,
              'nodes': len(engine.blocks.nodes), 'cache': len(engine.cache),
              'seconds': round(time.monotonic() - started, 6)}
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
