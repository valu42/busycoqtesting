"""Two-counter boundary reduction for a shifted word of line-33 stable pairs."""
import sys

from neglected33 import batch, split_reserve, CYCLE


def tile(pair, n):
    if pair == '22':
        return '22',2*n,7*n
    h = CYCLE.index(pair)
    m, r = divmod(n + (h+2)%3,3)
    g = (r+1)%3
    return CYCLE[g],m,5*(n-m) + 4*((g==1)-(h==1))


def cut(word):
    # After a leading digit eliminate an even number of canonical source cells.
    p,k = split_reserve(word)
    if (len(p)-1)%2:
        if k==0: raise ValueError('no aligned cut')
        p += '421'; k-=1
    if not p or any(p[j:j+2] not in (*CYCLE,'22') for j in range(1,len(p),2)):
        raise ValueError('uncanonical prefix')
    return p[0],p[1:],k


def shift(d, pairs, n=1,s=0):
    out=[]; clock=0
    for j in range(0,len(pairs),2):
        # When outer requests terminate, the remaining inner calls still apply
        # to an aligned word. Report a separate stop instead of skipping them.
        if not n:
            return ''.join(out),d,n,s,pairs[j:],clock
        p,t,local = tile(pairs[j:j+2],s)
        clock+=local
        a,b=p
        if d=='1':
            n-=1;clock+=1
            q='2'+a
        elif d=='4' and a=='1':
            n-=1;clock+=3
            q='22'
        elif d=='4' and a=='2':
            n-=1
            if b=='1':
                q='21'; b='4'; t+=1; clock+=6
            elif b=='2':
                q='22'; b='2'; t+=2; clock+=9
            else:
                q='22'; b='1'; clock+=7
        else:
            q=d+a
        emitted,n,local=tile(q,n)
        out.append(emitted);clock+=local
        d,s=b,t
    return ''.join(out),d,n,s,'',clock



U, V, W = ('1',0), ('4',0), ('4',1)
STATES = {U,V,W}
RULES = {
    U: (U,V,V),
    V: (W,V,U),
    W: (W,U,W),
}


def top_prediction(pairs):
    options = set(STATES)
    for i in range(0,len(pairs),2):
        trit = CYCLE.index(pairs[i:i+2])
        options = {RULES[q][trit] for q in options}
    return options


def align_orbit(last):
    y='1'
    previous_fresh=''
    passed=decided=0
    observations=[]
    for epoch in range(1,last+1):
        if epoch<3:
            y='2'+batch(y,1)[0]
            continue
        head, register, reserve=cut(y)
        prefix,d,n,s,left,clock=shift(head,register)
        assert not left
        if len(previous_fresh)>=18:
            assert register.endswith(previous_fresh)
            high=previous_fresh[-18:]
            _,d0,n0,s0,remaining,_=shift(head,register[:-18])
            assert not remaining and (d0,s0) in STATES and n0>0
            _,d1,n1,s1,remaining,_=shift(d0,high,n0,s0)
            assert not remaining and (d,n,s)==(d1,n1,s1)
            prediction=top_prediction(high)
            assert (d,s) in prediction
            passed+=1; decided+=len(prediction)==1
        if len(previous_fresh)>=4:
            _,d_pre,n_pre,s_pre,rem,_=shift(head,register[:-4])
            if not rem and n_pre>0 and (d_pre,s_pre) in STATES:
                state={U:'U',V:'V',W:'W'}[d_pre,s_pre]
                signed={'21':'+1','14':'-1','24':'0'}[previous_fresh[-4:-2]]
                observations.append((epoch,state,signed,'gain' if (d,s)==W else 'loss'))
        inner, cost_inner=batch('421'*reserve,s)
        output, cost_outer=batch(d+inner,n)
        original, original_cost=batch(y,1)
        assert original == prefix+output and original_cost==clock+cost_inner+cost_outer
        y='2'+original
        if (d,s)==W:
            virgin=n;new_reserve=reserve+1
        else:
            assert (d,s)==U and reserve>=1
            _,m,_=tile('14',n)
            _,virgin,_=tile('21',m);new_reserve=reserve-1
        previous_fresh=batch('',virgin)[0]
        assert y.endswith(previous_fresh+'421'*new_reserve)
        assert cut(y)[2]==new_reserve
        print(epoch,len(register)//2,reserve,d,s,n.bit_length(),new_reserve,flush=True)
    print(f'Nine high pairs: {decided} of {passed} eligible blank stages fix a unique sign.')
    print('Epoch, carry entering penultimate trit, penultimate balanced trit, sign')
    for row in observations:
        print(*row, sep=',')


def check_rule():
    from itertools import product
    for (d,s), row in RULES.items():
        for q in range(3):
            _,end,_,inner,_,_=shift(d,CYCLE[q],10,s)
            assert (end,inner)==row[q]
    expected=[1,3]
    for _ in range(7):
        expected.append(2*expected[-1]+expected[-2])
    for k in range(9):
        unresolved=sum(len(top_prediction(''.join(w)+'21'))>1 for w in product(CYCLE,repeat=k))
        assert unresolved==expected[k]
    print(f'Ambiguous high prefixes for 0..8 free trits: {expected}')


if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Enable assertions.')
    check_rule()
    align_orbit(int(sys.argv[1]) if len(sys.argv)>1 else 33)
