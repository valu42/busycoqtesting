"""Exact abstraction graphs and explicit counterexamples to DFA summaries."""
from certificates import END, STEP, pass_word
from dfa import BAD, DFA

def monoid_dfa(tables):
    initial = tuple(tuple(range(len(t))) for t in tables)
    states=[initial]; ids={initial:0};trans=[]
    for state in states:
        row=[]
        for bit in (0,1):
            nxt=tuple(tuple(table[q][bit] for q in component)
                      for component,table in zip(state,tables))
            if nxt not in ids: ids[nxt]=len(states);states.append(nxt)
            row.append(ids[nxt])
        trans.append(tuple(row))
    return DFA(tuple(trans),frozenset()),states

def abstraction(dfa,seed='001100',limit=1000000):
    """All exact abstract edges for P0 under the DFA-state partition."""
    states=[(dfa.initial,dfa.initial,0)]
    ids={states[0]:0};parents=[None];edges={}
    def witness(ix):
        out=[]
        while parents[ix] is not None:
            ix,b=parents[ix];out.append(str(b))
        return ''.join(reversed(out))
    for ix,(inp,out,m) in enumerate(states):
        end=END[m]
        dest=None if end is None else dfa.step_word(out,end)
        edges.setdefault(inp,{}).setdefault(dest,ix)
        for bit in (0,1):
            emit,nm=STEP[m][bit]
            st=(dfa.transitions[inp][bit],dfa.transitions[out][emit],nm)
            if st not in ids:
                ids[st]=len(states);states.append(st);parents.append((ix,bit))
        if len(states)>limit:
            return {'complete':False,'triples':len(states)}
    init=dfa.step_word(dfa.initial,seed)
    reached=[init];path={init:None}
    for state in reached:
        for nxt,ix in edges[state].items():
            if nxt not in path:
                path[nxt]=(state,witness(ix))
                if nxt is None:
                    failure=[];q=None
                    while path[q] is not None:
                        old,w=path[q];failure.append((old,w,q));q=old
                    return {'complete':True,'safe':False,'triples':len(states),
                            'feature_states':len(dfa.transitions),
                            'abstract_path':list(reversed(failure))}
                reached.append(nxt)
    return {'complete':True,'safe':True,'triples':len(states),
            'feature_states':len(dfa.transitions),'accepting':reached}

if __name__=='__main__':
    import json
    C=((0,1),(0,2),(1,0))
    joint, signatures = monoid_dfa([C, BAD.transitions])
    assert joint.step_word(joint.initial, '001100') == joint.step_word(joint.initial, '001010')
    assert sorted('001100') == sorted('001010')
    assert pass_word('001010') == '110010'
    assert pass_word('110010') == '011110'
    assert pass_word('011110') is None
    cases=[('C_final',DFA(C,frozenset())),
           ('C_monoid',monoid_dfa([C])[0]),
           ('C_and_B_monoids',monoid_dfa([C,BAD.transitions])[0])]
    for name,d in cases:
        print(name,json.dumps(abstraction(d)),flush=True)
