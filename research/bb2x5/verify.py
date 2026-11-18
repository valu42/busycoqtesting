"""Finite cross-checks for the four BB(2,5) reductions. Run with Python 3.10+."""
from collections import Counter
from hashlib import sha256
from itertools import product
from pathlib import Path

import prior_frontier as old
import prior_sweeps as sweep
from mark_prefix import check_extensions

M2 = '1RB---4LB0LA4RA_2LB2LA3RA4LB0RB'
T2 = old.parse(M2)
assert [old.LIST[i-1] for i in (2,10,17,26)] == [M2,old.M10,old.M17,sweep.COUNTER]


def half_request(tape, state):
    """Mutate a list representing a semi-infinite tape. Return (exit state, steps)."""
    x = 0
    for steps in range(10_000_000):
        if x < 0:
            return state, steps
        if x == len(tape):
            tape.append(0)
        op = T2[state][tape[x]]
        if op is None:
            return None, steps
        tape[x], dx, state = op
        x += dx
    raise AssertionError('uncompleted right-half request')


def left_slice(n, answers):
    """Run the literal negative side through cell zero with an externally supplied suffix."""
    pattern = (2,4,2)
    tape = {x:pattern[(x+n-1)%3] for x in range(-n+1,1)}
    x, state, i = -n, 0, 0
    sent = []
    for _ in range(5000):
        if x == 1:
            sent.append('AB'[state])
            if i == len(answers):
                return ''.join(sent), 'waiting'
            state, x = 'AB'.index(answers[i]), 0
            i += 1
        if x == -n-1 and state == 0:
            assert [tape[j] for j in range(-n,1)] == [pattern[d%3] for d in range(n+1)]
            return ''.join(sent), 'extended'
        op = T2[state][tape.get(x,0)]
        if op is None:
            assert (state,tape[x]) == (0,1)
            return ''.join(sent), 'halt'
        tape[x], dx, state = op
        x += dx
    raise AssertionError('uncompleted left slice')


def audit2():
    for n in range(16):
        r = n%3
        if r == 0:
            assert left_slice(n,'B') == ('B','extended')
            if n:
                for a,b in product('AB', repeat=2):
                    expected = 'BB' if a=='A' else 'BBA'
                    assert left_slice(n,'A'+a+b) == (expected,'halt')
            else:
                assert left_slice(0,'A') == ('B','halt')
        elif r == 1:
            assert left_slice(n,'B') == ('A','extended')
            assert left_slice(n,'A') == ('A','halt')
        else:
            for pre in ('','A'):
                assert left_slice(n,pre+'BB') == ('A'*len(pre)+'AB','extended')
                for diagnosis in 'AB':
                    assert left_slice(n,pre+'BA'+diagnosis) == ('A'*len(pre)+'ABB','halt')

    tape, exceptions, right_steps = [], [], 0
    for cycle in range(800):
        for phase, req in enumerate((1,0,0,1)):
            reply, steps = half_request(tape,req)
            right_steps += steps
            if reply == 0 and phase == 2:
                exceptions.append(cycle)
                reply, steps = half_request(tape,0)
                right_steps += steps
            assert reply == 1
    assert exceptions == [0] and len(tape)==3979
    assert set(tape) <= {0,2,4}
    # Independently execute the *entire two-way blank Turing machine*, without a driver.
    # The time cap makes an unfinished verification fail explicitly.
    t = {}
    x = q = 0
    epochs = 0
    for steps in range(70_000_000):
        if q == 0 and x == -epochs-1:
            epochs += 1
            if epochs == 2400:
                break
        v = T2[q][t.get(x,0)]
        assert v is not None
        t[x], dx, q = v
        x += dx
    else:
        raise AssertionError('raw checkpoint not reached')
    assert q==0 and x==-2400 and max(t)==3979
    assert [t[i] for i in range(x+1,1)] == [2,4,2]*800
    assert [t[i] for i in range(1,3980)] == tape
    print('line 2: 2400 blank left extensions at',steps,'raw steps; rightmost cell 3979')
    print('line 2: fixed-cut right steps',right_steps,'and flexible retries at cycles',exceptions)

    w = [2,2]
    for op in 'GGFF':
        if op=='G':
            w = [2,2]+w
        else:
            result,_ = half_request(w,1)
            assert result==1
            w=[2]+w
    assert w == [2,4,2,4,4,4,4,2] and half_request(w,1)==(0,125)
    print('line 2: unrestricted generator word GGFF returns A to the next B in 125 steps')


def section(word, phase):
    """Ordinary line-2 digit, in phase 0 (symbol 2) or 1 (symbol 4)."""
    out = []
    for b in word:
        if phase:
            out.extend((0,1) if b==0 else (1,))
        elif b:
            out.append(0)
        phase ^= 1
    return tuple(out)


