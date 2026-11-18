#!/usr/bin/env python3
"""Exact-clock mixed-counter probes and arithmetic target obstructions.

Run from any directory: python3 arithmetic_checks.py --zeros 300 --max-n 200000
Only Python's standard library is required. Output is deterministic JSON.
"""
import argparse
from collections import Counter
import json
import math
from pathlib import Path
import random
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT/'frontiers'))
from mixed_and_sweeps import MIX, canonical, decode, skip, tokens
from prior_sweeps import TapeMachine
from arithmetic5 import State, scalar, a_repeat_count
from line5_timed import step as timed5, verify_local_rules


def timed_probe(m, cap=None):
    """Batch complete probes with a full or carry-safe partial binary prefix.

    Returns (number of successful probes, exact raw cost); zero means fallback.
    Each child call is below the token capacity, so no call touches the far cut.
    """
    t, x = m.tape, m.head
    if m.state != 'A' or t.get(x) not in (2,4):
        return 0, 0
    j=x-1
    value,power=0,1
    while t.get(j) in (2,3):
        if t[j]==3: value+=power
        power*=2
        j-=1
    full=j==min(t) and t[j]==1 and j+1<x and t.get(j+1)==3
    if full:
        power//=2
        value-=power
        X=power+value
    elif value==power-1:
        return 0,0
    else:
        X=value
    ts = tokens(m)
    n = 0
    for _, digit in reversed(ts):
        n = n//2 if digit is None else 3*n+digit
    if not full: n=min(n,power-1-value)
    if cap is not None:
        n = min(n,cap)
    if not n:
        return 0, 0
    requests, right_cost = n, 0
    for _, digit in ts:
        if digit is None:
            right_cost += 3*requests
            requests *= 2
        else:
            child = (requests+2-digit)//3
            right_cost += 3*requests+child
            requests = child
    assert requests == 0
    Y = X+n
    left_cost = 3*n+2*(X.bit_count()-Y.bit_count())
    if full: left_cost+=2*(Y.bit_length()-X.bit_length())
    assert skip(m, cap=n) == n
    return n, right_cost+left_cost


def verify_probe():
    rng = random.Random(20261118)
    cases = []
    # Tractable canonical and mixed/misaligned token words, all legal starts.
    for X in range(1,12):
        for d in range(1,4):
            for v in range(1,3**d):
                cases.append(canonical(X,d,0,v))
    for _ in range(500):
        m = canonical(rng.randrange(1,65),0,0)
        x = m.head
        word = []
        for _ in range(rng.randrange(1,9)):
            word.extend([4] if rng.randrange(4)==0 else [2,rng.choice((0,2,4))])
        for j,v in enumerate(word,x):
            if v: m.tape[j]=v
            else: m.tape.pop(j,None)
        cases.append(m)
        # A non-binary symbol blocks the left prefix; n is capped before carry.
        partial=TapeMachine(MIX)
        partial.tape=m.tape.copy()
        partial.head=m.head
        partial.tape[min(partial.tape)]=4
        cases.append(partial)
    checked = 0
    for m in cases:
        b = TapeMachine(MIX)
        b.tape,b.head,b.state = m.tape.copy(),m.head,m.state
        n,cost = timed_probe(m,32)
        if not n: continue
        for _ in range(cost): assert b.step(), 'concealed halt'
        assert (m.tape,m.head,m.state)==(b.tape,b.head,b.state)
        assert b.steps == cost
        checked += 1
    # Independent literal run on the actual blank prefix, complete state and clock.
    a,b = TapeMachine(MIX),TapeMachine(MIX)
    raw, jumps = 0,0
    while raw < 200000:
        n,cost = timed_probe(a,32)
        if n: jumps += 1
        else:
            assert a.step()
            cost=1
        for _ in range(cost): assert b.step(), 'concealed blank halt'
        raw += cost
        assert (a.tape,a.head,a.state)==(b.tape,b.head,b.state)
        assert raw==b.steps
    return {'auxiliary_full_configuration_and_clock_cases':checked,
            'blank_comparison_raw_steps':raw,'blank_compared_jumps':jumps}


