#!/usr/bin/env python3
"""Exact call-stream statistics, checked against raw blank-tape execution.

Run from the repository root. See streams.md for interpretation.
"""
import argparse
import json
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
sys.path[:0]=[str(ROOT),str(ROOT/'frontiers')]
from longitudinal import Driver
from prior_sweeps import TapeMachine
from test_longitudinal import cells


def advance(engine,driver,state,groups,budget):
    proc=subprocess.run([str(engine.resolve()),str(groups),str(budget)],
        input=f"{driver.machine} {driver.period} {driver.first} {state['positive_tape'] or '.'}\n",
        text=True,capture_output=True,check=True)
    lines=proc.stdout.splitlines()
    assert lines[-1].startswith('tape\t')
    tape=lines.pop().split('\t')[1]
    cuts=[]
    for row in lines:
        x,n,b,bb,last,prefix=row.split('\t')
        cuts.append(dict(cell=int(x),entries=int(n),B=int(b),BB=int(bb),last=int(last),prefix=prefix))
    before=driver.excursions(state['groups']); after=driver.excursions(state['groups']+groups)
    right=2*sum(x['entries'] for x in cuts)-cuts[0]['entries']
    steps=state['steps']+driver.left(after)[0]-driver.left(before)[0]+right
    return {**state,'groups':state['groups']+groups,'steps':steps,'positive_tape':tape,'state':driver.period[-1]},cuts


def merge(total,cuts):
    for b in cuts:
        x=b['cell']
        if x==len(total): total.append({**b}); continue
        a=total[x]
        a['BB']+=b['BB']+(a['last']==1 and b['prefix'].startswith('B'))
        a['B']+=b['B']; a['entries']+=b['entries']; a['last']=b['last']
        a['prefix']=(a['prefix']+b['prefix'])[:128]


def local(machine,word):
    """One cell with the proved first/ordinary return contract; count local ops."""
    driver=Driver(13 if machine==Driver(13).machine else 21 if machine==Driver(21).machine else 22)
    rules=TapeMachine(machine).rules
    symbol=0;virgin=True;outputs='';cost=0
    for entry in word:
        q=entry
        while True:
            if (q,symbol) not in rules:return True,outputs,cost
            symbol,d,q=rules[q,symbol];cost+=1
            if d<0:break
            outputs+=q
            q=driver.first['AB'.index(q)] if virgin else 'A';virgin=False
    return False,outputs,cost


def verify(engine,reference):
    from itertools import product
    results=[]
    for line in (13,21,22):
        driver=Driver(line);state=driver.blank();aggregate=[]
        literal=TapeMachine(driver.machine);words=['A']
        for q in (1,2,7,17,100):
            old=state
            state,cuts=advance(engine,driver,state,q,1<<20);merge(aggregate,cuts)
            assert state==driver.advance(reference,old,q,1<<20)
            while literal.steps<state['steps']:
                old_head=literal.head
                assert literal.step()
                if literal.head==old_head+1 and literal.head>=0:
                    x=literal.head
                    while len(words)<=x:words.append('')
                    words[x]+=literal.state
            assert (literal.head,literal.state,literal.tape)==(0,state['state'],cells(driver,state))
            for a,w in zip(aggregate,words):
                if a['cell']==0:w=w[:-1] # current entry is still unconsumed
                assert (a['entries'],a['B'],a['BB'],a['prefix'])==(len(w),w.count('B'),sum(w[i:i+2]=='BB' for i in range(len(w)-1)),w[:128])
        # The terminal return to cell 0 belongs to the next batch; remove it
        # from a raw trace by comparing only actually consumed call entries above.
        for size in range(11):
            for bits in product('AB',repeat=size):
                w=''.join(bits);h,_,_=local(driver.machine,w)
                if line==13:
                    k=len(w)-len(w.lstrip('B'))
                    expected=k>0 and k%2==0 and k<len(w)
                else:expected=w.startswith('BB')
                assert h==expected,(line,w,h,expected)
        results.append({'line':line,'raw_steps':state['steps'],'groups':state['groups'],'full_configuration':True,'streams':True,'local_words_checked':2047})
        for q in range(1,10001):
            expected=15*q*q if line==13 else 52*q*q-21*q+8
            assert driver.left(driver.excursions(q))[0]==expected
        results[-1]['negative_clock_formula_checked_through']=10000
    return results


def main():
    p=argparse.ArgumentParser();p.add_argument('--engine',type=Path,required=True)
    p.add_argument('--reference',type=Path);p.add_argument('--verify',action='store_true')
    p.add_argument('--line',type=int,choices=(13,21,22));p.add_argument('--groups',type=int)
    p.add_argument('--batches',type=int,default=1);p.add_argument('--max-bits',type=int,default=1<<29)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    if a.verify:
        result={'verification':verify(a.engine,a.reference)}
    else:
        d=Driver(a.line);state=d.blank();cuts=[];checkpoints=[]
        for i in range(a.batches):
            state,b=advance(a.engine,d,state,a.groups,a.max_bits);merge(cuts,b)
            baseline=d.load(ROOT/'frontiers'/'runs'/f'stream-{a.line:02}.json')
            if state['groups']==baseline['groups']:assert state==baseline
            checkpoints.append({'groups':state['groups'],'steps':state['steps'],'positive_cells':len(state['positive_tape'])})
            result={'line':a.line,'machine':d.machine,'state':state,'cuts':cuts,'checkpoints':checkpoints,
                    'parameters':{'groups_per_batch':a.groups,'batches_completed':i+1,'max_bits':a.max_bits}}
            a.output.write_text(json.dumps(result,indent=2)+'\n')
            print(json.dumps(checkpoints[-1]),flush=True)
    a.output.write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':main()
