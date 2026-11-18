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
# See ../mixed-and-sweeps.md and the line 10 derivation in README.md.
# Timing and finite-cycle checks use the literal instructions.
DRIVERS = {8: ('BBABA',1,1,'A'), 10: ('AB',5,1,'A'), 11: ('BBBA',2,1,'A'), 12: ('BBBABABAABABBA',2,1,'A'),
           13: ('BABAB',1,1,'A'), 21: ('BAABABABAAABA',2,1,'A'),
           22: ('BAABABABAAABA',2,1,'A'), 31: ('ABAAA',1,2,'B')}
PREFIX = {10: 'BBA'}
FORMAT = 'bb2x5-longitudinal-v1'
HALTED = 'bb2x5-longitudinal-halt-v1'


class CandidateUndefined(RuntimeError):
    pass


def check_return_contract(rules, first, usual):
    """Check every successful one-cell call reachable from a fresh right suffix."""
    pending = [(0, True, True)]
    known = set()
    while pending:
        start = pending.pop()
        if start in known:
            continue
        known.add(start)
        for entry in 'AB':
            symbol, virgin_neighbor, virgin_cell = start
            state = entry
            seen = set()
            while (symbol, state, virgin_neighbor) not in seen:
                seen.add((symbol, state, virgin_neighbor))
                rule = rules.get((state, symbol))
                if rule is None:
                    break
                symbol, move, state = rule
                if move < 0:
                    expected = first['AB'.index(entry)] if virgin_cell else usual
                    if state != expected:
                        raise ValueError('reachable cell has an incompatible left return')
                    pending.append((symbol, virgin_neighbor, False))
                    break
                state = first['AB'.index(state)] if virgin_neighbor else usual
                virgin_neighbor = False


class Driver:
    def __init__(self, line):
        self.line=line
        self.period, self.transient, width, self.usual=DRIVERS[line]
        self.prefix = PREFIX.get(line, '')
        self.machine=holdouts()[line-1]
        rules=parse(self.machine)
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
        check_return_contract(rules, self.first, self.usual)
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
                config=x,q,tuple(w),self.phase(used)
                if config in seen:
                    raise ValueError('cyclic left driver')
                seen.add(config)
                w[x],move,q=rules[q,w[x]]
                x+=move
                cost+=1
                if x<0:
                    if q!=self.usual or used>=j:
                        raise ValueError('left driver violates the induction guard')
                    x,q=0,self.letter(used)
                    used+=1
            if q!=self.letter(j):
                raise ValueError('left driver emitted the wrong letter')
            self.table.append((used,cost,tuple(w)))
        u,c,w=self.table[self.transient]
        if ((used-u, tuple(self.table[-1][2])) != (period, w)
                or self.phase(u) != self.phase(used)
                or self.phase(self.transient) != self.phase(self.transient + period)):
            raise ValueError('left driver failed to close its period')
        self.cost_period=cost-c

    def phase(self, index):
        size = len(self.prefix)
        return index if index < size else size + (index-size) % len(self.period)

    def letter(self, index):
        return (self.prefix + self.period)[self.phase(index)]

    def excursions(self, groups):
        return len(self.period)*groups + (len(self.prefix) if groups else 0)

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
              or p['steps']<self.left(self.excursions(groups))[0]+self.excursions(groups) or p['steps']%2):
            raise ValueError('invalid canonical boundary state')
        return p

    def advance(self,engine,state,groups,max_bits):
        """Compute a complete batch, leaving the incoming state intact on failure."""
        if type(groups) is not int or groups < 1:
            raise ValueError('batch size must be a positive integer')
        protocol=' '.join((self.machine,self.prefix or '.',self.period,self.usual,self.first,state['positive_tape'] or '.'))+'\n'
        proc=subprocess.run([str(Path(engine).resolve()),str(groups),str(max_bits)],
                            input=protocol,text=True,capture_output=True)
        if proc.returncode:
            detail = proc.stderr.strip() or f'worker failed ({proc.returncode})'
            if detail.startswith('candidate undefined instruction at cell '):
                raise CandidateUndefined(detail)
            raise RuntimeError(detail)
        tape,*raw=proc.stdout.splitlines()
        calls=list(map(int,raw))
        old=state['groups']; new=old+groups
        before, after = self.excursions(old), self.excursions(new)
        if not calls or calls[0]!=after-before or min(calls)<=0 or len(tape)!=max(len(calls),len(state['positive_tape'])):
            raise ValueError('inconsistent worker result')
        right_cost=2*sum(calls)-calls[0]
        left_cost=self.left(after)[0]-self.left(before)[0]
        return {**state,'groups':new,'steps':state['steps']+left_cost+right_cost,
                'positive_tape':tape,'state':self.period[-1]}


