#!/usr/bin/env python3
"""Independent literal-replay and checkpoint tests for exact_blocks.py."""
import copy
import itertools
import hashlib
import json
from pathlib import Path
import random
import tempfile
from unittest.mock import patch
import unittest

from exact_blocks import Answer, Blocks, Engine, ResourceLimit, Run, integer_text, read_integer, save_checkpoint

MACHINES = Path(__file__).with_name('BB2x5_Rocq_holdouts_37.txt').read_text().splitlines()


class Literal:
    """Separate table decoding and sparse one-step semantics; no accelerator calls."""
    def __init__(self, encoding, tape=None, head=0, state=0):
        self.rows = encoding.split('_')
        self.tape = {} if tape is None else dict(tape)
        self.head, self.state, self.steps = head, state, 0

    def step(self):
        symbol = self.tape.get(self.head, 0)
        token = self.rows[self.state][symbol*3:symbol*3+3]
        if token == '---':
            return False
        write = int(token[0])
        if write:
            self.tape[self.head] = write
        else:
            self.tape.pop(self.head, None)
        self.head += 1 if token[1] == 'R' else -1
        self.state = ord(token[2]) - ord('A')
        self.steps += 1
        return True

    def snapshot(self):
        return self.state, self.head, dict(self.tape)


class ExactTests(unittest.TestCase):
    def check_local(self, encoding, word, state, side):
        engine = Engine(encoding, max_work=100000)
        node = engine.blocks.word(word)
        answer = engine.exit(node, state, side)
        machine = Literal(encoding, {i: x for i, x in enumerate(word) if x},
                          0 if side == 0 else len(word)-1, state)
        for _ in range(answer.steps):
            self.assertTrue(0 <= machine.head < len(word))
            self.assertTrue(machine.step())
        self.assertEqual((machine.state, machine.head, machine.tape),
                         (answer.state, answer.position, dict(engine.blocks.nonzero(answer.node))))
        if answer.status == 'exit':
            self.assertIn(machine.head, (-1, len(word)))
        elif answer.status == 'halt':
            self.assertFalse(machine.step())
        else:
            self.assertEqual(answer.status, 'loop')
            self.assertGreater(answer.period, 0)
            before = machine.snapshot()
            for _ in range(answer.period):
                self.assertTrue(0 <= machine.head < len(word))
                self.assertTrue(machine.step())
            self.assertEqual(machine.snapshot(), before)
        self.assertEqual(engine.exit(node, state, side), answer)

    def test_all_holdout_small_blocks(self):
        randomizer = random.Random(20261118)
        for encoding in MACHINES:
            words = [(i,) for i in range(5)]
            words += list(itertools.product(range(5), repeat=2))
            words += [tuple(randomizer.randrange(5) for _ in range(4)) for _ in range(20)]
            for word in words:
                for state in (0, 1):
                    for side in (0, 1):
                        self.check_local(encoding, word, state, side)

    def test_blank_trajectories_and_resume(self):
        for encoding in MACHINES:
            engine = Engine(encoding)
            run = Run.blank(engine, 3)
            literal = Literal(encoding)
            for index in range(80):
                run.advance(engine)
                self.assertLess(run.steps, 1000000)
                while literal.steps < run.steps:
                    self.assertTrue(literal.step())
                self.assertEqual((run.state, run.head, run.sparse_tape(engine)), literal.snapshot())
                if index == 39:
                    document = json.loads(json.dumps(run.checkpoint(engine)))
                    fresh = Engine(encoding)
                    restored = Run.restore(fresh, document)
                    self.assertEqual(restored.checkpoint(fresh), document)
                    engine, run = fresh, restored
                if run.status != 'running':
                    break

    def test_halt_loop_and_boundary_semantics(self):
        # Primitive exiting a block must not peek at the neighbor's halt.
        self.check_local('1RB---_---0LA', [0], 0, 0)
        engine = Engine('1RB---_---0LA')
        run = Run.blank(engine, 0)
        run.advance(engine)
        self.assertEqual((run.status, run.steps, run.head), ('running', 1, 1))
        run.advance(engine)
        self.assertEqual((run.status, run.steps, run.head), ('halt', 1, 1))
        # Two cells keep bouncing in a genuine exact loop.
        self.check_local('0RB_0LA', [0, 0], 0, 0)
        engine = Engine('0RB_0LA')
        run = Run.blank(engine, 1)
        run.advance(engine)
        self.assertEqual(run.status, 'loop')
        self.assertEqual(run.period, 2)
        document = run.checkpoint(engine)
        fresh = Engine(engine.encoding)
        self.assertEqual(Run.restore(fresh, document).checkpoint(fresh), document)

    def test_atomic_budgets(self):
        for options in ({'max_work': 0}, {'max_work': 3}, {'max_nodes': 6},
                        {'max_cache': 0}, {'seconds': 0}):
            engine = Engine(MACHINES[20], **options)
            run = Run.blank(engine, 8)
            before = run.checkpoint(engine)
            with self.assertRaises(ResourceLimit):
                run.advance(engine)
            self.assertEqual(run.checkpoint(engine), before)

    def test_checkpoint_rejects_damage(self):
        engine = Engine(MACHINES[0])
        run = Run.blank(engine, 2)
        for _ in range(10):
            run.advance(engine)
        document = run.checkpoint(engine)
        document['payload']['steps'] = '999'
        with self.assertRaises(ValueError):
            Run.restore(Engine(engine.encoding), document)

    def test_checkpoint_rejects_negative_period(self):
        engine = Engine('---')
        run = Run.blank(engine, 0)
        run.advance(engine)
        document = run.checkpoint(engine)
        document['payload']['period'] = '-1'
        canonical = json.dumps(document['payload'], sort_keys=True, separators=(',', ':')).encode()
        document['sha256'] = hashlib.sha256(canonical).hexdigest()
        with self.assertRaises(ValueError):
            Run.restore(Engine(engine.encoding), document)

    def test_atomic_checkpoint_write(self):
        engine = Engine(MACHINES[0])
        run = Run.blank(engine, 2)
        with tempfile.TemporaryDirectory(dir=Path.cwd()) as directory:
            path = Path(directory) / 'checkpoint.json'
            save_checkpoint(run, engine, path)
            before = path.read_bytes()
            with patch('exact_blocks.json.dump', side_effect=OSError('injected write failure')):
                with self.assertRaises(OSError):
                    save_checkpoint(run, engine, path)
            self.assertEqual(path.read_bytes(), before)
            self.assertEqual(list(Path(directory).iterdir()), [path])

    def test_exponential_reuse(self):
        engine = Engine('1RA1RA', max_work=1000)
        node = engine.blocks.zero(60)
        answer = engine.exit(node, 0, 0)
        self.assertEqual((answer.steps, answer.position, answer.status), (1 << 60, 1 << 60, 'exit'))
        self.assertLess(engine.work, 400)
        self.assertLess(len(engine.blocks.nodes), 130)
        self.assertEqual(engine.blocks.symbol_at(answer.node, (1 << 60)-1), 1)

    def test_large_integer_checkpoint(self):
        engine = Engine(MACHINES[0])
        run = Run.blank(engine, 1)
        run.steps = 1 << 20000
        document = run.checkpoint(engine)
        self.assertTrue(document['payload']['steps'].startswith('0x'))
        restored = Run.restore(Engine(engine.encoding), json.loads(json.dumps(document)))
        self.assertEqual(restored.steps, run.steps)
        self.assertEqual(read_integer(integer_text(-run.steps)), -run.steps)

    def test_arbitrarily_large_zero_block_export(self):
        blocks = Blocks(5)
        node = blocks.zero(60)
        self.assertEqual(list(blocks.nonzero(node)), [])
        self.assertEqual(len(blocks.nodes), 65)


if __name__ == '__main__':
    unittest.main()
