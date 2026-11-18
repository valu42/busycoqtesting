#!/usr/bin/env python3
"""Batch consecutive equal suffix calls of formal line 7 in chronological order."""
import argparse
from functools import lru_cache
import json
from pathlib import Path
import re
import sys

from checkpoints import ROOT, atomic_json, checksum, holdouts

sys.path.insert(0, str(ROOT))
from prior_sweeps import parse

MACHINE = '1RB---3RA2LA2RB_2LB3LA4LB4RA0RA'
RULES = parse(MACHINE)
FORMAT = 'bb2x5-line7-calls-v1'
HALT = 'halt'
TWOS = re.compile(b'\x02+')
ORDINARY = frozenset((2, 4))
WIDTH = 8


@lru_cache(maxsize=16384)
def skeleton(word, state):
    """The downstream entry letters and the denominator depend only on the initial digits."""
    divided = 0
    for digit in word:
        if state == 'B':
            divided += 1
            state = 'A'
        else:
            state = 'B' if digit == 4 else 'A'
    return state, divided


@lru_cache(maxsize=65536)
def coefficients(word, state, low):
    """For N=2^d h+low, descendant count and local cost are both affine in h."""
    child_state, divided = skeleton(word, state)
    scale, offset = 1 << divided, low
    cost_scale = cost_offset = 0
    image = bytearray(word)
    for j, digit in enumerate(word):
        cost_scale += scale
        cost_offset += offset
        if state == 'B':
            if offset & 1:
                image[j] = 6-digit
            scale //= 2
            offset = (offset + (digit == 4)) // 2
            state = 'A'
        elif digit == 2:
            scale *= 3
            offset *= 3
        else:
            state = 'B'
        cost_scale += scale
        cost_offset += offset
    return child_state, scale, offset, cost_scale, cost_offset, bytes(image)


