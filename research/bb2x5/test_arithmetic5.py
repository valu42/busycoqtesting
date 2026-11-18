"""Differential and control tests: python3 -m unittest test_arithmetic5 -v."""
import hashlib
import json
from pathlib import Path
import random
import tempfile
import unittest

from arithmetic5 import (Accelerator, MACHINE, Run, State, a_repeat_count,
                         advance, load, save, scalar, strip_threes)
from prior_sweeps import ARITHMETIC, audit_arithmetic_transition, published_return


def repeat(s, n):
    for _ in range(n):
        if s is None:
            raise AssertionError("accelerator crossed a halt")
        s = scalar(s)
    return s


class ArithmeticTests(unittest.TestCase):
    def test_identity_and_literal_machine(self):
        self.assertEqual(MACHINE, ARITHMETIC)
        self.assertEqual(audit_arithmetic_transition(None, ("A", 4, 4)), 136)
        for tag in "AB":
            for a in range(12):
                for b in range(18):
                    s = scalar(State(tag, a, b))
                    expected = None if s is None else (s.tag, s.a, s.b)
                    self.assertEqual(expected, published_return(tag, a, b))
                    audit_arithmetic_transition((tag, a, b), expected)

    def test_a_jump_guards(self):
        acc = Accelerator()
        for a in range(40):
            for b in range(150):
                s = State("A", a, b)
                t, events, _ = acc.step(s)
                self.assertEqual(t, repeat(s, events))
                k = a_repeat_count(a, b)
                if k:
                    self.assertLessEqual((a+4)*((1<<k)-1)-k, b)
                self.assertGreater((a+4)*((1<<(k+1))-1)-(k+1), b)
        for k in (1, 10, 100, 10000):
            a = 27
            bound = (a+4)*((1<<k)-1)-k
            for delta in (-1, 0, 1):
                self.assertEqual(a_repeat_count(a, bound+delta), k-1 if delta < 0 else k)

    def test_b_blocks_exhaustive_quotient_lifting(self):
        for width in range(1, 6):
            acc = Accelerator(width)
            for residue in range(3**width):
                for b in (0, 2, 3):
                    block = acc.compile_block(residue, b)
                    for quotient in (0, 1, 13, 2**150+19):
                        start = State("B", residue+3**width*quotient, b)
                        t = block.state
                        extra = block.coefficient*quotient
                        expected = State("A", t.a, t.b+extra) if t.tag == "A" else State("B", t.a+extra, t.b)
                        self.assertEqual(repeat(start, block.events), expected)
                        q = start
                        for j in range(block.events):
                            self.assertEqual(q.tag, "B")
                            q = scalar(q)

    def test_random_full_accelerator(self):
        rng = random.Random(20261118)
        acc = Accelerator(6, max_cache=100)
        for _ in range(3000):
            s = State(rng.choice("AB"), rng.getrandbits(rng.randrange(1, 300)),
                      rng.choice((0, 2, 3, rng.getrandbits(80))))
            t, n, _ = acc.step(s)
            self.assertEqual(t, repeat(s, n))
        self.assertLessEqual(len(acc.cache), 100)

    def test_long_b_valuation_branches(self):
        for k in (0, 1, 2, 7, 100, 1000):
            q, count = strip_threes(7*3**k)
            self.assertEqual((q, count), (7, k))
        acc = Accelerator()
        for k in (2, 3, 17, 500):
            for shift, b in ((9, 0), (11, 2)):
                a = (7*3**k-shift)//2
                s = State("B", a, b)
                out, events, rule = acc.step(s)
                self.assertEqual((events, rule), (k, "B-valuation"))
                self.assertEqual(out, repeat(s, k))
                self.assertEqual(out.a, (7*5**k-shift)//2)

    def test_halts_and_adjacent_guards(self):
        for k in range(15):
            b = 16*(1<<k)-11-k
            for delta in (-1, 0, 1):
                s = State("A", 4, b+delta)
                acc = Accelerator()
                if k:
                    s, n, _ = acc.step(s)
                    self.assertEqual(n, k)
                out, _, _ = acc.step(s)
                self.assertEqual(out is None, delta == 0)
            run = Run(State("A", 4, b))
            self.assertEqual(advance(run, 1, 3, Accelerator()), "halt")
            self.assertTrue(run.halted)
            self.assertEqual(advance(run, 1, 3, Accelerator()), "halt")

    def test_blank_rounds_against_scalar(self):
        a = Run()
        b = State("A", 4, 4)
        events = 0
        first = []
        acc = Accelerator()
        for i in range(150):
            first.append(b.b)
            while True:
                old, b = b, scalar(b)
                events += 1
                self.assertIsNotNone(b)
                if old.tag == "B" and b.tag == "A":
                    break
            self.assertEqual(advance(a, 1, 10000, acc), "round-budget")
            self.assertEqual(a.state, b)
            self.assertEqual(a.macro_events, events)
            self.assertEqual(a.rounds, i+1)
        self.assertEqual(first[:4], [4, 64, 104, 569])

    def test_budget_resume_and_rejection(self):
        acc = Accelerator()
        reference = Run()
        self.assertEqual(advance(reference, 1000, 100000, acc), "round-budget")
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/"state.json"
            run = Run()
            self.assertEqual(advance(run, 1000, 1, acc), "work-budget")
            self.assertEqual(run.state.tag, "B")
            save(run, p)
            run = load(p)
            self.assertEqual(advance(run, 1000-run.rounds, 100000, acc), "round-budget")
            self.assertEqual(run, reference)
            save(run, p)
            self.assertEqual(load(p), run)
            doc = json.loads(p.read_text())
            doc["payload"]["state"]["b_hex"] = "0x0"
            p.write_text(json.dumps(doc))
            with self.assertRaisesRegex(ValueError, "checksum"):
                load(p)
            for change in ("machine", "halted", "rounds_hex"):
                save(run, p)
                doc = json.loads(p.read_text())
                doc["payload"][change] = {"machine": "other", "halted": True, "rounds_hex": "0x-1"}[change]
                raw = json.dumps(doc["payload"], sort_keys=True, separators=(",", ":")).encode()
                doc["sha256"] = hashlib.sha256(raw).hexdigest()
                p.write_text(json.dumps(doc))
                with self.assertRaises(ValueError):
                    load(p)
            huge = Run(State("B", 1<<20000, 2))
            save(huge, p)
            self.assertEqual(load(p), huge)
        paused = Run()
        self.assertEqual(advance(paused, 10, 0, acc), "work-budget")
        self.assertEqual(paused, Run())
        self.assertEqual(advance(paused, 0, 100, acc), "round-budget")
        self.assertEqual(advance(paused, 10, 100, acc, seconds=0), "time-budget")
        for seconds in (-1, float("inf"), float("nan"), True):
            with self.assertRaises(ValueError):
                advance(paused, 10, 100, acc, seconds=seconds)
        for invalid in (-1, True):
            with self.assertRaises(ValueError):
                State("A", invalid, 0)
        with self.assertRaises(ValueError):
            Accelerator(0)
        with self.assertRaises(ValueError):
            advance(Run(), -1, 10, acc)


if __name__ == "__main__":
    unittest.main()
