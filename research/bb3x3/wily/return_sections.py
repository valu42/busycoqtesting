"""Exact recursive return sections of the boundary-free prefix action of P0.

Boundary extensions are NOT applied while deriving prefix actions. When a
return section is used on a nonempty finite tail, the reductions here preserve
both output and definedness of the full sequence of partial passes.
"""
from certificates import STEP, pass_word

# Temporal composition: [p,q] means apply p first, then q.
def reduce_word(word):
    out=[]
    for q in word:
        if q == 4:
            continue
        if out and out[-1] == 3 and q in (0,2,3):
            out.pop()
            if q == 0: out.append(2)  # a after d = c.
            elif q == 2: out.append(0)  # c after d = a.
        else:
            out.append(q)
    return tuple(out)

def section(word, bit):
    out=[]
    for q in word:
        bit,qnext=STEP[q][bit]
        if qnext != 4:out.append(qnext)
    return bit,reduce_word(out)

def return_section(prefix):
    period=1;word=(0,)
    for b in prefix:
        bit=int(b)
        out,left=section(word,bit)
        if out != bit:
            _,right=section(word,out)
            word=reduce_word(left+right)
            period*=2
        else:
            word=left
    return period,word

def inverse_prefix(word):
    q=0;out=[]
    for b in word:
        b=int(b)
        incoming=next(x for x in (0,1) if STEP[q][x][0]==b)
        _,q=STEP[q][incoming]
        out.append(str(incoming))
    return ''.join(out)

def prefix_action(word):
    q=0;out=[]
    for b in word:
        b,q=STEP[q][int(b)]
        out.append(str(b))
    return ''.join(out),q

def validate(depth=9):
    from certificates import words
    for n in range(depth+1):
        for prefix in words(n):
            period,computed=return_section(prefix)
            x=prefix;actual=[]
            for _ in range(period):
                x,q=prefix_action(x)
                if q!=4:actual.append(q)
            assert x==prefix
            assert reduce_word(actual)==computed,(prefix,computed,actual)
    return True

if __name__=='__main__':
    import json
    assert validate()
    w='001100';steps=100000
    for _ in range(steps):
        w=pass_word(w)
        assert w is not None
    initial=w
    for _ in range(steps):initial=inverse_prefix(initial)
    assert initial.startswith('001100')
    for label,word in [('current',w),('reconstructed_initial',initial)]:
        print(label,word)
        for n in range(6,len(word)):
            period,ret=return_section(word[:n])
            homogeneous=len(set(ret))<=1
            if homogeneous or n in (6,10,20,30,40,50):
                print(json.dumps({'depth':n,'period':period,'return_length':len(ret),
                                  'homogeneous':homogeneous,'word':ret if homogeneous else ''}))