class Calls:
    def __init__(self, word=b'', raw=0, limit=10**9, on_guard=None, on_round=None):
        self.tape = bytearray(word)
        self.steps = raw
        self.work = 0
        self.limit = limit
        self.halt_cell = None
        self.on_guard = on_guard
        self.on_round = on_round

    def tick(self):
        self.work += 1
        if self.work > self.limit:
            raise RuntimeError('call-work limit reached')

    def digit(self, i):
        if i == len(self.tape):
            self.tape.append(0)
        return self.tape[i]

    def guard_three(self, i):
        """Run the B call on the 3 next to an A0 guard. Report each reply word."""
        while True:
            self.tick()
            self.tape[i] = 4  # B3 sends A
            self.steps += 1
            _, first = yield self.many(i+1, 'A', 1)
            if first == HALT:
                return HALT
            # B4 sends A from a suspended 0; A4 sends B from a suspended 2.
            self.tape[i], entry = (0, 'A') if first == 'B' else (2, 'B')
            self.steps += 1
            _, second = yield self.many(i+1, entry, 1)
            if second == HALT:
                return HALT
            if second == 'B':
                if self.on_round is not None:
                    self.on_round(i, first+second)
                self.tape[i] = 2 if first == 'B' else 4
                self.steps += 1  # B0 or B2 returns B
                return 'B'
            if first == 'B':
                if self.on_round is not None:
                    self.on_round(i, 'BA')
                # A0 now installs another real guard on this cell.
                return (yield self.unit(i, 'A'))
            self.tape[i] = 3  # A2 sends the third call, in A
            self.steps += 1
            _, third = yield self.many(i+1, 'A', 1)
            if third == HALT:
                return HALT
            if self.on_round is not None:
                self.on_round(i, 'AA'+third)
            if third == 'A':
                self.tape[i] = 2
                self.steps += 1  # A3 returns A onto the parent guard
                return 'A'
            # B returned onto 3. Start the next round on the evolved suffix.

    def unit(self, i, state):
        """Finish one call from its current instruction, including every exceptional reply."""
        while True:
            self.tick()
            scanned = self.digit(i)
            if state == 'A' and scanned == 0:
                if self.on_guard is not None:
                    self.on_guard(self.tape, i+1)
                # A0 installs 1 and calls right in B. B0 or B2 returns B
                # immediately. B1 then exits to the left in A.
                child = self.digit(i+1)
                if child in (0, 2):
                    self.tape[i:i+2] = bytes((3, child+2))
                    self.steps += 3
                    return 'A'
                if child == 3:
                    self.tape[i] = 1
                    self.steps += 1
                    state = yield self.guard_three(i+1)
                    if state == HALT:
                        return HALT
                    continue
            rule = RULES.get((state, scanned))
            if rule is None:
                self.halt_cell = i
                return HALT
            digit, move, state = rule
            self.tape[i] = digit
            self.steps += 1
            if move == -1:
                return state
            _, state = yield self.many(i+1, state, 1)
            if state == HALT:
                return HALT

    def many(self, i, state, count, width=WIDTH):
        """Return (number of B replies, first different reply) for up to count calls."""
        done = 0
        while done < count:
            self.tick()
            digit = self.digit(i)
            n = count-done
            if digit not in ORDINARY:
                response = yield self.unit(i, state)
            else:
                word = bytes(self.tape[i:i+width])
                # A run of twos triples the calls at each level and preserves every digit.
                if width > 1 and word == bytes([2])*width and state == 'A':
                    length = TWOS.match(self.tape, i).end()-i
                    child_n = n * 3**length
                    local_cost = 2*(child_n-n)
                    image = None
                    child_state = 'A'
                else:
                    length = next((j for j, x in enumerate(word) if x not in ORDINARY), len(word))
                    word = word[:length]
                    _, divided = skeleton(word, state)
                    high, low = divmod(n, 1 << divided)
                    child_state, a, b, c, d, image = coefficients(word, state, low)
                    child_n = a*high+b
                    local_cost = c*high+d
                if child_n:
                    j, response = yield self.many(i+length, child_state, child_n)
                else:
                    j, response = 0, 'B'
                if response == 'B':
                    self.steps += local_cost
                    if image is not None:
                        self.tape[i:i+length] = image
                    return count, 'B'
                # Descendants have already run. Recover the parent instructions suspended
                # at their first exceptional reply, working back across this packet.
                # Later requests in the packet can resume using wide packets again.
                position = i + length
                frames = []
                parent_state, parent_n = state, n
                for pos in range(i, position):
                    s = self.tape[pos]
                    frames.append((pos, s, parent_state, parent_n))
                    if parent_state == 'A':
                        parent_n *= 3 if s == 2 else 1
                        parent_state = 'A' if s == 2 else 'B'
                    else:
                        parent_n = (parent_n + (s == 4)) // 2
                        parent_state = 'A'
                for pos, s, parent_state, parent_n in reversed(frames):
                    if response == 'B':
                        # All child calls now succeeded. Finish the pending parent batch.
                        self.steps += parent_n+j
                        if parent_state == 'B' and parent_n & 1:
                            self.tape[pos] = 6-s
                        j = parent_n
                        continue
                    if parent_state == 'A' and s == 2:
                        p, phase = divmod(j, 3)
                        suspended = (3, 4, 0)[phase]
                    elif parent_state == 'A':
                        p, suspended = j, 2
                    else:
                        p, suspended = 2*j + int(s == 2), 0
                    self.tape[pos] = suspended
                    self.steps += p+j+1
                    if response == 'A':
                        response = yield self.unit(pos, 'A')
                        if response == 'B':
                            p += 1
                            if p < parent_n:
                                added, response = yield self.many(pos, parent_state, parent_n-p)
                                p += added
                    j = p
                return done+j, response
            if response != 'B':
                return done, response
            done += 1
        return done, 'B'

    def run(self, request):
        # The active call tree may be tens of thousands of cells deep.
        stack = [request]
        value = None
        while stack:
            try:
                child = stack[-1].send(value)
            except StopIteration as finished:
                value = finished.value
                stack.pop()
            else:
                stack.append(child)
                value = None
        return value

    def epoch(self):
        # A0 writes 1 and calls the suffix in B. B1 restores 3 and moves to a fresh zero.
        self.steps += 1
        if self.tape and self.tape[0] == 3:
            response = self.run(self.guard_three(0))
        else:
            _, response = self.run(self.many(0, 'B', 1))
        if response == 'B':
            self.steps += 1
            self.tape.insert(0, 3)
            return True
        if response == 'A':
            self.halt_cell = -1  # A on the new guard 1.
        return False

    def epoch_block(self, count, on_block=None):
        """Advance up to count epochs, preserving the physical state at the first exception."""
        if count < 1:
            raise ValueError('expected a positive epoch count')
        if ((count == 1 and on_block is None) or self.on_guard is not None or self.on_round is not None
                or self.tape[:2] != b'\x03\x02'):
            if on_block is not None:
                on_block(0, 1, 'literal', None)
            return (1, False) if self.epoch() else (0, True)
        end = TWOS.match(self.tape, 1).end()
        block = 3**(end-1)
        calls = block*(3**count-1)

        def probe(n):
            trial = Calls(self.tape[end:], limit=self.limit-self.work)
            j, reply = trial.run(trial.many(0, 'A', n))
            self.work += trial.work
            return trial, j, reply

        trial, j, reply = probe(calls)
        if reply != 'B':
            # Only complete epochs with all-B tail replies can use the geometric
            # formula. The failed probe mutated a private copy of the tail.
            lo, hi = 0, count
            while lo+1 < hi:
                mid = (lo+hi)//2
                if block*(3**mid-1) <= j:
                    lo = mid
                else:
                    hi = mid
            if not lo:
                if on_block is not None:
                    on_block(end-1, 1, reply, j)
                return (1, False) if self.epoch() else (0, True)
            count = lo
            calls = block*(3**count-1)
            trial, j, reply = probe(calls)
        if reply != 'B' or j != calls:
            raise ValueError('inconsistent tail reply in geometric epoch batch')
        self.tape = bytearray([3]) + bytearray([2])*(end-1+count) + trial.tape
        self.steps += trial.steps + 2*calls + count
        if on_block is not None:
            on_block(end-1, count, 'B', None)
        return count, False


