"""Check the timed register against the elementary machine, including cut-off bursts."""
import itertools
import os
import subprocess
import sys
import tempfile
from pathlib import Path
import unittest

from line17 import (DATA, HEAD, M17, ROOT, ReachesTerminal, advance, advance_packed, deepest_probe, load, literal_counts, once_counts,
                    mark_image, periodic_counts, replay, word_counts)
from prior_frontier import T17, digits, header17, marks_on_word, mark_step
from prior_sweeps import TapeMachine
import survey

WORKER = Path(os.environ.get('BB25_MARK17', '/tmp/bb25-marks17'))
PACKED = Path(os.environ.get('BB25_PACK17', '/tmp/bb25-packed17'))
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

    def test_arbitrary_epoch_resume(self):
        for start, more in ((0,0),(1,1),(7,100),(9999,12345),(10**9,7000000),(10**11,10**7)):
            saved = replay(start,27)
            expected = replay(start+more,27)
            self.assertEqual(advance(saved,more,WORKER),expected)
            if more < 20000:
                self.assertEqual(advance(saved,more,None),expected)
        deep = load(ROOT/'frontiers/runs/line17-epochs.json')
        direct = advance(deep, 1000001, WORKER)
        split = advance(advance(deep, 317801, WORKER), 682200, WORKER)
        self.assertEqual(direct, split)
        self.assertEqual(advance(deep,0,WORKER),deep)
        # A rightward carry through 424 trits of value two reaches the
        # singleton on the very first U, providing a concrete stop control.
        altered = {**deep,'register':'22'*424}
        with self.assertRaises(ReachesTerminal):
            advance(altered,1,WORKER)
        with self.assertRaises(ValueError):
            advance(deep,-1,WORKER)

    def test_packed_streams_and_resumed_phases(self):
        entry = replay(0,6)
        for target in (0,1,2,9,71,10001,10**7):
            target_state = replay(target,27)
            # Force streaming deep inside short words and also keep whole periods.
            for bits in (16,127,65536):
                self.assertEqual(advance_packed(entry,target,PACKED,bits),target_state)
        deep = load(ROOT/'frontiers/runs/line17-epochs.json')
        first = advance_packed(deep,14681,PACKED,127)
        combined = advance_packed(first,1000001,PACKED,65536)
        self.assertEqual(combined,advance(deep,1014682,WORKER))
        with self.assertRaises(ReachesTerminal):
            advance_packed({**deep,'register':'22'*424},1,PACKED,16)

    def test_packed_budget_preserves_checkpoint(self):
        path = ROOT/'frontiers/runs/line17-epochs.json'
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)/'checkpoint.json'
            saved = path.read_bytes()
            output.write_bytes(saved)
            result = subprocess.run([sys.executable,str(ROOT/'frontiers/line17.py'),
                                     '--resume',str(output),'--checkpoint',str(output),
                                     '--epochs',str(load(path)['epochs']+10**6),'--word-bits','16',
                                     '--finite-slots','0','--packed-engine',str(PACKED)],
                                    text=True,capture_output=True)
            self.assertNotEqual(result.returncode,0)
            self.assertIn('finite slot budget',result.stderr)
            self.assertEqual(output.read_bytes(),saved)

    def test_fused_pairs_against_literal_slots(self):
        for left,right in itertools.product(('12','13','02','03','22','23'),repeat=2):
            register = DATA[:12]+left+right+'031322'
            data = digits(register)
            word = bytes((0,1,0,0))*75
            rows = []
            worker = subprocess.run([str(PACKED),'75','16','100000'],input=register,
                                    text=True,capture_output=True)
            try:
                for i,(trit,_) in enumerate(data):
                    state = trit,data[i-1][1] if i else 0
                    c = literal_counts(state,word)
                    rows.append((*c.state,c.slots,c.calls,c.interior))
                    _,word = marks_on_word(state,word)
            except AssertionError:  # The literal rule detected an overlapping mark.
                self.assertNotEqual(worker.returncode,0)
                self.assertIn('overlapping marked bursts',worker.stderr)
            else:
                self.assertEqual(worker.returncode,0,worker.stderr)
                self.assertEqual(rows,[tuple(map(int,r.split())) for r in worker.stdout.splitlines()])

    def test_deepest_probe_from_a_completed_register(self):
        for start,more in ((0,0),(0,1),(11,73),(10**9,171)):
            seed = replay(start,27)
            final = advance_packed(seed,more,PACKED,16)
            word = bytes((0,1,0,0))*more
            data = digits(seed['register'])
            last = None
            for i,(trit,_) in enumerate(data):
                if not word: break
                last = i,len(word)
                _,word = marks_on_word((trit,data[i-1][1] if i else 0),word)
            self.assertEqual(last,deepest_probe(final['register'],seed['register']))

    def test_native_period_lifting_and_budget(self):
        # Check every count and child word for several copy phases, including
        # a marked burst split between the last complete copy and the suffix.
        for period, marks in ((6,[5]), (7,[1,4]), (28,[3,7,14,23])):
            source = ' '.join(map(str,marks))
            for n in (0, 11, 97, 1007):
                cmd = [str(WORKER),str(n),str(period),'8','100000','3']
                reference = subprocess.check_output(cmd+['0'],input=source,text=True)
                for levels in (1,3,6):
                    self.assertEqual(reference,subprocess.check_output(cmd+[str(levels)],input=source,text=True))
        result=subprocess.run([str(WORKER),'1000','7','3','2'],input='1 4',text=True,capture_output=True)
        self.assertNotEqual(result.returncode,0)
        self.assertIn('budget',result.stderr)

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
