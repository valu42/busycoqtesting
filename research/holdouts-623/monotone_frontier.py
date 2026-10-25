#!/usr/bin/env python3
"""Falsify proposed tape grammars for the monotone frontier in Coq.

This is unverified exploration. It starts B on a blank right side with an
arbitrary finite left word, not the blank A start. The symbolic search reads
an input bit only when needed, memoizing (control, work word, grammar state).
Every reported counterexample is replayed by an independent coordinate-tape
interpreter. No bounded negative result is a proof of closure or nonhalting.

The no00 grammar excludes adjacent zeros within the finite word; implicit
blank padding is unrestricted. The residues grammar additionally bounds the
leading run by five, permits interior one-runs congruent to 1 or 2 mod 4,
bounds the number of the latter, and requires a final run after the head to
be congruent to 0 or 1. A word consisting only of the head run is allowed.
These are hypotheses, not established properties of the blank orbit.
"""
import argparse
from collections import deque
import json
import math
import time

MACHINE = '1RB0LE_0RC---_1RD0LA_1RE0RA_1LC0LF_0RC1LC'
BAD_WORD = 0x37ed6bf
_flat = MACHINE.replace('_', '')
TABLE = [None if _flat[i:i+3] == '---' else
         (int(_flat[i]), _flat[i+1] == 'R', ord(_flat[i+2])-65)
         for i in range(0, 36, 3)]


class Grammar:
    def __init__(self, name='no00', cap=1):
        self.name, self.cap = name, cap
        self.initial = ('start',) if name == 'no00' else ('ones', True, 0, 0)
        self.end = ('end',)

    def advance(self, state, bit):
        if state == self.end:
            return state if bit == 0 else None
        if self.name == 'no00':
            if state == ('start',):
                return ('one',) if bit else None
            if bit:
                return ('one',)
            return self.end if state == ('zero',) else ('zero',)
        kind, head, n, count = state
        if kind == 'ones':
            if bit:
                if head and n == 5:
                    return None
                return ('ones', head, n+1 if head else (n+1) % 4, count)
            if head and n == 0:
                return None
            return ('zero', head, n, count)
        if not bit:
            return self.end if head or n in (0, 1) else None
        if head or n == 1 or (n == 2 and count < self.cap):
            return ('ones', False, 1, count + int(not head and n == 2))
        return None

    def completion(self, state):
        queue, seen = deque([(state, 0, 0)]), set()
        while queue:
            s, word, length = queue.popleft()
            if s == self.end:
                return word, length
            if s in seen:
                continue
            seen.add(s)
            for bit in (0, 1):
                nxt = self.advance(s, bit)
                if nxt is not None:
                    queue.append((nxt, word | (bit << length), length+1))
        return None

    def accepts(self, word):
        state = self.initial
        for i in range(word.bit_length()+2):
            state = self.advance(state, (word >> i) & 1)
            if state is None:
                return False
        return state == self.end


def raw_root(word, limit=1000000):
    """Independent literal coordinate-tape execution to the next B/root."""
    tape = {-i-1 for i in range(word.bit_length()) if (word >> i) & 1}
    q, head = 1, 0
    for steps in range(limit):
        op = TABLE[2*q + (head in tape)]
        if op is None:
            return {'status': 'halt', 'steps': steps}
        write, direction, q = op
        if write:
            tape.add(head)
        else:
            tape.discard(head)
        head += 1 if direction else -1
        if q == 1 and all(i < head for i in tape):
            result = sum(1 << (head-i-1) for i in tape)
            return {'status': 'return', 'steps': steps+1, 'word': result}
    return {'status': 'unknown', 'steps': limit}


