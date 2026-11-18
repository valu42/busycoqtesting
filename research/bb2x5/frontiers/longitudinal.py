#!/usr/bin/env python3
"""Advance certified periodic boundary drivers in batches with exact raw TM timing."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

from checkpoints import ROOT, atomic_json, checksum, holdouts

sys.path.insert(0, str(ROOT))
from prior_sweeps import parse, TapeMachine

# (period on external returns, transient length, block width, usual left return).
# These left-half drivers are derived in ../mixed-and-sweeps.md. The timing and
# finite-cycle checks below are repeated directly on the literal instructions.
DRIVERS = {8: ('BBABA',1,1,'A'), 11: ('BBBA',2,1,'A'), 12: ('BBBABABAABABBA',2,1,'A'),
           13: ('BABAB',1,1,'A'), 21: ('BAABABABAAABA',2,1,'A'),
           22: ('BAABABABAAABA',2,1,'A'), 31: ('ABAAA',1,2,'B')}
FORMAT = 'bb2x5-longitudinal-v1'


class Driver:
    def __init__(self, line):
        self.line=line
        self.period, self.transient, width, self.usual=DRIVERS[line]
        self.machine=holdouts()[line-1]
        rules=parse(self.machine)
        exceptional=[r for (_,r),(_,move,q) in rules.items() if move<0 and q!=self.usual]
        if exceptional and (any(exceptional) or any(w==0 for w,_,_ in rules.values())):
            raise ValueError('revisited cells do not have a uniform left return')
        first=[]
        for q in 'AB':
            m=TapeMachine(self.machine)
            m.state=q
            for _ in range(1000):
                if not m.step():
                    raise ValueError('virgin call halted')
                if m.head<0:
                    first.append(m.state)
                    break
            else:
                raise ValueError('virgin call did not return within the setup budget')
        self.first=''.join(first)
        if self.first[0]!=self.usual:
            raise ValueError('first positive excursion returns in the wrong state')
        # Table after j external calls: cumulative subordinate calls, count of
        # local transitions, and block contents in increasing physical order.
        w=[0]*width
        self.table=[(0,0,tuple(w))]
        used=cost=0
        period=len(self.period)
        for j in range(self.transient+period):
            x,q=width-1,self.usual
            seen=set()
            while 0<=x<width:
                config=x,q,tuple(w),used%period
                if config in seen:
                    raise ValueError('cyclic left driver')
                seen.add(config)
                w[x],move,q=rules[q,w[x]]
                x+=move
                cost+=1
                if x<0:
                    if q!=self.usual or used>=j:
                        raise ValueError('left driver violates the induction guard')
                    x,q=0,self.period[used%period]
                    used+=1
            if q!=self.period[j%period]:
                raise ValueError('left driver emitted the wrong letter')
            self.table.append((used,cost,tuple(w)))
        u,c,w=self.table[self.transient]
        if (used-u,tuple(self.table[-1][2]))!=(period,w):
            raise ValueError('left driver failed to close its period')
        self.cost_period=cost-c

    def block(self,n):
        if n<self.transient:
            return self.table[n]
        k,r=divmod(n-self.transient,len(self.period))
        u,c,w=self.table[self.transient+r]
        return u+k*len(self.period),c+k*self.cost_period,w

    def left(self, n):
        """Exact negative-half time and tape. Pieces list blocks from nearest to farthest."""
        total=0
        pieces=[]
        seen={}
        visits=[]
        period=len(self.period)
        while n:
            if n>=self.transient and n%period in seen:
                old,old_cost,index=seen[n%period]
                drop=old-n
                repeat=(n-self.transient)//drop
                if repeat:
                    cycle=tuple(visits[index:])
                    saving=len(cycle)*(drop//period)*self.cost_period
                    total+=repeat*(total-old_cost)-saving*repeat*(repeat+1)//2
                    pieces.append((repeat,cycle))
                    n-=repeat*drop
                seen.clear()
                visits.clear()
            if n>=self.transient:
                seen[n%period]=n,total,len(visits)
            used,cost,word=self.block(n)
            if not 0<=used<n:
                raise ValueError('left recursion failed to decrease')
            total+=cost
            visits.append(word)
            pieces.append((1,(word,)))
            n=used
        return total,pieces

    def blank(self):
        return {'format':FORMAT,'machine':self.machine,'line':self.line,'groups':0,'steps':0,
                'positive_tape':'','head':0,'state':'A'}

    def load(self,path):
        doc=json.loads(Path(path).read_text()); p=doc['payload']
        if doc['sha256']!=checksum(p) or p.keys()!=self.blank().keys():
            raise ValueError('invalid longitudinal checkpoint')
        if (p['format'],p['machine'],p['line'],p['head'])!=(FORMAT,self.machine,self.line,0):
            raise ValueError('wrong machine or boundary')
        groups=p['groups']
        if type(groups) is not int or groups<0 or type(p['steps']) is not int:
            raise ValueError('invalid counters')
        if groups==0:
            if p!=self.blank(): raise ValueError('invalid blank seed')
        elif (p['state']!=self.period[-1] or not p['positive_tape'] or set(p['positive_tape'])-set('01234')
              or p['steps']<self.left(len(self.period)*groups)[0]+len(self.period)*groups or p['steps']%2):
            raise ValueError('invalid canonical boundary state')
        return p

    def advance(self,engine,state,groups,max_bits):
        """Compute a complete batch, leaving the incoming state intact on failure."""
        length=len(self.period)
        if type(groups) is not int or groups < 1:
            raise ValueError('batch size must be a positive integer')
        protocol=' '.join((self.machine,self.period,self.usual,self.first,state['positive_tape'] or '.'))+'\n'
        proc=subprocess.run([str(Path(engine).resolve()),str(groups),str(max_bits)],
                            input=protocol,text=True,capture_output=True)
        if proc.returncode:
            raise RuntimeError(proc.stderr.strip() or f'worker failed ({proc.returncode})')
        tape,*raw=proc.stdout.splitlines()
        calls=list(map(int,raw))
        if not calls or calls[0]!=length*groups or min(calls)<=0 or len(tape)!=max(len(calls),len(state['positive_tape'])):
            raise ValueError('inconsistent worker result')
        old=state['groups']; new=old+groups
        right_cost=2*sum(calls)-calls[0]
        left_cost=self.left(new*length)[0]-self.left(old*length)[0]
        return {**state,'groups':new,'steps':state['steps']+left_cost+right_cost,
                'positive_tape':tape,'state':self.period[-1]}


def save(path,state):
    atomic_json(path,{'payload':state,'sha256':checksum(state)})


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--engine',type=Path,required=True)
    p.add_argument('--line',type=int,choices=DRIVERS,required=True)
    p.add_argument('--groups',type=int,required=True,help='additional source periods per batch')
    p.add_argument('--batches',type=int,default=1)
    p.add_argument('--max-bits',type=int,default=2**30,help='maximum materialized bits in any one word')
    p.add_argument('--resume',type=Path)
    p.add_argument('--checkpoint',type=Path,required=True,help='atomically saved after each complete batch')
    args=p.parse_args()
    if args.batches<1 or args.max_bits<16:
        p.error('require a positive batch count and at least 16 bits')
    try:
        d=Driver(args.line)
        state=d.load(args.resume) if args.resume else d.blank()
        for _ in range(args.batches):
            state=d.advance(args.engine,state,args.groups,args.max_bits)
            save(args.checkpoint,state)
            print(json.dumps({'status':'unknown','line':d.line,'groups':state['groups'],'steps':state['steps'],
                              'positive_cells':len(state['positive_tape'])}),flush=True)
    except (OSError,ValueError,RuntimeError,KeyError,TypeError) as error:
        p.exit(2,f'Batch stopped: {error}\n')


if __name__=='__main__':
    main()
