#!/usr/bin/env python3
"""Check the aligned line-31 reduction and reconstruct a physical blank checkpoint."""
import argparse
from functools import cache
import hashlib
from itertools import product
from math import gcd
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "frontiers"))
from checkpoints import atomic_json, checksum, holdouts
from longitudinal import Driver, HALTED, literal_group
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


def longest_input(phases, output=""):
    """Maximum input length giving exactly the specified strip output."""
    a = b = 1
    rank = 0
    for phase in phases:
        rank += phase * b
        a, b = 3 * b, a + b
    return rank + a * output.count("A") + b * output.count("B")


def check_silent_rank():
    @cache
    def longest(phases, target):
        lengths = [] if target else [0]
        for letter in "AB":
            current = list(phases)
            for i, p in enumerate(phases):
                letter, current[i] = transform(p, letter)
                if not letter:
                    break
            if target.startswith(letter):
                lengths.append(1 + longest(tuple(current), target[len(letter):]))
        return max(lengths)

    for h in range(1, 6):
        for phases in product(range(3), repeat=h):
            for length in range(4 if h <= 3 else 1):
                for letters in product("AB", repeat=length):
                    word = "".join(letters)
                    assert longest_input(phases, word) == longest(phases, word)


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


def read_rows(stream, first=0):
    rows = []
    for line in stream.splitlines():
        x, n, p, w = line.split()
        n, p = int(n), int(p)
        if (int(x) != first + len(rows) or n < 1 or not 0 <= p < 3
                or len(w) != min(n, 16) or set(w) - {"A", "B"}):
            raise ValueError("invalid worker row")
        if rows and n > rows[-1][0]:
            raise ValueError("ordinary cells cannot increase the input count")
        rows.append((n, p, w))
    return rows


def run(engine, groups, split, last=None):
    command = [str(engine.resolve()), str(groups), str(split)]
    if last is not None:
        command.append(str(last))
    proc = subprocess.run(command,
                          check=True, text=True, capture_output=True)
    rows = read_rows(proc.stdout)
    if not rows or rows[0][0] != 5 * groups:
        raise ValueError("worker did not process the requested root horizon")
    return rows


def from_period56(engine, groups, split, path):
    cycles, remainder = divmod(groups, 3**32)
    if not cycles:
        return run(engine, groups, split)
    digest = hashlib.sha256()
    with path.open("rb") as archive:
        for block in iter(lambda: archive.read(4 << 20), b""):
            digest.update(block)
    if digest.hexdigest() != "f7229ff07bdf8c80e94c3a1ad3f778f2971212785b00f5b33c3325e5b65b62ae":
        raise ValueError("incorrect cut-56 period digest")
    one = run(engine, 3**32, split, 56)
    if (len(one) != 57 or one[56][0] != 53_427_204_485
            or any(row[1] != alignment(i)[1] for i, row in enumerate(one[:56]))):
        raise ValueError("the cut-56 period did not close upstream")
    extra = run(engine, remainder, split, 56) if remainder else []
    rows = []
    for i, (count, phase, prefix) in enumerate(one[:56]):
        n, end = extra[i][:2] if i < len(extra) else (0, phase)
        rows.append((cycles * count + n, end, prefix))
    n56 = cycles * one[56][0] + (extra[56][0] if len(extra) > 56 else 0)
    proc = subprocess.run([str(engine.resolve()), "--from56", str(path), str(n56)],
                          check=True, text=True, capture_output=True)
    tail = read_rows(proc.stdout, 56)
    if tail[0][0] != n56 or tail[0][2] != one[56][2]:
        raise ValueError("wrong cut-56 stream")
    return rows + tail


def check_period56(engine, split):
    first = run(engine, 3**32, split, 56)
    triple = run(engine, 3**33, split, 57)
    assert len(first) == 57 and len(triple) == 58
    assert all(row[1] == alignment(x)[1] for x, row in enumerate(first[:56]))
    assert all(row[1] == alignment(x)[1] for x, row in enumerate(triple[:57]))
    assert first[56][1] != alignment(56)[1]
    length = first[56][0]
    assert triple[56][0] == 3 * length
    # Over the three starts every A emits three letters, every B just one.
    twice_bs = 3 * length - triple[57][0]
    bs, remainder = divmod(twice_bs, 2)
    assert remainder == 0 and gcd(length, bs) == 1
    assert (length, bs) == (53_427_204_485, 15_648_460_017)
    print(f"Cut +56 has primitive period {length}, with {bs} Bs, in {3**32} root groups.")


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