def search(grammar, max_states=500000, seconds=30, segment_steps=100000,
           check_closure=False):
    # Checked by MonotoneFrontier.enter: B/root -> C scanning the input,
    # with work word 1001 to its right. Words are nearest-cell first.
    queue = deque([(2, 9, grammar.initial, 0, 0)])
    seen, returns, max_depth = set(), 0, 0
    start = time.monotonic()
    completions = {}
    reason = 'state limit'
    def finish(s):
        if s not in completions:
            completions[s] = grammar.completion(s)
        return completions[s]
    while queue and len(seen) < max_states:
        if time.monotonic()-start >= seconds:
            reason = 'time limit'
            break
        q0, work, state, word, depth = queue.popleft()
        key = (q0, work, state)
        if key in seen:
            continue
        seen.add(key)
        max_depth = max(max_depth, depth)
        for bit in (0, 1):
            nxt = grammar.advance(state, bit)
            if nxt is None or finish(nxt) is None:
                continue
            word1, depth1 = word | (bit << depth), depth+1
            l, r, q, h = 0, (work << 1) | bit, q0, 0
            event = None
            for _ in range(segment_steps):
                if h < 0:
                    queue.append((q, r >> 1, nxt, word1, depth1))
                    break
                tail, _ = finish(nxt)
                concrete = word1 | (tail << depth1)
                if q == 1 and r == 0:
                    returns += 1
                    output = l | (tail << h)
                    if check_closure and not grammar.accepts(output):
                        event = 'closure_counterexample'
                    break
                op = TABLE[2*q + (r & 1)]
                if op is None:
                    event = 'halting_counterexample'
                    break
                write, direction, q = op
                r = (r & ~1) | write
                if direction:
                    l, r, h = (l << 1) | (r & 1), r >> 1, h+1
                else:
                    l, r, h = l >> 1, (r << 1) | (l & 1), h-1
            else:
                return {'status': 'unknown', 'detail': 'segment step limit',
                        'states': len(seen), 'max_depth': max_depth}
            if event:
                assert grammar.accepts(concrete)
                replay = raw_root(concrete, segment_steps*100)
                if event == 'halting_counterexample':
                    assert replay['status'] == 'halt', replay
                else:
                    assert replay['status'] == 'return' and replay['word'] == output, replay
                    assert not grammar.accepts(replay['word'])
                    replay['word_hex'] = hex(replay.pop('word'))
                return {'status': event, 'word_hex': hex(concrete),
                        'nearest_first': bin(concrete)[2:][::-1],
                        'word_bits': concrete.bit_length(), 'replay': replay,
                        'states': len(seen), 'max_depth': max_depth,
                        'seconds': round(time.monotonic()-start, 3)}
    return {'status': 'unknown', 'detail': reason if queue else 'queue exhausted; unverified',
            'states': len(seen), 'returns': returns, 'pending': len(queue),
            'max_depth': max_depth, 'seconds': round(time.monotonic()-start, 3)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--grammar', choices=('no00', 'residues'), default='no00')
    parser.add_argument('--cap', type=int, default=1)
    parser.add_argument('--states', type=int, default=500000)
    parser.add_argument('--seconds', type=float, default=30)
    parser.add_argument('--segment-steps', type=int, default=100000)
    parser.add_argument('--check-closure', action='store_true')
    parser.add_argument('--selftest', action='store_true')
    args = parser.parse_args()
    if args.cap < 0 or args.states < 1 or args.segment_steps < 1:
        parser.error('cap must be nonnegative and integer budgets positive')
    if not math.isfinite(args.seconds) or args.seconds <= 0:
        parser.error('seconds must be finite and positive')
    if args.selftest:
        assert Grammar().accepts(BAD_WORD)
        assert raw_root(BAD_WORD) == {'status': 'halt', 'steps': 434}
        assert raw_root(0) == {'status': 'return', 'steps': 13, 'word': 11}
        assert raw_root(1) == {'status': 'return', 'steps': 22, 'word': 15}
        for name in ('no00', 'residues'):
            grammar = Grammar(name)
            for w in range(1, 4096):
                state = grammar.initial
                for i in range(w.bit_length()):
                    state = grammar.advance(state, (w >> i) & 1)
                    if state is None:
                        break
                if state is not None and grammar.completion(state) is not None:
                    tail, _ = grammar.completion(state)
                    assert grammar.accepts(w | (tail << w.bit_length()))
        print(json.dumps({'status': 'selftest passed'}))
    else:
        result = search(Grammar(args.grammar, args.cap), args.states, args.seconds,
                        args.segment_steps, args.check_closure)
        result.update(machine=MACHINE, grammar=args.grammar, cap=args.cap)
        print(json.dumps(result))


if __name__ == '__main__':
    main()
