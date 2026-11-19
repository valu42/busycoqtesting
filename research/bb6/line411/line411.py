"""Replay blank-tape BB(6) line 411. Python 3, standard library only."""

import argparse
import hashlib
import re

from line411_rules import DIGITS, NORMAL, ROOT, verify

WALLS = re.compile(r"(?:11)+")
ATOMS = ({}, {})
for mode, word, new, child in DIGITS:
    if word != new:
        lo, hi = (word, new) if child is None else (new, word)
        ATOMS[mode][word] = (int(child is not None), lo, hi)
# These are the child *modes*, including on zero digits which emit no call.
NEXT = {"0000": 0, "0110": 0, "0011": 1, "0111": 1, "00": 0, "10": 0}


def excursion(r, rules, frame):
    pos = 0
    stack = []
    while True:
        if frame == ROOT and r.startswith("11", pos):
            end = WALLS.match(r, pos).end()
            # A 11 wall returns NORMAL and is unchanged. Skip a whole run.
            stack.append((None, (pos, end)))
            pos = end
        pair = r[pos:pos+2].ljust(2, "0")
        child, outcomes = rules[frame, pair]
        pos += 2
        if child is None:
            result, written = outcomes[None]
            break
        stack.append((outcomes, None))
        frame = child
    pieces = [written]
    for outcomes, span in reversed(stack):
        if outcomes is None:
            assert result == NORMAL
            pieces.append(r[span[0]:span[1]])
        else:
            result, written = outcomes[result]
            pieces.append(written)
    return result, ("".join(reversed(pieces)) + r[pos:]).rstrip("0")


def right_call(r, rules):
    result, new = excursion(r, rules, ROOT)
    assert result == NORMAL
    return new


def add_calls(limit, r):
    # Collect digits until their zero positions can absorb 'limit' calls
    # or the grammar ends. The untouched suffix receives no call.
    digits = []
    pos, mode, capacity, place = 0, 1, 0, 1
    while capacity < limit:
        if mode == 1 and r.startswith("11", pos):
            end = WALLS.match(r, pos).end()
            digits.append((None, (pos, end), None))
            pos = end
            continue
        width = 2 if mode else 4
        word = r[pos:pos+width].ljust(width, "0")
        if word not in ATOMS[mode]:
            break
        bit, lo, hi = ATOMS[mode][word]
        mode = NEXT[word]
        if not bit:
            capacity += place
        digits.append((bit, lo, hi))
        place *= 2
        pos += width
    if not capacity:
        return 0, r
    count = carry = min(capacity, limit)
    pieces = []
    for bit, lo, hi in digits:
        if bit is None:
            pieces.append(r[lo[0]:lo[1]])
        else:
            carry, val = divmod(carry+bit, 2)
            pieces.append(hi if val else lo)
    assert carry == 0
    return count, ("".join(pieces) + r[pos:]).rstrip("0")


def replay(steps, rules):
    a, b, r, mode = 11, 5, "1", "L"
    left_moves, overflows = 301, 0
    for i in range(steps):
        if mode == "R":
            r, mode = right_call(r, rules), "L"
        elif r.startswith("101"):
            left_moves += 2*a+12*b+16
            r, a = r[2:], a+4
        elif r.startswith("11"):
            left_moves += 2*a+12*b+8
            r, a, mode = r[2:], a+4, "R"
        elif b == 0:
            if not (r+"00").startswith("00"):
                raise ValueError(("Left boundary needs a new rule", i, a, r[:48]))
            assert a >= 3 and a % 2 == 1
            left_moves += 4*a+23
            r, a, b, mode = r[1:], 3, 2+a//2, "R"
            overflows += 1
        else:
            k, new_r = add_calls(b, r)
            if not k:
                k, mode = 1, "R"
            # Sum 2(a+4j)+12(b-j)+6 for 0 <= j < k.
            left_moves += k*(2*a+12*b+6)-2*k*(k-1)
            a, b, r = a+4*k, b-k, new_r
    return mode, a, b, r, left_moves, overflows


def boundary(n, r, rules):
    """One action from 0-infinity followed by n even ones and A scanning r."""
    assert n >= 8 and n % 2 == 0
    pos = 0
    while r.startswith("1001", pos):
        pos += 4
    tail = r[pos:]
    if not tail.startswith("1"):
        return "sweep", (n-2)//2, "1"*pos + tail[1:]
    if tail.startswith("11"):
        return "boundary", n+pos+4, right_call(tail[2:], rules)
    if tail.startswith("101"):
        return "boundary", n+pos+4, tail[2:]
    # The infinite blank continuation supplies any missing terminal zeros.
    assert (tail+"0000").startswith("1000")
    return "halt", None, None


def advance_epochs(count, rules):
    # Between successive empty-left boundaries, take every primitive
    # left increment, with its matching right call, even when a shortcut
    # from the main replay would also match.
    a, b, r = 11, 5, "1"
    total_boundaries = 0
    for epoch in range(1, count+1):
        n = a+4*b+5
        while b:
            k, new = add_calls(b, r)
            if k:
                b, r = b-k, new
            else:
                b, r = b-1, right_call(r, rules)
        while True:
            tag, val, r = boundary(n, r, rules)
            total_boundaries += 1
            if tag == "halt":
                return epoch, tag, None, None, total_boundaries
            if tag == "sweep":
                a, b, r = 3, val, right_call(r, rules)
                break
            n = val
    return count, "L", b, r, total_boundaries


def digest(mode, a, b, r):
    return hashlib.sha256(f"{mode}/{a:x}/{b:x}/{r}".encode("ascii")).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--steps", type=int, default=12418)
    parser.add_argument("--epochs", type=int,
                        help="replay the complete boundary reduction for this many sweeps")
    args = parser.parse_args()
    if args.steps < 0:
        parser.error("--steps must be nonnegative")
    rules = verify()
    # This wall optimization is separately verified by the generated pair table.
    assert rules[ROOT, "11"] == (ROOT, {NORMAL: (NORMAL, "11")})
    if args.epochs is not None:
        if args.epochs < 1:
            parser.error("--epochs must be positive")
        epochs, tag, b, r, visits = advance_epochs(args.epochs, rules)
        print(f"Epochs {epochs}, outcome {tag}, boundary tests {visits}")
        if tag == "L":
            print(f"Left counter b has {b.bit_length()} bits. Right word has {len(r)} bits.")
            print(f"State SHA-256 {digest(tag, 3, b, r)}")
        return
    mode, a, b, r, lower, overflows = replay(args.steps, rules)
    result = digest(mode, a, b, r)
    print(f"Macro steps {args.steps}, overflows {overflows}, mode {mode}")
    print(f"Bit lengths a={a.bit_length()}, b={b.bit_length()}, right word={len(r)}")
    print(f"State SHA-256 {result}")
    print(f"Completed elementary transitions > 10^{len(str(lower))-1}")
    if args.steps in CHECKPOINTS:
        assert (overflows, result, len(str(lower))-1) == CHECKPOINTS[args.steps]


CHECKPOINTS = {
    12418: (374, "e76aeeb8d94d8168c4669c302d991c5d7caf4d280c515403f8b8e7d5d2143dfa", 227),
    300000: (3338, "3e3bfc1d6742ae3b92cc8fe3aff1b3f608ec0f7092b7560f39706a0741bab9ab", 2012),
}

if __name__ == "__main__":
    main()
