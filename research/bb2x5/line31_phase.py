#!/usr/bin/env python3
"""Check the aligned line-31 reduction and reconstruct a physical blank checkpoint."""
import argparse
from itertools import product
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "frontiers"))
from checkpoints import atomic_json, checksum, holdouts
from longitudinal import Driver
from prior_sweeps import TapeMachine, parse

MACHINE = "1RB3RB---4RA2RA_2LA2RA3LB4LB1LB"
BAD = ("ABABAA", "ABABABB")
HEAD = ("", "B", "A", "AB", "AA", "AAB")
PHASE = (0, 0, 2, 2, 1, 1)


def alignment(x):
    if x < len(HEAD):
        return HEAD[x], PHASE[x]
    return ("BAAB", 2) if x % 2 else ("AAA", 0)


def transform(phase, word):
    output = []
    for letter in word:
        if letter == "A":
            output.append("BAA"[phase])
            phase = (phase + 1) % 3
        elif letter == "B":
            if phase == 0:
                output.append("A")
            phase = (phase - 1) % 3
        else:
            raise ValueError("invalid letter")
    return "".join(output), phase


def pair(word):
    return transform(2, transform(0, word)[0])[0]


def ordinary_rows(word):
    rows = []
    while word:
        next_word, p = transform(alignment(len(rows))[1], word)
        rows.append((len(word), p, word[:16]))
        word = next_word
    return rows


def physical(rows):
    """Return the first A2 coordinate, or the completed calls, prefixes and symbols."""
    calls, prefixes, tape = [], [], []
    for x, (n, p, w) in enumerate(rows):
        ghost, _ = alignment(x)
        expected = ghost[:min(n, len(ghost))]
        if not w.startswith(expected):
            raise ValueError(f"inconsistent preliminary letters at {x}")
        count = max(n - len(ghost), 0)
        prefix = w[len(ghost):]
        if x % 2 == 0:
            if not count:
                break
            if not prefix.startswith("A"):
                return x, calls, prefixes, "".join(tape)
        else:
            # The first real A at the parent already made two B calls here.
            if n < len(ghost):
                raise ValueError(f"missing preliminary odd-cell letters at {x}")
            count += 2
            prefix = "BB" + prefix
        tape.append("143"[p])
        calls.append(count)
        prefixes.append(prefix[:min(12, count)])
    if len(calls) % 2:
        raise ValueError("incomplete last pair")
    return None, calls, prefixes, "".join(tape)


def read_rows(stream):
    rows = []
    for line in stream.splitlines():
        x, n, p, w = line.split()
        n, p = int(n), int(p)
        if (int(x) != len(rows) or n < 1 or not 0 <= p < 3
                or len(w) != min(n, 16) or set(w) - {"A", "B"}):
            raise ValueError("invalid worker row")
        if rows and n > rows[-1][0]:
            raise ValueError("ordinary cells cannot increase the input count")
        rows.append((n, p, w))
    return rows


def run(engine, groups, split):
    proc = subprocess.run([str(engine.resolve()), str(groups), str(split)],
                          check=True, text=True, capture_output=True)
    rows = read_rows(proc.stdout)
    if not rows or rows[0][0] != 5 * groups:
        raise ValueError("worker did not process the requested root horizon")
    return rows


def checkpoint(driver, groups, rows):
    halt, counts, prefixes, tape = physical(rows)
    if halt is not None:
        raise ValueError(f"candidate A2 at {halt}; localize the first failing group")
    n = 5 * groups
    if counts[0] != n:
        raise ValueError("wrong number of physical root calls")
    left, _ = driver.left(n)
    if left != 2 * n * n + 3 * n:
        raise ValueError("negative clock mismatch")
    steps = left + 2 * sum(counts) - n
    state = {**driver.blank(), "groups": groups, "steps": steps,
             "positive_tape": tape, "state": driver.period[-1]}
    return state, prefixes


def candidate(prefixes):
    for x in range(0, len(prefixes) + 1, 2):
        w = prefixes[x] if x < len(prefixes) else ""
        if any(w.startswith(b) or b.startswith(w) for b in BAD):
            return x + 2
    raise AssertionError("missing frontier")


def literal_word(word):
    tm = TapeMachine(MACHINE)
    histories = []
    for letter in word:
        tm.state, tm.head = letter, 0
        if not histories:
            histories.append("")
        histories[0] += letter
        while tm.head >= 0:
            old = tm.head
            if not tm.step():
                return tm.head, histories, None
            if tm.head > old:
                if tm.head == len(histories):
                    histories.append("")
                histories[tm.head] += tm.state
    symbols = "".join(str(tm.tape[i]) for i in range(len(histories)))
    return None, histories, symbols


def cyclic_image(phase, word):
    repeats = 1 if (word.count("A") - word.count("B")) % 3 == 0 else 3
    image, end = transform(phase, word * repeats)
    assert end == phase
    length = (image + image).index(image, 1)
    return image[:length]


