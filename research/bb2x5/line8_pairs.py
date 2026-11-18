#!/usr/bin/env python3
"""Check the line-8 pair reduction and its finite blank-orbit comparison."""
from itertools import product
from pathlib import Path
import sys

MACHINE = "1RB4LA1RA1RB1LA_2LB3LA---4RA2RB"
ROW = [[block[i:i+3] for i in range(0, 15, 3)] for block in MACHINE.split("_")]
PULSES = ("A", "B", "BA")


def cell(symbol, entries):
    """Probe an ordinary cell. Each successful excursion to the right returns A."""
    requests = ""
    for state in entries:
        while True:
            rule = ROW[state == "B"][int(symbol)]
            assert rule != "---"
            symbol, direction, state = rule
            if direction == "L":
                assert state == "A"
                break
            requests += state
            state = "A"
    return symbol, requests


def ordinary(pair, pulse):
    left, requests = cell(pair[0], pulse)
    right, output = cell(pair[1], requests)
    assert output in ("", *PULSES)
    return left + right, output


def raw_positive(word, entries):
    """Use raw TM steps on the positive half, supplying an entry when the head exits left."""
    tape = list(word)
    for state in entries:
        pos = 0
        while pos >= 0:
            if pos == len(tape):
                tape.append("0")
            rule = ROW[state == "B"][int(tape[pos])]
            if rule == "---":
                return None
            tape[pos], direction, state = rule
            pos += 1 if direction == "R" else -1
        assert state == "A"
    return "".join(tape)


def advance(tape, signal):
    pairs = [tape[i:i+2] for i in range(0, len(tape), 2)]
    assert pairs[-1] == "32"
    for i, pair in enumerate(pairs[:-1]):
        pairs[i], signal = ordinary(pair, signal)
        if not signal:
            return "".join(pairs)
    if signal == "A":
        return None
    pairs[-1] = {"B": "1432", "BA": "4432"}[signal]
    return "".join(pairs)


def stream(pair, signals):
    emitted = []
    for signal in signals:
        pair, value = ordinary(pair, signal)
        if value:
            emitted.append(value)
    return pair, emitted


def check():
    assert raw_positive("", "A") == "32"
    for signal in PULSES:
        assert raw_positive("32", signal) == advance("32", signal)
    for size in range(3):
        for digits in product("134", repeat=2*size):
            word = "".join(digits) + "32"
            for signal in PULSES:
                assert raw_positive(word, signal) == advance(word, signal)
    # The first B acts on 32, and the driver's remaining letters are (BABAB)^omega.
    assert stream("14", "BABAB") == ("31", ["BA", "BA"])
    assert stream("31", "BABAB") == ("31", ["BA"])
    # The artificial drive (BA, B, BA)^omega starts with BA, so 32 becomes 4432.
    assert stream("44", ("B", "BA", "BA")) == ("44", ["BA", "B", "BA"])
    # Each ordinary cell can pass exactly one requested letter.
    codes = {"1": ("BB", "BA"), "3": ("B", "A"), "4": ("ABB", "ABA")}
    for old in "134":
        for target, inputs in zip("AB", codes[old]):
            new, output = cell(old, inputs)
            assert new in "134" and output == target
    # Direct comparison of entire right tapes after successive blank driver letters.
    tape = "32"
    for letter in "BBABA" * 4000:
        expected = raw_positive(tape, letter)
        tape = advance(tape, letter)
        assert expected == tape and tape is not None
    print("All pair, driver, control and 20,000 sequential tape checks passed.")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        listed = Path(sys.argv[1]).read_text().splitlines()[7].strip()
        assert listed == MACHINE
    check()
