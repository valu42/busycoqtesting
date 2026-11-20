"""Verify pairwise-distinct DFA states for a regular invariant of BB(6) line 429.
Python 3, standard library only. A tape word has its state marker immediately
before the scanned bit. Keep the scanned bit and trim exterior blank cells.
For each unordered pair of prefixes this checks a true blank-orbit positive
word and a crossed negative word reaching the D1 halt on the same suffix.
Any DFA that accepts all the positives and rejects all the negatives must
map these prefixes to distinct states when reading from the left.
"""
from itertools import combinations
TABLE = '1RB0LC_1RC1RA_1RD0RF_0LE---_1LA1LE_0RA0RF'
RULES = [r[i:i+3] for r in TABLE.split('_') for i in (0, 3)]
PREFIXES = ['E01', 'E010', '1E', '10A', '10C', '1001C', '1D01', '10010010010010010010010C0']
# Bad prefix index, good prefix index, blank-run clock, steps to D reading 1.
CASES = [
    (0, 1, 244, 29),
    (4, 0, 113, 1),
    (5, 0, 113, 1),
    (0, 6, 521, 29),
    (1, 3, 1529, 24),
    (1, 4, 3752, 9),
    (1, 5, 222, 9),
    (1, 6, 242, 9),
    (2, 0, 113, 49),
    (2, 1, 244, 31),
    (5, 2, 3460, 1),
    (2, 6, 521, 31),
    (3, 0, 98, 34),
    (3, 2, 14816, 34),
    (4, 3, 1529, 1),
    (3, 6, 3463, 34),
    (4, 2, 3460, 1),
    (4, 7, 5169, 1),
    (5, 3, 1529, 1),
    (5, 4, 10921, 33),
    (7, 5, 2329, 1),
    (6, 4, 10921, 13),
    (6, 5, 1706, 16),
    (7, 0, 98, 1),
    (7, 1, 14833, 1),
    (7, 2, 14816, 1),
    (7, 3, 93, 1),
    (7, 6, 3463, 1),
]

def advance(q, pos, ones, n):
    for _ in range(n):
        v, d, new = RULES[2*q + (pos in ones)]
        assert v != '-', "halted before the advertised clock"
        if v == '1':
            ones.add(pos)
        else:
            ones.discard(pos)
        q = ord(new) - ord('A')
        pos += 1 if d == 'R' else -1
    return q, pos, ones

def encode(q, pos, ones):
    lo, hi = min(ones | {pos}), max(ones | {pos})
    bits = ''.join('1' if i in ones else '0' for i in range(lo, hi+1))
    cut = pos-lo
    return bits[:cut] + chr(ord('A')+q) + bits[cut:]

def verify():
    pairs = set()
    for bad, good, clock, steps in CASES:
        q, pos, ones = advance(0, 0, set(), clock)
        word = encode(q, pos, ones)
        assert word.startswith(PREFIXES[good])
        candidate = PREFIXES[bad] + word[len(PREFIXES[good]):]
        tag, = (x for x in candidate if x not in '01')
        pos = candidate.index(tag)
        tape = candidate.replace(tag, '')
        cells = {i for i, x in enumerate(tape) if x == '1'}
        assert encode(ord(tag)-ord('A'), pos, cells) == candidate, (bad, good, candidate)
        q, pos, cells = advance(ord(tag)-ord('A'), pos, cells, steps)
        assert q == 3 and pos in cells, "failed to reach D1"
        pairs.add(tuple(sorted((bad,good))))
    assert pairs == set(combinations(range(len(PREFIXES)), 2))
    print(f"{len(CASES)} distinguishing suffixes verified; at least {len(PREFIXES)} DFA states.")

if __name__ == '__main__':
    verify()