def check_next_group(driver, state, rows):
    # Start the aligned cells in their computed end phases; newly encountered
    # aligned cells retain their specified initial phases.
    word = "AABAA"
    following = []
    x = 0
    while x < len(rows) or word:
        count, phase, prefix = rows[x] if x < len(rows) else (0, alignment(x)[1], "")
        emitted, end = transform(phase, word)
        following.append((count + len(word), end, (prefix + word)[:16]))
        word = emitted
        x += 1
    observed = literal_group(driver, state, 20 * (len(rows) + 12))
    halt = physical(following)[0]
    if halt is not None:
        assert observed["format"] == HALTED and observed["head"] == halt
        return observed
    expected, _ = checkpoint(driver, state["groups"] + 1, following)
    if expected != observed:
        raise ValueError("literal next group differs in its physical state or clock")
    return observed


def candidate(prefixes):
    for x in range(0, len(prefixes) + 1, 2):
        w = prefixes[x] if x < len(prefixes) else ""
        if any(w.startswith(b) or b.startswith(w) for b in BAD):
            return x + 2
    raise AssertionError("missing frontier")


def verify_continuation(driver, path, engine, target):
    rows = read_rows(path.read_text())
    groups, remainder = divmod(rows[0][0], 5)
    if remainder:
        raise ValueError("the starting ledger must end on a source group")
    start, _ = checkpoint(driver, groups, rows)
    check_next_group(driver, start, rows)
    expected = driver.load(target)
    extra = expected["groups"] - groups
    if extra <= 0:
        raise ValueError("the comparison checkpoint must follow the ledger")
    if driver.advance(engine, start, extra, 1 << 28) != expected:
        raise ValueError("the physical continuation differs from the saved checkpoint")
    print(f"Physical replay of {extra:,} groups matches the full checkpoint at "
          f"{expected['steps']:,} defined instructions.")


def first_visit(driver, boundary):
    """Replay one group and report the first arrival beyond its starting tape."""
    target = len(boundary["positive_tape"])
    tm = TapeMachine(driver.machine, map(int, boundary["positive_tape"]))
    old = driver.excursions(boundary["groups"])
    left = driver.left(old)[0]
    for finished in range(old, driver.excursions(boundary["groups"] + 1)):
        tm.head = 0
        tm.state = driver.letter(finished-1) if finished else "A"
        while tm.head >= 0:
            if tm.head == target:
                steps = boundary["steps"] + tm.steps + driver.left(finished)[0] - left
                return target, finished + 1, steps, tm.state, tm.tape.get(target, 0)
            if not tm.step():
                raise ValueError(f"halted before reaching +{target}")
        assert tm.state == driver.usual
    raise ValueError(f"the next group completes before reaching +{target}")


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


def check_rotation():
    period = "AABAA"
    for _ in range(18):
        assert period[0] == "A"
        rotated = period[1:] + period[0]
        period = cyclic_image(2, cyclic_image(1, rotated))
    assert len(period) == 7_751_148
    offset = 5_182_449
    sample = period[offset:offset+248]
    assert sample[:25] == period[:25] and sample[25] != period[25]
    assert literal_word(period[:248])[0] is None
    assert literal_word(sample[:-1])[0] is None
    head, histories, _ = literal_word(sample)
    assert head == 16 and histories[14].startswith(BAD) and histories[16] == "BA"
    print("Cut +36 shift: 25 matched entries, then literal A2 at +52 on input 248.")


