"""Exact regular preimages; optional bounded-survival exploration is not a proof."""
from dfa import DFA, END, STEP, verify_invariant

def minimize(dfa):
    classes = [int(q in dfa.accepting) for q in range(len(dfa.transitions))]
    while True:
        tab = {}
        new = []
        for q, (a,b) in enumerate(dfa.transitions):
            sig = (q in dfa.accepting, classes[a], classes[b])
            if sig not in tab: tab[sig] = len(tab)
            new.append(tab[sig])
        if new == classes: break
        classes = new
    transitions = [None]*len(tab)
    accepting = set()
    for q, (a,b) in enumerate(dfa.transitions):
        transitions[classes[q]] = (classes[a], classes[b])
        if q in dfa.accepting: accepting.add(classes[q])
    return DFA(tuple(transitions), frozenset(accepting), classes[dfa.initial])

def safe_preimage(dfa, prepend=True, mode=0):
    init=(dfa.step_word(dfa.initial, '0') if prepend else dfa.initial,mode)
    states=[init];ids={init:0};trans=[];acc=set()
    for ix,(q,m) in enumerate(states):
        row=[]
        for b in (0,1):
            out,nm=STEP[m][b];t=(dfa.transitions[q][out],nm)
            if t not in ids:ids[t]=len(states);states.append(t)
            row.append(ids[t])
        trans.append(tuple(row))
        if END[m] is not None and dfa.step_word(q, END[m]) in dfa.accepting:acc.add(ix)
    return minimize(DFA(tuple(trans),frozenset(acc)))

if __name__=='__main__':
    import sys
    d=DFA(((0,0),),frozenset({0}))
    for n in range(1,26):
        d=safe_preimage(d,prepend='--pass' not in sys.argv)
        cert=verify_invariant(d, prepend='--pass' not in sys.argv)
        print(n,len(d.transitions), cert['contains_start'], cert['closure_counterexample'], flush=True)
        if len(d.transitions)>30000 or cert['valid']:break
