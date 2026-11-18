#!/usr/bin/env python3
"""Check the line-18 root-return barrier and the safe binary-tail transfers."""
import argparse
from itertools import product
from pathlib import Path

from checkpoints import ROOT
from line18 import MACHINE, RULES, load
from prior_sweeps import TapeMachine


def explore_guard(word):
    """Accept A then any number of B entries. The exterior may reply A or B."""
    todo = [(word, 0, 'A')]
    seen = set()
    returns, halts = set(), set()
    while todo:
        node = todo.pop()
        if node in seen:
            continue
        seen.add(node)
        cells, pos, state = node
        if pos < 0:
            returns.add(state)
            if state == 'B':
                if cells[0] != '3':
                    raise AssertionError('a B exit must have used A2')
                todo.append((cells, 0, 'B'))
        elif pos == len(word):
            todo.extend((cells, pos-1, reply) for reply in 'AB')
        else:
            rule = RULES.get((state, int(cells[pos])))
            if rule is None:
                halts.add(pos)
            else:
                write, move, control = rule
                tape = cells[:pos] + str(write) + cells[pos+1:]
                todo.append((tape, pos+move, control))
    return returns, halts, len(seen)


def tile(cells, entry, child_reply='B'):
    """First left exit of one tile, given the indicated reply to each child."""
    word = list(map(int, cells))
    pos, steps, state = 0, 0, entry
    calls = ''
    while pos >= 0:
        if pos == len(word):
            calls += state
            pos, state = pos-1, child_reply
        if steps >= 30:
            raise AssertionError('tile failed to exit')
        word[pos], move, state = RULES[state, word[pos]]
        pos += move
        steps += 1
    return ''.join(map(str, word)), state, calls, steps


def literal(word, calls):
    tm = TapeMachine(MACHINE, map(int, word))
    replies = ''
    for state in calls:
        tm.head, tm.state = 0, state
        while tm.head >= 0:
            if not tm.step():
                return replies, 'halt', tm
            if tm.steps > 100_000:
                raise AssertionError('literal test exceeded its budget')
        replies += tm.state
    return replies, 'done', tm


def check_rules():
    risky = {'1314', '1334'} | {'134'+c for c in '01234'}
    total = 0
    for c, d in product('01234', repeat=2):
        word = '13'+c+d
        returns, halts, states = explore_guard(word)
        if 'A' in returns or bool(halts) != (word in risky):
            raise AssertionError(f'unexpected guard outcome for {word}')
        total += states

    # Inside each row the conditional child replies are all B. Together these
    # rows generate the transfers for an arbitrary number of following calls.
    rows = {
        ('13', 'A'): ('34', 'B', '', 3),
        ('34', 'B'): ('32', 'B', 'A', 4),
        ('32', 'B'): ('31', 'B', '', 3),
        ('31', 'B'): ('32', 'B', 'B', 4),
        ('133', 'A'): ('343', 'B', '', 3),
        ('343', 'B'): ('313', 'B', 'A', 10),
        ('313', 'B'): ('313', 'B', 'BB', 11),
    }
    for (word, entry), result in rows.items():
        if tile(word, entry) != result:
            raise AssertionError(f'incorrect tile row {word} {entry}')

    # Leading A at a binary pair, or virgin-pair recursions. The first
    # three fields specify the local input and the reply oracle.
    reset_rows = {
        ('31', 'A', 'A'): ('41', 'A', '', 1),
        ('41', 'B', 'A'): ('23', 'A', 'A', 4),
        ('32', 'A', 'A'): ('42', 'A', '', 1),
        ('42', 'B', 'A'): ('23', 'A', '', 3),
        ('23', 'B', 'A'): ('13', 'A', '', 1),
        ('13', 'B', 'A'): ('23', 'A', 'B', 4),
        ('13', 'B', 'B'): ('13', 'A', 'BB', 9),
        ('00', 'A', 'A'): ('13', 'A', '', 5),
        ('00', 'B', 'A'): ('20', 'A', '', 1),
        ('20', 'B', 'A'): ('10', 'A', '', 1),
        ('10', 'B', 'A'): ('13', 'A', 'A', 8),
    }
    for args, result in reset_rows.items():
        if tile(*args) != result:
            raise AssertionError(f'incorrect binary reset row {args}')
    replies, status, tm = literal('3', 'AB')
    if (replies, status, tm.tape) != (
            'AA', 'done', {i: int(c) for i, c in enumerate('1332')}):
        raise AssertionError('terminal-3 reset base mismatch')

    # At a binary overflow the last pair sees a real virgin suffix, or the
    # terminal singleton 3 followed by blanks. Check these physical bases.
    for word, expected, steps in [('31', '31313', 15), ('3', '32', 3)]:
        replies, status, tm = literal(word, 'B')
        if (replies, status, tm.steps, tm.tape) != (
                'B', 'done', steps, {i: int(c) for i, c in enumerate(expected)}):
            raise AssertionError(f'wrong binary overflow base {word}')
    replies, status, tm = literal('134', 'AB')
    if (replies, status, tm.state, tm.tape.get(tm.head)) != ('B', 'halt', 'A', 4):
        raise AssertionError('the physical A4 control changed')
    # This clean six-cell pattern constructs its own A4. No move exits the
    # right edge, so the witness is independent of all farther cells.
    word = '133313'
    tm = TapeMachine(MACHINE, map(int, word))
    for index, entry in enumerate('ABB'):
        tm.head, tm.state = 0, entry
        while 0 <= tm.head < len(word) and tm.step():
            if tm.steps > 31:
                raise AssertionError('clean halt trace exceeded its known clock')
        if tm.head >= len(word) or (index < 2 and (tm.head, tm.state) != (-1, 'B')):
            raise AssertionError('clean halt trace left its interface')
    if (tm.steps, tm.head, tm.state, tm.tape.get(tm.head)) != (31, 5, 'A', 4):
        raise AssertionError('clean A4 witness changed')
    return total


