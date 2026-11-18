"""Closure certificate and independent literal checks for line6-prefix.md."""
from collections import defaultdict
from pathlib import Path
import argparse
import re
import subprocess

from line6 import HEADER, MACHINE, literal_probe, probe
from prior_sweeps import TapeMachine


def prepend(word, profile):
    """Greedy matching profile and change in unmatched twos."""
    change = 0
    for symbol in reversed(word):
        if symbol == "0":
            profile = "N"
        elif symbol == "2":
            if profile == "S":
                profile = "N"
            else:
                change += 1
                profile = "T"
        elif symbol == "3":
            if profile == "T":
                change -= 1
                profile = "N"
            else:
                profile = "S"
        else:
            raise ValueError(symbol)
    return profile, change


def check_closure():
    bounds = {}
    for source in "NTS":
        for target in ("NS" if source == "S" else "NTS"):
            bounds[source, "B", target] = -int(source == "T")
        bounds[source, "A", "N"] = -int(source == "T")

    def check(source, state, target, left, right, change):
        source, before = prepend(left, source)
        target, after = prepend(right, target)
        assert change + after - before <= bounds[source, state, target]

    for profile in "NTS":
        check(profile, "B", profile, "0", "", 0)
    prefixes = {("B", "B"): "23", ("B", "A"): "32", ("A", "B"): "3"}
    for (source, first, middle), cost in bounds.items():
        check(source, first, middle, "32", "23" if first == "B" else "32", cost)
        check(source, first, middle, "33", "33" if first == "B" else "00", cost)
        if first == "B":
            check(source, "A", middle, "30", "032", cost)
        for (start, second, end), extra in bounds.items():
            if start == middle and (first, second) in prefixes:
                check(source, second, end, "2", prefixes[first, second], cost + extra)


def traffic(history, two):
    assert len(history) % 2 == 0
    total = 0
    for request, reply in zip(history[::2], history[1::2]):
        toggle = request == "A" and reply == "B"
        total += -1 if toggle and two else 1
        two = not two if toggle else reply == "B"
    return total


def check_unary(n, expected):
    tm = TapeMachine(MACHINE, [2] * n)
    tm.state = "B"
    histories = defaultdict(list)
    histories[0].append("B")
    while tm.head >= 0:
        before = tm.head
        assert tm.step()
        histories[max(before, tm.head)].append(tm.state)
    assert tm.steps >= n * (n + 1) + 1
    assert sum(map(len, histories.values())) == tm.steps + 1
    assert sum(value == 2 for value in tm.tape.values()) == n + 1
    prefix_count = 0
    for cut in range(max(histories) + 1):
        history = histories[cut]
        assert traffic(history, cut < n) == n+1-prefix_count-max(n-cut, 0)
        prefix_count += tm.tape.get(cut) == 2
        if expected is not None and cut <= n:
            digest = 0
            for state in history:
                digest = (131*digest + (1 if state == "A" else 2)) % (1 << 64)
            assert expected[n, cut] == (len(history), digest)
    assert len({tuple(histories[i]) for i in range(n+1)}) == n+1
    offset = int(tm.state == "B")
    residual = "".join(str(tm.tape.get(i, 0)) for i in range(offset, max(tm.tape)+1))
    assert prepend(residual, "N")[1] == 0


def check_suffix_examples():
    # A single call to the suffix starts and ends at a header boundary.
    for offset, before, after in ((0, 31, 17), (1, 28, 48), (2, 27, 13)):
        for suffix, verdict in (("0", "B"), ("3", "A")):
            word = HEADER[offset:]
            tm = TapeMachine(MACHINE, map(int, word + suffix))
            tm.state = "B"
            events = []
            while tm.head >= 0:
                previous = tm.head
                if not tm.step():
                    break
                if max(previous, tm.head) == len(word):
                    events.append((tm.steps, tm.state))
            cost = 1 if verdict == "B" else 5
            assert events == [(before, "B"), (before+cost, verdict)]
            assert tm.steps == before + cost + (after if verdict == "B" else 0)
            assert tm.head == (-1 if verdict == "B" else len(word)-1)
    for offset, verdict, steps in ((3,"B",17),(4,"B",27),(5,"B",9),
                                  (6,"A",5),(7,"B",1),(8,"B",1)):
        word = HEADER[offset:]
        tm = TapeMachine(MACHINE, map(int, word))
        tm.state = "B"
        while tm.head >= 0:
            assert tm.head < len(word) and tm.step()
        assert (tm.state, tm.steps) == (verdict, steps)
    control = "322300003"
    for i in range(len(control)):
        visible = re.match(r"(?:3[23])*30(?:3[23])*0", control[i:]+"000")
        assert literal_probe(control[i:]).state == ("A" if visible else "B")
    first = literal_probe(control)
    assert first.state == "B" and first.steps == 19
    second = literal_probe("32" + first.word)
    assert second.state == "H" and second.steps == 36
    word = ""
    for _ in range(113):
        result = probe(word)
        assert result.state == "B"
        word = "32" + result.word
    assert literal_probe(word[10:]).state == "A" and literal_probe(word[10:]).steps == 181
    tm = TapeMachine(MACHINE, map(int, word))
    tm.state = "B"
    events = []
    while tm.head >= 0:
        previous = tm.head
        assert tm.step()
        if max(previous, tm.head) == 10:
            events.append((tm.steps, tm.state))
    assert events == [(32,"A"),(33,"B"),(34,"A"),(189,"B")]
    assert (tm.state,tm.steps) == ("B",207)