def snapshot(epochs, vm, halted=False):
    # After e successes the fresh guard is at -e and the stored word starts at 1-e.
    left = -epochs if halted else 1-epochs
    word = (bytes([1]) + vm.tape) if halted else vm.tape
    return {'format': FORMAT, 'line': 7, 'machine': MACHINE, 'epochs': epochs,
            'steps_hex': hex(vm.steps), 'head': 1-epochs+vm.halt_cell if halted else -epochs,
            'state': 'A', 'status': 'halt' if halted else 'unknown', 'word_left': left,
            'word': ''.join(map(str, word))}


def load(path):
    doc = json.loads(Path(path).read_text())
    p = doc['payload']
    if doc['sha256'] != checksum(p) or (p['format'], p['machine'], p['line']) != (FORMAT, MACHINE, 7):
        raise ValueError('line 7 checkpoint identity or checksum mismatch')
    e = p['epochs']
    word = p['word']
    if type(e) is not int or e < 0 or set(word)-set('01234') or p['state'] != 'A':
        raise ValueError('invalid line 7 epoch state')
    steps = int(p['steps_hex'], 16)
    if steps < abs(p['head']) or (steps-p['head']) % 2:
        raise ValueError('invalid raw step count')
    if p['status'] == 'unknown':
        if p['head'] != -e or p['word_left'] != 1-e or (not e and (word or steps)) or (e and not word.startswith('3')):
            raise ValueError('expected a completed blank extension')
    elif (p['status'] != 'halt' or p['word_left'] != -e or not 0 <= p['head']+e < len(word)
          or word[p['head']+e] != '1'):
        raise ValueError('invalid halting instruction')
    return p


def save(path, state):
    atomic_json(path, {'payload': state, 'sha256': checksum(state)})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--epochs', type=int, required=True, help='absolute number of successful left extensions')
    parser.add_argument('--resume', type=Path)
    parser.add_argument('--checkpoint', type=Path, required=True)
    parser.add_argument('--every', type=int, default=100)
    parser.add_argument('--batch', type=int, default=1, help='maximum epochs per geometric tail batch')
    parser.add_argument('--work', type=int, default=10**9)
    args = parser.parse_args()
    if holdouts()[6] != MACHINE or min(args.epochs, args.work) < 0 or min(args.every, args.batch) < 1:
        parser.error('invalid dataset or work limits')
    try:
        state = load(args.resume) if args.resume else snapshot(0, Calls())
        epochs = state['epochs']
        if state['status'] == 'halt' or epochs > args.epochs:
            parser.error('expected a running seed at or before target')
        vm = Calls(map(int, state['word']), int(state['steps_hex'], 16), args.work)
        save(args.checkpoint, state)
        while epochs < args.epochs:
            count = min(args.batch, args.epochs-epochs, args.every-epochs % args.every)
            completed, halted = vm.epoch_block(count)
            epochs += completed
            if halted:
                save(args.checkpoint, snapshot(epochs, vm, halted=True))
                print(f'Halt at epoch {epochs}, raw time {hex(vm.steps)}.')
                return
            if epochs % args.every == 0 or epochs == args.epochs:
                save(args.checkpoint, snapshot(epochs, vm))
                print(f'{epochs} completed epochs, {vm.steps.bit_length()} raw counter bits, {len(vm.tape)} cells.', flush=True)
    except (OSError, KeyError, TypeError, ValueError, RuntimeError) as error:
        parser.exit(2, f'Batch stopped: {error}\n')


if __name__ == '__main__':
    main()
