#!/usr/bin/env python3
"""Certify local suffix filters for line 19's A:03U guard on both blank seeds."""
from collections import defaultdict, deque
import sys

from checkpoints import ROOT

from line19_pair import MACHINES, verify_tables
sys.path.insert(0, str(ROOT))
from prior_sweeps import TapeMachine, parse

MACHINE = MACHINES[19]
RULES = parse(MACHINE)
LEFT, RIGHT = 3, 5
PREFIXES = frozenset('0202 0222 0230 0233 3000 3020 3022 3023 '
                     '3202 3222 3230 3232 3233 3302 3330 3333'.split())
SAFE = frozenset(('0222', '3000', '3202'))


def collect(widths=(LEFT, RIGHT), seeds='AB'):
    """Saturate finite head windows and side words. Both sides face outwards."""
    left_width, right_width = widths
    heads = set()
    pending = deque()
    side_words = [set(), set()]
    completions = [defaultdict(list), defaultdict(list)]
    waiting = [defaultdict(set), defaultdict(set)]

    def add_head(head):
        if head not in heads:
            heads.add(head)
            pending.append(head)

    def complete(side, word, partial):
        state, scanned, pushed = partial
        add_head((word, state, scanned, pushed) if side == 0
                 else (pushed, state, scanned, word))

    def add_word(side, word):
        if word not in side_words[side]:
            side_words[side].add(word)
            prefix = word[:-1]
            completions[side][prefix].append(word)
            # Older popped windows must also use this newly discovered digit.
            for partial in waiting[side][prefix]:
                complete(side, word, partial)

    for side, width in enumerate(widths):
        add_word(side, '0'*width)
    for state in seeds:
        add_head(('0'*left_width, state, '0', '0'*right_width))
    while pending:
        left, state, scanned, right = pending.popleft()
        rule = RULES.get((state, int(scanned)))
        if rule is None:
            continue
        write, move, new_state = rule
        side = 1 if move > 0 else 0
        popped, opposite = (right, left) if side else (left, right)
        pushed = str(write) + opposite[:-1]
        add_word(1-side, pushed)
        prefix = popped[1:]
        partial = (new_state, popped[0], pushed)
        if partial not in waiting[side][prefix]:
            waiting[side][prefix].add(partial)
            for word in completions[side][prefix]:
                complete(side, word, partial)
    return heads, side_words


def check_closed(heads, side_words, widths=(LEFT, RIGHT), seeds='AB'):
    """Check closure by single-stepping physical tapes with every allowed exterior digit."""
    left_words, right_words = side_words
    left_width, right_width = widths
    if ('0'*left_width not in left_words or '0'*right_width not in right_words or
            any(('0'*left_width, q, '0', '0'*right_width) not in heads for q in seeds)):
        raise ValueError('missing blank seed or background')
    tm = TapeMachine(MACHINE)
    for left, state, scanned, right in heads:
        cells = {i-left_width: int(c) for i, c in enumerate(left[::-1] + scanned + right)}
        rule = tm.rules.get((state, int(scanned)))
        if rule is None:
            continue
        # The newly exposed side word is an old interior word on the popped side.
        # Try all five possibilities for its far digit. The opposite side is pushed.
        rightward = rule[1] == 1
        pop_words, push_words = (right_words, left_words) if rightward else (left_words, right_words)
        pos = right_width+1 if rightward else -left_width-1
        for digit in range(5):
            tm.tape = {**cells, pos: digit}
            tm.state, tm.head = state, 0
            if not tm.step():
                raise ValueError('expected a defined instruction')
            def read_side(direction, length):
                return ''.join(str(tm.tape.get(tm.head + direction*i, 0)) for i in range(1, length+1))
            lnew, rnew = read_side(-1, left_width), read_side(1, right_width)
            pushed, popped = (lnew, rnew) if rightward else (rnew, lnew)
            if pushed not in push_words:
                raise ValueError('missing pushed side word')
            candidate = lnew, tm.state, str(tm.tape.get(tm.head, 0)), rnew
            if popped in pop_words and candidate not in heads:
                raise ValueError('missing permitted successor window')


def permits_aaa(prefix):
    """Can three calls B, B, A return A, A, A given arbitrary replies on the right?"""
    root = (0, 'B', 0, prefix)
    pending, visited = deque([root]), {root}
    while pending:
        phase, state, pos, word = pending.popleft()
        following = []
        if pos < 0:
            if state == 'A':
                if phase == 2:
                    return True
                following.append((phase+1, 'BBA'[phase+1], 0, word))
        elif pos == len(word):
            following.extend((phase, reply, pos-1, word) for reply in 'AB')
        else:
            rule = RULES.get((state, int(word[pos])))
            if rule is not None:
                write, move, new_state = rule
                updated = word[:pos] + str(write) + word[pos+1:]
                following.append((phase, new_state, pos+move, updated))
        for item in following:
            if item not in visited:
                visited.add(item)
                pending.append(item)
    return False


def verify():
    verify_tables()
    heads, side_words = collect()
    check_closed(heads, side_words)
    launch = {right[1:] for _, q, s, right in heads if q == 'A' and s == '0' and right[0] == '3'}
    if launch != PREFIXES or {p for p in launch if not permits_aaa(p)} != SAFE:
        raise ValueError('guard prefix sets do not match the finite checks')
    return len(heads), len(side_words[0]), len(side_words[1])


if __name__ == '__main__':
    n, left, right = verify()
    print(f'{n} closed head windows, {left} left words and {right} right words.')
    print('Possible launch prefixes:', ' '.join(sorted(PREFIXES)))
    print('Prefixes excluding AAA:', ' '.join(sorted(SAFE)))
