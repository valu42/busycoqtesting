#!/usr/bin/env python3
"""Timed Hydra recurrence; full literal configurations and deterministic parity audit.

Run from repository root: python3 research/bb2x5/halting-outlook/hydra_check.py
Published rules are credited in hydra.md. Standard library only; no random inputs.
"""
import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from prior_sweeps import TapeMachine

MACHINE = '1RB3RB---3LA1RA_2LA3RA4LB0LB0LA'


def concrete(a, b, left=0):
    return {left: 2, **{left+a+1+i: 3 for i in range(b)}, left+a+b+1: 2}


def rule(a, b):
    n, odd = divmod(a, 2)
    if not odd and not b:
        return None, 6*n*n+20*n+4, 0
    cost = 6*n*n+23*n+(4*b+26 if odd else 10)
    return (3*n+3, b+(2 if odd else -1)), cost, -n-2


def check():
    groups = 0
    for a in range(40):
        for b in range(8):
            m = TapeMachine(MACHINE, [2]+[0]*a+[3]*b+[2], head=-1)
            target, cost, shift = rule(a, b)
            for _ in range(cost):
                assert m.step(), (a, b, m.steps)
            assert m.steps == cost
            if target is None:
                n = a//2
                expected = {i: 3 for i in range(-n-1, 2*n)}
                expected.update({2*n: 1, 2*n+1: 2})
                assert (m.state, m.head, m.tape) == ('A', 2*n+1, expected)
                assert not m.step()
            else:
                assert (m.state, m.head, m.tape) == ('A', shift-1, concrete(*target, shift))
            groups += 1
    # Blank entry and successive complete macro configurations, with absolute head.
    m = TapeMachine(MACHINE)
    for _ in range(20):
        assert m.step()
    a, b, left, total = 3, 0, -3, 20
    assert (m.state, m.head, m.tape) == ('A', left-1, concrete(a, b, left))
    for _ in range(12):
        target, cost, shift = rule(a, b)
        assert target is not None
        for _ in range(cost):
            assert m.step()
        a, b = target
        left += shift
        total += cost
        assert (m.steps, m.state, m.head, m.tape) == (total, 'A', left-1, concrete(a,b,left))
    # Exact finite ensemble test: every binary k-word occurs once among residues.
    # This is NOT a test of randomness of the one blank-tape orbit.
    for k in range(1, 13):
        words = set()
        for seed in range(2**k):
            a, word = seed, 0
            for _ in range(k):
                word = 2*word+a%2
                a = 3*(a//2)+3
            words.add(word)
        assert len(words) == 2**k
    return {'synthetic_rules': groups, 'blank_macros': 12,
            'blank_literal_steps': total, 'residue_word_widths': [1,12]}


def run(events):
    a,b,left,total = 3,0,-3,20
    bits = []
    blocks = []
    last_zero_b_event = 0
    for i in range(events):
        bits.append(a%2)
        target,cost,shift = rule(a,b)
        assert target is not None, ('halt', i, a, b)
        a,b = target
        left += shift
        total += cost
        if b == 0: last_zero_b_event = i+1
        if (i+1)%10000 == 0:
            w = bits[-10000:]
            blocks.append({'event':i+1,'odd':sum(w),'even':len(w)-sum(w),'b':b})
    pairs = Counter(''.join(map(str,bits[i:i+2])) for i in range(len(bits)-1))
    words4 = Counter(''.join(map(str,bits[i:i+4])) for i in range(len(bits)-3))
    # Pearson correlations for each lag, using actual marginal means at that lag.
    def lag_corr(k):
        x,y=bits[:-k],bits[k:]
        n=len(x); sx=sum(x); sy=sum(y)
        numerator=n*sum(a*b for a,b in zip(x,y))-sx*sy
        denominator=math.sqrt((n*sx-sx*sx)*(n*sy-sy*sy))
        return numerator/denominator
    # Integer log10 bounds, deliberately rounded down/up without huge decimal conversion.
    digits_lower = int((total.bit_length()-1)*math.log10(2))
    while 10**digits_lower > total: digits_lower -= 1
    while 10**(digits_lower+1) <= total: digits_lower += 1
    state = {'machine':MACHINE,'events':events,'a_hex':hex(a),'b':b,
             'left_hex':hex(left),'head_hex':hex(left-1),'state':'A',
             'raw_steps_hex':hex(total),'normal_form':'2 0^a 3^b 2; head on blank left of first 2'}
    blob=json.dumps(state,sort_keys=True,separators=(',',':')).encode()
    return {'checkpoint':state,'checkpoint_sha256':hashlib.sha256(blob).hexdigest(),
            'raw_floor_power10':digits_lower,'a_bits':a.bit_length(),
            'odd':sum(bits),'even':len(bits)-sum(bits),'blocks':blocks,
            'adjacent_pairs':dict(sorted(pairs.items())),
            'four_bit_words':dict(sorted(words4.items())),
            'lag_correlation':{str(k):lag_corr(k) for k in (1,2,3,4,8,16,32)},
            'last_zero_b_event':last_zero_b_event}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--events',type=int,default=20000)
    parser.add_argument('--output',type=Path,default=HERE/'hydra-results.json')
    args=parser.parse_args()
    verification=check()
    result=run(args.events)
    result['verification']=verification
    result['baseline_commit']='2ab106f706cb1715d494c7f67464e9222092058f'
    result['research_date']='2026-11-18'
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='checkpoint'},indent=2))
