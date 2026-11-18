"""Replay ordinary left extensions of BB(2,5) line 33. Python 3.10+."""
import argparse
import base64
from collections import deque
from itertools import product
import json
from pathlib import Path
import sys
import zlib

MACHINE = '1RB2LA0RB4LB1RA_1LA3RA1RA---0LA'
SOURCE = Path(__file__).resolve().parents[1] / 'BB2x5_Rocq_holdouts_37.txt'
CYCLE = ('21', '14', '24')
COST = (4, 1, 5)


class ExceptionalReturn(Exception):
    """The ordinary recurrence demanded F(2) at a virgin right edge."""


class Batch:
    """A queue containing literal digits and pending counts of A requests."""

    def __init__(self, word, count):
        self.queue = deque(word)
        self.cost = 0
        self.schedule(count)

    def schedule(self, count):
        if count:
            if self.queue and isinstance(self.queue[0], int):
                count += self.queue.popleft()
            self.queue.appendleft(count)

    def digit(self):
        while self.queue:
            count = self.queue.popleft()
            if isinstance(count, str):
                return count
            first = self.digit()
            if not first:
                self.cost += 3
                self.queue.extendleft(reversed('21'))
                self.schedule(count - 1)
            elif first == '4':
                self.cost += 2
                self.schedule(1)
                self.queue.appendleft('2')
                self.schedule(count - 1)
            elif first == '1':
                self.cost += 1
                self.queue.appendleft('2')
                self.schedule(count - 1)
            else:
                assert first == '2'
                second = self.digit()
                if not second:
                    raise ExceptionalReturn
                if second == '2':
                    self.cost += 7 * count
                    self.schedule(2 * count)
                    self.queue.extendleft('22')
                else:
                    phase = CYCLE.index('2' + second)
                    cycles, remainder = divmod(count, 3)
                    self.cost += 10 * cycles
                    children = cycles
                    for offset in range(remainder):
                        event = (phase + offset) % 3
                        self.cost += COST[event]
                        children += event == 0
                    self.schedule(children)
                    final = CYCLE[(phase + remainder) % 3]
                    self.queue.extendleft(reversed(final))
        return ''


def batch(word, count):
    pending = Batch(word, count)
    result = ''.join(iter(pending.digit, ''))
    return result, pending.cost


# Independent physical interpreter. Positions absent from the map are blank.
def literal_step(tape, head, state):
    row = MACHINE.split('_')[state == 'B']
    i = 3 * tape.get(head, 0)
    entry = row[i:i + 3]
    if entry == '---':
        raise ValueError('literal halt')
    if entry[0] == '0':
        tape.pop(head, None)
    else:
        tape[head] = int(entry[0])
    return head + (1 if entry[1] == 'R' else -1), entry[2]


def full_request(word):
    """Scalar return including the exceptional replies. Intended for small words."""
    if not word:
        return 'A', '21', 3
    if word == '2':
        return 'B', '421421', 19
    if word.startswith('1'):
        return 'A', '2' + word[1:], 1
    if word.startswith('24'):
        return 'A', '21' + word[2:], 5
    prefix = '4' if word.startswith('4') else word[:2]
    initial = 1 if prefix == '4' else 2
    state, output, cost = full_request(word[len(prefix):])
    if state == 'H':
        return 'H', '', initial + cost
    if state == 'B':
        k = len(output) // 3
        assert output == '421' * k and k >= 2
        if prefix == '21':
            return 'H', '', cost + 2
        if prefix == '4':
            return 'B', '421' + output, cost + 6 * k + 6
        assert prefix == '22'
        return 'A', '1421' + output, cost + 6 * k + 8
    if prefix == '4':
        return 'A', '2' + output, cost + 2
    if prefix == '21':
        return 'A', '14' + output, cost + 4
    assert prefix == '22'
    state, output, second = full_request(output)
    if state == 'H':
        return 'H', '', cost + second + 5
    if state == 'B':
        k = len(output) // 3
        assert output == '421' * k and k >= 2
        return 'B', '421421' + output, cost + second + 12 * k + 21
    return 'A', '22' + output, cost + second + 7


def concrete(word):
    return {i: int(symbol) for i, symbol in enumerate(word)}


