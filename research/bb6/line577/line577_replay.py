"""Replay the six-state, two-symbol BB(6) ranking line 577. Python 3.10+.

The digit words, local rewrites and scans are read from the cited DeepMind
Lean source. Each extracted rule is independently checked against the literal
table. The source can be kept outside this directory.
"""
import argparse
import ast
import hashlib
import json
import re
from functools import lru_cache
from pathlib import Path

from line577_rules import RuleBook

# This is the reflected table in the DeepMind certificate. Its C start
# corresponds to the target's A start after renaming and the B0 detour.
REFERENCE = "1LB1LE_1RC1LB_1LA0RD_1LC0RB_0LF---_0RD1LA".split("_")
TARGET = "1RB0LD_1LC1RE_1LA1RC_1RA0LC_0RF---_0LD1RB"
SOURCE_SHA256 = "68c78d084149e072cd1aecfb68cab24154554ed84ad1cffb26f77df1d5d4fd53"
WALL = "101111111"
HUB_LEFT = "10010101010"[::-1]
GLIDER_LEFT = "0010"
GLIDER_RIGHT = "101101111101111110"

def rule_source(path):
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        raise ValueError("Expected the DeepMind source at commit 3647718")
    source = raw.decode()
    digit_section = source.split("def q0 : Digit", 1)[1].split("def qQ", 1)[0]
    digits = [table_bits(word) for word in re.findall(r"\| \.D\d+ => \[([IO,]+)\]", digit_section)]
    pattern = r"def (macro|scan)_(\d+) : [^\n⟨]+⟨([^\n]+)⟩\n[^\n]+?\(n := (\d+)\)"
    macros, scans = {}, {}
    for kind, number, fields, steps in re.findall(pattern, source):
        fields = fields.replace(".left", "'L'").replace(".right", "'R'")
        fields = re.sub(r"\b([A-F])\b", r"'\1'", fields)
        fields = fields.replace("I", "1").replace("O", "0")
        row = ast.literal_eval("(" + fields + ")")
        number, steps = int(number), int(steps)
        if kind == "scan":
            state, direction, inp, out, context = row
            scans[number] = state, direction, word(inp), word(out), word(context), steps
        else:
            state, direction, left, right, dest, end_dir, left_out, right_out = row
            def output(runs):
                return tuple((word(w), n) for w, n in runs)
            macros[number] = (state, direction, word(left), word(right), dest, end_dir,
                              output(left_out), output(right_out), steps)
    assert len(digits) == 22 and len(macros) == 118 and len(scans) == 15
    return digits, macros, scans

def table_bits(s):
    return s.replace(",", "").replace("I", "1").replace("O", "0")

def word(bits):
    return "".join(map(str, bits))

# A half-tape is a nearest-first tuple of (nonempty word, positive count)
# followed by infinitely many zeros. It may be exponentially large.
def prepend(pattern, count, tail):
    if not count or not pattern or (not tail and "1" not in pattern):
        return tail
    if tail and tail[0][0] == pattern:
        return ((pattern, count + tail[0][1]),) + tail[1:]
    if tail:
        near, repeats = tail[0]
        if len(pattern) * count <= 36 and len(near) * repeats <= 36:
            return ((pattern * count + near * repeats, 1),) + tail[1:]
    return ((pattern, count),) + tail

def push(runs, tail):
    for pattern, count in reversed(runs):
        tail = prepend(pattern, count, tail)
    return tail

def peek(stack, length):
    parts = []
    for pattern, count in stack:
        take = min(length, len(pattern) * count)
        copies = (take + len(pattern) - 1) // len(pattern)
        parts.append((pattern * copies)[:take])
        length -= take
        if not length:
            break
    return "".join(parts) + "0" * length

def drop(stack, length):
    for index, (pattern, count) in enumerate(stack):
        run_length = len(pattern) * count
        if length < run_length:
            if not length:
                return stack[index:]
            copies, remainder = divmod(length, len(pattern))
            count -= copies
            if not remainder:
                return ((pattern, count),) + stack[index + 1:]
            rest = prepend(pattern, count - 1, stack[index + 1:])
            return prepend(pattern[remainder:], 1, rest)
        length -= run_length
    return ()

