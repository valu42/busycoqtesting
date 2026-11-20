"""Reproduce the two-gap test for BB(6) line 429. Uses only Python's standard library."""
import argparse
from dataclasses import dataclass
from functools import lru_cache
import hashlib
import re
import subprocess

MACHINE = "1RB0LC_1RC1RA_1RD0RF_0LE---_1LA1LE_0RA0RF"
TABLE = [tuple(row[i:i+3] for i in (0, 3)) for row in MACHINE.split("_")]
WIDTH = 256
MASK = (1 << WIDTH) - 1


def ones(length):
    return (1 << length) - 1


def initial_ones(side):
    """Length of the initial one run, reading the integer least-significant bit first."""
    return (side ^ (side + 1)).bit_length() - 1


@dataclass(frozen=True, slots=True)
class Frame:
    mode: str  # "0"/"1" for R with that pending bit, "L" for the left scan
    u: int
    v: int
    head: int = 0

    def tape(self):
        """Left of the head outward, then head and rightward. Both have implicit zero tails."""
        if self.mode == "L":
            return self.u >> 1, (self.u & 1) | 2 | (self.v << 2)
        return (self.u << 1) | int(self.mode), self.v


def step(frame):
    mode, u, v, h = frame.mode, frame.u, frame.v, frame.head
    if mode == "L":
        if not u & 1:
            return 2, Frame("1", (u & ~1) | 1, v, h+2)
        if u & 2:
            return 8, Frame("L", u >> 2, 1 | (v << 2), h-2)
        k = initial_ones(u >> 2)
        output = ones(k+1) | (1 << (k+2))
        return k+5, Frame("L", u >> (k+3), output | (v << (k+3)), h-k-3)

    p = int(mode)
    if v & 1:
        if p:
            return 3, Frame("0", u << 1, v >> 1, h+1)
        k = initial_ones(u)
        right = ones(k+1) | ((v >> 1) << (k+2))
        return k+5, Frame("L", u >> (k+1), right, h-k-3)
    if v & 2:
        return 2, Frame("1", 1 | (p << 1) | (u << 2), v >> 2, h+2)
    if v & 4:
        k = initial_ones(v >> 2)
        written = (3 | (p << 2) | (u << 3)) << k
        return k+3, Frame("0", written, v >> (k+3), h+k+3)
    if v & 8:
        return 3, None
    left = p | (u << 1)
    k = initial_ones(left)
    right = ones(k+3) | ((v >> 4) << (k+4))
    return k+8, Frame("L", left >> (k+1), right, h-k-2)


def literal(q, left, right, head, count):
    for _ in range(count):
        action = TABLE[ord(q)-ord("A")][right & 1]
        assert action != "---", "premature halt in a proposed rule"
        symbol, direction, q = action
        if direction == "R":
            left = (left << 1) | int(symbol)
            right >>= 1
            head += 1
        else:
            right = ((right & ~1) << 1) | (int(symbol) << 1) | (left & 1)
            left >>= 1
            head -= 1
    return q, left, right, head


def verify_rule(f):
    elapsed, g = step(f)
    q, left, right, head = literal("A", *f.tape(), f.head, elapsed)
    if g is None:
        assert (q, right & 1) == ("D", 1)
    else:
        assert (q, left, right, head) == ("A", *g.tape(), g.head)


@lru_cache(65536)
def scan_piece(mode, word, width):
    """Consume complete tokens in one direction. Stop before any turn or unknown bit."""
    consumed = written = clock = 0
    while consumed < width:
        room = width - consumed
        if mode == "L":
            if not word & 1 or room < 2:
                break
            if word & 2:
                length = 2
                written = (written << 2) | 1
                clock += 8
            else:
                k = initial_ones(word >> 2)
                length = k+3
                if length > room:
                    break
                written = (written << length) | ones(k+1) | (1 << (k+2))
                clock += k+5
        elif word & 1:
            if mode == "0":
                break
            length = 1
            written <<= 1
            clock += 3
            mode = "0"
        elif room >= 2 and word & 2:
            length = 2
            written = (written << 2) | (int(mode) << 1) | 1
            clock += 2
            mode = "1"
        elif room >= 3 and word & 4:
            k = initial_ones(word >> 2)
            length = k+3
            if length > room:
                break
            written = (written << length) | ((3 | (int(mode) << 2)) << k)
            clock += k+3
            mode = "0"
        else:
            break
        word >>= length
        consumed += length
    return consumed, written, clock, mode