def verify():
    controls = [('2', 19, 'B', '421421'), ('212', 21, 'halt', None)]
    for word, count, result, final in controls:
        tape, head, state = concrete(word), 0, 'A'
        for _ in range(count):
            assert head >= 0
            head, state = literal_step(tape, head, state)
        if result == 'halt':
            assert head == 1 and state == 'B' and tape[head] == 3
        else:
            assert (head, state, tape) == (-1, result, concrete(final))
    outcomes = {'A': 0, 'B': 0, 'H': 0}
    for width in range(7):
        for letters in product('124', repeat=width):
            word = ''.join(letters)
            result, output, count = full_request(word)
            tape, head, state = concrete(word), 0, 'A'
            for _ in range(count):
                assert head >= 0
                head, state = literal_step(tape, head, state)
            if result == 'H':
                assert state == 'B' and tape[head] == 3
            else:
                assert (head, state, tape) == (-1, result, concrete(output))
            outcomes[result] += 1
    for k in range(2, 33):
        tape = concrete('421' * k)
        head, state = -1, 'B'
        for _ in range(12 * k + 18):
            head, state = literal_step(tape, head, state)
        expected = {i - 2: a for i, a in concrete('421' * (k + 2)).items()}
        assert (head, state, tape) == (-3, 'B', expected)
    print(f'full scalar returns {outcomes}; 31 whole bouncer periods')
    checks = exceptions = 0
    for width in range(6):
        for letters in product('124', repeat=width):
            word = ''.join(letters)
            tape = concrete(word)
            time = 0
            for requests in range(1, 7):
                try:
                    result, cost = batch(word, requests)
                except ExceptionalReturn:
                    exceptions += 1
                    break
                head, state = 0, 'A'
                while head >= 0:
                    head, state = literal_step(tape, head, state)
                    time += 1
                    assert time <= cost
                assert (head, state, time, tape) == (-1, 'A', cost, concrete(result))
                checks += 1
    tape, head, state, elapsed = {}, 0, 'A', 0
    y, clock = '1', 3
    for epoch in range(1, 11):
        while elapsed < clock:
            head, state = literal_step(tape, head, state)
            elapsed += 1
        expected = {i - epoch + 1: int(symbol) for i, symbol in enumerate('2' + y)}
        assert (head, state, tape) == (-epoch, 'A', expected)
        y, cost = batch(y, 1)
        y = '2' + y
        clock += cost + 4
    # Directly compare two explicit obstructing suffixes under free calls.
    stage_three = '2221421'
    reordered = stage_three
    for action in 'PPFFPFP':
        reordered = '2' + reordered if action == 'P' else batch(reordered, 1)[0]
    assert reordered == '2222222222221242421'
    for w, n in [('42421', 2), ('42142421421', 5), (reordered, 1)]:
        batch(w, n - 1)
        try:
            batch(w, n)
        except ExceptionalReturn:
            continue
        raise AssertionError('expected exceptional demand')
    print(f'{checks} full request comparisons, {exceptions} inputs stopped at an exceptional demand')
    print('10 full blank checkpoints through step 272898; two literal exceptional controls')


def split_reserve(word):
    end = len(word)
    while end >= 3 and word[end - 3:end] == '421':
        end -= 3
    return word[:end], (len(word) - end) // 3


def compare_reserve(epoch, word, result, cost):
    prefix, count = split_reserve(word)
    for needed in range(count + 1):
        cut = prefix + '421' * needed
        try:
            trimmed, base_cost = batch(cut, 1)
        except ExceptionalReturn:
            continue
        rest = count - needed
        assert result == trimmed + '421' * rest
        assert cost == base_cost + 3 * rest * (len(trimmed) - len(cut))
        gain = split_reserve('2' + trimmed)[1]
        print(f'{epoch} {count} {needed} {gain} {rest + gain}')
        return
    raise AssertionError('full word was already checked')


def checkpoint(epoch, y, steps):
    return {
        'line': 33, 'machine': MACHINE, 'left_extension': epoch,
        'state': 'A', 'head': -epoch, 'steps': str(steps),
        'word_start': 1 - epoch, 'word_length': len(y) + 1,
        'word_zlib_base64': base64.b64encode(zlib.compress(('2' + y).encode(), 9)).decode(),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--reserve', action='store_true', help='check terminal 421 counts per epoch')
    parser.add_argument('--epoch', type=int)
    parser.add_argument('--save', type=Path)
    parser.add_argument('--check', type=Path)
    args = parser.parse_args()
    assert SOURCE.read_text().splitlines()[32] == MACHINE
    if hasattr(sys, 'set_int_max_str_digits'):
        sys.set_int_max_str_digits(0)
    if args.verify:
        verify()
    if args.epoch is None:
        if args.save or args.check:
            parser.error('supply --epoch for a saved checkpoint')
        return
    if args.epoch < 1:
        parser.error('epochs start at 1')
    y, steps = '1', 3
    if args.reserve:
        print('epoch reserve required produced next')
    for epoch in range(1, args.epoch):
        try:
            result, cost = batch(y, 1)
        except ExceptionalReturn:
            raise SystemExit(f'epoch {epoch} requires the exceptional physical branch')
        if args.reserve:
            compare_reserve(epoch, y, result, cost)
        steps += 4 + cost
        y = '2' + result
    end = checkpoint(args.epoch, y, steps)
    if args.save:
        args.save.write_text(json.dumps(end, indent=2) + '\n')
    if args.check:
        previous = json.loads(args.check.read_text())
        packed = previous.pop('word_zlib_base64')
        actual = end.copy()
        del actual['word_zlib_base64']
        assert actual == previous
        assert zlib.decompress(base64.b64decode(packed)).decode() == '2' + y
    digits = str(steps)
    print(f'epoch {args.epoch}, head {-args.epoch}, width {len(y)+1}, '
          f'raw clock {digits[:8]}... ({len(digits)} digits)')


if __name__ == '__main__':
    main()
