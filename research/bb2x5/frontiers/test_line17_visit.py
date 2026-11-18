"""Check slot ancestry, partial-sweep clocks and the complete suspended tape."""
import copy
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

from checkpoints import checksum
from line17_visit import (HEAD, M17, event_in_sweep, fresh_at, header_crossings, line17, locate,
                          pair_crossings, probes, suspended_pile, verify)
from prior_frontier import digits, mark_step
from prior_sweeps import TapeMachine


PACKED=Path(os.environ.get('BB25_PACK17','/tmp/bb25-packed17')).resolve()


def literal_slot(register,epochs):
    data=digits(register)
    state=[(v,data[i-1][1] if i else 0) for i,(v,_) in enumerate(data)]
    def reaches(i,bit):
        if i==len(state): return True
        v,p,bits=mark_step(*state[i],bit)
        state[i]=v,p
        return any(reaches(i+1,b) for b in bits)
    return next((j for j in range(1,4*epochs+1) if reaches(0,int(j%4==2))),None)


class VisitTests(unittest.TestCase):
    def test_reverse_slot_selection(self):
        for start in (0,37,10**8):
            reg=line17.replay(start,22)['register']
            for depth in (1,2,6,9,17,29,50):
                prefix=reg[:2*depth]
                want=literal_slot(prefix,2500)
                for bits in (16,127,1<<18):
                    output=subprocess.check_output([str(PACKED),'2500',str(bits),'100000','first'],
                                                   input=prefix,text=True)
                    self.assertEqual(output.strip(),str(want) if want is not None else 'none')

    def test_literal_physical_clock_and_tape(self):
        for k in (0,1,2,3,5,13,31,73,225):
            seed=line17.replay(k,20)
            end=line17.replay(k+1,20)
            origin=seed['head']+7+2*k
            word=HEAD+'12'*k+seed['register']+'2'
            m=TapeMachine(M17,map(int,word),head=seed['head'],left=seed['head']+1)
            m.steps=seed['steps']
            visited=set()
            while m.steps<end['steps']:
                self.assertTrue(m.step())
                offset=m.head-origin
                if offset<0 or offset%2 or offset//2 in visited: continue
                i=offset//2
                visited.add(i)
                e=event_in_sweep(seed,i)
                observed=e['header']+''.join(b['word']*b['copies'] for b in e['pile'])+e['data_and_singleton']
                physical={e['tape_left']+x:int(a) for x,a in enumerate(observed) if a!='0'}
                self.assertEqual((e['steps'],e['state'],e['head'],physical),(m.steps,m.state,m.head,m.tape))
                self.assertEqual(sum(len(b['word'])*b['copies'] for b in e['pile']),2*k)
            self.assertIsNone(event_in_sweep(seed,max(visited)+1))

    def test_pile_cost_for_every_raw_request(self):
        normal=pair_crossings(0)
        for v in range(3):
            for j in range(len(probes(v))):
                inner=pair_crossings(v)[j]
                expected=inner.clock
                index=inner.parent
                for pile in range(1,31):
                    got,_,pieces=suspended_pile(pile,v,j)
                    self.assertEqual(got,expected+header_crossings(0)[index].clock)
                    self.assertEqual(sum(p['copies'] for p in pieces),pile)
                    step=normal[index]
                    expected+=step.clock
                    index=step.parent
                small=suspended_pile(3,v,j)[0]
                increment=suspended_pile(4,v,j)[0]-small
                huge,_,pieces=suspended_pile(10**100,v,j)
                self.assertEqual(huge,small+(10**100-3)*increment)
                self.assertLessEqual(len(pieces),3)

    def test_first_visit_witness_and_no_hit(self):
        seed=line17.replay(0,6)
        for pair in (0,1,4,7,12,19):
            result=locate(seed,pair,50000,PACKED,127,10**7)
            self.assertIsNotNone(result)
            event=verify(result)
            before=result['payload']['before']['payload']
            self.assertTrue(fresh_at(before,pair))
            self.assertFalse(fresh_at(line17.replay(event['sweep'],19),pair))
            self.assertIsNone(locate(seed,pair,event['sweep']-1,PACKED,16,10**7))
        corrupt=copy.deepcopy(result)
        corrupt['payload']['arrival']['steps']+=2
        corrupt['sha256']=checksum(corrupt['payload'])
        with self.assertRaises(ValueError): verify(corrupt)
        with self.assertRaises(ValueError): locate(line17.replay(1,6),0,5,PACKED,16,10000)
        self.assertIsNone(locate(seed,424,10000,PACKED,16,10**7))

    def test_complete_checkpoint_from_a_miss(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'boundary.json'
            for start in (0, 12345, 10**8):
                seed=line17.replay(start,22)
                for budget in (16, 2**18):
                    for target in (100, 424):
                        self.assertIsNone(locate(seed,target,start+1000,PACKED,budget,10**7,miss_checkpoint=path))
                        self.assertEqual(line17.load(path),line17.advance_packed(seed,1000,PACKED,budget))
            seed=line17.replay(0,6)
            self.assertIsNone(locate(seed,7,0,PACKED,16,0,miss_checkpoint=path))
            original=path.read_bytes()
            self.assertIsNotNone(locate(seed,7,1000,PACKED,16,10000,miss_checkpoint=path))
            self.assertEqual(path.read_bytes(),original)
            with self.assertRaises(ValueError):
                locate(seed,100,10**12,PACKED,16,0,miss_checkpoint=path)
            self.assertEqual(path.read_bytes(),original)


if __name__=='__main__': unittest.main()