def checks(driver, engine):
    assert holdouts()[30] == driver.machine == MACHINE
    assert driver.period == "ABAAA" and driver.usual == "B" and driver.first == "BA"
    check_silent_rank()
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
    assert pair("A") == "" and pair("B") == "A"
    assert transform(0, "AAAA") == ("BAAB", 1)
    assert transform(2, "BAAB") == ("AAA", 2)
    for x in range(12):
        ghost, p = alignment(x)
        image, end = transform(p, ghost + ("" if x % 2 else "A"))
        assert image == alignment(x + 1)[0] and end == 1 + x % 2
    for w, expected in (("BAAAA", "ABBA"), ("ABBA", "AAAABBA"),
                        ("AAAABBA", "AAAABBA")):
        assert cyclic_image(2, cyclic_image(0, w)) == expected
    for w, expected in (("ABAAA", "A"), ("A", "ABBAAAA"), ("ABBAAAA", "ABBAAAA")):
        assert cyclic_image(2, cyclic_image(1, w[1:] + w[:1])) == expected
    changed = ("AAAAABA" + "AAAABBA" * 5)[3:]
    assert literal_word(changed[:27])[0] is None
    assert literal_word(changed[:28])[0] == 8
    for length, delta in product(range(3), repeat=2):
        # Four successive triples would require four nonzero displacements.
        residues = []
        for _ in range(4):
            residues.append(delta)
            length, delta = (2 * length + delta) % 3, length
        assert 0 in residues
    for symbol, p in product(range(3), repeat=2):
        aligned_out = (transform(p, " AB"[symbol])[0] if symbol else "")
        assert {"": 0, "A": 1, "B": 2}[aligned_out] == (-symbol - symbol**2*p**2) % 3
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
    check_rotation()
    if engine:
        from test_longitudinal import cells
        for g in (1, 9, 41, 107):
            wanted = ordinary_rows(("AABAA" * g))
            for split in (0, 4, 200):
                assert run(engine, g, split) == wanted
                assert run(engine, g, split, 5) == wanted[:6]
            state, _ = checkpoint(driver, g, wanted)
            check_next_group(driver, state, wanted)
            tm = TapeMachine(MACHINE)
            while tm.steps < state["steps"]:
                assert tm.step()
            assert (tm.head, tm.state) == (0, "A")
            assert tm.tape == cells(driver, state)
            if g == 1:
                visit = first_visit(driver, state)
                while tm.head != 4:
                    assert tm.step()
                assert visit == (4, 7, tm.steps, tm.state, tm.tape.get(4, 0))
            left, _ = driver.left(5 * g)
            assert left == 2 * (5 * g)**2 + 15 * g
        print("Four blank clocks and twelve worker/split comparisons passed.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine", type=Path)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--check-period56", action="store_true")
    parser.add_argument("--verify-continuation", type=Path, metavar="ROWS",
                        help="replay from an aligned ledger to --compare with the physical worker")
    parser.add_argument("--physical-engine", type=Path, help="compiled frontiers/longitudinal.cpp")
    parser.add_argument("--next-first-visit", type=Path, metavar="CHECKPOINT",
                        help="locate the first new positive cell within the following group")
    parser.add_argument("--groups", type=int)
    parser.add_argument("--split", type=int, default=48)
    parser.add_argument("--packed56", type=Path, help="reuse the verified cut-56 period for a long run")
    parser.add_argument("--checkpoint", type=Path)
    parser.add_argument("--compare", type=Path)
    args = parser.parse_args()
    driver = Driver(31)
    if not (args.check or args.check_period56 or args.verify_continuation or args.next_first_visit
            or args.groups is not None):
        parser.error("choose a check or supply a group count")
    if args.next_first_visit:
        cell, request, steps, state, symbol = first_visit(driver, driver.load(args.next_first_visit))
        print(f"First visit to +{cell} on root request {request:,}, after {steps:,} defined "
              f"instructions, reading {state}{symbol}.")
    if args.verify_continuation:
        if not args.physical_engine or not args.compare:
            parser.error("--verify-continuation needs --physical-engine and --compare")
        verify_continuation(driver, args.verify_continuation, args.physical_engine, args.compare)
    if args.check_period56:
        if not args.engine or args.split < 0:
            parser.error("--check-period56 needs an engine and a nonnegative split")
        check_period56(args.engine, args.split)
    if args.check:
        checks(driver, args.engine)
    if args.groups is not None:
        if not args.engine or not 1 <= args.groups <= (2**64 - 1) // 5 or args.split < 0:
            parser.error("a run needs an engine, a positive supported group count, and a nonnegative split")
        rows = (from_period56(args.engine, args.groups, args.split, args.packed56)
                if args.packed56 else run(args.engine, args.groups, args.split))
        halt, _, histories, _ = physical(rows)
        if halt is not None:
            assert halt >= 2 and halt % 2 == 0
            parent = next(w for w in BAD if histories[halt-2].startswith(w))
            head, local, _ = literal_word(parent)
            assert head == 2 and local[2] == "BA"
            if args.compare or args.checkpoint:
                raise ValueError(f"literal A2 at +{halt}; there is no completed checkpoint at this horizon")
            print(f"Blank A2 at +{halt} within {args.groups} groups. "
                  f"The +{halt-2} input {parent} gives literal BA at the fresh cell.")
            return
        state, prefixes = checkpoint(driver, args.groups, rows)
        next_state = check_next_group(driver, state, rows)
        if args.compare and driver.load(args.compare) != state:
            raise ValueError("saved physical checkpoint differs")
        if args.checkpoint:
            atomic_json(args.checkpoint, {"payload": state, "sha256": checksum(state)})
        print(f"{state['groups']} groups, {state['steps']} defined steps, last cell {len(prefixes)-1}.")
        if next_state["format"] == HALTED:
            print(f"The next group halts at +{next_state['head']} after {next_state['steps']} instructions.")
        else:
            print(f"First remaining A2 coordinate {candidate(prefixes)}; next group replayed literally on the positive tape.")
        for x in range(max(0, len(prefixes)-10), len(prefixes)):
            print(x, prefixes[x])


if __name__ == "__main__":
    main()
