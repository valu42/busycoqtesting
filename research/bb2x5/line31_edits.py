#!/usr/bin/env python3
"""Replay the single-edit certificates and the periodic postponement identities."""
import argparse
from itertools import chain, cycle, islice
from pathlib import Path
import subprocess

from line31_phase import ROOT, MACHINE, TapeMachine, alignment, cyclic_image, read_rows, transform

BLOCK = "AABAA"
REFERENCE = "BAAAA"
FIXED = "AAAABBA"
CAPTURES = {2: 2, 4: 4, 46: 9, 104: 9, 211: 11, 246: 11}


def normalize(prefix, period):
    """Shortest repeating block and shortest preperiod, with the origin retained."""
    period = period[:(period + period).index(period, 1)]
    i, offset = len(prefix), 0
    while i and prefix[i - 1] == period[(offset - 1) % len(period)]:
        i -= 1
        offset = (offset - 1) % len(period)
    return prefix[:i], period[offset:] + period[:offset]


def edited(n):
    if n < 2 or BLOCK[(n-1) % 5] != "A":
        raise ValueError("the edit must replace an A after the first request")
    before = (BLOCK * ((n+4)//5))[:n-1]
    return normalize("AAA" + before + "B", BLOCK[n % 5:] + BLOCK[:n % 5])


def image(stream, phase):
    prefix, period = stream
    prefix, end = transform(phase, prefix)
    return normalize(prefix, cyclic_image(end, period))


def pair(stream):
    return image(image(stream, 0), 2)


def states(n, depth):
    s = edited(n)
    yield s
    for _ in range(depth):
        s = pair(s)
        yield s


def true_block(x):
    word, groups = BLOCK, 1
    for i in range(x):
        copies = 3 if (word.count("A") - word.count("B")) % 3 else 1
        start = alignment(i)[1]
        word, end = transform(start, word * copies)
        assert end == start
        groups *= copies
    return groups, word


def first_halt(letters, limit):
    """Literal positive tape, driven by the supplied physical (unprefixed) requests."""
    tm = TapeMachine(MACHINE)
    for n, letter in enumerate(islice(letters, limit), 1):
        tm.head, tm.state = 0, letter
        while tm.head >= 0:
            if not tm.step():
                return n, tm.head, tm.state, tm.tape.get(tm.head, 0)
    raise ValueError("the supplied requests completed")


def physical_edit(n):
    for i, c in enumerate(cycle(BLOCK), 1):
        yield "B" if i == n else c


def feed(phases, letter):
    for i, p in enumerate(phases):
        phases[i] = (p + (1 if letter == "A" else 2)) % 3
        if letter == "B" and p:
            break
        letter = "B" if letter == "A" and p == 0 else "A"


def small_sync():
    # Compare the two words immediately after the moved B. The true-side ray
    # starts after its three introductory As. Both words have read n+3 letters.
    width = 13
    orig = [2*(x % 2) for x in range(width)]
    ref = orig.copy()
    for c in "AAA":
        feed(orig, c)
    for c in REFERENCE[:3]:
        feed(ref, c)
    starts = orig.copy(), ref.copy()
    matches = []
    for n in range(1, 5*3**8 + 1):
        feed(ref, REFERENCE[(n+2) % 5])
        c = BLOCK[(n-1) % 5]
        if c == "A":
            changed = orig.copy()
            feed(changed, "B")
            if changed == ref:
                matches.append(n)
        feed(orig, c)
    assert (orig, ref) == starts and matches == [2]


def final_phases(word):
    phases = []
    while word:
        word, end = transform(2*(len(phases) % 2), word)
        phases.append(end)
    while phases and phases[-1] == 2*((len(phases)-1) % 2):
        phases.pop()
    return phases


def check_sync():
    small_sync()
    assert final_phases("AAAAB") == final_phases(REFERENCE)
    # Use primitive reference periods. Keep their multiplicity in a complete
    # return, so that the period length stays small even at large heights.
    word, copies, groups = REFERENCE, 1, 1
    for h in range(1, 60):
        p = 2*((h-1) % 2)
        drift = word.count("A") - word.count("B")
        factor = 3 if copies*drift % 3 else 1
        groups *= factor
        period_factor = 3 if drift % 3 else 1
        out, end = transform(p, word * period_factor)
        assert end == p
        word = out[:(out+out).index(out, 1)]
        copies, rem = divmod(copies*factor*len(out), period_factor*len(word))
        assert not rem and groups == 3**max(0, (h-2)//2)
    # The committed 40-cycle ledger covers 40*3^32 groups. A shorter
    # return would have to divide the cut's letter count by the same factor.
    rows = read_rows((ROOT / "frontiers/runs/line31-phase-rows.txt").read_text())
    assert rows[0][0] == 5*40*3**32
    for valuation in range(8, 32):
        for h in range(1, 57):
            calls, rem = divmod(rows[h][0], 40)
            assert not rem
            reference_exponent = max(0, (h-2)//2)
            if reference_exponent <= valuation and calls % 3**(32-valuation):
                break
        else:
            raise AssertionError(f"missing unequal return at valuation {valuation}")
    length, bs = 53_427_204_485, 15_648_460_017
    d = length - 2*bs
    assert d % 3 and length % 3 and (2*length+d) % 3 == 0
    print(f"Phase agreement on the first 59 cells requires and is attained at edit 2 modulo {5*3**34:,}.")


def checks(long_replay):
    assert pair(("", FIXED)) == ("", FIXED)
    assert normalize("AAA", BLOCK)[0]
    assert pair(normalize("AAA", BLOCK)) == ("", "AAAABAAABB")
    for n, d in CAPTURES.items():
        path = list(states(n, d))
        assert all((u+v*4)[:4] == "AAAA" for u, v in path)
        assert path[-1] == ("", FIXED) and ("", FIXED) not in path[:-1]
    assert list(states(4, 1))[-1] == list(states(46, 6))[-1] == ("AA", "AAAAB")
    bridge = ("AAAABAAAA", "AAB")
    for n in (211, 246):
        assert list(states(n, 7))[-1] == bridge
    u, v = list(states(281, 7))[-1]
    assert u == "AAAABAAAAAA" and len(v) == 544
    assert first_halt(physical_edit(1), 2) == (2, 0, "A", 2)
    assert first_halt(physical_edit(36), 5_386) == (5_386, 34, "A", 2)

    k6, q6 = true_block(6)
    assert (k6, len(q6)) == (81, 117)
    for k in (1, 2):
        assert list(states(2 + 5*k6*k, 3))[-1] == normalize(q6*k, FIXED)
    assert first_halt(physical_edit(407), 23_727) == (23_727, 38, "A", 2)
    assert first_halt(chain(q6[3:], cycle(FIXED)), 7_371) == (7_371, 32, "A", 2)
    k14, q14 = true_block(14)
    k22, q22 = true_block(22)
    assert (5*k14, k22, len(q22)) == (98_415, 1_594_323, 74_190)
    checkpoint_groups = 40 * 3**32 + 10**9
    assert checkpoint_groups == 74_120_808_554_073_640
    assert (checkpoint_groups + k22 - 1) // k22 == 46_490_459_308
    # Before an inserted whole cycle is exhausted, every earlier even aligned
    # cut has received its fourth A. Check the single cycle at its own cut and
    # use the proved periodic closure for every positive number of cycles.
    for h in (6, 14, 22):
        groups, _ = true_block(h)
        stream = "AAA" + BLOCK * min(groups, 2048)
        for i in range(h):
            if i % 2 == 0:
                assert stream[:4] == "AAAA"
            stream, _ = transform(2*(i % 2), stream)
    if long_replay:
        u, v = bridge
        assert first_halt(chain((q14+u)[3:], cycle(v)), 1_301_444) == (1_301_444, 54, "A", 2)
        hit = first_halt(chain((q22*3)[3:], cycle(FIXED)), 2_082_606)
        assert hit == (2_082_606, 58, "A", 2)
        print("All six edits shifted by 23,914,845 halt at +80. Literal cut-22 request 2,082,606.")
    check_sync()
    print("Six safe edits, both exact bridges, and the literal halt for edit 407 checked.")


def crosscheck(engine):
    for depth, limit in ((2, 12), (4, 25), (7, 80)):
        p = subprocess.run([str(engine.resolve()), "--capture-edits", str(depth), str(limit),
                            "1000", "1000000"], check=True, capture_output=True, text=True)
        captures = {int(n): int(j) for _, n, j in
                    (row.split() for row in p.stdout.splitlines() if row.startswith("capture "))}
        expected = {}
        for n in range(2, limit + 1):
            if BLOCK[(n-1) % 5] != "A":
                continue
            for j, (u, v) in enumerate(states(n, depth)):
                if (u+4*v)[:4] != "AAAA":
                    break
                if not u and v == FIXED:
                    expected[n] = j
                    break
        assert captures == expected
    print("Small native classifications agree with direct infinite-word transformations.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--long-replay", action="store_true", help="also replay the complete cut-22 halt")
    parser.add_argument("--engine", type=Path, help="also cross-check the compiled edit search")
    args = parser.parse_args()
    checks(args.long_replay)
    if args.engine:
        crosscheck(args.engine)
