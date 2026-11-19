#!/usr/bin/env python3
"""Certify return-or-halt bounds on intervals below the known #758 halting basin.

Run alongside check_bb33.py. A completed cover means that each seed in the
requested interval halts or reaches a strictly larger reset parameter <= U.
See COVER_758.md for the induction that turns this into a halting statement.
"""
import argparse
from bisect import bisect_right
from dataclasses import dataclass

from check_bb33 import HALTING_TARGET as H, WALL_FAR, WALL_NEAR, champion_step


U = H - WALL_NEAR
# This many powers suffice to batch the J runs near H. A shorter table would
# merely split some runs into several batches.
POWERS = tuple(3**k for k in range(H.bit_length() + 1))


@dataclass(frozen=True)
class Trace:
    word: bytes
    max_mass_gain: int
    reset: int | None  # None is a verified terminal instruction.


def trace(seed, step_limit):
    """Stop at the first even-a nonbulk state; it halts or returns in one step."""
    if seed < 3:
        raise ValueError("a reset seed must be at least 3")
    a, c = champion_step(1, seed)
    gain = a + 2*c - (1 + 2*seed)
    steps = 1
    word = bytearray()
    while steps < step_limit:
        q = (c + 1) // 4
        if a >= 4*q + 3:
            a, c = a - 4*q - 3, 6*q + 5
            word.append(ord("L"))
            gain += 9
        elif a % 2 == 0:
            end = champion_step(a, c)
            if end is None:
                return Trace(bytes(word), gain + 5, None)
            assert end[0] == 1 and seed < end[1] and 2*(end[1]-seed) <= gain + 5
            return Trace(bytes(word), gain + 5, end[1])
        elif a <= c:
            u = a + 1
            k = max(1, bisect_right(POWERS, (2*c + u)//u) - 1)
            if steps + k >= step_limit:
                return None  # A terminal map call still has to follow the batch.
            factor = POWERS[k]
            a, c = factor*u - 1, c - u*((factor - 1)//2) + 2*k
            word.extend(b"J" * k)
            gain += 4*k
            steps += k
            continue
        else:
            assert c % 4 == 3 and a == c + 2
            a, c = 3*c + 8, 1
            word.append(ord("E"))
            gain += 8
        steps += 1
    return None  # Budget exhausted. This proves nothing about the seed.


@dataclass(frozen=True)
class Cover:
    frontier: int  # All requested seeds of this parity >= frontier were covered.
    nodes: int
    blocks: int
    status: str


def cover(lo, hi, ceiling, parity, node_limit, step_limit):
    first = lo + (parity-lo) % 2
    last = hi - (hi-parity) % 2
    if first > last:
        return Cover(first, 0, 0, "complete")
    left = trace(first, step_limit)
    right = left if first == last else trace(last, step_limit)
    pending = [(first, last, left, right)]
    frontier, nodes, blocks = last + 2, 0, 0
    while pending:
        if nodes == node_limit:
            return Cover(frontier, nodes, blocks, "node limit")
        low, high, left, right = pending.pop()
        nodes += 1
        assert high == frontier - 2
        if low == high:
            if left is None:
                return Cover(frontier, nodes, blocks, "step limit at " + str(low))
            if left.reset is not None and left.reset > ceiling:
                return Cover(frontier, nodes, blocks, "return above ceiling at " + str(low))
        elif (left is not None and right is not None and left.word == right.word
              and high + left.max_mass_gain // 2 <= ceiling):
            # All interior starts of this parity execute the same word. Halts
            # are safe; every returned parameter obeys the common mass bound.
            pass
        else:
            mid = low + 2*((high-low)//4)
            mid_trace = left if mid == low else trace(mid, step_limit)
            next_trace = right if mid+2 == high else trace(mid+2, step_limit)
            pending.extend(((low, mid, left, mid_trace),
                            (mid+2, high, next_trace, right)))
            continue
        frontier, blocks = low, blocks + 1
    return Cover(frontier, nodes, blocks, "complete")


def audit():
    # An independent, unbatched execution of the published two-counter rules.
    for seed in range(3, 2003):
        result = trace(seed, 2000)
        assert result is not None
        a, c = champion_step(1, seed)
        for code in result.word:
            old = a, c
            a, c = champion_step(a, c)
            old_a, old_c = old
            if code == ord("L"):
                q = (old_c + 1)//4
                assert (a, c) == (old_a-4*q-3, 6*q+5)
            elif code == ord("J"):
                assert (a, c) == (3*old_a+2, old_c-old_a+1)
            else:
                assert code == ord("E") and (a,c) == (3*old_c+8, 1)
        end = champion_step(a, c)
        assert end == (None if result.reset is None else (1, result.reset))
        calls = 2 + len(result.word)
        assert trace(seed, calls) == result and trace(seed, calls-1) is None
    # An unresolved singleton on the final pop must still report failure.
    assert cover(3,3,3,1,5,1).status == "step limit at 3"
    assert cover(3,3,3,1,5,2000).status == "return above ceiling at 3"
    assert cover(3,3,100,1,0,2000).status == "node limit"
    assert cover(3,3,100,1,1,2000).status == "complete"
    assert cover(3,3,3,0,0,1).status == "complete"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--far", type=int, help="include seeds from H minus this distance")
    group.add_argument("--to-blank", action="store_true", help="include every seed down to 3")
    parser.add_argument("--near", type=int, default=WALL_FAR,
                        help="exclude seeds at or above H minus this distance")
    parser.add_argument("--node-limit", type=int, default=200000,
                        help="maximum search nodes per parity")
    parser.add_argument("--step-limit", type=int, default=10000,
                        help="maximum individual map calls per endpoint")
    args = parser.parse_args()
    if not __debug__:
        parser.error("run without -O to execute the verification checks")
    far = H-3 if args.to_blank else args.far if args.far is not None else 16_000_000
    if not WALL_FAR <= args.near < far <= H-3:
        parser.error("require 12,000,000 <= near < far <= H-3")
    if args.node_limit < 0 or args.step_limit < 1:
        parser.error("require nonnegative node limit and positive step limit")
    audit()
    lo, hi = H-far, H-args.near-1
    results = [cover(lo, hi, U, p, args.node_limit, args.step_limit) for p in (0,1)]
    for p, result in enumerate(results):
        print(f"parity {p}: {result.status}; nodes={result.nodes}; blocks={result.blocks}; "
              f"frontier={result.frontier}", flush=True)
    joint = max(lo, max(r.frontier for r in results)-1)
    if joint <= hi:
        print(f"Both parities covered from H-{H-joint} through H-{args.near+1}, inclusive.")
    else:
        print("No joint extension.")
    if any(r.status != "complete" for r in results):
        print("Requested interval incomplete.")
        return 1
    print("Requested interval complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
