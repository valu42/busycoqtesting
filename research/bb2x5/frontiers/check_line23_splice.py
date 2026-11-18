#!/usr/bin/env python3
"""Check the three-cell guard transfer and a halting splice of two blank-orbit tapes."""
import sys

from checkpoints import ROOT
from line19_pair import MACHINES, strip_trace, verify_tables

sys.path.insert(0, str(ROOT))
from prior_sweeps import TapeMachine


def check_transfer():
    # All replies at the right edge are supplied explicitly. Every row exits
    # on the left, and the recorded request word exhausts its oracle input.
    rows = (
        ('022', 'B', '',  '222', 'A', '', 1),
        ('320', 'B', '',  '222', 'A', '', 5),
        ('222', 'B', 'A', '202', 'B', 'B', 6),
        ('222', 'B', 'B', '020', 'A', 'B', 6),
        ('020', 'A', '',  '232', 'B', '', 7),
    )
    for word, entry, exterior, final, reply, calls, cost in rows:
        if strip_trace(word, entry, 0, exterior) != (final, -1, reply, calls, cost):
            raise AssertionError(f'three-cell transfer changed on {word}/{entry}')


def snapshots(times):
    tm = TapeMachine(MACHINES[19])
    tm.state = 'B'
    found = []
    last_move = 0
    for t in range(max(times)+1):
        if t in times:
            centered = {pos-tm.head: digit for pos, digit in tm.tape.items()}
            found.append((t, tm.head, tm.state, last_move, centered))
        old = tm.head
        if not tm.step():
            raise AssertionError('early halt while replaying genuine blank configurations')
        last_move = tm.head-old
    return {row[0]: row[1:] for row in found}


def overlap(a, b, start, delta):
    different = [abs(pos-start) for pos in a.keys() | b.keys()
                 if (pos-start)*delta >= 0 and a.get(pos, 0) != b.get(pos, 0)]
    return min(different) if different else None


def replay_splice(left_time, right_time, through, launch):
    source = snapshots((left_time, right_time))
    left_pos, state, move, left = source[left_time]
    right_pos, right_state, right_move, right = source[right_time]
    if (state, move) != (right_state, right_move):
        raise AssertionError('incompatible control at the join')
    match = overlap(left, right, -1, -1), overlap(left, right, 0, 1)
    tm = TapeMachine(MACHINES[19])
    tm.state = state
    tm.tape = ({i: c for i, c in left.items() if i < 0}
               | {i: c for i, c in right.items() if i >= 0})
    guard_pos = None
    initial = None
    replies = []
    for t in range(through+1):
        x = tm.head
        if t == launch:
            if tm.state != 'A' or tm.tape.get(x, 0) or tm.tape.get(x+1, 0) != 3:
                raise AssertionError('missing physical guard launch')
            guard_pos = x+1
            initial = ''.join(str(tm.tape.get(i, 0)) for i in range(x+2, x+6))
        if x == guard_pos and move == -1 and len(replies) < 3:
            prefix = ''.join(str(tm.tape.get(i, 0)) for i in range(x+1, x+4))
            replies.append((t, tm.state, prefix))
        if t == through:
            break
        if not tm.step():
            raise AssertionError('unexpected early halt in splice')
        move = tm.head-x
    end = tm.head, tm.state, tm.tape.get(tm.head, 0)
    return (left_pos, right_pos), match, (guard_pos, initial, tuple(replies)), end


def main():
    verify_tables()
    check_transfer()
    if replay_splice(365, 645, 308, 127) != (
            (-1, 7), (4, 4), (-6, '3023', ((302, 'A', '023'), (304, 'A', '223'),
                                           (306, 'A', '323'))), (-6, 'A', 3)):
        raise AssertionError('halting splice witness changed')
    if replay_splice(10055, 107420, 1751, 1286) != (
            (-9, 136), (10, 10), (-15, '3233', ((1733, 'A', '220'), (1739, 'A', '022'),
                                               (1751, 'B', '230'))), (-15, 'B', 2)):
        raise AssertionError('twenty-cell splice witness changed')
    print('022 and 320 both give 020 after two A replies; its A call returns B in seven steps.')
    print('Splice of 365 and 645: eight shared cells, AAA, undefined A3 at -6 after 308 steps.')
    print('Splice of 10055 and 107420: twenty shared cells, launch 3233, third A input 022.')


if __name__ == '__main__':
    main()
