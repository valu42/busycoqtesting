"""Checks of the local kernels, the old exact clocks and the saved continuations."""
from copy import copy
import json
import unittest
from unittest.mock import patch

from checkpoints import checksum
from hydra import MACHINES, ROOT, Machine, load
from exact_blocks import Engine, Run
from line4_cert import ZERO, verify_rule
from prior_sweeps import TapeMachine


def physical(machine):
    raw = TapeMachine(machine.code)
    raw.head, raw.state, raw.steps = machine.head, machine.state, machine.steps
    for stack, x, direction in ((machine.left, machine.head - 1, -1), (machine.right, machine.head, 1)):
        for digit, n in reversed(stack):
            if digit:
                raw.tape.update((x + direction*i, digit) for i in range(n))
            x += direction * n
    return raw


def approach(machine, target):
    """Stop at the last complete operation at or before the specified raw time."""
    while machine.steps < target:
        before = copy(machine)
        before.right, before.left = machine.right.copy(), machine.left.copy()
        if not machine.step():
            raise AssertionError('unexpected halt')
        if machine.steps > target:
            return before
    return machine


class HydraTests(unittest.TestCase):
    def test_opaque_core(self):
        # The sentinel 9 is arbitrary context and the verifier rejects a read of it.
        for line, code in MACHINES.items():
            stride = 3 if line == 29 else 2
            rules = {(q, d): row[3*d:3*d+3] for q, row in zip('AB', code.split('_')) for d in range(5)}
            verify_rule(([9], [0, 2] + [0]*stride + [9]),
                        ([9] + [3]*stride, [3, 2, 9]), ZERO + 12 + stride, rules)
            verify_rule(([9], [0, 3, 9]), ([9, 3], [0, 9]), ZERO + 3, rules)

    def test_literal_from_blank(self):
        for line in MACHINES:
            m = Machine(line)
            raw = TapeMachine(m.code)
            while m.steps < 20000:
                self.assertTrue(m.step())
                while raw.steps < m.steps:
                    self.assertTrue(raw.step())
                self.assertEqual((m.state, m.head, physical(m).tape), (raw.state, raw.head, raw.tape))

    def test_halt(self):
        for line in MACHINES:
            m = Machine(line)
            m.right = [(2, 1)]
            self.assertFalse(m.step())
            self.assertEqual((m.steps, m.operations, m.payload()['status']), (0, 0, 'halt'))

    def test_old_block_checkpoints(self):
        for line in MACHINES:
            m = Machine(line)
            path = ROOT/'accelerator-results'/f'line-{line}-level-12.json'
            engine = Engine(m.code)
            old = Run.restore(engine, json.loads(path.read_text()))
            m = approach(m, old.steps)
            # Split the last multi-sweep, then finish the last run literally.
            with patch.object(Machine, 'bulk_sweep', return_value=False):
                m = approach(m, old.steps)
            raw = physical(m)
            while raw.steps < old.steps:
                self.assertTrue(raw.step())
            self.assertEqual((raw.head, raw.state, raw.tape), (old.head, 'AB'[old.state], old.sparse_tape(engine)))

    def test_published_hydra_normal_form(self):
        # Re-encode our physical tape in the other replay's checkpoint format.
        # hydra.md links its exact source and commit; this check works offline.
        m = Machine(30)
        m.advance(329461)
        self.assertEqual(m.left, [])
        self.assertEqual(m.state, 'A')
        a = m.right[2][1]
        self.assertEqual(m.right, [(2, 1), (3, 9889), (0, a), (2, 1), (0, 1)])
        normal = {'machine': m.code, 'events': 20000, 'a_hex': hex(a), 'b': m.right[1][1],
                  'left_hex': hex(m.head + 1), 'head_hex': hex(m.head), 'state': m.state,
                  'raw_steps_hex': hex(m.steps), 'normal_form': '2 0^a 3^b 2; head on blank left of first 2'}
        self.assertEqual(checksum(normal), '7e16ac0a179fdd5ebee8c31d8da51191013b14d6d1ffcee96c5ec7277009043d')

    def test_replay_and_published_bonus_entry(self):
        for line in MACHINES:
            m = Machine(line)
            if line == 29:
                m.advance(2259)
                self.assertEqual((m.steps, m.state, m.left, m.right),
                                 (1894603970741566467769886232237213051, 'B', [],
                                  [(2, 1), (3, 10), (0, 1287547464911049660)]))
            saved = load(ROOT/'frontiers'/'runs'/f'hydra-{line}.json', line)
            m.advance(saved.operations)
            self.assertEqual(saved.payload(), m.payload())
            m.advance(m.operations + 100)
            saved.advance(saved.operations + 100)
            self.assertEqual(saved.payload(), m.payload())


if __name__ == '__main__':
    unittest.main()
