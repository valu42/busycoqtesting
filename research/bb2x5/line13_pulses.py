"""Blank growth on line 13, with literal checks of the single-pulse reduction."""
import argparse
from itertools import product
from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "frontiers"))
from checkpoints import checksum
from longitudinal import Driver, literal_group
from prior_sweeps import TapeMachine, parse

MACHINE = "1RB3RA3RB4LA1LA_1LB2LA1LA---1RB"
A, B, C = 1, 2, 3
WORDS = ("", "A", "B", "BA")
# Each pair is (new tape digit, packet to the right). Zero is silence.
CELL = {
    1: ((1, 0), (4, A), (2, 0), (4, B)),
    2: ((2, 0), (4, B), (1, 0), (4, A)),
    4: ((4, 0), (1, 0), (4, C), (1, C)),
}


def send(tape, packet):
    """Pass one packet through the given occupied strip, in place."""
    for pos, digit in enumerate(tape):
        tape[pos], packet = CELL[digit][packet]
        if not packet:
            break
    return packet


def first_returns(width):
    """Next outgoing packet for every binary starting strip under repeated C.

    A one bit means digit 4. The leftmost cell is the low bit. All cells
    traversed by the outgoing packet finish on 1 or 4.
    """
    table = [(1, C, 0)]
    for i in range(width):
        following = []
        for last in (1, 4):
            for bits in range(len(table)):
                digit = last
                elapsed = 0
                while True:
                    wait, packet, bits = table[bits]
                    elapsed += wait
                    digit, packet = CELL[digit][packet]
                    if packet:
                        assert digit in (1, 4)
                        following.append((elapsed, packet, bits | ((digit == 4) << i)))
                        break
        table = following
    return table


def extension(binary, tables):
    """Compute the first crossing of binary + 21, returning its pre-crossing strip too."""
    width = min(len(binary), len(tables) - 1)
    low = sum((digit == 4) << i for i, digit in enumerate(binary[:width]))
    tape = list(binary[width:]) + [2, 1]
    elapsed = 0
    while True:
        before = tape.copy()
        wait, packet, low = tables[width][low]
        elapsed += wait
        outgoing = send(tape, packet)
        if outgoing:
            assert outgoing in (A, B)
            assert (elapsed % 2 == 1) == (outgoing == A)
            result = [4 if low >> i & 1 else 1 for i in range(width)] + tape
            assert set(result) <= {1, 4}
            assert all(result[j:j+3] != [1, 4, 1] for j in range(len(result) - 2))
            return elapsed, outgoing, result, before, packet


def literal_strip(digits, requests):
    tm = TapeMachine(MACHINE, digits)
    entries = []
    for letter in requests:
        tm.head, tm.state = 0, letter
        while tm.head >= 0:
            if tm.head == len(digits):
                entries.append(tm.state)
            if not tm.step():
                return tm, entries, False
    return tm, entries, True


def check_local(driver):
    assert driver.machine == MACHINE
    rules = parse(MACHINE)
    for digit, packet in product(CELL, (A, B, C)):
        s = digit
        emitted = ""
        for q in WORDS[packet]:
            while True:
                s, move, q = rules[q, s]
                if move < 0:
                    assert q == "A"
                    break
                emitted += q
                q = "A"  # Child already visited.
        new, child = CELL[digit][packet]
        assert (s, emitted) == (new, WORDS[child])
        assert ((digit == 2) ^ (new == 2)) == ((packet in (B, C)) ^ (child in (B, C)))

    pair = [2, 1]  # Fresh pair after the leading A.
    ref = "ABABB"
    assert "".join(WORDS[send(pair, A if q == "A" else B)] for q in ref[1:]) == "ABAB"
    assert pair == [4, 4]
    assert "".join(WORDS[send(pair, A if q == "A" else B)] for q in ref) == "BABAB"
    assert pair == [4, 4]

    # Literal four-cell projection. The first five root entries initialize
    # the periodic boundary. Each later group sends its BA on entry four.
    tm = TapeMachine(MACHINE)
    outputs = []
    crossing_counts = [0] * 4
    for completed in range(15):
        tm.head = 0
        tm.state = "A" if not completed else driver.letter(completed - 1)
        at_four = ""
        while tm.head >= 0:
            old = tm.head
            assert tm.step()
            if tm.head == old + 1 and 1 <= tm.head <= 4:
                crossing_counts[tm.head - 1] += 1
                if tm.head == 4:
                    at_four += tm.state
        outputs.append(at_four)
        if completed % 5 == 4:
            q = (completed + 1) // 5
            assert [tm.tape[x] for x in range(4)] == [1, 1, 4, 4]
            assert crossing_counts == [3*q+1, 3*q, q+1, 2*q-1]
    assert outputs == ["", "", "", "A", ""] + ["", "", "", "BA", ""] * 2