def mixed_run(count):
    m=TapeMachine(MIX)
    raw=0
    for _ in range(5): assert m.step(); raw+=1
    assert decode(m)==(1,0,0,0)
    records=[]
    operations=0
    # The per-checkpoint budget is computational work, never a halt prediction.
    for epoch in range(1,count+1):
        for _ in range(1000000):
            n,cost=timed_probe(m)
            if not n:
                assert m.step(), 'actual blank halt'
                cost=1
            raw+=cost
            operations+=1
            c=decode(m)
            if c and c[-1]==0:
                X,d,p,v=c
                k=((X+1)&-(X+1)).bit_length()-1
                records.append({'zero_checkpoint':epoch,'X_hex':hex(X),'d':d,'pad':p,
                                'trailing_ones':k,'steps_hex':hex(raw)})
                break
        else: raise RuntimeError('per-checkpoint work budget')
    checkpoint={'machine':MIX,'origin':'blank','raw_steps_hex':hex(raw),
                'state':m.state,'head':m.head,'nonzero_tape':sorted(m.tape.items()),
                'zero_checkpoints':count,'operations':operations,'records':records}
    (HERE/'arithmetic_line3_checkpoint.json').write_text(json.dumps(checkpoint,indent=2)+'\n')
    odd=[r for r in records if r['pad']==1]
    halves=[]
    for part in (odd[:len(odd)//2],odd[len(odd)//2:]):
        halves.append(dict(sorted(Counter(r['trailing_ones'] for r in part).items())))
    transitions=Counter((a['trailing_ones'],b['trailing_ones']) for a,b in zip(odd,odd[1:]))
    return {'zero_checkpoints':count,'odd_zero_checkpoints':len(odd),
            'raw_steps_hex':hex(raw),'raw_step_decimal_digits':len(str(raw)),
            'final_X_hex':records[-1]['X_hex'],'final_d':records[-1]['d'],
            'final_pad':records[-1]['pad'],'operations':operations,
            'trailing_one_histograms_first_second_halves':halves,
            'trailing_one_transitions':{f'{a},{b}':v for (a,b),v in sorted(transitions.items())}}


def target_gap(n):
    """Necessary lower-width escape for n=13 or18 mod20; all exact integers."""
    assert n%20 in (13,18)
    p=1<<n
    low,high=16*p+n+5,16*p+3*n+5
    C=3*n+11
    # Floating point chooses only an initial guess. Exact guards certify j.
    j=max(0,int(((n+4)*math.log(2)-math.log(C))/math.log(3)))
    value=C*3**j
    while value<low: value*=3; j+=1
    while j and value//3>=low: value//=3; j-=1
    assert value>=low and (j==0 or value//3<low)
    return j,value<=high


def inverse5(max_n):
    tested=0
    escapes=[]
    for n in range(13,max_n+1):
        if n%20 not in (13,18): continue
        j,possible=target_gap(n)
        tested+=1
        if possible: escapes.append([n,j])
    # Independently verify every direct-return formula on a tractable domain.
    direct_cases=0
    for b in range(50000):
        n=a_repeat_count(4,b)
        p=1<<n
        a=8*p-4
        u=b-8*(p-1)+n
        if u<=a and (a-u)%3==1:
            s=scalar(State('A',a,u))
            assert s is not None and s.tag=='B'
            t=scalar(s)
            assert t==State('A',4,(b+32*p+n-11)//3)
            direct_cases+=1
    return {'candidate_exponents_through':max_n,'classes_mod20':[13,18],
            'tested':tested,'possible_lower_width_escape':escapes,
            'excluded_targets':tested-len(escapes),
            'direct_return_identity_checked':direct_cases}


def clock_checks():
    # Existing universal symbolic rules; independent literal cost comparisons.
    verify_local_rules()
    from prior_sweeps import audit_arithmetic_transition
    checked=0
    for tag in 'AB':
        for a in range(8):
            for b in range(12):
                state=State(tag,a,b)
                end,cost,events=timed5(state)
                pos,total=state,0
                for _ in range(events):
                    target=scalar(pos)
                    out=None if target is None else (target.tag,target.a,target.b)
                    total+=audit_arithmetic_transition((pos.tag,pos.a,pos.b),out)
                    pos=target
                assert (pos,total)==(end,cost)
                checked+=1
    return {'line5_literal_full_configuration_and_clock_cases':checked,
            'line5_inherited_universal_symbolic_timing_rules':'passed'}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--zeros',type=int,default=300)
    parser.add_argument('--max-n',type=int,default=200000)
    args=parser.parse_args()
    if args.zeros<1 or args.max_n<18: parser.error('positive investigation budgets required')
    machines=(ROOT/'BB2x5_Rocq_holdouts_37.txt').read_text().splitlines()
    assert machines[2]==MIX
    assert machines[4]=='1RB3LA1LA1RA1RA_2LB2RA---4RB1LB'
    out={'starting_commit':'2ab106f706cb1715d494c7f67464e9222092058f',
         'research_date':'2026-11-18','verification':verify_probe(),
         'clock_checks':clock_checks(),'line3':mixed_run(args.zeros),
         'line5_inverse':inverse5(args.max_n)}
    (HERE/'arithmetic_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__': main()
