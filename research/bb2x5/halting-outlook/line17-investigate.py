#!/usr/bin/env python3
"""Finite audits, exact next-overflow bounds and conditional count quantiles.

Run from repository root: python3 research/bb2x5/halting-outlook/line17-investigate.py
The optional --engine points to the existing compiled line17_marks.cpp worker.
No random sampling and no newly invented acceleration are used.
"""
import argparse
from collections import Counter
from decimal import Decimal, localcontext
from itertools import product
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path[:0] = [str(ROOT / 'frontiers'), str(ROOT)]
from line17 import advance, load, save
from prior_frontier import DATA, M17, digits, mark_step, periodic_marks
from prior_sweeps import TapeMachine


def no_conflict_words(state, n):
    tasks = [(state, 0, 0)]
    for _ in range(n):
        new = []
        for (v,p), output, compounds in tasks:
            for bit in (0,1):
                if p and bit:
                    continue
                nv,np,out = mark_step(v,p,bit)
                new.append(((nv,np),output+len(out),compounds+bool(p or bit)))
        tasks = new
    return tasks


def bound(seed):
    d = digits(seed['register'])
    required = 1
    for v,_ in reversed(d):
        required = 3*required-v
    more = (required+3)//4
    k = seed['epochs']
    # Complete a virtual epoch with normal boundary replies. The final cut
    # has an extra R_w right-exit term absent from the no-overflow clock.
    # R_w <= 4 n_w <= 16 D 2^w. One further real B2 reaches virgin cell 12.
    raw = (seed['steps'] + 58*more + 14*more*(2*k+more-1)
           + 56*more*(2**len(d)-1) + 16*more*2**len(d) + 1)
    return {'remaining_root_slots_sufficient':required,
            'additional_virtual_epochs_sufficient':more,
            'next_virgin_visit_raw_upper_bound':raw}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--engine')
    args = ap.parse_args()
    assert (ROOT/'BB2x5_Rocq_holdouts_37.txt').read_text().splitlines()[16] == M17
    # 3m = n + v_initial - v_final + 4C, exact for every pulse.
    checked = 0
    for v,p,bit in product(range(3),range(2),range(2)):
        if p and bit:
            continue
        nv,np,out = mark_step(v,p,bit)
        assert 3*len(out) == 1+v-nv+4*bool(p or bit)
        checked += 1
    words = 0
    for v,p in product(range(3),range(2)):
        for (nv,np),output,compounds in no_conflict_words((v,p),12):
            assert 3*output == 12+v-nv+4*compounds
            assert output >= (12+v)//3
            words += 1
    seed = load(ROOT/'frontiers/runs/line17-epochs.json')
    summary = {'machine':M17,'local_identity_cases':checked,
               'valid_length_12_input_words_checked':words,
               'inherited_epochs':seed['epochs'], 'inherited_steps':seed['steps'],
               'next_overflow_bound':bound(seed)}
    # Chronological raw checks on the two earlier ACTUAL blank registers.
    machine = TapeMachine(M17)
    waiting = None
    early = []
    while machine.steps < 2308940:
        if machine.steps in (252,2889):
            assert machine.state=='A'
            right=max(machine.tape)
            word=''.join(str(machine.tape.get(i,0)) for i in range(machine.head+1,right+1))
            assert word.startswith('231302') and word.endswith('2')
            small={'register':word[6:-1],'epochs':0,'steps':machine.steps}
            waiting = {'entry_steps':machine.steps,'pairs':len(small['register'])//2,
                       'terminal_coordinate':right,'bound':bound(small)}
        assert machine.step()
        if waiting and machine.head>waiting['terminal_coordinate']:
            waiting['actual_next_virgin_steps']=machine.steps
            assert machine.steps <= waiting['bound']['next_virgin_visit_raw_upper_bound']
            early.append(waiting)
            waiting=None
    summary['literal_early_overflow_checks']=early
    # Actual pure input periods, retaining distinguished phase and all gaps.
    prefix, period = b'', bytes((0,1,0,0))
    d = digits(DATA)
    streams = []
    for cut in range(54):
        if cut in (0,6,20,35,53):
            positions = [i+1 for i,b in enumerate(period) if b]
            gaps = [b-a for a,b in zip(positions,positions[1:]+[positions[0]+len(period)])]
            pairs = Counter((a%3,b%3) for a,b in zip(gaps,gaps[1:]+gaps[:1]))
            streams.append({'cut':cut, 'prefix_slots':len(prefix), 'period_slots':len(period),
                            'marks':len(positions), 'first_marks':positions[:12],
                            'gap_histogram':dict(sorted(Counter(gaps).items())),
                            'adjacent_gap_residues':{f'{a},{b}':n for (a,b),n in sorted(pairs.items())}})
        if cut<53:
            prefix,period=periodic_marks((d[cut][0],d[cut-1][1] if cut else 0),prefix,period)
    summary['actual_streams']=streams
    # Geometric model is explicitly conditional, not a fitted probability law.
    quantiles = {}
    for p_text in ('0.20','0.35'):
        with localcontext() as ctx:
            ctx.prec=50
            p=Decimal(p_text)
            quantiles[p_text]={}
            for q_text in ('0.05','0.50','0.95'):
                q=Decimal(q_text)
                n=1
                while 1-(1-p)**n<q:
                    n+=1
                quantiles[p_text][q_text]=n
    summary['conditional_geometric_overflow_count_quantiles']=quantiles
    if args.engine:
        # Independent partitions of the SAME actual continuation, full equality.
        more=1000000001
        direct=advance(seed,more,args.engine)
        split=advance(advance(seed,317801,args.engine),more-317801,args.engine)
        assert direct==split
        save(HERE/'line17-continuation.json',direct)
        summary['new_continuation']={'epochs':direct['epochs'],'steps':direct['steps'],
                                     'additional_epochs':more,'full_split_equality':True,
                                     'next_overflow_bound':bound(direct)}
    (HERE/'line17-results.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':
    main()
