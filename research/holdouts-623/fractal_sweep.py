#!/usr/bin/env python3
"""Explore the exact recurrence in ResearchFractalSweep.v.

This Python implementation is unverified. A limit/time/space result is UNKNOWN,
not nonhalting. The Coq theorem reduces blank-run halting to recurrence halting;
it does not decide either question. Optional transfers implement the general
rule in ResearchFractalTransfer.v. Iterations count calls to a sweep or batch,
not raw TM steps and not a certified lower bound.
Time and space budgets are checked between calls, so one call may exceed them.

Both words are nonnegative, arbitrary-precision integers, nearest bit first.
The right integer includes the scanned cell. Start A uses pair (1, 0),
reached after the blank machine's first step. Start E uses (1, 1), also
covering machine 549 through ResearchStartVariants.v's checked reduction.
No input attachment is required.
"""
import argparse
import hashlib
import itertools
import json
import math
import random
import time
from pathlib import Path

MACHINE = "1RB1LE_0RC1RC_0RD0RB_1RE0RF_1LA0LE_---1RB"
SCHEMA = "fractal-sweep-v1"


def ones(n):
    """Length of the low-order run of ones, including n=0."""
    return (n ^ (n + 1)).bit_length() - 1


def periodic_prefix(n, word, width):
    """Number of whole copies of a nonzero periodic low-order word."""
    count = n.bit_length() // width + 2
    pattern = word * ((1 << (width * count)) - 1) // ((1 << width) - 1)
    difference = n ^ pattern
    return ((difference & -difference).bit_length() - 1) // width


