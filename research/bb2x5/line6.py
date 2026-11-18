"""Exact word recurrence and finite checks for BB(2,5) formal line 6.

Run from research/bb2x5 with Python 3.10+ and assertions enabled.
"""
from itertools import product
from pathlib import Path
from typing import NamedTuple

from prior_sweeps import TapeMachine


MACHINE = "1RB---3LB4RB0LA_2LB3LA3RB4RA0RA"
HEADER = "322323300"


class Result(NamedTuple):
    state: str
    word: str | None
    steps: int


def probe(word):
    """B probe on a word padded by zeros. Only completed returns have a word.

    For a B return omit its first cell, which is necessarily 2.
    All costs count defined elementary transitions. The explicit stack permits
    arbitrarily deep finite derivations, subject to available resources.
    """
    if any(digit not in "023" for digit in word):
        raise ValueError("probe words use only 0, 2 and 3")
    frames = []
    word = word.rstrip("0")
    while True:
        # Descend to the first literal zero, the base case.
        while word and word[0] != "0":
            if word[0] == "2":
                frames.append(("2", 0))
                word = word[1:]
            else:
                token = word[:2].ljust(2, "0")
                frames.append((token, 0))
                word = word[2:]
        state, word, steps = "B", word[1:], 1
        while frames:
            token, prior = frames.pop()
            if state == "H":
                if token == "2":
                    steps += 1
                elif token == "32":
                    steps += 4
                elif token in ("33", "30"):
                    steps += 2
                else:
                    steps += prior
            elif token == "2":
                # Both outcomes need a second probe on the residual word.
                # Save the number of steps already taken, including the
                # instructions that enter this second probe.
                frames.append((state, steps + (5 if state == "B" else 2)))
                break
            elif token == "B":
                word = ("23" if state == "B" else "32") + word
                steps += prior + 4
            elif token == "A":
                word = ("3" if state == "B" else "0") + word
                steps += prior + (3 if state == "B" else 1)
            elif token == "32":
                word = ("23" if state == "B" else "32") + word
                steps += 8
            elif token == "33":
                word = ("33" if state == "B" else "00") + word
                steps += 8 if state == "B" else 4
            elif token == "30":
                if state == "B":
                    state, word = "A", "032" + word
                    steps += 4
                else:
                    state, word = "H", None
                    steps += 2
            else:
                raise AssertionError(token)
        else:
            return Result(state, None if word is None else word.rstrip("0"), steps)


def literal_probe(word, limit=500_000):
    tm = TapeMachine(MACHINE, map(int, word))
    tm.state = "B"
    while 0 <= tm.head and tm.steps < limit:
        if not tm.step():
            return Result("H", None, tm.steps)
    if tm.head >= 0:
        raise RuntimeError("Literal probe reached work limit")
    first = int(tm.state == "B")
    if first:
        assert tm.tape[0] == 2
    right = max(tm.tape, default=-1)
    word = "".join(str(tm.tape.get(i, 0)) for i in range(first, right+1))
    return Result(tm.state, word, tm.steps)


def check_header():
    tm = TapeMachine(MACHINE, map(int, HEADER))
    tm.state = "B"
    while 0 <= tm.head < len(HEADER) and tm.steps < 32:
        assert tm.step()
    def block():
        return "".join(str(tm.tape.get(i, 0)) for i in range(len(HEADER)))
    assert (tm.steps, tm.head, tm.state, block()) == (31, 9, "B", "040434441")
    tm.head = 8
    tm.state = "A"
    assert not tm.step()
    tm.state = "B"
    while 0 <= tm.head < len(HEADER) and tm.steps < 49:
        assert tm.step()
    assert (tm.steps, tm.head, tm.state, block()) == (48, -1, "B", "223233003")


def audit():
    lines = Path(__file__).with_name("BB2x5_Rocq_holdouts_37.txt").read_text().splitlines()
    assert lines[5] == MACHINE
    check_header()
    for copies in range(12):
        word = "0" + HEADER*copies + "3"
        tm = TapeMachine(MACHINE, map(int, word))
        for _ in range(31*copies+6):
            assert tm.step()
        assert not tm.step()
        assert tm.head == 9*copies and tm.tape[tm.head] == 1
    count = 0
    for n in range(8):
        for digits in product("023", repeat=n):
            word = "".join(digits)
            result = probe(word)
            assert result == literal_probe(word), word
            if result.state != "H":
                assert result.word.count("2") == word.count("2") + (result.state == "A")
                if "02" not in word and "222" not in word:
                    assert "02" not in result.word and "222" not in result.word
                    assert result.state != "B" or not result.word.startswith("22")
                if result.state == "A":
                    assert not result.word or result.word.startswith(("0", "32"))
            count += 1
    print(f"{count} finite input words match the literal return, word and step count.")
    # Independently compare full checkpoint words from the blank orbit.
    tm = TapeMachine(MACHINE)
    residual, headers, total = "", 0, 0
    for epoch in range(1, 377):
        state, rest, cost = probe(residual)
        assert state == "B"
        total += 2 + cost + 48*headers
        residual = "32" + rest
        while residual.startswith(HEADER):
            headers += 1
            residual = residual[len(HEADER):]
            print(f"Header {headers} at left extension {epoch}, step {total}.")
        while tm.head > -epoch:
            assert tm.step()
        word = HEADER*headers + residual
        if epoch <= 32:
            unary = probe("2"*(epoch-1))
            assert (unary.state, "32"+unary.word) == ("B", word)
            assert unary.steps + epoch + 1 == total
        assert word.count("2") == epoch
        assert "02" not in word and "222" not in word
        assert word.count("3") >= (epoch+1)//2
        assert max(tm.tape) >= (epoch+1)//2
        assert (tm.head, tm.state, tm.steps) == (-epoch, "A", total)
        assert tm.tape == {tm.head+i: int(c) for i, c in enumerate(word, 1) if c != "0"}
    assert (headers, total) == (3, 4_808_934)


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run with assertions enabled.")
    audit()