def act_on_bits(word, bits):
    ans = []
    for bit in bits:
        ans.append(bit^(len(word)%2))
        word = section(word,bit)
    return tuple(ans)


def check_orders():
    for size in range(1,5):
        for w in product((0,1),repeat=size):
            if size%2:
                odd=True
            elif w.count(0)%2:
                odd=False
            else:
                continue
            for width in range(1,7):
                expected=2**((width+int(odd))//2)
                for x in product((0,1),repeat=width):
                    y=act_on_bits(w,x)
                    for k in range(1,expected+1):
                        if y==x:
                            break
                        y=act_on_bits(w,y)
                    assert y==x and k==expected
    print('line 2: ordinary-word orbit formulas cross-checked on binary widths 1 through 6')


def arithmetic26(u,e,m,token):
    if token=='d':
        # Lowest position in neither u nor e. All lower positions outside u carry.
        stop=(~(u|e)) & ((u|e)+1)
        e ^= (~u) & (2*stop-1)
    else:
        assert token=='a'
        selected=2*e
        available=u & selected
        if available:
            stop=available & -available
            u ^= selected & (2*stop-1)
        else:
            u ^= selected
            m+=1
    return u,e,m


def paired_cycle26(U,E,m):
    """One whole aadd cycle in coordinates u=4U and e=2E."""
    selected=E & (E-1)
    common=U & selected
    if common:
        stop=common & -common
        U ^= selected & (2*stop-1)
    else:
        U ^= selected
        m += 1+int(E==0)
    excluded=2*U
    stop=(~(excluded|E)) & ((excluded|E)+1)
    E ^= (~excluded) & (2*stop-1)
    return U,E,m


def physical26(cols):
    return (sum((1-o)<<i for i,(o,e) in enumerate(cols)),
            sum(e<<i for i,(o,e) in enumerate(cols)),len(cols))


def audit26():
    # Test the formula on every physical digit word through length four, including halting words.
    for length in range(5):
        for digits in product(product(range(2),repeat=2),repeat=length):
            initial=physical26(digits)
            for token in 'ad':
                tup=arithmetic26(*initial, token)
                cols=list(digits)
                live=sweep.feed_columns(cols,token)
                assert live==(tup[1]<2**tup[2])
                if live:
                    assert physical26(cols)==tup
    u=e=m=0
    compressed=(0,0,0)
    for i in range(131072):
        for c in 'aadd':
            old_u,old_e,old_m=u,e,m
            u,e,m=arithmetic26(u,e,m,c)
            assert e < 1<<m
            if c=='a' and old_m==m:
                assert u<old_u
            if c=='d':
                assert e>old_e
        previous_U,previous_E,previous_size=compressed
        compressed=paired_cycle26(*compressed)
        U,E,size=compressed
        if previous_size==size:
            assert E+U*U <= previous_E+previous_U*previous_U
        assert (4*U,2*E,size)==(u,e,m)
    assert (u,e,m)==(14809968640,81588923392,74)
    print('line 26: after 131072 aadd cycles, (u,e,m) =', (u,e,m))
    u=e=m=0
    for c in 'adad':
        u,e,m=arithmetic26(u,e,m,c)
    assert e>=1<<m
    print('line 26: finite alternative input adad reaches its first virtual overflow at token 4')
    sweep.check_counter()


def audit_return_slice(i, known):
    """All suspensions reachable from the given input prefix and the mark constraints."""
    d=old.digits(old.DATA)
    initial=(old.DATA[2*i:]+'2',d[i-1][1],0,0)
    states=[initial]
    seen={initial}
    edges=set()
    for row,pending,cool,consumed in states:
        for bit in ((known[consumed],) if consumed<len(known) else (0,1)):
            if bit and (pending or cool):
                continue
            special=bool(bit or pending)
            edge,next_row=old.pulse_on_tail(row,special)
            if edge:
                edges.add(next_row)
                continue
            item=(next_row, int(special and row[0]!='1'),
                  2 if bit else max(0,cool-1), min(consumed+1,len(known)))
            if item not in seen:
                seen.add(item)
                states.append(item)
    fates=Counter()
    for row in edges:
        t=list(map(int,row))
        x,state=len(t),1
        for n in range(1000):
            if x<0:
                tag='AB'[state]
                fates[tag,n]+=1
                assert len(t)-len(row)==(2 if tag=='A' else 1)
                break
            if x==len(t):
                t.append(0)
            op=old.T17[state][t[x]]
            if op is None:
                assert (state,t[x],x+12-len(row))==(0,3,-4)
                if i==414:
                    assert (row,n) in {('040242440444040444444',242), ('040244044444040444444',288)}
                fates['H',n]+=1
                break
            t[x],dx,state=op
            x+=dx
        else:
            raise AssertionError('post-edge slice failed to finish')
    return len(states),len(edges),fates


def audit17():
    data=old.digits(old.DATA)
    fixed='01000000'
    results={}
    for b9,b10,expected in ((0,0,'4'),(0,1,'0'),(1,0,'1')):
        bits=tuple(map(int,fixed))+ (b9,b10)
        rows=old.right_events(data,bits)
        assert rows == {expected+'444040444444'}
        results[b9,b10]=expected
    prefix=bytes((0,0,0,0,1,0))*4+bytes(4)
    cases=[]
    for gap in (6,13,17):
        p,q=prefix,bytes((1,))+bytes(gap-1)
        for i in range(403,418):
            p,q=old.periodic_marks((data[i][0],data[i-1][1]),p,q)
        sample=(p+q*10)[:10]
        assert sample[:8]==bytes(map(int,fixed))
        cases.append(results[sample[8],sample[9]])
    assert cases==['4','0','1']
    print('line 17: gap choices 6, 13, 17 yield the three edge symbols',cases)

    for i,k,state_count,edge_count,results in (
        (415,'0000001000',411,32,{'A':(3,132,200),'B':(29,62,126)}),
        (414,'010001000',1352,71,{'A':(7,134,338),'B':(62,64,152),'H':(2,242,288)})):
        n,z,counts=audit_return_slice(i,tuple(map(int,k)))
        assert (n,z)==(state_count,edge_count)
        spans={}
        for tag in {tag for tag,steps in counts}:
            entries=[(steps,count) for (q,steps),count in counts.items() if q==tag]
            spans[tag]=sum(c for _,c in entries),min(x for x,_ in entries),max(x for x,_ in entries)
        assert spans==results
        if i==414:
            assert {step for tag,step in counts if tag=='H'}=={242,288}
    print('line 17: blank return crosses -8 without halting; before -10 only A3 at -4 is possible')

    short=tuple(map(int,'01000010000000100100100'))
    row=old.DATA[2*412:]+'2'
    pending=data[411][1]
    for slot,bit in enumerate(short,1):
        assert not (pending and bit)
        special=bool(bit or pending)
        next_pending=int(special and row[0]!='1')
        edge,row=old.pulse_on_tail(row,special)
        if edge:
            assert slot==23 and row.endswith('040242440444040444444')
            break
        pending=next_pending
    else:
        raise AssertionError('short conditional input missed the edge')

    # A specific admissible external input reaches the literal forbidden instruction.
    # The remaining 21 pairs start at absolute coordinate -31.
    row=old.DATA[2*403:]+'2'
    pending=data[402][1]
    tenured=tuple(prefix)
    for slot in range(1,6514):
        bit=tenured[slot-1] if slot<=len(tenured) else int((slot-len(tenured)-1)%56==0)
        assert not (pending and bit)
        special=bool(bit or pending)
        trit='102'.index(row[0])
        edge,row=old.pulse_on_tail(row,special)
        if edge:
            assert slot==6513 and row=='4444444444040444444404040242440444040444444'
            break
        pending=int(special and trit!=0)
    else:
        raise AssertionError('conditional edge never reached')
    t=list(map(int,row))
    x,state=len(t),1
    for moves in range(243):
        assert x>=0
        if x==len(t):
            t.append(0)
        op=old.T17[state][t[x]]
        if op is None:
            assert state==0 and t[x]==3 and x+12-len(row)==-4 and moves==242
            break
        t[x],dx,state=op
        x+=dx
    else:
        raise AssertionError('conditional branch failed to halt')
    print('line 17: gap 56 at cut 403 reaches the edge on slot 6513 then A3 at -4 in 242 moves')


def audit10():
    p=bytes((1,0,0))
    for x in range(3,16):
        a,b=p.count(0),p.count(1)
        assert (a%3,b%3)==(2,1)
        if x==15:
            circ=p+p[:9]
            assert len(p)==409152
            assert sum(circ[i:i+3]==b'\0\0\0' for i in range(len(p)))==19024
            assert len({circ[i:i+10] for i in range(len(p))})==1023
            break
        p=old.rotate_image(2,p)
        assert (p.count(0),p.count(1))==(2*b,a+2*b)
    print('line 10: coordinate 15 has 19024 AAA rotations out of',len(p))


if __name__=='__main__':
    digest=sha256((Path(__file__).with_name('BB2x5_Rocq_holdouts_37.txt')).read_bytes()).hexdigest()
    assert digest=='89ea92fd4643166b92fca4ae80e37a699ab8615ac1dd375dae777e6b3e45ecc6'
    audit2()
    check_orders()
    audit26()
    old.audit17()
    audit17()
    check_extensions()
    audit10()
