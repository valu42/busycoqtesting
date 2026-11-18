#!/usr/bin/env python3
"""Finite checks for the paired cut and period theorem on line 13."""
from collections import Counter
from itertools import product
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "frontiers"), str(ROOT)]
from longitudinal import Driver
from prior_sweeps import TapeMachine, parse

MACHINE = "1RB3RA3RB4LA1LA_1LB2LA1LA---1RB"
RULES = parse(MACHINE)


def cell(start, stream):
    """Read a finite input on one cell using the checked return contract."""
    symbol, virgin = start
    emitted = []
    for q in stream:
        while (q, symbol) in RULES:
            symbol, direction, q = RULES[q, symbol]
            if direction < 0:
                break
            emitted.append(q)
            q = q if virgin else "A"
            virgin = False
        else:
            return None, "".join(emitted)
    return (symbol, virgin), "".join(emitted)


def parse_open(word):
    """Return status and count consumed through the decisive external entry."""
    assert word[0] == "A"
    second = word.find("A", 1)
    if second < 0:
        return "pending", len(word)
    if (second-1) % 2:
        return "safe", second+1
    k = 0
    index = second+1
    while index < len(word):
        if word[index] == "B":
            return ("halt" if k % 2 else "safe"), index+1
        end = word.find("A", index+1)
        if end < 0:
            break
        if (end-index-1) % 2 == 0:
            return ("safe" if k % 2 else "halt"), end+1
        k += 1
        index = end+1
    return "pending", len(word)


def literal_open(word):
    tm = TapeMachine(MACHINE)
    for i, q in enumerate(word, 1):
        tm.head, tm.state = 0, q
        next_even = None
        while tm.head >= 0:
            if tm.head == 2 and next_even is None:
                next_even = tm.state
            if not tm.step():
                assert (tm.head, tm.state, tm.tape[1]) == (1, "B", 3)
                assert next_even == "B"
                return "halt", i
        if next_even is not None:
            assert next_even == "A" and (tm.tape[0], tm.tape[1]) == (4, 4)
            return "safe", i
    return "pending", len(word)


def compact(prefix, period):
    least = (period + period).find(period, 1)
    assert least > 0
    period = period[:least]
    removed = 0
    while prefix and prefix[-1] == period[-1-removed % len(period)]:
        prefix = prefix[:-1]
        removed += 1
    shift = removed % len(period)
    if shift:
        period = period[-shift:] + period[:-shift]
    return prefix, period


def period_image(prefix, period):
    state, prefix = cell((0, True), prefix)
    parts = []
    seen = {}
    while state not in seen:
        assert state is not None
        seen[state] = len(parts)
        state, piece = cell(state, period)
        parts.append(piece)
    j = seen[state]
    return compact(prefix + "".join(parts[:j]), "".join(parts[j:]))


def counts(period):
    # Rotate the period to an A so that its last B gap wraps to that A.
    i = period.index("A")
    gaps = (period[i+1:] + period[:i]).split("A")
    a, b = period.count("A"), period.count("B")
    r = sum(len(gap) % 2 for gap in gaps)
    return a+b-r, b+r


def main():
    driver = Driver(13)
    assert (driver.machine, driver.first, driver.usual) == (MACHINE, "AB", "A")
    cases = Counter()
    for n in range(13):
        for suffix in product("AB", repeat=n):
            w = "A"+"".join(suffix)
            decision = parse_open(w)
            assert literal_open(w) == decision
            cases[decision[0]] += 1
            if decision[0] == "safe":
                end = decision[1]
                s, odd = cell((0, True), w)
                _, even = cell((0, True), odd)
                _, rest = cell((4, False), w[end:])
                _, rest = cell((4, False), rest)
                assert even == "A"+rest and s is not None
    print("Literal pair classification through 13 entries (counts):", dict(sorted(cases.items())))

    periods = 0
    for n in range(1, 11):
        for letters in product("AB", repeat=n):
            w = "".join(letters)
            if w.count("A") % 2 == 0 or "B" not in w:
                continue
            a, b = counts(w)
            assert a % 2 and b > 0 and b % 2 == 0
            for s in (1, 2, 4):
                settled, _ = cell((s, False), w*2)
                finish, out = cell(settled, w*2)
                assert settled == finish and (out.count("A"), out.count("B")) == (a, b)
                periods += 1
    print("Ordinary initial states × short mixed odd-A period checks:", periods)

    # From any mature cell, at most three inputs emit any one requested letter.
    for s in (1, 2, 4):
        for desired in "AB":
            assert any(cell((s, False), "".join(w))[1] == desired
                       for n in range(1, 4) for w in product("AB", repeat=n))

    hist = json.loads((ROOT / "frontiers/runs/line13-entry-prefixes.json").read_text())["payload"]
    assert hist["machine"] == MACHINE and hist["groups"] == 10**17
    seen = hist["entry_prefixes"]
    for i in range(0, len(seen), 2):
        status, _ = parse_open(seen[i])
        assert status == ("safe" if i < len(seen)-2 else "pending")
    print("Exceptional even-gap parents:", [(i, seen[i][:18], seen[i+1][:8]) for i in range(0,len(seen),2)
        if "A" in seen[i][1:] and (seen[i].find("A", 1)-1) % 2 == 0])
    u, p = "A", driver.period
    print("True aligned tail representations (cut, prefix, primitive period)")
    for x in range(11):
        print(x, u or "ε", p)
        expanded = u+p*100
        assert expanded.startswith(seen[x])
        if x < 10:
            u, p = period_image(u, p)
    assert u == "" and len(p) == 27
    rotated = p[12:] + p[:12]
    assert parse_open(p*2)[0] == "safe"
    assert parse_open(rotated*2) == literal_open(rotated*2) and parse_open(rotated*2)[0] == "halt"
    print("Cut 10 at offset 12:", rotated, literal_open(rotated*2))


if __name__ == "__main__":
    main()
