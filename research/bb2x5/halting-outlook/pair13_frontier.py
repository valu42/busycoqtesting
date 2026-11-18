#!/usr/bin/env python3
"""Shortest future inputs from the actual 10^17-group suffix to resolve cell 155."""
from collections import deque
from functools import lru_cache
import argparse
import json
from pathlib import Path

from pair13 import MACHINE, ROOT, TapeMachine, cell
from longitudinal import Driver
from test_longitudinal import cells

HERE = Path(__file__).resolve().parent


@lru_cache(None)
def ordinary(symbol, word):
    (after, _), out = cell((symbol, False), word)
    return after, out


def edge(state, request):
    """Project one request from the chosen cut to the rightmost waiting cell."""
    symbols, odd = state
    child = request
    mutable = list(symbols)
    for i, s in enumerate(symbols):
        if not child:
            break
        mutable[i], child = ordinary(s, child)
    for c in child:
        if c == "A":
            return "opens" if odd else "halts"
        odd = not odd
    return tuple(mutable), odd


def shortest(symbols):
    start = tuple(symbols), True
    parent = {start: None}
    pending = deque([start])
    answers = {}
    while len(answers) < 2:
        s = pending.popleft()
        for c in "AB":
            t = edge(s, c)
            if isinstance(t, str):
                if t not in answers:
                    trail = [c]
                    back = s
                    while parent[back] is not None:
                        back, char = parent[back]
                        trail.append(char)
                    answers[t] = "".join(reversed(trail))
            elif t not in parent:
                parent[t] = s, c
                pending.append(t)
    return answers


def physical(tape, start, word):
    tm = TapeMachine(MACHINE, map(int, tape[start:]), left=start)
    for request in word:
        tm.head, tm.state = start, request
        while tm.head >= start:
            if tm.head == 155 and tm.state == "A":
                raw = tm.steps
                if tm.tape[155] == 1:
                    return "opens", raw
                assert tm.tape[155] == 2
                assert tm.step() and tm.step() and not tm.step()
                return "halts", tm.steps
            assert tm.step()
    raise AssertionError("test word failed to decide the frontier")


def main():
    driver = Driver(13)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine", type=Path)
    args = parser.parse_args()
    if args.engine:
        for groups in (1, 7, 31, 111):
            cp = driver.advance(args.engine, driver.blank(), groups, 1 << 23)
            tm = TapeMachine(MACHINE)
            while tm.steps < cp["steps"]:
                assert tm.step()
            assert (tm.steps, tm.head, tm.state, tm.tape) == (cp["steps"], cp["head"], cp["state"], cells(driver, cp))
        print("Four literal blank configurations and raw clocks agree.")
    previous = driver.load(ROOT / "frontiers/runs/stream-13.json")
    extra = driver.load(HERE / "pair13_checkpoint.json")
    log = json.loads((HERE / "pair13_batch.json").read_text())
    assert log["from_groups"] == previous["groups"] and log["groups"] == extra["groups"]
    assert log["steps"] == extra["steps"] and len(log["entry_prefixes"]) == 128
    tape = previous["positive_tape"]
    assert len(tape) == 156 and tape[-1] == "1" and tape[128:] == extra["positive_tape"][128:]
    for start in (154, 153, 152, 150, 147, 144):
        answers = shortest(map(int, tape[start:155]))
        for mode, word in sorted(answers.items()):
            actual, steps = physical(tape, start, word)
            assert actual == mode
            print(start, actual, len(word), steps, word)
    print(f"Future batch from {previous['groups']} through {extra['groups']} groups"
          f" reaches only coordinates 0–127 on the right; raw time {extra['steps']}.")


if __name__ == "__main__":
    main()
