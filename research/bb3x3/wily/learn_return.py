"""Small state-merging experiment, with exact all-word return-map checks.

A candidate is a proof only when the exact finite-product check succeeds.
Excluded closure witnesses are synthesis choices, not claims of halting.
"""
from return_abstraction import *
from certificates import words
from dfa import shortest_product_witness

def learn(positive,negative,implications=()):
    prefixes={''}
    for w in set(positive)|{w for pair in implications for w in pair}:prefixes.update(w[:j]for j in range(1,len(w)+1))
    ps=sorted(prefixes,key=lambda w:(len(w),w));ids={w:i for i,w in enumerate(ps)}
    trans=[{b:ids[w+str(b)]for b in(0,1)if w+str(b)in ids}for w in ps]
    accepting={ids[w]for w in positive};parent=list(range(len(ps)))
    def root(p,i):
        while p[i]!=i:i=p[i]
        return i
    def attempt(x,y):
        p=parent.copy();t=[row.copy()for row in trans];acc=accepting.copy();todo=[(x,y)]
        while todo:
            x,y=todo.pop();x=root(p,x);y=root(p,y)
            if x==y:continue
            p[y]=x
            if y in acc:acc.add(x)
            for b,z in t[y].items():
                if b in t[x]:todo.append((t[x][b],z))
                else:t[x][b]=z
        def accepted(w):
            q=root(p,0)
            for b in w:
                q=root(p,q)
                if int(b)not in t[q]:return False
                q=t[q][int(b)]
            return root(p,q)in acc
        if any(accepted(w)for w in negative):return None
        if any(accepted(x)and not accepted(y)for x,y in implications):return None
        return p,t,acc
    red={0}
    while True:
        red={root(parent,q)for q in red}
        blue={root(parent,z)for q in red for z in trans[q].values()}-red
        if not blue:break
        q=min(blue)
        for r in sorted(red):
            result=attempt(r,q)
            if result is not None:
                parent,trans,accepting=result;break
        else:red.add(q)
    init=root(parent,0);states=[init];outids={init:0};rows=[];acc=set()
    for q in states:
        if q in accepting:acc.add(outids[q])
        row=[]
        for b in(0,1):
            z=root(parent,trans[q][b])if q != -1 and b in trans[q]else-1
            if z not in outids:outids[z]=len(states);states.append(z)
            row.append(outids[z])
        rows.append(tuple(row))
        if q==-1:
            rows[-1]=(outids[-1],outids[-1])
    if -1 in outids:rows[outids[-1]]=(outids[-1],outids[-1]);acc.discard(outids[-1])
    return DFA(tuple(rows),frozenset(acc))

def intersect(a,b):
    states=[(a.initial,b.initial)];ids={states[0]:0};rows=[];acc=set()
    for ix,(p,q) in enumerate(states):
        if p in a.accepting and q in b.accepting:acc.add(ix)
        row=[]
        for bit in(0,1):
            z=(a.transitions[p][bit],b.transitions[q][bit])
            if z not in ids:ids[z]=len(states);states.append(z)
            row.append(ids[z])
        rows.append(tuple(row))
    return DFA(tuple(rows),frozenset(acc))

PREFIX_FILTER=DFA(((3,1),(2,3),(2,2),(3,3)),frozenset({0,2}))
DOUBLE_FILTER=DFA(((1,2),(3,4),(5,6),(3,4),(5,6),(3,4),(5,6)),frozenset({0,3,6}))

def exact_check(candidate):
    base=Moore(candidate.transitions,tuple(q in candidate.accepting for q in range(len(candidate.transitions))),candidate.initial)
    cl=base
    for q in reversed(R):cl=pullback(cl,q)
    def nxt(s):return[(candidate.transitions[s[0]][b],cl.transitions[s[1]][b])for b in(0,1)]
    def bad(s):return s[0]in candidate.accepting and cl.labels[s[1]] is not True
    w,n=shortest_product_witness((candidate.initial,cl.initial),nxt,bad)
    return w,cl.label(w)if w is not None else None,n,len(cl.transitions)

if __name__=='__main__':
    import json
    positive=set();w=''
    for _ in range(40):
        positive.add(w);w=run_return(w)
        assert w is not None
    negative={w for n in range(8)for w in words(n)if run_return(w)is None}
    chosen=set();implications=[]
    for iteration in range(30):
        dfa=intersect(intersect(learn(positive,negative|chosen,implications),PREFIX_FILTER),DOUBLE_FILTER)
        assert all(dfa.accepts(w)for w in positive)
        assert not any(dfa.accepts(w)for w in negative|chosen)
        failure,label,product,clstates=exact_check(dfa)
        print(json.dumps({'iteration':iteration,'states':len(dfa.transitions),'positives':len(positive),
                          'negatives':len(negative),'implications':len(implications),'witness':failure,
                          'output_accepted':label,'product_states':product,'classifier_states':clstates}),flush=True)
        if failure is None:
            print('VALID',dfa);break
        if label is None:negative.add(failure)
        elif failure in positive:
            out=run_return(failure);assert out is not None;positive.add(out)
        else:
            out=run_return(failure);assert out is not None;implications.append((failure,out))
