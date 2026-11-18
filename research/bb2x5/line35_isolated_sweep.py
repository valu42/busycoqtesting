"""Execute machine 35 one normalized sweep at a time and explain any debt at cut 28."""

import argparse
import base64
from bisect import bisect_right
from collections import Counter
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import zlib

from frontiers.checkpoints import atomic_json, checksum
from line35_guard_stream import (
    ALPHABET, CLOSE, HEADERS, NEUTRAL, OPEN, birth_columns, packed_successor,
)
from line35_pascal import normalized35
from line37_orbit import match, matching_layers
from prior_sweeps import TERNARY_CLOSE, TapeMachine, direct_epoch


CUT = 28
RIGHT_MOVES_AT_GUARD = (1, 1, 2, 8, 9, 11)
EPOCH_FORMAT = 'bb2x5-line35-epoch-v1'
CONTROL_FORMAT = 'bb2x5-line35-control-epoch-v1'
MASK_TABLE = {q: bytes(49 if i == q else 48 for i in range(256)) for q in (OPEN, CLOSE)}


@dataclass(frozen=True)
class Epoch:
    number: int
    steps: int
    head: int
    width: int
    opens: int
    closes: int

    @classmethod
    def from_word(cls, number, steps, head, word):
        word = bytes(word)
        if not word or word[-1] != CLOSE or not set(word) <= set(ALPHABET):
            raise ValueError('a normalized word must use digits 1, 2, 3 and end in 2')
        return cls(number, steps, head, len(word),
                   int(word.translate(MASK_TABLE[OPEN]), 2),
                   int(word.translate(MASK_TABLE[CLOSE]), 2))

    def digits(self):
        size = (self.width + 7) // 8
        o = self.opens.to_bytes(size, 'little')
        c = self.closes.to_bytes(size, 'little')
        return bytes(OPEN if o[j//8] & (1 << (j%8)) else CLOSE if c[j//8] & (1 << (j%8))
                     else NEUTRAL for j in reversed(range(self.width)))

    def location(self):
        return {'epoch': self.number, 'steps': self.steps, 'head': self.head, 'cells': self.width}


def blank_epoch():
    machine = TapeMachine(TERNARY_CLOSE)
    word = direct_epoch(machine, ALPHABET)
    return Epoch.from_word(1, machine.steps, machine.head, word)


@dataclass(frozen=True)
class Reading:
    cut: int
    balance: int
    internal: int
    exterior: int
    guard: int

    @property
    def threshold(self):
        return 0 if self.internal >= 6 else 6 + self.balance

    @property
    def margin(self):
        return self.threshold - self.exterior


def sweep(state):
    """Return the cut reading, birth letter and next epoch. None marks an actual B4."""
    n, opens, closes = state.width, state.opens, state.closes
    cut = min(CUT, n)
    gap = n - cut
    po, pc = opens >> gap, closes >> gap
    _, internal, _ = match(cut, po, pc, cut)
    balance = po.bit_count() - pc.bit_count()
    finite = (1 << (n + 1)) - 1
    survivors = opens
    area = guard = exterior = 0
    for survivors, occupied in matching_layers(opens, closes):
        guard += (occupied >> n) & 1
        exterior += (occupied >> gap) & 1
        area += (occupied & finite).bit_count()
    if guard != max(internal, exterior - balance):
        raise ArithmeticError('cut and full-word guard disagree')
    reading = Reading(cut, balance, internal, exterior, guard)
    if guard >= 6:
        return reading, None, None
    header = len(HEADERS[guard])
    right_moves = 2*n + 1 + area - survivors.bit_count() + RIGHT_MOVES_AT_GUARD[guard]
    new = packed_successor(n, survivors, guard)
    letter = guard + 1 if guard else (survivors >> (n - 1)) & 1
    return reading, letter, Epoch(state.number + 1, state.steps + 2*right_moves + header,
                                 state.head - header, *new)


def halt_witness(state):
    """Stop at the sixth unmatched closing and recover the literal B4 state and clock."""
    available = []
    unmatched = []
    distance = 0
    for pos, q in enumerate(state.digits(), 1):
        if q == OPEN:
            available.append(pos)
        elif q == CLOSE:
            partner = available.pop() if available else 0
            distance += pos - partner
            if not partner:
                unmatched.append(pos)
                if len(unmatched) == 6:
                    elapsed = 2*distance + 18
                    return {'unmatched_closings': unmatched, 'trigger_cell': pos,
                            'trigger_coordinate': state.head + pos, 'pair_distance': distance,
                            'sweep_steps': elapsed, 'steps': state.steps + elapsed,
                            'state': 'B', 'read': 4, 'head': state.head - 2,
                            'final_tape': {'left': state.head - 3, 'guard_digits': '3433',
                                           'following_threes': pos, 'untouched_input_from_cell': pos + 1}}
    raise ValueError('this sweep has fewer than six unmatched closings')


class Births:
    """Right indices are permanent. Each width increase records a two- or five-cell packet."""

    def __init__(self, state):
        self.start = state.number
        self.widths = [state.width]
        self.letters = bytearray()

    def record(self, letter, new_width):
        self.letters.append(letter)
        self.widths.append(new_width)

    def cell(self, state, position):
        index = state.width - position
        first = bisect_right(self.widths, index)
        result = {'cell': position, 'right_index': index}
        if first == 0:
            result['present_in_starting_word'] = True
        else:
            packet = normalized35(birth_columns(self.letters[first - 1]))
            result['birth_epoch'] = self.start + first
            result['birth_digit'] = packet[index - self.widths[first - 1]]
        return result


def explain(state, reading, births):
    word = state.digits()
    stack = []
    own = []
    for pos, q in enumerate(word[:reading.cut], 1):
        if q == OPEN:
            stack.append(pos)
        elif q == CLOSE:
            if stack:
                stack.pop()
            else:
                own.append(pos)
    # Only these crossings can reach the physical sweep before B4.
    needed = 0 if len(own) >= 6 else min(reading.exterior, len(stack) + 6 - len(own))
    crossings = []
    height = 0
    if needed:
        for pos in range(reading.cut + 1, state.width + 1):
            q = word[pos - 1]
            height += (q == OPEN) - (q == CLOSE)
            if height == -len(crossings) - 1:
                origin = births.cell(state, pos)
                origin['absorbed_by'] = births.cell(state, stack.pop()) if stack else None
                crossings.append(origin)
                if len(crossings) == needed:
                    break
    if len(crossings) != needed or len(own) != reading.internal:
        raise ArithmeticError('literal digit witnesses differ from the cut reading')
    return {**state.location(), 'cut': reading.cut, 'prefix': ''.join(map(str, word[:reading.cut])),
            'prefix_balance': reading.balance, 'prefix_deficit': reading.internal,
            'threshold': reading.threshold, 'exterior_debt': reading.exterior,
            'exterior_margin': reading.margin, 'guard_debt': min(6, reading.guard),
            'unmatched_in_prefix': own[:6], 'crossings': crossings}


def entry83(copies):
    if copies < 0:
        raise ValueError('extra copies must be nonnegative')
    state = blank_epoch()
    while state.number < 83:
        _, _, state = sweep(state)
    word = state.digits()
    block = word[14:24]
    if block != bytes(map(int, '1231111112')):
        raise ArithmeticError('wrong blank epoch 83')
    altered = word[:14] + block * (1 + copies) + word[24:]
    return Epoch.from_word(83, 0, 0, altered), {'kind': 'epoch83-copy-control', 'extra_copies': copies}


def read_checkpoint(path):
    doc = json.loads(path.read_text())
    record = doc['payload']
    fmt = record['format']
    if (doc['sha256'] != checksum(record) or fmt not in (EPOCH_FORMAT, CONTROL_FORMAT)
            or record['machine'] != TERNARY_CLOSE or record['state'] != 'A'
            or record['left'] != record['head'] + 1 or record['steps'] < 0
            or record['epoch'] < (1 if fmt == EPOCH_FORMAT else 0)):
        raise ValueError('invalid line 35 epoch checkpoint')
    word = zlib.decompress(base64.b64decode(record['tape_zlib_base64'], validate=True))
    if len(word) != record['cells']:
        raise ValueError('checkpoint width differs from its tape')
    state = Epoch.from_word(record['epoch'], record['steps'], record['head'], word)
    origin = record['origin'] if fmt == CONTROL_FORMAT else {'kind': 'checkpoint'}
    if fmt == CONTROL_FORMAT and origin['kind'] in ('blank', 'checkpoint'):
        raise ValueError('an experimental checkpoint must identify its altered starting word')
    return state, origin, doc['sha256']


def save_checkpoint(path, state, origin):
    control = origin['kind'] not in ('blank', 'checkpoint')
    record = {'format': CONTROL_FORMAT if control else EPOCH_FORMAT, 'machine': TERNARY_CLOSE,
              **state.location(), 'state': 'A', 'left': state.head + 1,
              'tape_zlib_base64': base64.b64encode(zlib.compress(state.digits(), 9)).decode()}
    if control:
        record['origin'] = origin
    digest = checksum(record)
    atomic_json(path, {'payload': record, 'sha256': digest})
    return digest


def run(start, count, origin, source_digest=None):
    if count < 1:
        raise ValueError('at least one sweep is needed')
    state = start
    births = Births(start)
    guards = Counter()
    exterior = Counter()
    closest = strongest = None
    full = high = 0
    first_above_six = previous_high = smallest_gap = None
    report = {'machine': TERNARY_CLOSE, 'origin': origin, 'start': start.location()}
    if source_digest:
        report['starting_checkpoint_sha256'] = source_digest
    for _ in range(count):
        reading, letter, successor = sweep(state)
        guards[min(6, reading.guard)] += 1
        exterior[reading.exterior] += 1
        at_cut = reading.cut == CUT
        if at_cut:
            full += 1
            if reading.exterior > 6 and first_above_six is None:
                first_above_six = (state.number, reading.exterior)
            if reading.exterior > 2:
                high += 1
                if previous_high is not None:
                    item = (state.number - previous_high - 1, previous_high, state.number)
                    if smallest_gap is None or item < smallest_gap:
                        smallest_gap = item
                previous_high = state.number
        # The smaller a positive margin, the fewer exterior units still needed.
        near_key = (not at_cut, reading.margin, -reading.exterior)
        peak_key = (at_cut, reading.exterior, -reading.margin)
        if closest is None or near_key < closest[0]:
            closest = (near_key, state, reading)
        if strongest is None or peak_key > strongest[0]:
            strongest = (peak_key, state, reading)
        if successor is None:
            halt = halt_witness(state)
            halt.update(from_epoch=state.number, cut_witness=explain(state, reading, births),
                        unmatched_origins=[births.cell(state, pos) for pos in halt['unmatched_closings']])
            report['halt'] = halt
            break
        births.record(letter, successor.width)
        state = successor
    report.update(attempted_sweeps=sum(guards.values()), successful_sweeps=state.number - start.number,
                  last_boundary=state.location(), guard_histogram=dict(sorted(guards.items())),
                  exterior_histogram=dict(sorted(exterior.items())),
                  closest=explain(closest[1], closest[2], births),
                  strongest=explain(strongest[1], strongest[2], births))
    report['pulse_window'] = {'cut_28_sweeps': full, 'readings_above_two': high,
                              'first_above_six_epoch_and_debt': first_above_six,
                              'shortest_gap_and_its_epochs': smallest_gap}
    return state, report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--checkpoint', type=Path)
    group.add_argument('--word', help='normalized experimental word, A on the blank immediately before it')
    group.add_argument('--epoch83-copies', type=int, metavar='EXTRA', help='insert extra copies into blank epoch 83')
    parser.add_argument('--sweeps', type=int, default=1)
    parser.add_argument('--save', type=Path, help='save the last reached normalized boundary for replay')
    parser.add_argument('--report', type=Path, help='also save the JSON result and cell witnesses')
    args = parser.parse_args()
    if args.report and args.save and args.report.resolve() == args.save.resolve():
        parser.error('the report and checkpoint need separate output paths')
    digest = None
    try:
        if args.checkpoint:
            start, origin, digest = read_checkpoint(args.checkpoint)
        elif args.word is not None:
            start = Epoch.from_word(0, 0, 0, tuple(map(int, args.word)))
            origin = {'kind': 'supplied-word', 'sha256': hashlib.sha256(start.digits()).hexdigest()}
        elif args.epoch83_copies is not None:
            start, origin = entry83(args.epoch83_copies)
        else:
            start, origin = blank_epoch(), {'kind': 'blank'}
        state, report = run(start, args.sweeps, origin, digest)
        if args.save:
            report['saved_boundary_sha256'] = save_checkpoint(args.save, state, origin)
        if args.report:
            atomic_json(args.report, report)
    except (ValueError, KeyError, OSError, zlib.error) as exc:
        parser.error(str(exc))
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
