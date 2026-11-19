#!/usr/bin/env python3
"""Check which odd reset residues occur near H after one or two returns from even seeds."""
from check_bb33 import HALTING_TARGET as H, champion_step


MOD = 2**16
RADIUS = 2**380
EVEN = 'I' + 'J'*291 + 'LLJLLJLR'
ODD_PREFIX = 'J'*292 + 'L'*8 + 'J' + 'L'*6


def check_word(seed, word):
    a, c = 1, seed
    for i, letter in enumerate(word):
        if a <= c:
            actual = ('J' if c % 2 else 'I') if a % 2 else 'R'
        else:
            assert c % 2 and a >= 4*((c+1)//4)+3
            actual = 'L'
        assert actual == letter
        a, c = champion_step(a, c)
        assert a == 1 if i == len(word)-1 else a > 1
    return c


def verify_blocks():
    for k in range(32):
        center = H - H//(2300*3**k)
        lo, hi = center - RADIUS, center + RADIUS
        for p, word in ((0, EVEN), (1, ODD_PREFIX + 'J'*k + 'LR')):
            # The second word also covers any overshoot of the first return.
            left, right = lo + (p-lo)%2, hi + 616 - (hi+616-p)%2
            check_word(left, word)
            check_word(right, word)


def finish_prefix(y):
    p = 3**292 % MOD
    a, c = 2*p-1, y-p+585
    high = 0
    for run in (8, 6):
        for _ in range(run):
            q = (c+1)//4
            high += c % 4 == 3
            a, c = a-4*q-3, 6*q+5
        if run == 8:
            a, c = 3*a+2, c-a+1
    assert a % 4 == 3
    return high, c % 4


def main():
    if not __debug__:
        raise SystemExit('run without -O to execute all assertions')
    verify_blocks()
    base = H - H%64 - 64_000_000
    even_gain = [check_word(base+i, EVEN)-base-i for i in range(0,64,2)]
    assert max(even_gain) == 615
    once = set()
    twice = [set(), set()]
    for x in range(0, MOD, 2):
        y = x + even_gain[(x%64)//2]
        once.add(y % MOD)
        high, c = finish_prefix(y)
        for k in (0, 1):
            last_high = (c-2*k) % 4 == 3
            twice[k].add((y + 626 + 2*k + 2*(high+last_high)) % MOD)
    assert {y%64 for y in once} == {3,11,15,17,19,25,29,33,37,41,45,51,53,55,59}
    found = set(once)
    for k in range(32):
        found.update((y + 4*(k//2)) % MOD for y in twice[k%2])
    assert found == set(range(1, MOD, 2))
    print('All odd residues modulo 2^380 occur after one or two returns '
          'from even seeds in the verified corridors below H.')


if __name__ == '__main__':
    main()
