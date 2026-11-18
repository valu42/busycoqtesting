#!/usr/bin/env python3
"""Actual blank-orbit metrics using the inherited exact line-7 simulator."""
import argparse, collections, json, math, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'frontiers'))
from line7 import Calls, HALT, RULES, load, save, snapshot

class Probe(Calls):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fresh=[]
        self.guards=collections.Counter()
        self.residual=[]
    def unit(self,i,state):
        while True:
            self.tick()
            digit=self.digit(i)
            rule=RULES.get((state,digit))
            if rule is None:
                self.halt_cell=i
                return HALT
            fresh=(i==len(self.tape)-1 and digit==0)
            if fresh:self.fresh.append(state)
            # epoch() handles its outer guard separately; these are internal guards.
            is_guard=(state=='A' and digit==0)
            if is_guard:
                self.guards['fresh' if fresh else 'reused']+=1
                suffix=tuple(self.tape[i+1:i+9])
                self.guards['child_prefix_'+''.join(map(str,suffix))]+=1
                child=self.tape[i+1] if i+1<len(self.tape) else 0
                if child==2:self.guards['forced_B_child_2']+=1
                elif child==0:self.guards['forced_B_child_0']+=1
                elif child==3:
                    n=2;q='A';j=i+2
                    while n and j<len(self.tape) and self.tape[j] in (2,4):
                        x=self.tape[j]
                        if q=='B':n=(n+(x==4))//2;q='A'
                        elif x==2:n*=3
                        else:q='B'
                        j+=1
                    if n==0:self.guards['forced_B_ordinary_prefix']+=1
                    elif bytes(self.tape[i+1:])==bytes((3,2)):
                        self.guards['forced_B_terminal_32']+=1
                    else:
                        self.guards['residual_guard_test']+=1
                        self.residual.append({'cell_index':i,'word':''.join(map(str,self.tape[i+1:]))})
                else:self.guards['unexpected_child_'+str(child)]+=1
            digit,move,state=rule
            self.tape[i]=digit;self.steps+=1
            if move==-1:return state
            _,state=yield self.many(i+1,state,1)
            if is_guard:self.guards['reply_'+state]+=1
            if state==HALT:return HALT

def leading_twos(word):
    n=0
    for x in word[1:]:
        if x!=2:break
        n+=1
    return n

def log10(n):
    b=n.bit_length(); shift=max(0,b-53)
    return math.log10(n>>shift)+shift*math.log10(2)

def summary(rows):
    ks=[r['leading_twos'] for r in rows]
    ds=[r['leading_twos_delta'] for r in rows]
    drops=[-x for x in ds if x<0]
    return {'epochs':len(rows),'first':rows[0]['epoch'],'last':rows[-1]['epoch'],
            'leading_twos_final':ks[-1],'delta_counts':dict(sorted(collections.Counter(ds).items())),
            'negative_deltas':len(drops),'max_drop':max(drops,default=0),
            'fresh_A':sum(r['fresh_A'] for r in rows),'fresh_B':sum(r['fresh_B'] for r in rows),
            'growth_cells':sum(r['new_cells'] for r in rows),
            'guard_tests':dict((k,v) for k,v in sum((collections.Counter(r['guard_tests']) for r in rows),collections.Counter()).items() if not k.startswith('child_prefix_')),
            'guard_prefixes':dict(sum((collections.Counter({k[13:]:v for k,v in r['guard_tests'].items() if k.startswith('child_prefix_')}) for r in rows),collections.Counter())),
            'min_log10_increment':min(r['log10_raw_increment'] for r in rows),
            'max_log10_increment':max(r['log10_raw_increment'] for r in rows),
            'final_log10_raw':rows[-1]['log10_raw'],
            'all_epochs_without_zero_or_one':all(r['clean'] for r in rows)}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--epochs',type=int,default=1024); ap.add_argument('--resume',type=Path); ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args()
    p=load(args.resume) if args.resume else snapshot(0,Calls())
    vm=Probe(map(int,p['word']),int(p['steps_hex'],16)); rows=[]
    k=leading_twos(vm.tape)
    for e in range(p['epochs']+1,args.epochs+1):
        before=vm.steps; width=len(vm.tape); vm.fresh=[]; vm.guards=collections.Counter(); vm.residual=[]
        ok=vm.epoch()
        if not ok:raise RuntimeError('halt: preserve and inspect this run')
        nk=leading_twos(vm.tape)
        rows.append({'epoch':e,'leading_twos':nk,'leading_twos_delta':nk-k,'new_cells':len(vm.tape)-width,
                     'fresh_A':vm.fresh.count('A'),'fresh_B':vm.fresh.count('B'),
                     'guard_tests':dict(vm.guards),'residual_guards':vm.residual,'internal_threes':vm.tape.count(3)-1,'clean':not any(x in (0,1) for x in vm.tape),
                     'log10_raw_increment':log10(vm.steps-before),'log10_raw':log10(vm.steps)})
        k=nk
    doc={'machine':p['machine'],'starting_commit':'2ab106f706cb1715d494c7f67464e9222092058f',
         'research_date':'2026-11-18','source_checkpoint':str(args.resume) if args.resume else 'blank',
         'summary':summary(rows),'halves':[summary(rows[:len(rows)//2]),summary(rows[len(rows)//2:])], 'rows':rows}
    args.out.write_text(json.dumps(doc,indent=2)+'\n')
    save(args.out.with_name(args.out.stem+'-checkpoint.json'),snapshot(args.epochs,vm))
    print(json.dumps({k:v for k,v in doc.items() if k!='rows'},indent=2))
if __name__=='__main__':main()