def check_growth():
    tables = [first_returns(n) for n in range(13)]
    # Compare the pulse boundary with the completely literal two-way machine.
    # The reference simulates from the initial blank, including all negative visits.
    tm = TapeMachine(MACHINE)
    root_returns = 0

    def step():
        nonlocal root_returns
        old = tm.head
        assert tm.step()
        root_returns += old == -1 and tm.head == 0

    binary = []
    ticks = 0
    for even in range(6, 22, 2):
        wait, packet, binary, _, _ = extension(binary, tables)
        ticks += wait
        assert packet == A
        while tm.head != even:
            step()
        assert tm.state == "A" and tm.tape.get(even, 0) == 0
        # Complete this root excursion, then the following one, reaching
        # the canonical boundary of group ticks+1.
        for _ in range(2):
            while tm.head >= 0:
                step()
            while tm.head < 0:
                step()
        tape = [tm.tape[x] for x in range(even + 2)]
        assert tape == [1, 1, 4, 4] + binary + [2, 1]
        assert tm.state == "B" and tm.head == 0
        assert root_returns == 5*(ticks+1)
        print(f"Cell {even} first reached on pulse {ticks}")

    # This nonblank prefix tests the proposed induction from a run of odd gaps.
    binary = [int(c) for c in "44441111114144144141"]
    ticks = 0
    gaps = []
    for _ in range(16):
        wait, packet, binary, before, incoming = extension(binary, tables)
        ticks += wait
        gaps.append(wait)
        if packet == B:
            tm, visits, finished = literal_strip(before, WORDS[incoming])
            assert not finished and visits == ["B"]
            assert (tm.head, tm.state, tm.tape[tm.head]) == (len(before) - 1, "B", 3)
            break
    assert len(gaps) == 16 and all(x % 2 for x in gaps[:-1]) and gaps[-1] % 2 == 0
    assert ticks == 12_212_553
    print("Altered binary prefix, successive gaps:", *gaps)


def literal_opening(driver, state, cell):
    """Locate the two rightward arrivals in the next canonical root group."""
    tm = TapeMachine(MACHINE, map(int, state["positive_tape"]))
    old = driver.excursions(state["groups"])
    base = state["steps"] - driver.left(old)[0]
    hits = {}
    for completed in range(old, old + 5):
        tm.head = 0
        tm.state = driver.letter(completed - 1)
        left_clock = driver.left(completed)[0]
        while tm.head >= 0:
            previous = tm.head
            assert tm.step()
            if tm.head == previous + 1 and tm.state == "A" and tm.head in (cell-1, cell):
                hits.setdefault(tm.head, base + left_clock + tm.steps)
    result = literal_group(driver, state, 20_000)
    assert len(result["positive_tape"]) == cell + 2
    assert result["positive_tape"] == "".join(str(tm.tape[x]) for x in range(cell + 2))
    assert result["steps"] == base + driver.left(old + 5)[0] + tm.steps
    return hits, result


def rank_search(engine, groups, additional, depth, tape):
    command = [str(engine.resolve()), str(groups), str(additional), str(depth), tape]
    answer = subprocess.run(command, check=True, text=True, stdout=subprocess.PIPE)
    return [line.split() for line in answer.stdout.splitlines()]


