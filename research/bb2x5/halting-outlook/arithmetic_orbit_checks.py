#!/usr/bin/env python3
"""Inspect actual arithmetic-return correlations; no randomness is assumed."""
from collections import Counter
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(HERE.parent),str(HERE.parent/'frontiers')]
from arithmetic5 import State,a_repeat_count
from line5_timed import step as step5
from line4_orbit import a_epoch,b_epoch,complete_rounds


def summary(records):
    result=[]
    for start in range(0,len(records),1000):
        data=records[start:start+1000]
        lengths=[r[1] for r in data]
        mean=sum(lengths)/len(lengths)
        variance=sum((x-mean)**2 for x in lengths)
        lag=sum((a-mean)*(b-mean) for a,b in zip(lengths,lengths[1:]))/variance if variance else None
        result.append({'first_return_index':start,'returns':len(data),
                       'width_first':data[0][0],'width_last':data[-1][0],
                       'B_events_histogram':dict(sorted(Counter(lengths).items())),
                       'B_events_mean':mean,'B_events_lag1_correlation':lag,
                       'within_width_deciles':dict(sorted(Counter(r[2] for r in data).items()))})
    return result


def line4(count):
    records=[]
    b=71
    raw=6393
    for _ in range(count):
        n=complete_rounds(b)
        p=3**n
        L=8*p-8-n
        width=16*p-1
        state,cost=a_epoch(b)
        raw+=cost
        assert state is not None
        events=0
        while state[0]=='B':
            state,cost=b_epoch(state[1],state[2])
            assert state is not None
            raw+=cost
            events+=1
        records.append((n,events,10*(b-L)//width))
        assert state[2]>b
        b=state[2]
    return {'windows':summary(records),'endpoint_b_hex':hex(b),'endpoint_raw_steps_hex':hex(raw)}


def line5(count):
    records=[]
    b=4
    raw=136
    for _ in range(count):
        n=a_repeat_count(4,b)
        p=1<<n
        L=8*p-8-n
        width=8*p-1
        state=State('A',4,b)
        while state.tag=='A':
            state,cost,_=step5(state)
            raw+=cost
            assert state is not None
        events=0
        while state.tag=='B':
            state,cost,_=step5(state)
            raw+=cost
            assert state is not None
            events+=1
        records.append((n,events,10*(b-L)//width))
        assert state.b>b
        b=state.b
    return {'windows':summary(records),'endpoint_b_hex':hex(b),'endpoint_raw_steps_hex':hex(raw)}


if __name__=='__main__':
    result={'return_convention':'line4 index0 is A(6,71); line5 index0 is A(4,4)',
            'line4':line4(4000),'line5':line5(4000)}
    (HERE/'arithmetic_orbit_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:{'windows':v['windows']} for k,v in result.items() if k!='return_convention'},indent=2))
