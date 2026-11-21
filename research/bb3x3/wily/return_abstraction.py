"""Exact finite predicate abstraction for the actual prefix return map.

No bounded word enumeration is used to derive abstract edges: a Moore machine
classifies every finite input by the exact return output's feature, or by halt.
"""
from __future__ import annotations
from dataclasses import dataclass
from certificates import STEP, END, pass_word
from dfa import DFA, BAD
from feature_analysis import monoid_dfa
from return_sections import return_section

R=return_section('001100')[1]

@dataclass(frozen=True)
class Moore:
    transitions:tuple[tuple[int,int],...]
    labels:tuple
    initial:int=0
    def step_word(self,q,w):
        for b in w:q=self.transitions[q][int(b)]
        return q
    def label(self,w):return self.labels[self.step_word(self.initial,w)]

def minimize(m):
    tab={};cl=[]
    for label in m.labels:
        if label not in tab:tab[label]=len(tab)
        cl.append(tab[label])
    while True:
        tab={};new=[]
        for q,row in enumerate(m.transitions):
            sig=(m.labels[q],cl[row[0]],cl[row[1]])
            if sig not in tab:tab[sig]=len(tab)
            new.append(tab[sig])
        if new==cl:break
        cl=new
    trans=[None]*len(tab);labels=[None]*len(tab)
    for q,row in enumerate(m.transitions):
        trans[cl[q]]=tuple(cl[t]for t in row);labels[cl[q]]=m.labels[q]
    return Moore(tuple(trans),tuple(labels),cl[m.initial])

def pullback(m,mode):
    states=[(m.initial,mode)];ids={states[0]:0};trans=[];labels=[]
    for q,s in states:
        row=[]
        for b in (0,1):
            emit,t=STEP[s][b];nxt=(m.transitions[q][emit],t)
            if nxt not in ids:ids[nxt]=len(states);states.append(nxt)
            row.append(ids[nxt])
        trans.append(tuple(row))
        labels.append(None if END[s]is None else m.labels[m.step_word(q,END[s])])
    return minimize(Moore(tuple(trans),tuple(labels)))

def return_classifier(feature,word=R,verbose=False):
    m=Moore(feature.transitions,tuple(range(len(feature.transitions))),feature.initial)
    for q in reversed(word):
        m=pullback(m,q)
        if verbose:print('pullback','abcd'[q],len(m.transitions),flush=True)
    return m

def exact_abstract_edges(feature,classifier):
    states=[(feature.initial,classifier.initial)];ids={states[0]:0};parents=[None];edges={}
    for ix,(q,r)in enumerate(states):
        label=classifier.labels[r]
        edges.setdefault(q,{}).setdefault(label,ix)
        for b in (0,1):
            nxt=(feature.transitions[q][b],classifier.transitions[r][b])
            if nxt not in ids:ids[nxt]=len(states);states.append(nxt);parents.append((ix,b))
    def witness(ix):
        chars=[]
        while parents[ix]is not None:
            ix,b=parents[ix];chars.append(str(b))
        return ''.join(reversed(chars))
    return {q:{r:witness(ix)for r,ix in dest.items()}for q,dest in edges.items()},len(states)

def closure_certificate(feature,edges,seed=''):
    init=feature.step_word(feature.initial,seed)
    todo=[init];path={init:None}
    for q in todo:
        for r,w in edges[q].items():
            if r not in path:
                path[r]=(q,w)
                if r is None:
                    trace=[];p=None
                    while path[p]is not None:
                        old,w=path[p];trace.append((old,w,p));p=old
                    return {'valid':False,'abstract_counterexample':list(reversed(trace))}
                todo.append(r)
    return {'valid':True,'accepting':todo}

def run_return(w,word=R):
    for q in word:
        w=pass_word(w,q)
        if w is None:return None
    return w

if __name__=='__main__':
    import json
    C=((0,1),(0,2),(1,0))
    feature,_=monoid_dfa([C,BAD.transitions])
    classifier=return_classifier(feature,verbose=True)
    edges,n=exact_abstract_edges(feature,classifier)
    result=closure_certificate(feature,edges)
    print(json.dumps({'feature_states':len(feature.transitions),'return_classifier_states':len(classifier.transitions),'product_states':n,**result}))