def check_ranks(engine):
    subprocess.run([str(engine.resolve()), "--check"], check=True)
    # Independent scalar packet traces from a small, genuine canonical tape.
    groups = 1
    tape = [2, 1]
    for _ in range(200):
        packet = send(tape, C)
        if packet:
            assert packet == A
            tape.extend([2, 1])
        groups += 1
    seed = "1144" + "".join(map(str, tape))
    expected = []
    for i in range(30_000):
        packet = send(tape, C)
        if packet:
            assert packet == A
            expected.append(["A", str(4 + len(tape)), str(groups + i)])
            tape.extend([2, 1])
    expected.append(["last_visited", str(3 + len(tape))])
    for depth in (0, 1, 4, 8, 13):
        assert rank_search(engine, groups, 30_000, depth, seed) == expected
    # Also check a partial startup and the first two pulse ranks on a virgin tail.
    assert rank_search(engine, groups, 0, 13, seed) == [["last_visited", str(len(seed)-1)]]
    assert rank_search(engine, 1, 2, 0, "114421") == [
        ["A", "6", "1"], ["A", "8", "2"], ["last_visited", "9"]]
    # Altered tapes give genuine B outputs. Compare the whole search prefix
    # including its terminal event, for every short binary seed.
    for bits in product((1, 4), repeat=6):
        word = list(bits) + [2, 1]
        data = "1144" + "".join(map(str, word))
        expected = []
        for pulse in range(1, 129):
            packet = send(word, C)
            if packet == B:
                expected.append(["B3", str(len(word)+3), str(pulse)])
                break
            if packet == A:
                expected.append(["A", str(len(word)+4), str(pulse)])
                word.extend([2, 1])
        else:
            expected.append(["last_visited", str(len(word)+3)])
        assert rank_search(engine, 1, 128, 4, data) == expected
    print("Pulse ranks and first B3 agree with scalar replay.")


def saved_record():
    document = json.loads((ROOT / "frontiers/runs/line13-pulses.json").read_text())
    record = document["payload"]
    assert checksum(record) == document["sha256"] and record["machine"] == MACHINE
    driver = Driver(13)
    seed = driver.load(ROOT / "frontiers/runs/stream-13.json")
    assert seed["groups"] == record["start_groups"]
    last = seed["groups"] - 1
    even = len(seed["positive_tape"])
    for opening in record["openings"]:
        assert opening["even_cell"] == even and last < opening["pulse"]
        if "before" in opening:
            state = opening["before"]
            assert state["machine"] == MACHINE and state["groups"] == opening["pulse"]
            assert len(state["positive_tape"]) == even
            hits, _ = literal_opening(driver, state, even)
            assert hits == {even-1: opening["odd_arrival_step"], even: opening["even_arrival_step"]}
        last = opening["pulse"]
        even += 2
    assert record["endpoint"]["groups"] > last
    assert len(record["endpoint"]["positive_tape"]) == even
    return record


def verify_native(engine, record):
    """Independent replay with the repository's A/B stream engine and literal final groups."""
    driver = Driver(13)
    state = driver.load(ROOT / "frontiers/runs/stream-13.json")
    for entry in record["openings"]:
        pulse, cell = entry["pulse"], entry["even_cell"]
        gap = pulse - state["groups"]
        if gap:
            state, _ = driver.run_batch(engine, state, gap, 1_400_000_000, 0, 1_000_000_000_000)
        assert len(state["positive_tape"]) == cell
        if "before" in entry:
            assert state == entry["before"]
        hits, state = literal_opening(driver, state, cell)
        assert set(hits) == {cell - 1, cell}
        if "odd_arrival_step" in entry:
            assert [hits[cell - 1], hits[cell]] == [entry["odd_arrival_step"], entry["even_arrival_step"]]
        assert state["format"] == "bb2x5-longitudinal-v1" and len(state["positive_tape"]) == cell + 2
        assert state["groups"] == pulse + 1 and state["positive_tape"].endswith("21")
        print(f"Literal opening at cell {cell} on pulse {pulse}. Group ended at {state['steps']} steps.", flush=True)
    target = record["endpoint"]
    if state["groups"] < target["groups"]:
        state, _ = driver.run_batch(engine, state, target["groups"] - state["groups"],
                                    1_400_000_000, 0, 1_000_000_000_000)
    assert state == target
    print("Full native endpoint agrees.")


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run with assertions enabled.")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--native", type=Path, help="Also run the long independent A/B replay")
    parser.add_argument("--rank", type=Path, help="Check the compiled pulse-rank search")
    parser.add_argument("--until-groups", type=int, help="Continue the rank search from the master checkpoint")
    parser.add_argument("--shallow", type=int, default=51, help="Mature cells in the dyadic startup and period")
    args = parser.parse_args()
    if args.until_groups is not None and args.rank is None:
        parser.error("--until-groups requires --rank")
    record = saved_record()
    check_local(Driver(13))
    check_growth()
    if args.rank:
        check_ranks(args.rank)
        if args.until_groups is not None:
            seed = Driver(13).load(ROOT / "frontiers/runs/stream-13.json")
            extra = args.until_groups - seed["groups"]
            if extra < 0:
                parser.error("target precedes the starting checkpoint")
            for line in rank_search(args.rank, seed["groups"], extra, args.shallow, seed["positive_tape"]):
                print(*line)
    if args.native:
        verify_native(args.native, record)