@lru_cache(32768)
def periodic_piece(mode, window):
    """Find a complete repeated token sequence that restores its incoming mode."""
    for period in range(1, 17):
        if (window ^ (window >> period)) & ones(WIDTH-period):
            continue
        for copies in range(1, 5):
            length = period * copies
            n, output, clock, end = scan_piece(mode, window & ones(length), length)
            if n == length and end == mode:
                return period, length, output, clock
        break
    return None


def advance(f):
    side = f.u if f.mode == "L" else f.v
    window = side & MASK
    cycle = periodic_piece(f.mode, window)
    if cycle is None or side == 0:
        n, out, elapsed, mode = scan_piece(f.mode, window, WIDTH)
    else:
        period, width, block, cost = cycle
        mismatch = side ^ (side >> period)
        equal = (mismatch & -mismatch).bit_length() - 1
        copies = (period + equal) // width
        n = copies * width
        # Each input block has identical bits and restores the mode. Concatenate its output.
        out = (ones(n) // ones(width)) * block
        elapsed = copies * cost
        mode = f.mode
    if n == 0:
        return step(f)
    if mode == "L":
        return elapsed, Frame(mode, f.u >> n, out | (f.v << n), f.head-n)
    return elapsed, Frame(mode, out | (f.u << n), f.v >> n, f.head+n)


def word_bits(text):
    return int(text[::-1], 2)


def local_controls():
    for mode in ("0", "1", "L"):
        for u in range(64):
            for v in range(256):
                verify_rule(Frame(mode, u, v))

    # Compare the launch-word expression with the deterministic rightward parser.
    pattern = re.compile(r"^1(?:011?|001+0)*001+01001")
    for seed in range(1, 1 << 14, 2):
        word = format(seed, "b")[::-1]
        found = False
        f = Frame("1", 1, seed)
        while f.mode != "L":
            if (f.v & 3) == 0:
                k = initial_ones(f.v >> 2)
                if k and (f.v >> (k+2)) & 31 == word_bits("01001"):
                    found = True
                    break
            _, next_frame = step(f)
            if next_frame is None:
                break
            f = next_frame
        assert found == bool(pattern.match(word))

    # k >= 2 is independent of the left environment. For k = 1 use an even run of ones.
    for k in range(1, 65):
        right = word_bits("00" + "1"*k + "01001101")
        for left in ([ones(2*r) | (5 << (2*r+1)) for r in range(17)] if k == 1
                     else [0, 1, 2, 3, 7, 338, 4095]):
            expected = 27 + 5*initial_ones(left) if k == 1 else k+16
            q, _, tape, h = literal("A", left, right, 0, expected)
            assert (q, tape & 1, h) == ("D", 1, k+6)

    # Turn 5 has the same right word on the blank tape and a three-one perturbation.
    timelines = []
    for initial_left in (0, 1408):  # bits 7, 8, 10 stand for coordinates -8, -9, -11
        f = Frame(str(initial_left & 1), initial_left >> 1, 0)
        time = 0
        turns = []
        while time < 166:
            verify_rule(f)
            if initial_left and time == 148:
                assert f.head == -10 and f.v & 511 == word_bits("001101001")
            dt, g = step(f)
            time += dt
            if g is None:
                assert initial_left and time == 166
                break
            if f.mode == "L" and g.mode == "1":
                turns.append((time, g.head, g.v))
            f = g
        if initial_left:
            q, _, right, h = literal("A", initial_left, 0, 0, 166)
            assert (q, right & 1, h) == ("D", 1, -2)
        timelines.append(turns)
    assert timelines[0][:5] == timelines[1][:5]
    assert timelines[0][4] == (101, -5, word_bits("1101101101"))
    assert timelines[0][5] != timelines[1][5]


def check_frontier(frame, time, lowest, native):
    left, right = frame.tape()
    h = frame.head
    assert (time, h, lowest, left, right & 15) == (20200782534, -146976, -146978, 3, 11)
    marks = [h-3, h-4, h-6]
    assert max(marks) < lowest
    changed = left | (1 << 2) | (1 << 3) | (1 << 5)
    q, l, r, end = literal("A", changed, right, h, 65)
    assert (q, end, r & 1) == ("D", -146973, 1)
    if native:
        # Run from time zero with the three negative cells marked on the initial tape.
        args = [native, str(time+66)]
        for cell in marks:
            args.extend(["--one", str(cell)])
        lines = subprocess.check_output(args, text=True).splitlines()
        assert lines == [f"{time+65} D {end}", format(l, "x"), format(r, "x")]
    print(f"Three-one control halts at move {time+65}, head {end}.")


def run(limit, native):
    f = Frame("0", 0, 0)
    time = turns = births = lowest = 0
    shortest = fewest_zeros = None
    direct_shortest = direct_fewest = None
    while turns < limit:
        if f.mode == "0" and f.v & 15 == 9:
            print(f"first triple would be created at move {time}, head {f.head}")
        if f.mode == "0" and f.v & 7 == 5:
            # The splice replaces 1|01... by P10|01... . Distances between surviving pairs
            # are unchanged, so it suffices to measure from the just-created leftmost pair.
            births += 1
            tail = f.v >> 2
            pairs = (~tail) & (~(tail >> 1))
            gap = (pairs & -pairs).bit_length()-1
            if tail >> (gap+2):
                prefix = tail & ones(gap)
                zeros = gap - prefix.bit_count()
                shortest = gap if shortest is None else min(gap, shortest)
                fewest_zeros = zeros if fewest_zeros is None else min(zeros, fewest_zeros)
        dt, g = advance(f)
        time += dt
        if g is None:
            print(f"D1 after {time} defined moves")
            return
        lowest = min(lowest, f.head, g.head)
        # R on 1 with a pending 1 is the only advancing row dipping left of its start.
        if f.mode == "1" and f.v & 1:
            lowest = min(lowest, f.head-1)
        if f.mode == "L" and g.mode == "1":
            turns += 1
            if turns <= 5000:
                # Read the full launch word independently of the splice accounting.
                word = format(g.v, "b")[::-1].rstrip("0")
                assert "000" not in word
                pairs = [m.start() for m in re.finditer("00", word)]
                for a, b in zip(pairs, pairs[1:]):
                    between = word[a+2:b]
                    size, zeros = len(between), between.count("0")
                    direct_shortest = size if direct_shortest is None else min(size, direct_shortest)
                    direct_fewest = zeros if direct_fewest is None else min(zeros, direct_fewest)
                assert (direct_shortest, direct_fewest) == (shortest, fewest_zeros)
            if turns == 310644:
                check_frontier(g, time, lowest, native)
        f = g
    left, right = f.tape()
    first = f"{time} A {f.head}"
    left_hex, right_hex = format(left, "x"), format(right, "x")
    print(f"turns={turns}   moves={time}   head={f.head}   ones={left.bit_count()+right.bit_count()}")
    print(f"pair births={births}   minimum separation={shortest}   minimum intervening zeros={fewest_zeros}")
    digest = hashlib.sha256(f"{f.head}|{left_hex}|{right_hex}".encode("ascii")).hexdigest()
    print(f"head and tape SHA256 {digest}")
    if native:
        lines = subprocess.check_output([native, str(time)], text=True).splitlines()
        assert lines == [first, left_hex, right_hex], "independent replay disagrees"
        print("Independent state, head and both complete half-tapes agree.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--turns", type=int, default=100000)
    parser.add_argument("--compare", metavar="EXECUTABLE", help="path to the compiled literal.cpp")
    args = parser.parse_args()
    if args.turns < 0:
        parser.error("--turns must be nonnegative")
    local_controls()
    run(args.turns, args.compare)
