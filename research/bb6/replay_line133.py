"""Replay the line 133 checkpoint. Supply the pinned busy-beaver-explorer checkout
for both long simulations. Without an argument, run the literal blank-tape check.
"""

import argparse
import json
import sys
from pathlib import Path

from tracker import load_register


HERE = Path(__file__).resolve().parent
STATES = "ABCDEF"
RENAMING = dict(zip(STATES, "CDABEF"))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def instructions(machine):
    return {state: (row[:3], row[3:]) for state, row in zip(STATES, machine.split("_"))}


def check_tables(machine, sibling):
    renamed = instructions(sibling)
    for state, row in instructions(machine).items():
        for bit, op in enumerate(row):
            expected = "---" if op == "---" else op[0] + {"L": "R", "R": "L"}[op[1]] + RENAMING[op[2]]
            require(renamed[RENAMING[state]][bit] == expected, f"transition mismatch at {state}{bit}")


def literal_prefix(machine):
    # Words are in the reflected machine's left-to-right order. The current
    # head scans a fresh zero. Reflect the words back to absolute coordinates.
    samples = {
        58_272: (195, -618, [70, "11", 87, "11", 17, "11", 34, "01", 7, "0"]),
        62_084: (209, -660, [69, "01", 86, "01", 15, "01", 31, "01", 28, "0"]),
    }
    table = instructions(machine)
    ones = set()
    state, head, leftmost, visits = "A", 0, 0, 0
    for clock in range(max(samples) + 1):
        fresh = head < leftmost
        if fresh and state == "C":
            visits += 1
        leftmost = min(head, leftmost)
        if clock in samples:
            visit, position, tokens = samples[clock]
            require(fresh and (state, head, visits) == ("C", position, visit), f"frontier at {clock}")
            word = "".join("011" * t if isinstance(t, int) else t for t in tokens)
            expected = {head + i for i, bit in enumerate(reversed(word), 1) if bit == "1"}
            require(ones == expected, f"tape mismatch at {clock}")
            if clock == max(samples):
                break
        op = table[state][head in ones]
        require(op != "---", f"halt at {clock} defined steps")
        if op[0] == "1":
            ones.add(head)
        else:
            ones.discard(head)
        head += 1 if op[1] == "R" else -1
        state = op[2]
    print("Literal blank run matched visits 195 and 209 at 58,272 and 62,084 defined steps.")


def long_replay(project, sibling, checkpoint):
    engine = project / "holdouts" / sibling / "py"
    sys.path[:0] = [str(engine), str(project / "tools" / "py")]
    from accel import Acc, M, canon, zone
    from coqsim import CoqSim

    require(M == sibling, "the supplied accelerator uses a different transition table")
    seed = STATES.index(RENAMING["A"])
    by_round = CoqSim()
    by_round.st = seed
    for _ in range(checkpoint["rounds"]):
        if by_round.dirR and not by_round.front and by_round.st == 0:
            if not by_round.try_jump():
                by_round.back = by_round.canon()
        if not by_round.macro():
            by_round.step()
    require(by_round.dirR and not by_round.front and by_round.st == 0, "round replay missed the frontier")
    # A run stores its word nearest cell first. The back stack is ordered from
    # the far end toward the head, so reverse the word within each run.
    segments = [str(t) if isinstance(t, int) else ("".join(map(str, reversed(t[0]))), t[1])
                for t in by_round.back]
    words = checkpoint["normalized_left"]
    require(canon(segments) == words and by_round.steps == checkpoint["defined_steps"], "round replay differs")

    by_visit = Acc()
    by_visit.r.state = seed
    by_visit.r.next_visit()
    by_visit.visits = 1
    while by_visit.visits < checkpoint["visits"]:
        by_visit.advance(limit=checkpoint["visits"] - by_visit.visits)
    require(by_visit.visits == checkpoint["visits"], "visit count differs")
    require(by_visit.r.state == 0 and by_visit.r.at_right_end(), "visit replay missed the frontier")
    require(canon(by_visit.r.segs()) == words and by_visit.r.steps == by_round.steps, "visit replay differs")
    ones = sum(2 * t if isinstance(t, int) else t.count("1") for t in words)
    require(ones == checkpoint["ones"], "checkpoint population differs")
    print(f"Both runs matched all {len(words)} tape tokens, the blank right half and {by_round.steps} defined steps.")

    # The last two counters and their separator are in the domain of line133_recover.
    a, b = words[-3], words[-1]
    require(words[-4] == "11101" and words[-2] == "11" and a >= 1 and b >= 2, "unexpected recovery input")
    require(isinstance(words[-5], int), "expected a preceding 011 run at this checkpoint")
    for _ in range(5):
        by_visit.advance(limit=1)
    expected = words[:-5] + [words[-5] + 1, "11", a - 1, "11", b - 2, "01", 7, "0"]
    require(canon(by_visit.r.segs()) == expected, "recovery produced a different tape")
    require(by_visit.r.steps - by_round.steps == 6 * a + 12 * b + 139, "recovery clock differs")
    require(by_visit.advance() == 14, "expected a 14-visit jump")
    prefix, _, bits = zone(canon(by_visit.r.segs()))
    require(bits == [1] * 8 and prefix[-1] == "11101", "expected eight ones next to the marker")
    require(by_visit.advance(limit=1) == 1, "overflow visit failed")
    next_prefix, _, next_bits = zone(canon(by_visit.r.segs()))
    require(next_prefix == prefix[:-6] and next_bits == [1] + [0] * 10, "unexpected carry across the marker")
    print("Five recovery visits, a 14-visit jump, then an eight-bit overflow returning with eleven bits.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("explorer", type=Path, nargs="?", help="pinned busy-beaver-explorer checkout")
    args = parser.parse_args()
    rows = load_register()
    checkpoint = json.loads((HERE / "line133-checkpoint.json").read_text())
    row, sibling = rows[132], rows[580]["machine"]
    require((checkpoint["line"], checkpoint["machine_id"], checkpoint["machine"]) ==
            (int(row["line"]), int(row["machine_id"]), row["machine"]), "checkpoint identity mismatch")
    require((checkpoint["original_state"], checkpoint["normalized_state"]) == ("C", "A"), "wrong checkpoint states")
    check_tables(row["machine"], sibling)
    literal_prefix(row["machine"])
    if args.explorer is not None:
        long_replay(args.explorer.resolve(), sibling, checkpoint)


if __name__ == "__main__":
    main()