def check_suffix_survey(binary, epochs):
    totals = [0, 0, 0, 0]
    exceptions = []
    for epoch in range(1, epochs+1):
        rows = subprocess.check_output([binary, str(epoch), "--suffixes"], text=True).splitlines()
        summary = rows[-1].split()
        assert summary[::2] == ["suffixes_A","B","H","unexpected","longest_steps","at_offset"]
        for i in range(4):
            totals[i] += int(summary[2*i+1])
        if int(summary[7]):
            word = next(s[5:] for s in rows if s.startswith("word "))
            heads = len(re.match(r"(?:322323300)*", word)[0])
            offsets = []
            for i in range(len(word)):
                forced_a = re.match(r"(?:3[23])*30(?:3[23])*0", word[i:]+"000")
                if probe(word[i:]).state != ("A" if forced_a else "B"):
                    offsets.append(i)
            assert len(offsets) == int(summary[7])
            exceptions.append((epoch, offsets, heads))
    if epochs == 376:
        assert totals == [3065,270826,0,12]
        assert all(offsets == [heads+1] for _,offsets,heads in exceptions)
    print("Suffix totals (A, B, H, exceptions)", totals)
    print("Exceptional epochs and offsets", [(n,ofs) for n,ofs,_ in exceptions])


def main():
    args = argparse.ArgumentParser()
    args.add_argument("--binary", type=Path)
    args.add_argument("--suffix-epochs", type=int, default=0)
    args.add_argument("--width", type=int, default=100)
    options = args.parse_args()
    if options.width < 0:
        args.error("width must be nonnegative")
    check_closure()
    check_suffix_examples()
    if options.suffix_epochs:
        if not options.binary:
            args.error("--suffix-epochs requires --binary")
        check_suffix_survey(options.binary.resolve(), options.suffix_epochs)
    witness = "3223323232003223323232320032"
    assert prepend(witness, "N")[1] == 0
    assert probe(witness) == literal_probe(witness)
    assert probe(witness).state == "A" and probe(witness).steps == 511
    neighbor = witness[:14] + "3223" + witness[18:]
    assert probe(neighbor) == literal_probe(neighbor)
    assert probe(neighbor).state == "B" and probe(neighbor).steps == 885
    for word, width, state, steps in ((witness, 35, "A", 511), (neighbor, 39, "B", 885),
                                      ("30" + witness, 37, "H", 513)):
        tape = TapeMachine(MACHINE, map(int, word))
        tape.state = "B"
        rightmost = -1
        while tape.head >= 0:
            rightmost = max(rightmost, tape.head)
            if not tape.step():
                break
        outcome = "H" if tape.head >= 0 else tape.state
        assert (rightmost + 1, outcome, tape.steps) == (width, state, steps)
    tm = TapeMachine(MACHINE, map(int, "0" + witness))
    while tm.step():
        pass
    assert (tm.steps, tm.head, tm.state, tm.tape[tm.head]) == (512, 0, "A", 1)
    expected = None
    if options.binary:
        expected = {}
        output = subprocess.check_output(
            [options.binary.resolve(), str(options.width+1), "--histories"], text=True)
        for line in output.splitlines():
            if line.startswith("cut "):
                n, cut, length, digest = map(int, line.split()[1:])
                expected[n, cut] = (length, digest)
        assert len(expected) == (options.width+1)*(options.width+2)//2
    for n in range(options.width+1):
        check_unary(n, expected)
    print(f"Closure, 512-step control, and literal unary widths 0..{options.width} checked.")


if __name__ == "__main__":
    main()
