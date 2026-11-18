#!/usr/bin/env python3
"""Check the B-seed launch filter and an auxiliary 3233 tape admitted by it."""
from line19_guard_filter import MACHINE, PREFIXES, TapeMachine, check_closed, collect
from line19_pair import verify_tables

EXPECTED = PREFIXES - {'3000', '3232'}
CONTROL = '03323320202022'


def verify():
    verify_tables()
    sizes = []
    for widths in ((4, 5), (4, 8)):
        heads, sides = collect(widths, 'B')
        check_closed(heads, sides, widths, 'B')
        launches = {r[1:5] for _, q, c, r in heads if (q, c, r[0]) == ('A', '0', '3')}
        if launches != EXPECTED:
            raise ValueError('unexpected B-seed guard classes')
        sizes.append((len(heads), *(len(words) for words in sides)))
    if sizes != [(28492, 148, 80), (189076, 148, 543)]:
        raise ValueError(f'unexpected closure sizes {sizes}')

    # Check every side constraint on this finite auxiliary tape in the stronger
    # 4/8 closure. Its left side and both exterior tails are identically zero.
    right = CONTROL[1:] + '0'*8
    if (('0000', 'A', CONTROL[0], right[:8]) not in heads or
            '0000' not in sides[0] or
            any(right[i:i+8] not in sides[1] for i in range(len(right)-7))):
        raise ValueError('auxiliary launch is outside the closed window language')

    tm = TapeMachine(MACHINE, map(int, CONTROL))
    entries, replies = [], []
    furthest = tm.head
    for _ in range(149):
        old = tm.head
        if not tm.step():
            raise ValueError('auxiliary tape halted early')
        furthest = max(furthest, tm.head)
        if (old, tm.head) == (1, 2):
            entries.append(tm.state)
        elif (old, tm.head) == (2, 1):
            replies.append((tm.steps, tm.state))
    if (entries != list('BBA') or replies != [(49, 'A'), (55, 'A'), (147, 'A')]
            or (tm.head, tm.state, tm.tape.get(tm.head), furthest) != (1, 'A', 3, 15)
            or tm.step()):
        raise ValueError('auxiliary BBA trace did not reach A3')
    return sizes


if __name__ == '__main__':
    print('B-seed head and side word counts:', verify())
    print('Four-cell U prefixes:', ' '.join(sorted(EXPECTED)))
    print('The auxiliary 3233 launch receives AAA and halts in 149 defined steps.')
