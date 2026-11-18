"""Check the timed register against the elementary machine, including cut-off bursts."""
import itertools
import os
import subprocess
from pathlib import Path
import unittest

from line17 import (DATA, HEAD, M17, ROOT, literal_counts, once_counts,
                    mark_image, periodic_counts, replay, word_counts)
from prior_frontier import T17, header17, mark_step
from prior_sweeps import TapeMachine
import survey

WORKER = Path(os.environ.get('BB25_MARK17', '/tmp/bb25-marks17'))
WINDOW = Path(os.environ.get('BB25_WINDOW', '/tmp/bb25-window'))


def pulse(trit, is_c):
    if not is_c:
        return [('B','A')]
    return [('B','A'),('B','A'),('A','A' if trit else 'B')] + ([] if trit else [('B','A')])


def check_local(v, flag, child, is_c):
    # Construct every normal subordinate probe and return letter, then run the
    # literal two cells until all requested input probes complete or physically halt.
    emitted = (((),(),(0,)), ((0,), (0,1), (0,0)))[is_c][v]
    tape = [int('102'[v]),2+flag]
    requests = pulse(v, is_c)
    children = []
    conflict = False
    for mark in emitted:
        if mark and flag:
            conflict = True
            break
        compound = bool(mark or flag)
        children.extend(pulse(child, compound))
        flag = int(compound and child != 0)
        child = (child+1+compound)%3
    clock = sent = 0
    for entry, leave in requests:
        q = 'AB'.index(entry)
        x = 0
        while x >= 0:
            if x == 2:
                expected, answer = children[sent]
                assert expected == 'AB'[q]
                sent += 1
                x,q = 1,'AB'.index(answer)
            else:
                op = T17[q][tape[x]]
                if op is None:
                    assert conflict
                    return
                tape[x], move, q = op
                x += move
                clock += 1
        assert 'AB'[q] == leave
    assert not conflict and sent == len(children)
    assert tape == [int('102'[(v+1+is_c)%3]),2+flag]
    result = literal_counts((v,0),[int(is_c)])
    assert clock == result.calls + sent + result.interior


class Line17Tests(unittest.TestCase):
    def test_pair_header_and_pile_costs(self):
        for v,f,child,c in itertools.product(range(3),range(2),range(3),(False,True)):
            check_local(v,f,child,c)
        for stop in (1,2,3):
            cost, probes = header17(stop)
            self.assertEqual(cost, 58+len(probes))
        leading = literal_counts((0,0), bytes((0,1,0,0)))
        self.assertEqual((leading.state,leading.slots,leading.calls,leading.interior), ((0,0),4,9,10))

    def test_all_partial_bursts_and_periods(self):
        for v,p in itertools.product(range(3),range(2)):
            for head,gap1,gap2 in itertools.product(range(4,7),range(3,6),range(3,6)):
                marks = [head,head+gap1,head+gap1+gap2]
                word = [int(i in marks) for i in range(1,22)]
                outputs = bytearray()
                state = v,p
                for n in range(len(word)+1):
                    exact = literal_counts((v,p),word[:n])
                    self.assertEqual(once_counts(n,marks,(v,p)), exact)
                    positions = [t for t in mark_image(marks,n,(v,p)) if t<=exact.slots]
                    self.assertEqual(positions, [t for t,b in enumerate(outputs,1) if b])
                    if n<len(word):
                        nv,np,out = mark_step(*state,word[n]);outputs.extend(out); state=nv,np
        for period, marks in [(6,[5]), (7,[1,4]), (10,[4,7]), (28,[3,7,14,23])]:
            word = bytes(int(i in marks) for i in range(1,period+1))
            for slots in range(8*period+1):
                self.assertEqual(periodic_counts(period,marks,slots),word_counts((1,0),b'',word,slots))

    def test_native_chunks_include_trailing_partial_bursts(self):
        period, marks = 10, [2,5,9]
        for slots in (0,1,2,3,20,251):
            args=[str(WORKER),str(slots),str(period),'7','500']
            reference=subprocess.check_output(args+['1'],input='2 5 9',text=True)
            self.assertEqual(reference,subprocess.check_output(args+['23'],input='2 5 9',text=True))
            word=bytes(int((i%period)+1 in marks) for i in range(slots))
            for row in reference.splitlines()[:-1]:
                v,p,n,calls,inner=map(int,row.split())
                result=literal_counts((1,0),word)
                self.assertEqual((result.state,result.slots,result.calls,result.interior),((v,p),n,calls,inner))
                from prior_frontier import marks_on_word
                _,word=marks_on_word((1,0),word)
            self.assertEqual(list(map(int,reference.splitlines()[-1].split()[1:])),
                             [i for i,bit in enumerate(word,1) if bit])

    def test_complete_blank_tapes_and_splits(self):
        machine=TapeMachine(M17)
        for n in (0,1,2,3,7,25,71,225,425):
            saved=replay(n,6)
            while machine.steps<saved['steps']:
                self.assertTrue(machine.step())
            word=HEAD+'12'*n+saved['register']+'2'
            expected={saved['head']+i:int(c) for i,c in enumerate(word,1) if c!='0'}
            self.assertEqual((machine.head,machine.state,machine.tape),(saved['head'],'A',expected))
        # A cut can pass through an outstanding marked burst. Compare all 424
        # physical pairs and the clock with different divisions of the same work.
        for n in (187,10000,10**7,10**11):
            reference=replay(n,27)
            self.assertEqual(reference,replay(n,34,engine=WORKER))

    def test_independent_window_at_100_million(self):
        ref=survey.load(ROOT/'frontiers/runs/window-17.json',17,M17)
        low,high=0,10000
        while high-low>1:
            mid=(low+high)//2
            if replay(mid,6)['steps']<ref['steps']:
                low=mid
            else:
                high=mid
        p=replay(low,6)
        rows=['unknown 0',M17,f"{p['steps']} {p['head']} 0"]
        pos=p['head']+1
        for symbol,group in itertools.groupby(HEAD+'12'*low+p['register']+'2'):
            size=sum(1 for _ in group)
            if symbol!='0':rows.append(f'{pos} {size} {symbol}')
            pos+=size
        seed,_=survey.pack(17,M17,'\n'.join(rows))
        got,_=survey.advance(WINDOW,17,M17,seed,ref['steps'],10**8,7)
        self.assertEqual(got,ref)


if __name__ == '__main__':
    unittest.main()