def repeats(stack, pattern):
    """Count repeated copies, including any final match on the infinite zeros."""
    if not stack:
        return 0
    width = len(pattern)
    total = 0
    for item, count in stack:
        size = len(item) * count
        # Two periodic words agreeing for a sum of their periods agree forever.
        check = min(size, len(item) + width)
        actual = (item * ((check + len(item) - 1) // len(item)))[:check]
        offset = total % width
        predicted = (pattern * ((offset + check + width - 1) // width))[offset:offset + check]
        if actual != predicted:
            mismatch = next(i for i, (a, b) in enumerate(zip(actual, predicted)) if a != b)
            return (total + mismatch) // width
        total += size
    assert "1" in pattern
    while pattern[total % width] == "0":
        total += 1
    return total // width

def all_zero(stack):
    return all("1" not in pattern for pattern, _ in stack)

def stored_width(stack):
    return sum(len(pattern) * count for pattern, count in stack)

def orient(config, direction):
    _, original, left, right = config
    if direction == original:
        return left, right
    if direction == "L":
        return prepend(peek(right, 1), 1, left), drop(right, 1)
    return drop(left, 1), prepend(peek(left, 1), 1, right)

def raw(config):
    state, direction, left, right = config
    scan, other = (right, left) if direction == "R" else (left, right)
    bit = int(peek(scan, 1))
    transition = REFERENCE[ord(state) - 65][3 * bit:3 * bit + 3]
    if transition == "---":
        return None
    value, move, dest = transition
    scan = drop(scan, 1)
    if move == direction:
        other = prepend(value, 1, other)
    else:
        scan = prepend(value, 1, scan)
    left, right = (other, scan) if direction == "R" else (scan, other)
    return dest, move, left, right

def glider_patterns():
    # All positions less than -3 are symbolic. One period moves the head right
    # by one, inserts a 1 behind the head, and preserves both required words.
    tape = dict(zip(range(0, -4, -1), GLIDER_LEFT))
    tape.update(dict(zip(range(1, len(GLIDER_RIGHT) + 1), GLIDER_RIGHT)))
    state, head = "A", 0
    patterns = {}
    for phase in range(125):
        assert head >= -3
        left = "".join(tape.get(j, "0") for j in range(head - 1, -4, -1))
        last_one = max(j for j, bit in tape.items() if bit == "1")
        right = "".join(tape.get(j, "0") for j in range(head, last_one + 1))
        patterns.setdefault(state, []).append((left, right, phase))
        bit = int(tape.get(head, "0"))
        value, move, state = REFERENCE[ord(state) - 65][3 * bit:3 * bit + 3]
        tape[head] = value
        head += 1 if move == "R" else -1
    assert state == "A" and head == 1
    assert "".join(tape.get(head - j, "0") for j in range(5)) == GLIDER_LEFT + "1"
    assert "".join(tape.get(head + j, "0") for j in range(1, len(GLIDER_RIGHT) + 1)) == GLIDER_RIGHT
    assert all(bit == "0" for pos, bit in tape.items() if pos > head + len(GLIDER_RIGHT))
    return patterns

class Replay:
    def __init__(self, path):
        self.digits, self.macros, self.scans = rule_source(path)
        self.priority = sorted(range(22), key=lambda p: -len(self.digits[p]))
        self.book = RuleBook(REFERENCE, self.digits, self.macros, self.scans)
        self.glider = glider_patterns()
        self.by_scan, self.by_macro = {}, {}
        for index, (q, d, *data) in self.scans.items():
            self.by_scan.setdefault((q, d), []).append((index, *data))
        for index, (q, d, *data) in self.macros.items():
            self.by_macro.setdefault((q, d), []).append((index, *data))

    @lru_cache(32768)
    def choices(self, prefix):
        valid = tuple(p for p in self.priority if prefix.startswith(self.digits[p]))
        stable = next((p for p in valid if prefix.startswith(WALL * 2, len(self.digits[p]))), None)
        return valid, stable

    def parse_digits(self, right):
        # Word boundaries may be ambiguous. Only a literal match is consumed.
        leading = repeats(right, WALL)
        right = drop(right, len(WALL) * leading)
        digits = []
        threshold = 2
        while True:
            valid, stable = self.choices(peek(right, 66))
            if stable is not None:
                rest = drop(right, len(self.digits[stable]))
                gap = repeats(rest, WALL)
                digits.append((stable, gap))
                right = drop(rest, gap * len(WALL))
            elif valid:
                @lru_cache(None)
                def island(position):
                    rest = drop(right, position)
                    candidates, _ = self.choices(peek(rest, 66))
                    best = position, 0, ()
                    for phase in candidates:
                        length = len(self.digits[phase])
                        gap = repeats(drop(rest, length), WALL)
                        end = position + length + gap * len(WALL)
                        score, neg_count, suffix = (end, 0, ()) if gap >= 2 else island(end)
                        if (score, neg_count - 1) > best[:2]:
                            best = score, neg_count - 1, ((phase, gap),) + suffix
                    return best
                consumed, _, extra = island(0)
                island.cache_clear()
                if not extra:
                    break
                digits.extend(extra)
                right = drop(right, consumed)
                if extra[-1][1] < 2:
                    break
            else:
                break
            if len(digits) >= threshold:
                if self.book.limit(digits, True) == self.book.limit(digits, False):
                    break
                threshold *= 2
        return leading, digits, right

    def bulk(self, left, right):
        if peek(left, len(HUB_LEFT)) != HUB_LEFT or not all_zero(drop(left, len(HUB_LEFT))):
            return None
        leading, digits, tail = self.parse_digits(right)
        rounds = self.book.limit(digits, True)
        if not rounds:
            return None
        extra, updated = self.book.update(rounds, digits)
        for phase, gap in reversed(updated):
            tail = prepend(self.digits[phase], 1, prepend(WALL, gap, tail))
        config = "D", "R", left, prepend(WALL, leading + extra, tail)
        return config, ("batch", leading, rounds, digits)

    def advance(self, config):
        state, direction, _, _ = config
        left, right = orient(config, "R")
        if state == "D":
            move = self.bulk(left, right)
            if move is not None:
                return move
        if stored_width(right) <= 80:
            observed = peek(right, 80).rstrip("0")
            for needed_left, needed_right, phase in self.glider.get(state, ()):
                if observed == needed_right and peek(left, len(needed_left)) == needed_left:
                    return None, ("glider", phase)
        if stored_width(left) < 58:
            out = raw(config)
            return out, ("raw",) if out is not None else ("halt",)
        best_cost, best = 0, None
        for facing in (direction, "L" if direction == "R" else "R"):
            left, right = orient(config, facing)
            pl, pr = peek(left, 76), peek(right, 76)
            for index, inp, out, context, steps in self.by_scan.get((state, facing), ()):
                scan, other = (right, left) if facing == "R" else (left, right)
                a, b = (pr, pl) if facing == "R" else (pl, pr)
                if not a.startswith(inp) or not b.startswith(context):
                    continue
                count = repeats(scan, inp)
                if count * steps <= best_cost:
                    continue
                scan = drop(scan, count * len(inp))
                other = prepend(context, 1, prepend(out, count, drop(other, len(context))))
                l2, r2 = (other, scan) if facing == "R" else (scan, other)
                best_cost = count * steps
                best = (state, facing, l2, r2), ("scan", index, count)
            for index, a, b, dest, end_dir, lo, ro, steps in self.by_macro.get((state, facing), ()):
                if steps > best_cost and pl.startswith(a) and pr.startswith(b):
                    best_cost = steps
                    best = (dest, end_dir, push(lo, drop(left, len(a))), push(ro, drop(right, len(b)))), ("macro", index)
        if best is not None:
            return best
        out = raw(config)
        return out, ("raw",) if out is not None else ("halt",)

    def cost(self, config, cmd):
        if cmd[0] == "batch":
            return self.book.batch_clocks(*cmd[1:])
        if cmd[0] == "scan":
            return tuple(n * cmd[2] for n in self.book.scan_clocks[cmd[1]])
        if cmd[0] == "macro":
            return self.book.macro_clocks[cmd[1]]
        assert cmd[0] == "raw"
        state, direction, left, right = config
        return 1, 1 + 2 * (state == "A" and peek(left if direction == "L" else right, 1) == "0")

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("lean_source", type=Path)
    parser.add_argument("--state", choices=["A", "C"], default="C",
                        help="C is the line 577 run. A is the published glider control.")
    parser.add_argument("--commands", type=int, required=True)
    parser.add_argument("--report", type=int, default=100000, help="progress interval")
    parser.add_argument("--dump", type=Path, help="write the final compressed configuration and exact clocks as JSON")
    parser.add_argument("--literal-checkpoints", type=Path,
                        help="write small complete tapes at intervals for the independent C++ simulator")
    args = parser.parse_args()
    if args.commands < 0 or args.report <= 0:
        parser.error("commands must be nonnegative and report must be positive")
    if args.literal_checkpoints and args.state != "C":
        parser.error("literal control uses the C start")
    replay = Replay(args.lean_source)
    import sys
    if hasattr(sys, "set_int_max_str_digits"):
        sys.set_int_max_str_digits(0)
    config = (args.state, "R", (), ())
    ref_steps, weighted_steps, executed = 0, 0, 0
    outcome = "running"
    if args.literal_checkpoints:
        args.literal_checkpoints.write_text("")
    while executed < args.commands:
        next_config, command = replay.advance(config)
        if next_config is None:
            outcome = command[0]
            break
        a, b = replay.cost(config, command)
        ref_steps += a
        weighted_steps += b
        config = next_config
        executed += 1
        if args.literal_checkpoints and executed % 2000 == 0 and weighted_steps <= 12_000_000_000:
            left, right = orient(config, "R")
            with args.literal_checkpoints.open("a") as stream:
                print(ref_steps, weighted_steps, config[0], file=stream)
                for side in (left, right):
                    print("".join(w * n for w, n in side).rstrip("0"), file=stream)
        if executed % args.report == 0:
            print(executed, ref_steps, weighted_steps, flush=True)
    payload = json.dumps(config, separators=(",", ":")).encode()
    fingerprint = hashlib.sha256(payload).hexdigest()
    print("outcome", outcome, "commands", executed)
    print("reference steps", ref_steps)
    if args.state == "C":
        print("line 577 steps", weighted_steps)
    print("compressed configuration SHA-256", fingerprint)
    if args.dump:
        args.dump.write_text(json.dumps(dict(outcome=outcome, state=args.state, commands=executed,
            reference_steps=ref_steps, weighted_steps=weighted_steps, config=config), indent=2) + "\n")

if __name__ == "__main__":
    main()
