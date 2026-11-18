"""Replay moving-window jumps and continuations against an independent literal TM."""
import os
from pathlib import Path
import sys
import unittest

from checkpoints import ROOT, holdouts
import survey
sys.path.insert(0,str(ROOT))
from prior_sweeps import TapeMachine

ENGINE=Path(os.environ.get('BB25_WINDOW','/tmp/bb25-window'))


class WindowTests(unittest.TestCase):
    def compare(self,line,machine,seed,target,width):
        r,_=survey.advance(ENGINE,line,machine,seed,target,10**8,width)
        lit=TapeMachine(machine)
        if seed:
            lit.steps,lit.head,lit.state=seed['steps'],seed['head'],seed['state']
            lit.tape={seed['left']+j:a for j,a in enumerate(survey.verify_state(seed,machine)) if a}
        while lit.steps<target and lit.step(): pass
        got={r['left']+j:a for j,a in enumerate(survey.verify_state(r,machine)) if a}
        self.assertEqual((lit.steps,lit.head,lit.state,lit.tape),(r['steps'],r['head'],r['state'],got))
        return r

    def test_blank_and_long_checkpoint_continuations(self):
        for i,m in enumerate(holdouts(),1):
            with self.subTest(line=i):
                r=self.compare(i,m,None,7777,3)
                self.compare(i,m,r,10345,9)
                cp=survey.load(ROOT/'frontiers'/'runs'/f'window-{i:02}.json',i,m)
                self.compare(i,m,cp,cp['steps']+1234,6)

    def test_halt_and_budget(self):
        for machine,target,expected in [('---'*5+'_'+'---'*5,0,0),('1RB'+'---'*4+'_'+'---'*5,1,1)]:
            r=self.compare(1,machine,None,target,4)
            self.assertEqual((r['status'],r['steps']),('halt',expected))
        m=holdouts()[6];p,work=survey.advance(ENGINE,7,m,None,10**6,0,7)
        self.assertEqual((p['status'],p['steps'],work),('unknown',0,0))
        # A confined loop repeatedly reaches the internal crossing cap. Its
        # intermediate state and counters must still agree at an odd stop.
        self.compare(1,'0RB'*5+'_'+'0LA'*5,None,22221,4)


if __name__=='__main__': unittest.main()
