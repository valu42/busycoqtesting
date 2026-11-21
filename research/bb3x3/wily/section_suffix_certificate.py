"""A finite certificate for nonempty return sections on a regular branch family.

This certifies boundary encounters, NOT nonhalting. It says nothing about
whether a encountered boundary mode is the halting mode b.
"""
from __future__ import annotations
from certificates import STEP
from return_sections import reduce_word, section, return_section

# temporal modes a=0,b=1,c=2,d=3
SUFFIXES = {
    'A': ((1,0),),
    'B': ((0,1),(2,1)),
    'C': ((0,3),(2,3)),
    'D': ((0,),(2,)),
    'E': ((1,),),
}
NEXT = {'A':('D','B'),'B':('A','C'),'C':('E','D'),
        'D':('D','E'),'E':('D',None)}

def has_class(word,cl):
    return any(len(word)>=len(s) and tuple(word[-len(s):])==s for s in SUFFIXES[cl])

def root_action(word,bit):
    for q in word:bit=STEP[q][bit][0]
    return bit

def raw_section(word,bit):
    out=[]
    for q in word:
        bit,nxt=STEP[q][bit]
        if nxt!=4:out.append(nxt)
    return bit,tuple(out)

def table_certificate():
    checks=0
    for cl,suffixes in SUFFIXES.items():
        for bit in (0,1):
            target=NEXT[cl][bit]
            if target is None:continue
            for suffix in suffixes:
                # The full return finishes at bit; therefore the input to the
                # last suffix is bit xor the suffix's root permutation.
                before=bit ^ root_action(suffix,0)
                after,tail=raw_section(suffix,before)
                assert after==bit
                # Only a trailing d in the preceding normal word can interact
                # with this section's first letter. Check every possible last
                # letter, plus an empty preceding word.
                for prefix in [(),(0,),(1,),(2,),(3,)]:
                    result=reduce_word(prefix+tail)
                    assert has_class(result,target),(cl,bit,suffix,prefix,result,target)
                    checks+=1
    assert has_class(return_section('001100')[1],'A')
    return checks

def branch_class(extension):
    cl='A'
    for b in extension:
        if cl is None:return None
        cl=NEXT[cl][int(b)]
    return cl

if __name__=='__main__':
    print('finite suffix-table checks:',table_certificate())
    # These are finite base checks of the parameterized path identities.
    for k in range(20):
        assert branch_class('10'*k)=='A'
        assert branch_class('10'*k+'1')=='B'
        assert branch_class('10'*k+'11')=='C'
        for j in range(1,20):
            assert branch_class('10'*k+'11'+'10'*j)=='D'
            assert branch_class('10'*k+'11'+'10'*j+'1')=='E'
    print('periodic and one-defect branch formulas checked')