def literal_group(driver, state, work):
    """Run one period in physical order. Only the proved negative replies are skipped."""
    old = driver.excursions(state['groups'])
    target = driver.excursions(state['groups']+1)
    word = list(map(int, state['positive_tape']))
    rules = parse(driver.machine)
    elapsed = 0
    old_left = driver.left(old)[0]
    for finished in range(old, target):
        head = 0
        control = 'A' if finished == 0 else driver.letter(finished-1)
        while head >= 0:
            if head == len(word):
                word.append(0)
            rule = rules.get((control, word[head]))
            if rule is None:
                raw = state['steps'] + elapsed + driver.left(finished)[0] - old_left
                return {'format': HALTED, 'machine': driver.machine, 'line': driver.line,
                        'completed_excursions': finished, 'steps': raw, 'positive_tape': ''.join(map(str, word)),
                        'head': head, 'state': control}
            if elapsed >= work:
                raise RuntimeError('literal work limit during positive excursion')
            word[head], move, control = rule
            head += move
            elapsed += 1
        if control != driver.usual:
            raise ValueError('unexpected return to negative driver')
    return {**state, 'groups': state['groups']+1, 'positive_tape': ''.join(map(str, word)),
            'state': driver.letter(target-1), 'steps': state['steps']+elapsed+driver.left(target)[0]-old_left}


def resolve_candidate(driver, engine, state, groups, max_bits, literal_work, progress):
    """Bisect in chronological order, keeping every completed prefix on disk."""
    pending = []
    count = groups  # the caller has already observed a candidate in this interval
    while True:
        if count == 1:
            state = literal_group(driver, state, literal_work)
            progress(state)
            if state['format'] == HALTED:
                return state
        else:
            first = count // 2
            pending.extend((count-first, first))
        while pending:
            count = pending.pop()
            try:
                state = driver.advance(engine, state, count, max_bits)
            except CandidateUndefined:
                break
            progress(state)
        else:
            return state


def save(path,state):
    atomic_json(path,{'payload':state,'sha256':checksum(state)})


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--engine',type=Path,required=True)
    p.add_argument('--line',type=int,choices=DRIVERS,required=True)
    p.add_argument('--groups',type=int,required=True,help='additional source periods per batch')
    p.add_argument('--batches',type=int,default=1)
    p.add_argument('--max-bits',type=int,default=2**30,help='maximum materialized bits in any one word')
    p.add_argument('--literal-work', type=int, default=10**7, help='positive raw steps allowed when resolving a candidate')
    p.add_argument('--resume',type=Path)
    p.add_argument('--checkpoint',type=Path,required=True,help='atomically saved after each complete batch')
    args=p.parse_args()
    if min(args.groups, args.batches, args.literal_work)<1 or args.max_bits<16:
        p.error('require a positive batch count and at least 16 bits')
    try:
        d=Driver(args.line)
        state=d.load(args.resume) if args.resume else d.blank()
        for _ in range(args.batches):
            try:
                state = d.advance(args.engine, state, args.groups, args.max_bits)
            except CandidateUndefined:
                state = resolve_candidate(d, args.engine, state, args.groups, args.max_bits,
                                          args.literal_work, lambda current: save(args.checkpoint, current))
                if state['format'] == HALTED:
                    print(json.dumps({'status':'halt', 'line':d.line, 'steps':state['steps'],
                                      'head':state['head'], 'state':state['state']}))
                    return
            save(args.checkpoint,state)
            print(json.dumps({'status':'unknown','line':d.line,'groups':state['groups'],'steps':state['steps'],
                              'positive_cells':len(state['positive_tape'])}),flush=True)
    except (OSError,ValueError,RuntimeError,KeyError,TypeError) as error:
        p.exit(2,f'Batch stopped: {error}\n')


if __name__=='__main__':
    main()
