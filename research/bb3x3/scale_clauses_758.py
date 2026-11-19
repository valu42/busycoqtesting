#!/usr/bin/env python3
"""Verify ordinary corridors at fixed H and list their exact possible exits."""
import argparse
from collections import deque
from functools import cache

from check_bb33 import HALTING_TARGET as H, champion_step


MOD = 65_536
BASE = 10**10
PREFIX = "J"*292 + "L"*8 + "J" + "L"*6
EVEN_WORD = "I" + "J"*291 + "LLJLLJLR"


def check_word(seed, word):
    a, c = 1, seed
    for letter in word:
        if letter == "I":
            assert a <= c and a % 2 == 1 and c % 2 == 0
        elif letter == "J":
            assert a <= c and a % 2 == c % 2 == 1
        elif letter == "L":
            assert c % 2 == 1 and a >= 4*((c+1)//4) + 3
        elif letter == "R":
            assert a <= c and a % 2 == 0 and c % 2 == 1
        else:
            raise ValueError(letter)
        a, c = champion_step(a, c)
        assert a == 1 if letter == "R" else a > 1
    return c-seed


@cache
def odd_residues():
    # Use the exact fixed J^292 result and fourteen unguarded bulk moves to
    # compute the residues for the 32,768 possible even countdown classes.
    # Initial seed increments of MOD leave all these branch residues intact.
    starts = []
    power = 3**292
    for d in range(0, MOD, 2):
        a, c = 2*power-1, H-d-power+585
        high = 0
        for i in range(14):
            if i == 8:
                a, c = 3*a+2, c-a+1
            q = (c+1)//4
            high += c % 4 == 3
            a, c = a-4*q-3, 6*q+5
        assert a % 4 == 3 and c % 2 == 1
        starts.append((high, c % 4))
    return starts


def cycle_exits(n):
    """Return the odd-orbit cycle data and the overshoots below the lower gate."""
    if not 0 <= n <= 264:
        raise ValueError("the certified scale is 0 through 264")
    k = 264-n
    low = BASE*3**n
    # Work on D/2 modulo MOD/2 since consecutive odd-reset distances are even.
    size = MOD//2
    gains = [(626+2*k+2*(high+int((r-2*k) % 4 == 3)))//2
             for high, r in odd_residues()]
    successor = [(i-step) % size for i, step in enumerate(gains)]
    indegree = [0]*size
    for j in successor:
        indegree[j] += 1
    queue = deque(i for i in range(size) if indegree[i] == 0)
    while queue:
        destination = successor[queue.popleft()]
        indegree[destination] -= 1
        if indegree[destination] == 0:
            queue.append(destination)

    cycles = []
    exits = []
    for i in range(size):
        if indegree[i]:
            j, length, total = i, 0, 0
            while indegree[j]:
                indegree[j] = 0
                length += 1
                total += gains[j]
                origin = low//2 + (j-low//2) % size
                if origin-gains[j] < low//2:
                    exits.append(low-2*(origin-gains[j]))
                j = successor[j]
            assert j == i and total % size == 0
            cycles.append((length, total//size))
    assert len(set(exits)) == len(exits) == sum(winding for _, winding in cycles)
    assert max(exits) <= 2*max(gains)
    return sorted(cycles), sorted(exits)


def check_corridor(n):
    low = BASE*3**n
    high = 3*low//2
    k = 264-n
    odd_word = PREFIX + "J"*k + "LR"
    for d in (low, high):
        raw = check_word(H-d, odd_word)
        a, b = odd_residues()[(d % MOD)//2]
        assert raw == 626+2*k+2*(a+int((b-2*k) % 4 == 3))
    for d in (low+1, high-1):
        assert check_word(H-d, EVEN_WORD) in range(605, 616, 2)


def verify():
    max_windings = total = 0
    single = {}
    for n in range(265):
        check_corridor(n)
        cycles, exits = cycle_exits(n)
        total += len(exits)
        max_windings = max(max_windings, len(exits))
        if len(exits) == 1:
            single[n] = exits[0]
        if n == 0:
            assert cycles == [(841, 15)]
            assert exits == [42, 138, 192, 268, 356, 422, 508, 608, 698, 742, 820,
                             874, 958, 1058, 1146]
    assert 615 + MOD//2*1184 < 39_000_000
    assert (total, max_windings) == (1_722, 20)
    assert single == {74:698, 80:478, 135:732, 194:246, 204:526,
                      225:144, 247:64, 254:490}
    return total, max_windings, len(single)


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run without -O to enable verification.")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scale", type=int, help="print the exact positive exit offsets")
    args = parser.parse_args()
    if args.scale is None:
        print("265 scale corridors verified. Total offsets, maximum per gate, single-exit gates:",
              verify())
    else:
        check_corridor(args.scale)
        print("Cycle lengths and windings, then exit offsets:", cycle_exits(args.scale))
