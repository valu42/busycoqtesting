#!/usr/bin/env python3
"""Time odd left records of line 18 using the exact header and suffix transfers."""
import argparse
import json
from pathlib import Path

from checkpoints import atomic_json, checksum
from line18_header import MACHINE, local_steps, verify
from prior_sweeps import TapeMachine, parse

FORMAT = 'bb2x5-line18-returns-v1'
RULES = parse(MACHINE)


class Suffix:
    def __init__(self, word, limit):
        self.cells = bytearray(map(int, word))
        self.steps = 0
        self.work = 0
        self.limit = limit

    def tick(self):
        self.work += 1
        if self.work > self.limit:
            raise RuntimeError('suffix work limit reached')

    def literal(self, pos, state, left):
        """Run an actual excursion until it exits at left-1."""
        while pos >= left:
            self.tick()
            if pos == len(self.cells):
                self.cells.append(0)
            rule = RULES.get((state, self.cells[pos]))
            if rule is None:
                raise RuntimeError(f'undefined {state}{self.cells[pos]} at suffix offset {pos}')
            self.cells[pos], delta, state = rule
            pos += delta
            self.steps += 1
        return state

    def batch(self, pos, count):
        """Yield sub-batches, returning ordinary B replies and the first A reply if any."""
        done = 0
        while done < count:
            self.tick()
            n = count - done
            if (pos+1 >= len(self.cells) or self.cells[pos] != 3
                    or self.cells[pos+1] not in (1, 2)):
                if self.literal(pos, 'B', pos) == 'A':
                    return done, 'A'
                done += 1
                continue
            digit = self.cells[pos+1]
            # Either width is sound. Choose the three-cell rule at the join
            # of two adjacent threes, and the binary pair everywhere else.
            if self.cells[pos+2:pos+4] == b'\x03\x03':
                if digit == 2:
                    self.cells[pos+1] = 1  # 323 -> 313 without any child
                    self.steps += 3
                    done += 1
                    continue
                passed, reply = yield self.batch(pos+3, 2*n)
                if reply == 'B':
                    self.steps += 11*n
                    return count, 'B'
                prior, phase = divmod(passed, 2)
                self.steps += 11*prior + (6 if phase else 3)
                self.cells[pos:pos+3] = bytes((2, 1, 0) if phase else (2, 0, 2))
                reply = self.literal(pos+2, 'A', pos)
            else:
                children = (n + (digit == 1)) // 2
                if children:
                    passed, reply = yield self.batch(pos+2, children)
                else:
                    passed, reply = 0, 'B'
                if reply == 'B':
                    if n % 2:
                        self.cells[pos+1] = 3-digit
                    self.steps += 3*n + children
                    return count, 'B'
                prior = digit - 1 + 2*passed
                # After all completed pairs, B3,B1 have suspended this call
                # on 20. The child's first A reply resumes at the second cell.
                self.steps += 3*prior + passed + 2
                self.cells[pos:pos+2] = bytes((2, 0))
                reply = self.literal(pos+1, 'A', pos)
            if reply == 'A':
                return done + prior, 'A'
            done += prior + 1
        return done, 'B'

    def b_calls(self, pos, count):
        stack = [self.batch(pos, count)]
        value = None
        while stack:
            try:
                child = stack[-1].send(value)
            except StopIteration as end:
                value = end.value
                stack.pop()
            else:
                stack.append(child)
                value = None
        return value


def record(k, steps, suffix):
    return {'format': FORMAT, 'line': 18, 'machine': MACHINE, 'record': k,
            'steps_hex': hex(steps), 'head': -2*k-1, 'state': 'A', 'suffix': suffix}


def blank_entry():
    tm = TapeMachine(MACHINE)
    for _ in range(47):
        if not tm.step():
            raise ValueError('halt in entry trace')
    if (tm.head != -3 or tm.state != 'A'
            or tm.tape != {i-2: int(c) for i, c in enumerate('13431313')}):
        raise ValueError('line 18 entry mismatch')
    return record(1, 47, '13')


def load(path):
    doc = json.loads(Path(path).read_text())
    p = doc['payload']
    k, steps, suffix = p['record'], int(p['steps_hex'], 16), p['suffix']
    if (doc['sha256'] != checksum(p) or type(k) is not int or k < 1
            or not isinstance(suffix, str) or set(suffix) - set('01234')
            or suffix.endswith('0') or steps < 47 or k+2+len(suffix) > steps or (steps - p['head']) % 2
            or steps.bit_length() < k or record(k, steps, suffix) != p
            or (k == 1 and p != blank_entry())):
        raise ValueError('invalid line 18 checkpoint')
    return p


def advance(start, target, limit=10**7, progress=None):
    k = start['record']
    if k > target or limit < 1:
        raise ValueError('invalid target or per-record work limit')
    suffix = Suffix(start['suffix'], limit)
    steps = int(start['steps_hex'], 16)
    while k < target:
        suffix.work = suffix.steps = 0
        try:
            if suffix.literal(0, 'A', 0) != 'B':
                raise RuntimeError('the initial A call returned A')
            count = 1 << (k-1)
            done, reply = suffix.b_calls(0, count)
            if done != count or reply != 'B':
                raise RuntimeError(f'B call {done+1} returned A across the suffix cut')
        except RuntimeError as exc:
            raise RuntimeError(f'left record {k}, suffix cut {k+3}: {exc}') from exc
        if not suffix.cells or suffix.cells[0] != 3:
            raise ValueError('completed suffix failed the moving-cut invariant')
        del suffix.cells[0]
        steps += suffix.steps + local_steps(k)
        k += 1
        if progress:
            progress(k, steps, suffix.cells)
    return record(k, steps, ''.join(map(str, suffix.cells)).rstrip('0'))


def save(path, p):
    atomic_json(path, {'payload': p, 'sha256': checksum(p)})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--record', type=int, required=True, help='absolute odd left record index')
    parser.add_argument('--work', type=int, default=10**7, help='per-record suffix work limit')
    parser.add_argument('--resume', type=Path)
    parser.add_argument('--checkpoint', type=Path, required=True)
    args = parser.parse_args()
    try:
        verify()
        state = load(args.resume) if args.resume else blank_entry()

        def progress(k, steps, cells):
            # Save regular restart points while avoiding an O(k)-sized JSON write every epoch.
            if k % 100 == 0:
                save(args.checkpoint, record(k, steps, ''.join(map(str, cells)).rstrip('0')))

        result = advance(state, args.record, args.work, progress)
        save(args.checkpoint, result)
        print(f"Record {result['record']}, {len(result['suffix'])} suffix cells, "
              f"{int(result['steps_hex'], 16).bit_length()} raw-clock bits.")
    except (KeyError, OSError, RuntimeError, TypeError, ValueError) as error:
        parser.exit(2, f'Line 18 stopped: {error}\n')


if __name__ == '__main__':
    main()
