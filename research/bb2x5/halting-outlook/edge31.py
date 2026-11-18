#!/usr/bin/env python3
"""Check the line 31 pair trigger, weighted flux, clock and actual cut prefixes."""
from collections import Counter
from itertools import product
from pathlib import Path
import argparse
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path[:0] = [str(ROOT), str(ROOT / "frontiers")]
from checkpoints import checksum
from longitudinal import Driver
from prior_sweeps import TapeMachine, parse
from test_longitudinal import cells

MACHINE = "1RB3RB---4RA2RA_2LA2RA3LB4LB1LB"
BAD = ("ABABAA", "ABABABB")
POTENTIAL = [36, 0, 27, 18, 9]
WEIGHT = {"A": 4, "B": 3}


def cell_step(rules, start, letter):
    symbol, fresh = start
    output = ""
    state = letter
    while (state, symbol) in rules:
        symbol, move, state = rules[state, symbol]
        if move < 0:
            return (symbol, fresh), output
        output += state
        # Both virgin return letters are taken from the literal instructions.
        state = "BA"["AB".index(state)] if fresh else "B"
        fresh = False
    return None, output


def check_table():
    rules = parse(MACHINE)
    todo = [(0, True)]
    known = set(todo)
    while todo:
        start = todo.pop()
        for entry in "AB":
            after, out = cell_step(rules, start, entry)
            if after is None:
                assert start == (2, True) and entry == "A"
                continue
            lhs = 7 * sum(WEIGHT[c] for c in out) - 3 * WEIGHT[entry]
            assert lhs >= POTENTIAL[after[0]] - POTENTIAL[start[0]]
            if after not in known:
                todo.append(after)
                known.add(after)
    return len(known)


def trace_word(word):
    # Literal right half with externally supplied entry letters. A halt beyond
    # coordinate 2 cannot make a previously safe pair fail its local criterion.
    machine = TapeMachine(MACHINE)
    prefixes = {}
    for entry in word:
        machine.state, machine.head = entry, 0
        while machine.head >= 0:
            old = machine.head
            if not machine.step():
                return machine.head, prefixes
            if machine.head > old:
                prefixes[machine.head] = prefixes.get(machine.head, "") + machine.state
    return None, prefixes


def check_words():
    counts = Counter()
    for k in range(12):
        for suffix in product("AB", repeat=k):
            word = "A" + "".join(suffix)
            head, prefixes = trace_word(word)
            counts["cases"] += 1
            assert prefixes[1].startswith("BB")
            assert (head == 2) == word.startswith(BAD), (word, head)
            if head is not None:
                assert head % 2 == 0
                parent = word if head == 2 else prefixes[head - 2]
                assert parent.startswith(BAD)
                counts["literal halts"] += 1
            elif 2 in prefixes:
                assert prefixes[2][0] == "A"
    return counts


def check_actual(driver, engine):
    for groups in (1, 9, 41, 107):
        cp, hist = driver.run_batch(engine, driver.blank(), groups, 1 << 22, 32)
        tm = TapeMachine(MACHINE)
        seen = {0: "A"}
        while tm.steps < cp["steps"]:
            old = tm.head
            assert tm.step()
            if tm.head > old and tm.head >= 0 and tm.steps < cp["steps"]:
                word = seen.get(tm.head, "")
                seen[tm.head] = word + tm.state if len(word) < 32 else word
        assert hist == [seen[i] for i in range(len(seen))]
        assert (tm.steps, tm.head, tm.state, tm.tape) == (cp["steps"], 0, cp["state"], cells(driver, cp))
    print("Four blank-run comparisons matched head, state, both tape halves, cut histories and clock.")


def check_trace(driver):
    doc = json.loads((HERE / "edge31_prefixes.json").read_text())
    payload = doc["payload"]
    assert checksum(payload) == doc["sha256"]
    cp = driver.load(ROOT / "frontiers/runs/stream-31.json")
    assert payload["checkpoint_sha256"] == checksum(cp)
    words = payload["entry_prefixes"]
    assert all(word.startswith("A") and not word.startswith(BAD) for word in words[::2])
    assert all(word.startswith("BB") for word in words[1::2])
    print(f"Through {payload['groups']} source groups: {len(words)} cuts, {payload['steps']} raw steps.")
    print("Even coordinates starting ABAB:", [(i, w[:8]) for i, w in enumerate(words) if i % 2 == 0 and w.startswith("ABAB")])
    print("Final even and odd prefixes:", words[-2:])
    print("Interior target occurrences among the 32-letter even-cut samples:",
          sum(w.startswith(BAD, i) for w in words[::2] for i in range(1, len(w))))

    # The new continuation follows the old lifetime prefixes in temporal order.
    rolling = [w[:8] for w in words]
    groups = cp["groups"]
    for row in (HERE / "edge31_batches.jsonl").read_text().splitlines():
        record = json.loads(row)
        assert record["status"] == "unknown" and record["from_groups"] == groups
        groups = record["groups"]
        batch = record["entry_prefixes"]
        rolling.extend([""] * (len(batch) - len(rolling)))
        for i, prefix in enumerate(batch):
            rolling[i] = (rolling[i] + prefix)[:8]
    end = driver.load(HERE / "edge31_checkpoint.json")
    assert groups == end["groups"] and record["steps"] == end["steps"]
    assert len(rolling) == len(end["positive_tape"]) == 142
    assert all(not any(t.startswith(w) or w.startswith(t) for t in BAD) for w in rolling[:140:2])
    assert rolling[-2:] == ["ABA", "BBB"]
    print(f"Through {groups} groups: {end['steps']} steps; next candidate A2 at 142 or farther.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine", type=Path)
    args = parser.parse_args()
    driver = Driver(31)
    assert driver.machine == MACHINE and driver.first == "BA" and driver.usual == "B"
    print("Reachable local states satisfying the weighted inequality:", check_table())
    print("Literal supplied words:", dict(check_words()))
    assert all(driver.block(n)[:2] == (n-1, 4*n+1) for n in range(1, 60))
    if args.engine:
        check_actual(driver, args.engine)
    check_trace(driver)


if __name__ == "__main__":
    main()