def sweep(l, r):
    """Return (next pair or None, raw steps executed before B/halting F0).

    A right scan terminates on a finite word; the left scan consumes its
    finite left word. The count is for differential testing, not a certificate.
    """
    steps = 0
    while True:
        a = r & 1
        if r & 2:
            # Repeated 11 or 01 chunks have closed-form output words.
            if a:
                count = ones(r) // 2
                l = (l << (2 * count)) | (2 * ((1 << (2 * count)) - 1) // 3)
            else:
                count = periodic_prefix(r, 2, 2)
                l <<= 2 * count
            r >>= 2 * count
            steps += 2 * count
        elif not r & 4:
            l = (l << 3) | (a << 2) | 1
            r >>= 3
            steps += 3
            break
        elif r & 8:
            count = periodic_prefix(r, 12 + a, 4)
            l = (l << (4 * count)) | ((1 + 8 * a) * ((1 << (4 * count)) - 1) // 15)
            r >>= 4 * count
            steps += 4 * count
        else:
            return None, steps + 3
    while True:
        if r & 1:
            count = ones(l) + 1
            r = (r >> 1) << (count + 1)
            l >>= count
            steps += count
        elif l & 1:
            count = periodic_prefix(l, 1, 2)
            if count:
                l >>= 2 * count
                r = ((r >> 1) << (2 * count + 1)) | ((1 << (2 * count + 1)) - 2)
                steps += 2 * count
            else:
                r = ((r >> 1) << 3) | 6 | ((l >> 1) & 1)
                l >>= 2
                steps += 2
        else:
            return (l | 1, r | 1), steps + 2


def transfer(l, r):
    """Apply the proved arithmetic batch, or return None if its guard fails."""
    a = ones(l)
    if not a or r & 3 != 1:
        return None
    tail = r >> 2
    b = ones(tail)
    if b < 2 or b % 2:
        return None
    tail >>= b + 1
    c = ones(tail)
    if c % 2:
        return None
    tail >>= c
    if tail & 3:
        return None
    tail >>= 2
    m = ones(tail)
    count = min(b // 2, m // 2)
    if not count:
        return None
    tail >>= m
    a2, b2, c2, m2 = a + 2 * count, b - 2 * count, c + 2 * count, m - 2 * count
    l2 = ((l >> a) << a2) | ((1 << a2) - 1)
    r2 = (tail << m2) | ((1 << m2) - 1)
    r2 <<= 2
    r2 = (r2 << c2) | ((1 << c2) - 1)
    r2 <<= 1
    r2 = (r2 << b2) | ((1 << b2) - 1)
    return (l2, (r2 << 2) | 1), count


def bits_to_int(bits):
    return sum(b << i for i, b in enumerate(bits))


def raw_check(l, r, result, steps):
    """Independent coordinate-tape interpreter; compare the entire tape."""
    table = MACHINE.replace("_", "")
    table = [None if table[i:i+3] == "---" else
             (int(table[i]), 1 if table[i+1] == "R" else -1, ord(table[i+2]) - 65)
             for i in range(0, 36, 3)]
    tape = {-i-1 for i in range(l.bit_length()) if l >> i & 1}
    tape.update(i for i in range(r.bit_length()) if r >> i & 1)
    head, state = 0, 1
    for _ in range(steps):
        op = table[2 * state + (head in tape)]
        assert op is not None, "shortcut passed a halt"
        write, move, state = op
        if write:
            tape.add(head)
        else:
            tape.discard(head)
        head += move
    if result is None:
        assert table[2 * state + (head in tape)] is None
    else:
        left = sum(1 << (head - i - 1) for i in tape if i < head)
        right = sum(1 << (i - head) for i in tape if i >= head)
        assert (state, left, right) == (1, *result), (l, r, result, (state, left, right))


def selftest():
    rng = random.Random(623007)
    cases = list(itertools.product(range(64), repeat=2))
    cases += [(rng.getrandbits(40), rng.getrandbits(40)) for _ in range(2000)]
    for l, r in cases:
        result, steps = sweep(l, r)
        raw_check(l, r, result, steps)
    batches = 0
    for a, b, c, m in itertools.product(range(1, 5), range(1, 5), range(4), range(2, 9)):
        left = bits_to_int([1]*a + [0] + [rng.randrange(2) for _ in range(8)])
        right = bits_to_int([1, 0] + [1]*(2*b) + [0] + [1]*(2*c) +
                            [0, 0] + [1]*m + [0] + [rng.randrange(2) for _ in range(8)])
        result, count = transfer(left, right)
        ordinary = (left, right)
        steps = 0
        for _ in range(2 * count):
            ordinary, n = sweep(*ordinary)
            steps += n
            assert ordinary is not None
        assert ordinary == result
        raw_check(left, right, result, steps)
        batches += 1
    assert sweep(1, 25)[0] == (1, 77)  # 10011 -> 1011001
    assert sweep(1, 77)[0] is None
    print(json.dumps({"selftest": "passed", "sweep_cases": len(cases), "batch_cases": batches}))


def run(args):
    initial_state = args.start or "A"
    l, r, base, batch_count = 1, int(initial_state == "E"), 0, 0
    if args.resume:
        data = json.loads(args.resume.read_text())
        if data.get("schema") != SCHEMA or data.get("machine") != MACHINE:
            raise ValueError("checkpoint is for a different recurrence")
        initial_state = data.get("initial_state", "A")
        if initial_state not in ("A", "E") or (args.start and args.start != initial_state):
            raise ValueError("checkpoint has a different starting state")
        if data.get("status") not in ("iteration_limit", "time_limit", "space_limit"):
            raise ValueError("checkpoint is not resumable")
        l, r = int(data["left_hex"], 16), int(data["right_hex"], 16)
        base, batch_count = data["iterations"], data["batches"]
        if l < 0 or r < 0 or type(base) is not int or type(batch_count) is not int:
            raise ValueError("invalid checkpoint integers")
        if not 0 <= batch_count <= base:
            raise ValueError("invalid checkpoint counters")
    start = time.monotonic()
    status = "iteration_limit"
    done = 0
    for _ in range(args.iterations):
        if time.monotonic() - start >= args.seconds:
            status = "time_limit"
            break
        if max(l.bit_length(), r.bit_length()) > args.max_bits:
            status = "space_limit"
            break
        batch = None if args.no_transfer else transfer(l, r)
        if batch:
            (l, r), _ = batch
            batch_count += 1
        else:
            result, _ = sweep(l, r)
            if result is None:
                status = "halt_candidate"
                done += 1
                break
            l, r = result
        done += 1
    data = dict(schema=SCHEMA, machine=MACHINE, initial_state=initial_state,
                left_hex=hex(l), right_hex=hex(r),
                iterations=base+done, batches=batch_count, status=status)
    if args.output:
        args.output.write_text(json.dumps(data) + "\n")
    digest = hashlib.sha256((hex(l) + ":" + hex(r)).encode()).hexdigest()
    print(json.dumps({k: data[k] for k in ("initial_state", "iterations", "batches", "status")} |
                     {"left_bits": l.bit_length(), "right_bits": r.bit_length(),
                      "seconds": time.monotonic()-start, "digest": digest}))
    return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--start", choices=("A", "E"),
                        help="blank starting state; defaults to A or the checkpoint's start")
    parser.add_argument("--iterations", type=int, default=100000)
    parser.add_argument("--seconds", type=float, default=20)
    parser.add_argument("--max-bits", type=int, default=200000)
    parser.add_argument("--no-transfer", action="store_true")
    parser.add_argument("--resume", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.iterations < 0 or not math.isfinite(args.seconds) or args.seconds < 0 or args.max_bits < 1:
        parser.error("invalid budget")
    if args.selftest:
        selftest()
    else:
        run(args)
