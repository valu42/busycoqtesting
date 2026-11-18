#!/usr/bin/env python3
"""Literal validation of instrumentation and the newly used safe-guard filters."""
import itertools,json,sys
from pathlib import Path
from line7_probe import Probe,ROOT
sys.path.insert(0,str(ROOT/'frontiers'))
from line7 import Calls,MACHINE,load,snapshot
from prior_sweeps import TapeMachine

def call_literal(word,state='B'):
    m=TapeMachine(MACHINE,word);m.state=state
    while m.head>=0 and m.step():
        assert m.steps<2_000_000
    return m

def main():
    v=Probe();m=TapeMachine(MACHINE)
    for e in range(1,19):
        assert v.epoch()
        while m.steps<v.steps:assert m.step()
        assert (m.steps,m.state,m.head)==(v.steps,'A',-e)
        assert m.tape=={1-e+i:x for i,x in enumerate(v.tape) if x}
    print('PASS: 18 blank epochs, complete configurations and exact raw counts; endpoint',v.steps)
    nchecks=0
    for length in range(1,9):
        for word in itertools.product((2,4),repeat=length):
            n=2;q='A'
            for x in word:
                if q=='B':n=(n+(x==4))//2;q='A'
                elif x==2:n*=3
                else:q='B'
            if n:continue
            for tail in itertools.product(range(5),repeat=2):
                w=(3,)+word+tail;m=call_literal(w)
                assert (m.head,m.state)==(-1,'B')
                # The ordinary-prefix calculation promises no call into tail.
                for i,x in enumerate(tail,start=len(word)+1):assert m.tape.get(i,0)==x
                v=Calls(w);assert v.run(v.many(0,'B',1))==(1,'B')
                assert v.steps==m.steps
                assert {i:x for i,x in enumerate(v.tape) if x}==m.tape
                nchecks+=1
    print('PASS: ordinary-prefix safe filter,',nchecks,'literal complete configurations with arbitrary two-cell tails')
    m=call_literal((3,2));assert (m.head,m.state,m.steps)==(-1,'B',9)
    assert ''.join(str(m.tape.get(i,0)) for i in range(4))=='4432'
    print('PASS: terminal 32 -> 4432 B return in 9 raw instructions')
    p=Path(__file__).with_name('line7-blank-1024.json')
    doc=json.loads(p.read_text())
    for row in doc['rows']:
        for case in row['residual_guards']:
            word=tuple(map(int,case['word']));m=call_literal(word)
            assert (m.head,m.state)==(-1,'B')
            v=Calls(word);assert v.run(v.many(0,'B',1))==(1,'B')
            assert v.steps==m.steps
            assert {i:x for i,x in enumerate(v.tape) if x}==m.tape
            print('PASS: residual guard at epoch',row['epoch'],'returns B in',m.steps,'raw steps; full suffix matched')
def deep_check():
    here=Path(__file__).resolve().parent
    p=load(here/'line7-8192-8256-checkpoint.json')
    v=Calls(map(int,p['word']),int(p['steps_hex'],16))
    for e in range(8257,9217):assert v.epoch()
    q=load(here/'line7-8192-9216-checkpoint.json')
    assert snapshot(9216,v)==q
    print('PASS: uninstrumented continuation 8256–9216 matches instrumented 8192–9216 full configuration and raw time')

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--deep',action='store_true',help='also repeat the slower split-checkpoint comparison')
    args=ap.parse_args()
    main()
    if args.deep:deep_check()