def protected_record(word, count):
    """Last safe four-cell guard after a sequence of whole tiles, or None.

    Return the end of the protected old strip (exclusive) and the guaranteed
    prefix after a completed record, already shifted to the next cut.
    """
    pos = 0
    tiles = []
    guard = None
    while word[pos:pos+2] == '13':
        if count == 0:
            # The incoming word now consists solely of A. This call consumes
            # no exterior reply and preserves all following input symbols.
            output = ''.join(tiles) + '34' + word[pos+2:]
            return len(word), output[1:]
        if len(word) >= pos+4 and set(word[pos+2:pos+4]) <= set('123'):
            # The closing guard contributes a known 3 on its final B exit.
            guard = pos+4, len(tiles)
        if word[pos+2:pos+3] == '3':
            tiles.append('313')
            pos += 3
            count = 2*(count-1)
        else:
            tiles.append('32' if count % 2 else '31')
            pos += 2
            count = (count-1)//2
    if guard is None:
        return None
    end, before = guard
    output = ''.join(tiles[:before]) + '3'
    return end, output[1:]


def horizon(k, prefix):
    """Strip guarantees until too little prefix is determined for another guard."""
    certificates = []
    while len(prefix) >= 2:
        answer = protected_record(prefix, 1 << (k-1))
        if answer is None:
            break
        end, prefix = answer
        certificates.append((k, end, len(prefix)))
        k += 1
    return certificates


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('checkpoint', nargs='?', type=Path,
                        default=ROOT/'frontiers/runs/line18-returns.json')
    args = parser.parse_args()
    total = check_rules()
    state = load(args.checkpoint)
    k = state['record']
    word = state['suffix']
    first = protected_record(word, 1 << (k-1))
    if first is None:
        parser.exit(1, 'No protected prefix found at this record.\n')
    width = first[0]
    rows = horizon(k, word[:width])
    print(f'All 25 four-cell guards exclude a root A ({total} states summed across starts).')
    print(f'Using {width} suffix cells: records {k} through {rows[-1][0]}, '
          f'{len(rows)} guarded attempts.')
    for index in sorted({0, len(rows)-1}):
        record, end, next_width = rows[index]
        print(f'Record {record}: local halt excluded left of {record+3+end}; '
              f'{next_width} suffix cells fixed at next cut on completion.')


if __name__ == '__main__':
    main()
