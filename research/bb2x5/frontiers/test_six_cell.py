"""Compare six-cell stride runs with a literal interpreter and the independent window checkpoints."""
import os
from pathlib import Path
import sys
import unittest

from checkpoints import ROOT
import six_cell
import survey

sys.path.insert(0, str(ROOT))
from prior_sweeps import TapeMachine

ENGINE = Path(os.environ.get('BB25_STRIDE', '/tmp/bb25-stride'))


class StrideTests(unittest.TestCase):
    def compare(self, line, seed, target, work=10**9):
        machine = six_cell.MACHINES[line]
        p, used = six_cell.advance(ENGINE, line, seed, target, work)
        self.assertLessEqual(used, work)
        m = TapeMachine(machine)
        if seed:
            m.steps, m.head, m.state = seed['steps'], seed['head'], seed['state']
            m.tape = {seed['left']+i: s for i, s in enumerate(survey.verify_state(seed, machine)) if s}
        while m.steps < p['steps'] and m.step():
            pass
        tape = {p['left']+i: s for i, s in enumerate(survey.verify_state(p,machine)) if s}
        self.assertEqual((m.steps,m.head,m.state,m.tape), (p['steps'],p['head'],p['state'],tape))
        self.assertEqual(p['status'], 'unknown' if (m.state, m.tape.get(m.head,0)) in m.rules else 'halt')
        if used < work and p['status'] != 'halt':
            self.assertEqual(p['steps'], target)
        return p

    def test_literal_targets_partial_and_resume(self):
        for line in six_cell.MACHINES:
            with self.subTest(line=line):
                seed = None
                for target in (0,1,2,3,6,13,100,777,7777,99999,100000):
                    seed = self.compare(line,seed,target)
                short = self.compare(line,seed,1000000,10)
                self.assertLess(short['steps'],1000000)
                self.compare(line,short,short['steps']+16017)

    def test_halt_inside_tile(self):
        machine = six_cell.MACHINES[14]
        p, _ = survey.pack(14, machine, f'unknown 0\n{machine}\n10 0 0\n1 1 3')
        # A0 sends B onto the undefined B3 in one step.
        self.assertEqual(self.compare(14,p,100)['steps'], 11)

    def test_ten_billion_from_blank(self):
        for line, machine in six_cell.MACHINES.items():
            with self.subTest(line=line):
                saved = survey.load(ROOT/f'frontiers/runs/window-{line:02}.json',line,machine)
                replay, _ = six_cell.advance(ENGINE,line,None,saved['steps'],10**9)
                self.assertEqual(replay,saved)
                self.compare(line,saved,saved['steps']+24681)


if __name__ == '__main__':
    unittest.main()
