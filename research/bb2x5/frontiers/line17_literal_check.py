"""Independent raw-instruction checker for short intervals at any line-17 header.

Usage: python3 line17_literal_check.py --self-test
       python3 line17_literal_check.py START.json END.json

The second form replays all intervening epochs, so use nearby checkpoints even
when the absolute clocks are enormous. The fixed register is run literally.
"""
import argparse
import hashlib
import json
from pathlib import Path

MACHINE = "1RB2RA3LB---2LB_2LA0LA4RB0RB1LA"
HEADER = "231302"
INITIAL_DATA = "220312221222" + "02" * 397 + "030202121212121303130222031302221302122212"
OPS = {}
for state, row in zip("AB", MACHINE.split("_")):
    for symbol in range(5):
        action = row[3 * symbol:3 * symbol + 3]
        if action != "---":
            OPS[state, int(symbol)] = (
                int(action[0]), 1 if action[1] == "R" else -1, action[2]
            )


def require(condition, message):
    if not condition:
        raise ValueError(message)


def raw_probe(data, state):
    """Enter at cell zero, then stop on the first return through the same cut."""
    head = clock = 0
    while head >= 0:
        if head == len(data):
            raise ValueError("fixed-register overflow during the checked interval")
        action = OPS.get((state, data[head]))
        if action is None:
            raise ValueError("A3 halt during the checked interval")
        data[head], move, state = action
        head += move
        clock += 1
    return state, clock


def physical_epoch(data, pile):
    # Header + pile local moves equal 58 + 28*pile + one per outgoing probe.
    clock = 58 + 28 * pile
    pending = False
    for slot in range(4):
        compound = (slot == 1) or pending
        entries = ["B", "B", "A"] if compound else ["B"]
        pending = False
        for entry in entries:
            answer, work = raw_probe(data, entry)
            clock += work + 1
            if entry == "B":
                require(answer == "A", "nonordinary B return")
            elif answer == "A":
                pending = True
            else:
                # A returning B completes C with one final B probe.
                answer, work = raw_probe(data, "B")
                require(answer == "A", "nonordinary final B return")
                clock += work + 1
    require(not pending, "incomplete final pulse")
    return clock


def load(path):
    envelope = json.loads(Path(path).read_text())
    payload = envelope["payload"]
    packed = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    require(hashlib.sha256(packed).hexdigest() == envelope["sha256"], "checksum mismatch")
    require(payload["machine"] == MACHINE and payload["header"] == HEADER
            and payload["line"] == 17 and payload["format"] == "bb2x5-line17-epochs-v1",
            "unexpected machine or format")
    require(len(payload["register"]) == 848 and payload["terminal"] == "2"
            and payload["state"] == "A" and payload["pile_pairs"] == payload["epochs"]
            and payload["head"] == -844 - 2 * payload["epochs"], "invalid physical boundary")
    require(all(v in "102" and flag in "23" for v, flag in
                zip(payload["register"][::2], payload["register"][1::2])), "invalid data pairs")
    return payload


def replay(start, end):
    count = end["epochs"] - start["epochs"]
    require(count >= 0, "checkpoints reversed")
    data = list(map(int, start["register"]))
    clock = start["steps"]
    for k in range(start["epochs"], end["epochs"]):
        clock += physical_epoch(data, k)
    require(clock == end["steps"], "elementary clock mismatch")
    require("".join(map(str, data)) == end["register"], "physical tape mismatch")
    return count


def self_test():
    # A separate sparse, unbounded blank-tape interpreter supplies the oracle.
    tape = {}
    head, state, clock = 0, "A", 0
    first_right = {0: 0}
    def advance(target):
        nonlocal head, state, clock
        while clock < target:
            written, move, state = OPS[state, tape.get(head, 0)]
            if written:
                tape[head] = written
            else:
                tape.pop(head, None)
            head += move
            clock += 1
            if head > 0 and head not in first_right:
                first_right[head] = clock

    checked = 0
    for steps, origin, width, ordinary in (
        (252, -12, 7, 9), (2889, -37, 20, 400), (2308940, -844, 424, 425)
    ):
        advance(steps)
        require((head, state) == (origin, "A"), "bad blank entry")
        data_start = origin + 1 + len(HEADER)
        data = [tape.get(data_start + j, 0) for j in range(2 * width)]
        if width == 424:
            require("".join(map(str, data)) == INITIAL_DATA, "initial register mismatch")
        for k in range(ordinary + 1):
            word = HEADER + "12" * k + "".join(map(str, data)) + "2"
            expected = {head + j: int(x) for j, x in enumerate(word, 1) if x != "0"}
            require(tape == expected and (head, state) == (origin - 2 * k, "A"),
                    "raw head, state, or tape mismatch")
            checked += 1
            if k < ordinary:
                advance(clock + physical_epoch(data, k))
    require((first_right[10], first_right[11]) == (2628, 2306191) and 12 not in first_right,
            "virgin-cell arrival mismatch")
    print(f"Matched {checked} complete blank-orbit boundaries through raw step {clock};"
          f" first +10 at {first_right[10]}, first +11 at {first_right[11]}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("checkpoints", nargs="*")
    args = parser.parse_args()
    if args.self_test:
        self_test()
    if len(args.checkpoints) == 2:
        print(f"Matched tape, head, state, and raw clock across "
              f"{replay(*map(load, args.checkpoints))} epochs.")
    elif args.checkpoints or not args.self_test:
        parser.error("supply --self-test or two checkpoint paths")