def four_cell_triggers():
    # The first parent A opens the pair. Subsequent entries use phases 1, 2.
    # At most nine inputs to an ordinary pair are needed for one output.
    def visit(p, q, emitted, word):
        if emitted in BAD:
            yield word
        elif any(b.startswith(emitted) for b in BAD):
            for c in "AB":
                middle, new_p = transform(p, c)
                out, new_q = transform(q, middle)
                yield from visit(new_p, new_q, emitted + out, word + c)

    return visit(1, 2, "", "A")


def checks(driver, engine):
    assert holdouts()[30] == driver.machine == MACHINE
    assert driver.period == "ABAAA" and driver.usual == "B" and driver.first == "BA"
    # Derive every ordinary transition from the literal instruction table.
    rules = parse(MACHINE)
    for p, symbol in enumerate((1, 4, 3)):
        for c in "AB":
            start, state, out = symbol, c, ""
            while True:
                start, move, state = rules[state, start]
                if move < 0:
                    assert state == "B"
                    break
                out += state
                state = "B"
            assert transform(p, c) == (out, (1, 4, 3).index(start))
    assert transform(0, "AAAA") == ("BAAB", 1)
    assert transform(2, "BAAB") == ("AAA", 2)
    for x in range(12):
        ghost, p = alignment(x)
        image, end = transform(p, ghost + ("" if x % 2 else "A"))
        assert image == alignment(x + 1)[0] and end == 1 + x % 2
    for w, expected in (("BAAAA", "ABBA"), ("ABBA", "AAAABBA"),
                        ("AAAABBA", "AAAABBA")):
        assert cyclic_image(2, cyclic_image(0, w)) == expected
    triggers = list(four_cell_triggers())
    lengths = list(map(len, triggers))
    minimum = min(lengths)
    shortest = [w for w in triggers if len(w) == minimum]
    assert (len(triggers), shortest, max(lengths), lengths.count(40)) == (3256, ["AABAAABAAAB"], 40, 1)
    for w in triggers:
        assert literal_word(w)[0] == 4 and literal_word(w[:-1])[0] is None

    tested = halted = 0
    for length in range(12):
        for suffix in product("AB", repeat=length):
            word = "A" + "".join(suffix)
            expected, hist, symbols = literal_word(word)
            found, calls, prefixes, tape = physical(ordinary_rows(word))
            assert expected == found, (word, expected, found)
            # The uniform pair map uses a three-letter prefix even at cell zero.
            aligned = "AAA" + word
            x = 0
            while len(aligned) >= 4 and aligned[3] == "A":
                aligned = pair(aligned)
                x += 2
            assert (x if len(aligned) >= 4 else None) == expected
            if found is None:
                assert calls == list(map(len, hist)) and symbols == tape
                assert all(w.startswith(p) for w, p in zip(hist, prefixes))
            else:
                halted += 1
            tested += 1
    print(f"{tested} supplied words checked against literal instructions, including {halted} halts.")
    print(f"{len(triggers)} minimal four-cell trigger prefixes, shortest {shortest[0]}, longest length 40.")
    if engine:
        for g in (1, 9, 41, 107):
            wanted = ordinary_rows(("AABAA" * g))
            for split in (0, 4, 200):
                assert run(engine, g, split) == wanted
            state, _ = checkpoint(driver, g, wanted)
            tm = TapeMachine(MACHINE)
            while tm.steps < state["steps"]:
                assert tm.step()
            assert (tm.head, tm.state) == (0, "A")
            assert "".join(str(tm.tape[i]) for i in range(len(state["positive_tape"]))) == state["positive_tape"]
            left, _ = driver.left(5 * g)
            assert left == 2 * (5 * g)**2 + 15 * g
        print("Four blank clocks and twelve worker/split comparisons passed.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine", type=Path)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--groups", type=int)
    parser.add_argument("--split", type=int, default=48)
    parser.add_argument("--checkpoint", type=Path)
    parser.add_argument("--compare", type=Path)
    args = parser.parse_args()
    driver = Driver(31)
    if not args.check and args.groups is None:
        parser.error("choose --check or --groups")
    if args.check:
        checks(driver, args.engine)
    if args.groups is not None:
        if not args.engine or not 1 <= args.groups <= (2**64 - 1) // 5 or args.split < 0:
            parser.error("a run needs an engine, a positive supported group count, and a nonnegative split")
        rows = run(args.engine, args.groups, args.split)
        state, prefixes = checkpoint(driver, args.groups, rows)
        if args.compare and driver.load(args.compare) != state:
            raise ValueError("saved physical checkpoint differs")
        if args.checkpoint:
            atomic_json(args.checkpoint, {"payload": state, "sha256": checksum(state)})
        print(f"{state['groups']} groups, {state['steps']} defined steps, last cell {len(prefixes)-1}.")
        print(f"First remaining A2 coordinate {candidate(prefixes)}.")
        for x in range(max(0, len(prefixes)-10), len(prefixes)):
            print(x, prefixes[x])


if __name__ == "__main__":
    main()
