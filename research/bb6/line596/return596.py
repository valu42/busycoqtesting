"""BB(6) line 596. Exact return from P(n, suffix) to its next P boundary or halt."""
import argparse
from functools import lru_cache

CODE = '1RB1LF_1LC0RD_---1LA_0LA0RE_1LA1RA_1LB0LD'


def parse(code):
    return tuple(None if cell == '---' else
                 (int(cell[0]), 1 if cell[1] == 'R' else -1, ord(cell[2]) - ord('A'))
                 for row in code.split('_') for cell in (row[:3], row[3:]))


TARGET = parse(CODE)
# On a D0 move, record whether the immediately preceding cell contained a one.
# G0 carries out the normal A0 instruction. G1 reports a failed comparison.
GUARDED = parse(CODE.replace('0LA0RE', '0LG0RE') + '_1RB---')


def cells(word, offset=0):
    return {i + offset for i, bit in enumerate(word) if bit == '1'}


def word_from(ones, start):
    return ''.join('1' if i in ones else '0'
                   for i in range(start, max(ones, default=start - 1) + 1))


def leading(word):
    suffix = word.lstrip('1')
    return len(word) - len(suffix), suffix


def literal_small(table, blocks, suffix):
    """Fallback when every repeated block was opened by the interface."""
    ones = cells('110110' + '1110' * blocks + suffix)
    head, state = -1, 0
    for steps in range(200000):
        transition = table[2 * state + (head in ones)]
        if transition is None:
            return 'halt', 0, '', steps
        bit, direction, state = transition
        (ones.add if bit else ones.discard)(head)
        head += direction
        if state in (0, 3) and head < min(ones, default=head):
            word = word_from(ones, head + 1)
            if state == 0 and word.startswith('110110'):
                return 'L', 0, word[6:], steps + 1
            if state == 3 and word.startswith('011101'):
                n, tail = leading(word[6:])
                return 'P', n, tail, steps + 1
    raise RuntimeError('literal fallback exceeded its step budget')


@lru_cache(maxsize=100000)
def interface(table, suffix, available):
    """Execute on the right word, opening pristine 0011 blocks only on demand."""
    ones = cells(suffix)
    wall, head, state, opened = 0, 0, 1, 0
    for steps in range(16000):
        if head < wall:
            assert head == wall - 1
            if state in (0, 2):
                return 'L' if state == 0 else 'P', opened, word_from(ones, wall), steps
            if opened == available:
                return 'more', opened, '', steps
            wall -= 4
            ones.update((wall + 2, wall + 3))
            opened += 1
        transition = table[2 * state + (head in ones)]
        if transition is None:
            return 'halt', opened, '', steps
        bit, direction, state = transition
        (ones.add if bit else ones.discard)(head)
        head += direction
    raise RuntimeError('right interface exceeded its step budget')


def next_boundary(n, suffix, table=TARGET, clock=True, affine=False):
    """Return (kind, n, suffix, cost). With clock=False the cost is omitted.

    For an affine certificate n=300+r. A successful row must also apply to
    n+3h for every h>=0. Opening the finite left marker would invalidate this
    argument, so affine=True reports that case as an unverified row.
    """
    blocks, ones, time = 0, n + 4, 60
    for _ in range(500):
        repeats = (ones - 1) // 3 if ones else 0
        if clock:
            time += repeats * (35 + 10 * blocks) + 5 * repeats * (repeats - 1)
        blocks += repeats
        right = '1' * (ones - 3 * repeats) + suffix
        while right.startswith('1110'):
            blocks += 1
            right = right[4:]
        capacity = 12
        while True:
            kind, opened, tail, steps = interface(table, right, min(capacity, blocks))
            if kind != 'more' or blocks <= capacity:
                break
            capacity *= 2
        if kind == 'more':
            if affine:
                raise ValueError('the right interface reached the left marker')
            kind, blocks, right, steps = literal_small(table, blocks, right)
            if clock:
                time += steps
            if kind != 'L':
                return kind, blocks, right, time if clock else None
            ones, suffix = leading(right)
            continue
        if clock:
            time += 9 + 4 * blocks + steps
        if kind == 'halt':
            return kind, 0, '', time if clock else None
        blocks -= opened
        if clock:
            time += 17 + (6 if kind == 'L' else 4) * blocks
        head_run, suffix = leading(tail)
        if kind == 'P':
            return kind, 4 * blocks + 1 + head_run, suffix, time if clock else None
        ones = 1 + head_run
    raise RuntimeError('exceeded the number of right-interface visits in one return')


def rules_file(count, path):
    """Enumerate verified affine rows in deterministic breadth-first order."""
    words, indices = [''], {'': 0}
    with open(path, 'w') as out:
        for index, word in enumerate(words):
            if index == count:
                break
            row = []
            for residue in range(3):
                try:
                    kind, value, dest, _ = next_boundary(300 + residue, word,
                                                        clock=False, affine=True)
                except (ValueError, RuntimeError):
                    row.extend((-2, 0))
                    continue
                if kind == 'halt':
                    row.extend((-1, 0))
                    continue
                # This stronger bound also allows unsigned arithmetic in the fast replay.
                assert value >= 400
                if dest not in indices:
                    indices[dest] = len(words)
                    words.append(dest)
                row.extend((indices[dest], value - 400))
            print(index, word or '.', *row, file=out)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--returns', type=int, default=600)
    parser.add_argument('--guard', action='store_true')
    parser.add_argument('--rules', metavar='FILE')
    parser.add_argument('--states', type=int, default=512)
    args = parser.parse_args()
    if args.rules:
        rules_file(args.states, args.rules)
    else:
        n, x, total = 2, '', 51
        table = GUARDED if args.guard else TARGET
        for index in range(1, args.returns + 1):
            kind, n, x, elapsed = next_boundary(n, x, table)
            total += elapsed
            if kind == 'halt':
                print('Guard reached' if args.guard else 'Machine halted',
                      'during return', index, 'after', total, 'elementary transitions')
                break
        else:
            print('Completed returns', args.returns, '| n bits', n.bit_length(),
                  '| n mod 1000000007', n % 1000000007, '| suffix', x or '(empty)')
            print('Elementary transitions so far have', total.bit_length(), 'binary digits')
