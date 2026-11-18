"""Which ordinary predecessor factors could yield five positive groups on line 34?"""
from functools import cache
from itertools import accumulate, groupby, product

from cut100 import SEED, first_digits
from line34_left import digits
from target34_orbit import TERNARY, TapeMachine, analyze, encode


def derivative(bits):
    return ''.join('1' if a == b else '3' if b else '2'
                   for a, b in zip(bits, bits[1:]))


def decode(word):
    first_turn = next((v for v in word if v != '1'), None)
    if first_turn is None:
        return None
    bit = int(first_turn == '2')
    bits = [bit]
    for digit in word:
        if digit != '1':
            if bit != (digit == '2'):
                return ()
            bit = 1 - bit
        bits.append(bit)
    return tuple(bits)


@cache
def gaps(length, start):
    """All ordinary fillings with zero surviving or externally matched openings."""
    found = []

    def extend(word, bit, balance):
        remaining = length - len(word)
        if remaining == 0:
            if balance == 0:
                found.append((word, bit))
            return
        if balance < remaining - 1:
            extend(word + '1', bit, balance + 1)
        if bit == 1:
            extend(word + '2', 0, balance)
        elif balance > 0:
            extend(word + '3', 1, balance - 1)

    extend('', start, 0)
    return tuple(found)


@cache
def parents(word):
    """Retain only the older factor between forced surviving openings, inclusive."""
    bits = decode(word)
    if bits == ():
        return frozenset()
    if bits is None or bits.count(1) < 2:
        return frozenset({''})  # No useful forced interior in this direction.
    ones = [i for i, bit in enumerate(bits) if bit]
    choices = {('1', 0), ('1', 1)}
    for left, right in zip(ones, ones[1:]):
        choices = {(prefix + gap + '1', end) for prefix, bit in choices
                   for gap, end in gaps(right - left - 1, bit)}
    return frozenset(prefix for prefix, _ in choices)


def literal_survivors(word, exterior):
    unmatched = []
    for i, digit in enumerate(word):
        if digit == '1':
            unmatched.append(i)
        elif digit == '3' and unmatched:
            unmatched.pop()
    if exterior:
        unmatched = unmatched[:max(0, len(unmatched) - exterior)]
    marked = set(unmatched)
    return tuple(int(i in marked) for i in range(len(word)))


def audit():
    comparisons = 0
    for width in range(2, 11):
        ordinary = {derivative(source) for source in product((0, 1), repeat=width+1)}
        for old in ordinary:
            for exterior in (0, 1, 3):
                s = literal_survivors(old, exterior)
                new = derivative(s)
                preceding = parents(new)
                if '' not in preceding:
                    first = s.index(1)
                    last = len(s) - 1 - s[::-1].index(1)
                    assert old[first:last+1] in preceding
                comparisons += 1
    print('Actual older factors retained in forward matching controls:', comparisons)


def certificate():
    word = '12113' * 5
    level = {word}
    for depth, expected in enumerate((33, 2, 0), 1):
        level = {old for current in level for old in parents(current)}
        assert len(level) == expected
        print(f'Depth {depth}: {len(level)} candidate interiors')
        if depth == 2:
            for current in sorted(level):
                runs = [(v, len(tuple(g))) for v, g in groupby(decode(current))]
                lengths = [n for v,n in runs[1:-1] if v == 0]
                assert lengths == [5, 5]
                print(' ', current, 'complete zero gaps', lengths)


PERIOD = '21111323111'


def periodic_control():
    word = PERIOD
    history = [word]
    for _ in range(8):
        heights = list(accumulate((int(d == '1') - int(d == '3') for d in word), initial=0))
        assert heights[-1] > 0
        cut = heights.index(min(heights))
        rotated = word[cut:] + word[:cut]
        matched = literal_survivors(rotated, 0)
        s = matched[-cut:] + matched[:-cut] if cut else matched
        word = derivative(s[-1:] + s)
        history.append(word)
    assert word == '13232131232' and word.count('3') - word.count('1') == 1
    print('Eight periodic ordinary sweeps:', ' -> '.join(history))


def finite_control(copies):
    """Extend the true seed on its right, then replay each instruction on the altered tape."""
    word = first_digits(SEED['width']) + tuple(map(int, PERIOD)) * copies
    head = SEED['head']
    raw = TapeMachine(TERNARY, word, head=head, left=head+1)
    config = encode(word)
    signals = []
    for t in range(9):
        result, guard, (debt,), _ = analyze(config, (100,))
        signals.append((guard, debt))
        if result is None:
            assert copies == 882 and t == 8
            for _ in range(12_000_000):
                if not raw.step():
                    break
            else:
                raise AssertionError('literal halt budget exhausted')
            assert (raw.state, raw.head, raw.tape[raw.head], raw.steps) == ('B', -1310, 4, 10293928)
            break
        config, shift, ticks = result
        head -= shift
        clock = raw.steps
        for _ in range(ticks):
            assert raw.step()
        assert (raw.state, raw.head, raw.steps) == ('A', head, clock+ticks)
        full = digits(config[1:], config[0])
        assert raw.tape == {head+1+j: d for j,d in enumerate(full)}
    assert signals[:8] == [(0,0), (1,0), (1,0), (1,0), (1,1), (1,0), (1,0), (1,0)]
    assert signals[-1] == ({0:(1,0), 881:(5,61), 882:(6,62)}[copies])
    print(f'Copies {copies}: ninth input (guard, cut-100 debt) {signals[-1]}, '
          f'ending state {raw.state}, head {raw.head}, elapsed defined instructions {raw.steps}')


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('enable assertions')
    audit()
    certificate()
    periodic_control()
    for number in (0, 881, 882):
        finite_control(number)
