#!/usr/bin/env python3
"""Exact integer accelerator for formal BB(2,5) holdout line 5.

The published A/B macro recurrence is credited to mxdys and Racheline; see
https://wiki.bbchallenge.org/wiki/1RB3LA1LA1RA1RA_2LB2RA---4RB1LB
A and B here name tape families: BOTH have the physical head in TM state A.
No theorem prover checks this Python implementation. A finite unfinished run
is unknown. Counts of macro events are NOT counts of elementary TM steps.

Run from any directory, e.g.:
  python3 arithmetic5.py --rounds 10000 --checkpoint arithmetic5-run.json
  python3 arithmetic5.py --resume arithmetic5-run.json --rounds 10000 \
      --checkpoint arithmetic5-run.json
Checkpoints are exact, atomic JSON writes using hexadecimal natural numbers.
They store a normal form; their checksums do not certify blank reachability.
Without --resume, the seed is A(4,4), reached from blank in 136 defined steps.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
import os
import math
import time
from pathlib import Path
import tempfile
from typing import Optional

MACHINE = "1RB3LA1LA1RA1RA_2LB2RA---4RB1LB"
FORMAT = "bb2x5-arithmetic5-v1"
DATA_SHA256 = "89ea92fd4643166b92fca4ae80e37a699ab8615ac1dd375dae777e6b3e45ecc6"


def natural(n: int, name: str) -> None:
    if type(n) is not int or n < 0:
        raise ValueError(f"{name} must be a nonnegative integer")


@dataclass(frozen=True)
class State:
    tag: str
    a: int
    b: int

    def __post_init__(self):
        if self.tag not in ("A", "B"):
            raise ValueError("tag must be A or B")
        natural(self.a, "a")
        natural(self.b, "b")


def scalar(state: State) -> Optional[State]:
    """One published macro event. None is the actual halting branch."""
    tag, a, b = state.tag, state.a, state.b
    if tag == "A":
        if b >= a + 3:
            return State("A", 2*a + 4, b - a - 3)
        if b == a + 2:
            return State("B", 2*a + 2, 3)
        if b == a + 1:
            return None
        return State("B", a-b, 2*b)
    q, r = divmod(a, 3)
    if r == 1:
        return State("A", 4, 2 + 5*q + b)
    if r == 2:
        return State("B", 5 + 5*q + b, 2)
    return State("B", 3 + 5*q + b, 0)


def a_repeat_count(a: int, b: int) -> int:
    """Largest k with (a+4)(2**k - 1)-k <= b; no floating point."""
    natural(a, "a")
    natural(b, "b")
    # The ratio supplies a lower estimate; adjust using exact guards.
    k = max(0, ((b // (a+4)) + 1).bit_length() - 1)
    while (a+4)*((1 << (k+1))-1) - (k+1) <= b:
        k += 1
    while (a+4)*((1 << k)-1) - k > b:
        k -= 1
    return k


def strip_threes(n: int) -> tuple[int, int]:
    """Return (n / 3**v3(n), v3(n)) for positive n, by power doubling."""
    if type(n) is not int or n <= 0:
        raise ValueError("strip_threes requires a positive integer")
    powers = []
    p, k = 3, 1
    while n % p == 0:
        powers.append((p, k))
        p *= p
        k *= 2
    count = 0
    for p, k in reversed(powers):
        if n % p == 0:
            n //= p
            count += k
    return n, count


@dataclass(frozen=True)
class Block:
    """Image of residue + 3**width*q, including its quotient coefficient."""
    state: State
    coefficient: int
    events: int


class Accelerator:
    def __init__(self, block_width: int = 6, max_cache: int = 20000):
        if type(block_width) is not int or not 1 <= block_width <= 12:
            raise ValueError("block_width must be from 1 through 12")
        natural(max_cache, "max_cache")
        self.width = block_width
        self.modulus = 3**block_width
        self.max_cache = max_cache
        self.cache: dict[tuple[int, int], Block] = {}

    def compile_block(self, residue: int, b: int) -> Block:
        """Compile <=width B events; never cross a return to family A.

        At event j the coefficient of the unknown quotient is
        5**j * 3**(width-j). Before every decision it is divisible by 3,
        so the residue execution selects exactly the same branch for all q.
        """
        if not 0 <= residue < self.modulus:
            raise ValueError("residue outside block modulus")
        natural(b, "b")
        s, coefficient = State("B", residue, b), self.modulus
        for events in range(1, self.width+1):
            s = scalar(s)
            coefficient = (coefficient // 3) * 5
            if s.tag == "A":
                break
        return Block(s, coefficient, events)

    def step(self, s: State) -> tuple[Optional[State], int, str]:
        """One accelerated operation, its exact macro-event count and rule."""
        if s.tag == "A":
            k = a_repeat_count(s.a, s.b)
            if k:
                delta = (s.a+4)*((1 << k)-1)
                return State("A", s.a+delta, s.b-delta+k), k, "A-doubling"
            return scalar(s), 1, "scalar"
        # The two closed B branches have affine conjugates x -> 5x/3.
        shift = 9 if s.b == 0 and s.a % 3 == 0 else (
            11 if s.b == 2 and s.a % 3 == 2 else None)
        if shift is not None:
            quotient, k = strip_threes(2*s.a + shift)
            if k > 1:
                return State("B", (quotient*5**k-shift)//2, s.b), k, "B-valuation"
        # Other b values may be huge; use one exact event before caching.
        if s.b not in (0, 2, 3):
            return scalar(s), 1, "scalar"
        q, residue = divmod(s.a, self.modulus)
        key = residue, s.b
        block = self.cache.get(key)
        if block is None:
            block = self.compile_block(*key)
            if len(self.cache) < self.max_cache:
                self.cache[key] = block
        t, extra = block.state, block.coefficient*q
        out = State("A", t.a, t.b+extra) if t.tag == "A" else State("B", t.a+extra, t.b)
        return out, block.events, "B-block"


@dataclass
class Run:
    state: State = State("A", 4, 4)
    rounds: int = 0
    macro_events: int = 0
    accelerated_operations: int = 0
    halted: bool = False

    def validate(self):
        if not isinstance(self.state, State):
            raise ValueError("invalid state")
        for name in ("rounds", "macro_events", "accelerated_operations"):
            natural(getattr(self, name), name)
        if type(self.halted) is not bool:
            raise ValueError("halted must be boolean")
        if self.halted and not (self.state.tag == "A" and self.state.b == self.state.a+1):
            raise ValueError("halted checkpoint is not at the halting macro guard")


def advance(run: Run, rounds: int, max_operations: int, accelerator: Accelerator,
            seconds: Optional[float] = None) -> str:
    """Run additional complete A(4,b) rounds, stopping safely at a work budget."""
    run.validate()
    natural(rounds, "rounds")
    natural(max_operations, "max_operations")
    if seconds is not None and (type(seconds) not in (int, float) or not math.isfinite(seconds) or seconds < 0):
        raise ValueError("seconds must be finite and nonnegative")
    deadline = None if seconds is None else time.monotonic() + seconds
    target = run.rounds + rounds
    if run.halted:
        return "halt"
    for _ in range(max_operations):
        if run.rounds >= target:
            return "round-budget"
        if deadline is not None and time.monotonic() >= deadline:
            return "time-budget"
        old = run.state
        new, events, _ = accelerator.step(old)
        run.accelerated_operations += 1
        run.macro_events += events
        if new is None:
            run.halted = True
            return "halt"
        run.state = new
        if old.tag == "B" and new.tag == "A":
            run.rounds += 1
    return "round-budget" if run.rounds >= target else "work-budget"


def payload(run: Run) -> dict:
    run.validate()
    return {
        "format": FORMAT, "machine": MACHINE,
        "origin": "normal-form-checkpoint",
        "state": {"tag": run.state.tag, "a_hex": hex(run.state.a), "b_hex": hex(run.state.b)},
        "rounds_hex": hex(run.rounds), "macro_events_hex": hex(run.macro_events),
        "accelerated_operations_hex": hex(run.accelerated_operations), "halted": run.halted,
    }


def save(run: Run, path: Path) -> None:
    """Atomic replace; checksum detects accidental changes, not proof validity."""
    data = payload(run)
    canonical = json.dumps(data, sort_keys=True, separators=(",", ":")).encode()
    document = {"payload": data, "sha256": hashlib.sha256(canonical).hexdigest()}
    path = Path(path)
    with tempfile.NamedTemporaryFile("w", dir=path.parent, prefix=path.name+".", delete=False) as out:
        tmp = out.name
        try:
            json.dump(document, out, indent=2)
            out.write("\n")
            out.flush()
            os.fsync(out.fileno())
        except BaseException:
            os.unlink(tmp)
            raise
    try:
        os.replace(tmp, path)
    except BaseException:
        os.unlink(tmp)
        raise


def load(path: Path) -> Run:
    document = json.loads(Path(path).read_text())
    if type(document) is not dict or set(document) != {"payload", "sha256"}:
        raise ValueError("invalid checkpoint envelope")
    data = document["payload"]
    canonical = json.dumps(data, sort_keys=True, separators=(",", ":")).encode()
    if document["sha256"] != hashlib.sha256(canonical).hexdigest():
        raise ValueError("checkpoint checksum mismatch")
    expected = set(payload(Run()))
    if type(data) is not dict or set(data) != expected:
        raise ValueError("invalid checkpoint fields")
    if (data["format"] != FORMAT or data["machine"] != MACHINE or
        data["origin"] != "normal-form-checkpoint"):
        raise ValueError("checkpoint format, machine or origin mismatch")
    def number(value):
        if type(value) is not str or not value.startswith("0x"):
            raise ValueError("expected hexadecimal natural number")
        n = int(value, 16)
        if hex(n) != value:
            raise ValueError("expected canonical hexadecimal natural number")
        return n
    s = data["state"]
    if type(s) is not dict or set(s) != {"tag", "a_hex", "b_hex"}:
        raise ValueError("invalid checkpoint state")
    run = Run(State(s["tag"], number(s["a_hex"]), number(s["b_hex"])),
              number(data["rounds_hex"]), number(data["macro_events_hex"]),
              number(data["accelerated_operations_hex"]), data["halted"])
    run.validate()
    return run


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--rounds", type=int, default=1000, help="additional complete returns to A(4,b)")
    p.add_argument("--max-operations", type=int, default=1000000, help="bounded accelerated work, including intermediate B states")
    p.add_argument("--seconds", type=float, help="wall-clock budget, checked between accelerated operations")
    p.add_argument("--block-width", type=int, default=6, help="B composition width, 1 through 12")
    p.add_argument("--resume", type=Path)
    p.add_argument("--checkpoint", type=Path)
    args = p.parse_args()
    try:
        data = Path(__file__).with_name("BB2x5_Rocq_holdouts_37.txt").read_bytes()
        if hashlib.sha256(data).hexdigest() != DATA_SHA256 or data.decode().splitlines()[4] != MACHINE:
            raise ValueError("holdout dataset identity mismatch")
        run = load(args.resume) if args.resume else Run()
        accelerator = Accelerator(args.block_width)
        reason = advance(run, args.rounds, args.max_operations, accelerator, args.seconds)
        if args.checkpoint:
            save(run, args.checkpoint)
        # Hex keeps output exact even above Python's decimal conversion limit.
        print(json.dumps({"status": "halt" if run.halted else "unknown", "stop_reason": reason,
              "machine_line": 5, "state_family": run.state.tag,
              "a_bits": run.state.a.bit_length(), "b_bits": run.state.b.bit_length(),
              "rounds_hex": hex(run.rounds), "macro_events_hex": hex(run.macro_events),
              "accelerated_operations_hex": hex(run.accelerated_operations),
              "counts_are_tm_steps": False, "checkpoint_is_reachability_proof": False, "cache_entries": len(accelerator.cache),
              "checkpoint": str(args.checkpoint) if args.checkpoint else None}, indent=2))
    except (ValueError, OSError, KeyError, TypeError, IndexError) as exc:
        p.error(str(exc))


if __name__ == "__main__":
    main()
