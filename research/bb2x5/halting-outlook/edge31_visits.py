#!/usr/bin/env python3
"""Locate the first physical rightward entries to 138 and 140 from the published run."""
from pathlib import Path
import argparse
import json
from edge31 import Driver, ROOT
from checkpoints import checksum
from prior_sweeps import parse, TapeMachine


def first_visit(driver, engine, start, target, ceiling):
    # At a completed group the positive tape contains every visited cell, even
    # if blank. Once reached, a target can never disappear from this record.
    assert len(start["positive_tape"]) <= target and start["groups"] < ceiling
    left = start
    right = ceiling
    while left["groups"] + 1 < right:
        guess = (left["groups"] + right) // 2
        cp = driver.advance(engine, left, guess - left["groups"], 1 << 30)
        if len(cp["positive_tape"]) > target:
            right = guess
        else:
            left = cp

    count = driver.excursions(left["groups"])
    negative_base = driver.left(count)[0]
    positive = 0
    tape = list(map(int, left["positive_tape"]))
    rules = parse(driver.machine)
    for offset in range(5):
        state = driver.letter(count + offset - 1) if count + offset else "A"
        head = 0
        while head >= 0:
            if head == target:
                return {"cell": head, "first_entry": state, "groups_completed": left["groups"],
                        "root_request": count + offset + 1,
                        "steps": left["steps"] + positive + driver.left(count + offset)[0] - negative_base,
                        "positive_tape": "".join(map(str, tape)) + "0",
                        "preceding_group_sha256": checksum(left)}
            if head == len(tape):
                tape.append(0)
            symbol, delta, state = rules[state, tape[head]]
            tape[head] = symbol
            head += delta
            positive += 1
    raise ValueError("target not visited by the recorded ceiling")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine", type=Path, required=True)
    args = parser.parse_args()
    driver = Driver(31)
    tm = TapeMachine(driver.machine)
    for target in (2, 4, 6):
        visit = first_visit(driver, args.engine, driver.blank(), target, 40)
        while tm.head != target:
            assert tm.step()
        assert (tm.steps, tm.state) == (visit["steps"], visit["first_entry"])
        negative = []
        for copies, blocks in driver.left(visit["root_request"] - 1)[1]:
            negative.extend([symbol for block in blocks for symbol in reversed(block)] * copies)
        full = list(reversed(negative)) + list(map(int, visit["positive_tape"]))
        assert tm.tape == {i-len(negative): v for i, v in enumerate(full) if v}
    cp = driver.load(ROOT / "frontiers/runs/stream-31.json")
    for target, ceiling in ((138, 13 * 10**12), (140, 14 * 10**12)):
        print(json.dumps(first_visit(driver, args.engine, cp, target, ceiling)), flush=True)


if __name__ == "__main__":
    main()
