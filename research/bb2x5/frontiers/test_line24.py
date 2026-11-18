"""Line 24 clock, full-tape comparisons and exceptional positive excursions."""
from itertools import chain
import os
from pathlib import Path
import unittest

from checkpoints import ROOT
from line24 import Line24
from longitudinal import HALTED
from prior_sweeps import TapeMachine
import survey


def expand(driver, state):
    """Materialize a small boundary, with the origin fixed at the tape join."""
    _, blocks = driver.left(2 * state['groups'])
    nearest = [c for copies, pattern in blocks for _ in range(copies)
               for c in chain.from_iterable(pattern)]
    cells = nearest[::-1] + list(map(int, state['positive_tape']))
    tm = TapeMachine(driver.machine, cells, left=-len(nearest))
    tm.steps = state['steps']
    return tm


class Sweeps(unittest.TestCase):
    def setUp(self):
        self.d = Line24()
        self.engine = Path(os.environ.get('BB25_STREAM', '/tmp/bb25-stream'))

    def advance(self, state, goal):
        return self.d.run(state, goal, self.engine, 2**26, 2**20, 2**27, 10**6, lambda _: None)

    def test_literal_boundaries(self):
        tm = TapeMachine(self.d.machine)
        state = self.d.blank()
        for groups in (0, 1, 2, 4, 30, 123):
            state = self.advance(state, groups)
            while tm.steps < state['steps']:
                self.assertTrue(tm.step())
            lifted = expand(self.d, state)
            self.assertEqual((tm.head, tm.state, tm.tape), (0, 'A', lifted.tape))
        self.assertEqual(state, self.advance(self.d.blank(), 123))

    def test_synthetic_exception(self):
        # A child B2 can reach B4 on a real instruction or return B across
        # the root. Neither case may count as a completed AB pair.
        seed = self.d.blank()
        halted = self.advance({**seed, 'positive_tape': '231'}, 1)
        self.assertEqual((halted['format'], halted['steps'], halted['state'], halted['head']),
                         (HALTED, 68, 'B', 0))
        self.assertEqual(halted['positive_tape'], '43333')
        with self.assertRaisesRegex(ValueError, 'unexpected return'):
            self.advance({**seed, 'positive_tape': '2'}, 1)

    def test_independent_window(self):
        old = survey.load(ROOT/'frontiers/runs/window-24.json', 24, self.d.machine)
        tm = expand(self.d, self.advance(self.d.blank(), 40815))
        self.assertLess(old['steps'] - tm.steps, 5_000_000)
        self.assertGreaterEqual(old['steps'], tm.steps)
        while tm.steps < old['steps']:
            self.assertTrue(tm.step())
        cells = survey.verify_state(old, self.d.machine)
        tape = {old['left'] + i: c for i, c in enumerate(cells) if c}
        self.assertEqual((tm.head, tm.state, tm.tape), (old['head'], old['state'], tape))


if __name__ == '__main__':
    unittest.main()
