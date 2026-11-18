"""Reproduce the finite BB(2,5) continuation checks with Python 3.10+."""
from collections import deque
from functools import lru_cache
from itertools import product
from pathlib import Path

from prior_sweeps import TapeMachine, PARITY, direct_epoch, word_sweep, parse

MIX = "1RB---0RB0LA2RA_2LB2LA3RA4LB0LB"
LEFT_RB = "1RB2RA3LA4LA2RB_2LA3RB---0RA1LA"
LEFT_RA = "1RB2RA3LA4LA2RB_2LA3RA---0RA1LA"
TRIPLE = "1RB4RB4RA1LA3LA_1LB2LA3RB2RB---"
P = "ABABBAAB"


def canonical(xval, d, pad, value=0):
    assert xval >= 1 and 0 <= value < 3**d and pad in (0, 1)
    left = [1, 3] + [2+int(c) for c in bin(xval)[3:]]
    word = left + [2]
    for _ in range(d):
        value, digit = divmod(value, 3)
        word += [(2, 0, 4)[digit], 2]
    return TapeMachine(MIX, word + [2]*pad, head=len(left))


def decode(m):
    t = m.tape
    x = m.head
    if m.state != 'A' or t.get(x) != 2:
        return None
    l, r = min(t), max(t)
    if x < l+2 or t[l] != 1 or t.get(l+1) != 3:
        return None
    X = 1
    for j in range(l+2, x):
        if t.get(j) not in (2, 3):
            return None
        X = 2*X + (t[j] == 3)
    d, pad = divmod(r-x, 2)
    if pad and t[r] != 2:
        return None
    v = 0
    for j in reversed(range(d)):
        a = t.get(x+2*j+1, 0)
        if a not in (0, 2, 4) or t.get(x+2*j+2) != 2:
            return None
        v = 3*v + {2:0, 0:1, 4:2}[a]
    return X, d, pad, v


def tokens(m):
    x = m.head
    t = m.tape
    out = []
    while True:
        if t.get(x) == 4:
            out.append((x, None))
            x += 1
        elif t.get(x) == 2 and t.get(x+1, 0) in (0, 2, 4):
            out.append((x, {2:0, 0:1, 4:2}[t.get(x+1, 0)]))
            x += 2
        else:
            return out


def skip(m, cap=None, *, exact=False):
    """Apply successful probes. Return their number, or their raw cost if exact."""
    t, x = m.tape, m.head
    if m.state != 'A' or t.get(x) not in (2, 4):
        return 0
    j = x-1
    value, power = 0, 1
    while t.get(j) in (2, 3):
        if t[j] == 3:
            value += power
        power *= 2
        j -= 1
    full = j == min(t) and t[j] == 1 and j+1 < x and t.get(j+1) == 3
    if full:
        power //= 2
        value -= power
    elif value == power-1:
        return 0
    ts = tokens(m)
    n = 0
    for _, digit in reversed(ts):
        n = n//2 if digit is None else 3*n+digit
    if not full:
        n = min(n, power-1-value)
    if cap is not None:
        n = min(n, cap)
    if n == 0:
        return 0
    # Incrementing z costs 1+2*v2(z+1), plus two steps when the
    # left marker grows. Sum v2 over the interval using binary popcounts.
    if exact:
        z = power+value if full else value
        cost = 3*n + 2*(z.bit_count() - (z+n).bit_count())
        if full:
            cost += 2*((z+n).bit_length() - z.bit_length())
    calls = n
    for j0, digit in ts:
        if exact:
            cost += 3*calls
        if digit is None:
            calls *= 2
            continue
        new = (2, 0, 4)[(digit-calls) % 3]
        calls = (calls+2-digit)//3
        if exact:
            cost += calls  # one extra local instruction on each pair underflow
        if new:
            t[j0+1] = new
        else:
            t.pop(j0+1, None)
    assert calls == 0
    if full:
        word = [1, 3] + [2+int(ch) for ch in bin(power+value+n)[3:]]
        for i, a in enumerate(word, x-len(word)):
            t[i] = a
    else:
        for i in range(power.bit_length()-1):
            t[x-1-i] = 2 + (((value+n) >> i) & 1)
    return cost if exact else n


def next_zero(m, limit=120000, *, exact=False):
    elapsed = 0
    for work in range(1, limit+1):
        count = skip(m, exact=exact)
        if count:
            elapsed += count
        else:
            if not m.step():
                return None, elapsed, work
            elapsed += 1
        c = decode(m)
        if c and c[-1] == 0:
            return c, elapsed, work
    raise RuntimeError("work limit in next_zero")


def exact_target(m, target, limit):
    for n in range(limit+1):
        if decode(m) == target:
            return n
        if n == limit or not m.step():
            break
    raise AssertionError(target)


def check_mixed():
    m = TapeMachine(MIX)
    for k in range(59171):
        assert m.step()
    assert decode(m) == (6947, 8, 1, 0)
    assert exact_target(m, (217, 12, 1, 531433), 113) == 113
    print('Direct blank trajectory at steps 59171 and 59284 verified.')
    for d in range(4):
        for w in (1, 2, 3, 7, 8, 15):
            m = canonical(32*w+3, d, 1)
            exact_target(m, (w,d+4,1,3**(d+4)-8), 1500)
            m = canonical(16*w-5, d, 1)
            u = 9*(3**(d+1)-1)//2
            exact_target(m, (w+u+1,d+5,1,3**(d+5)-1), 100000)
        for n in range(2, 9):
            for X in (2**n-1, 2**(n+3)-13, 2**(n+4)-25):
                m = canonical(X, d, 1)
                for _ in range(1000):
                    if not m.step():
                        break
                else:
                    raise AssertionError((d,X))
                assert (m.state, m.tape[m.head]) == ('A',1)
    for d in range(4):
        for y in (1,2,3,7,8,15):
            m = canonical(16*y+7,d,1)
            expected = [1,3] + [2+int(ch) for ch in bin(y+1)[3:]]
            target = expected + [2]*(2*(d+2)+4)
            for _ in range(300):
                l = min(m.tape)
                if (m.state == 'A' and m.head == l+len(expected)-1 and
                    len(m.tape) == len(target) and
                    all(m.tape.get(l+j) == a for j,a in enumerate(target))):
                    break
                assert m.step()
            else:
                raise AssertionError((d,y))
    print('24 three-trailing-one reductions verified on the concrete tape.')
    print('48 concrete reset transitions and 84 halting auxiliary inputs verified.')
    # Check mixed-word macros by meeting their predicted result on the literal tape.
    from random import Random
    rng = Random(20261103)
    tested = 0
    for _ in range(750):
        X = rng.randrange(1, 32)
        a = canonical(X, 0, 0)
        x = a.head
        for j in range(rng.randrange(1, 14)):
            digit = rng.choice((0, 2, 4))
            if digit:
                a.tape[x+j+1] = digit
        b = canonical(X, 0, 0)
        b.tape = a.tape.copy()
        count = skip(a, cap=32)
        if count:
            for _ in range(5000):
                assert b.step()
                if b.head == x and b.state == 'A' and b.tape == a.tape:
                    break
            else:
                raise AssertionError((X,count))
            tested += 1
    print(f'{tested} independent mixed-word jumps compared to elementary execution.')
    m = TapeMachine(MIX)
    for _ in range(5):
        assert m.step()
    assert decode(m) == (1,0,0,0)
    low = 5
    moves = 0
    checkpoints = 0
    while low <= 10**150:
        c,n,work = next_zero(m)
        assert c is not None
        low += n
        moves += work
        checkpoints += 1
    print(f'Blank execution exceeds 10^150 transitions. Macro or single-step operations {moves}.')
    print(f'Checkpoints {checkpoints}. Final (X,d,p,v) = {c}.')
    print(f'Certified-by-macro lower bound as an integer: {low}')


def cross_block(rules, w, state, side):
    """Enter a finite block on its left (L) or right (R). Stop upon exit or halt."""
    w = list(w)
    x = 0 if side == 'L' else len(w)-1
    seen = set()
    while 0 <= x < len(w):
        key = tuple(w), x, state
        assert key not in seen
        seen.add(key)
        a = rules.get((state,w[x]))
        if a is None:
            return ('H',state,tuple(w))
        w[x],delta,state = a
        x += delta
    return ('L' if x < 0 else 'R',state,tuple(w))


def left_period(enc, period, cycle, width=1, prefix="", entry="A"):
    def cursor(j):
        return j if j < len(prefix) else len(prefix)+(j-len(prefix))%len(period)
    def letter(j):
        return (prefix+period)[cursor(j)]
    rules = parse(enc)
    p, n = cycle
    w = (0,)*width
    used = 0
    seen = {}
    for j in range(p+n+1):
        key = w,cursor(j),cursor(used)
        if j == p+n:
            assert seen[key] == (p,used-n)
            break
        assert key not in seen
        seen[key] = (j,used)
        side,s,w = cross_block(rules,w,entry,'R')
        while side == 'L':
            assert s == entry and used < j
            side,s,w = cross_block(rules,w,letter(used),'L')
            used += 1
        assert side == 'R' and s == letter(j)


@lru_cache(None)
def cell(enc, w, q):
    rules = parse(enc)
    side,q,w = cross_block(rules,w,q,'L')
    out = ''
    seen = set()
    while side == 'R':
        assert (q,w) not in seen
        seen.add((q,w))
        out += q
        side,q,w = cross_block(rules,w,'A','R')
    if side == 'H':
        return 'halt',out
    if q != 'A':
        return 'other return',out
    return w,out


def feed(enc, s, word):
    out = []
    for a in word:
        s,v = cell(enc,s,a)
        out.append(v)
        if isinstance(s,str):
            break
    return s,''.join(out)


def single_output(start,b):
    queue = deque([(start,'')])
    visited = {start}
    while queue:
        s,w = queue.popleft()
        for a in 'AB':
            v,out = cell(TRIPLE,s,a)
            if out == b:
                return w+a,v
            if not out and v not in visited:
                visited.add(v)
                queue.append((v,w+a))
    raise AssertionError((start,b))


def check_columns():
    for enc in (LEFT_RB,LEFT_RA):
        left_period(enc,'BAABABABAAABA',(2,13))
        terminal = 'B' if enc == LEFT_RB else 'A'
        table = {
            0: ((3,'BA'),(2,'')), 2: ((3,''),('halt','')),
            3: ((4,''),(3,'ABA')), 4: ((3,'B'),(1,'')),
            1: ((3,'A'),(4,terminal))
        }
        for t,row in table.items():
            for a,(v,out) in zip('AB',row):
                assert cell(enc,(t,),a) == ((v,) if isinstance(v,int) else v,out)
        w = 'A' + 'BAABABABAAABA'*20
        # Test a closed strip under an A-returning right boundary, entry by entry.
        for width in (1,2,3,5):
            expected = w
            for _ in range(width):
                s,expected = feed(enc,(0,),expected)
                assert not isinstance(s,str)
            s,actual = feed(enc,(0,)*width,w)
            assert not isinstance(s,str) and actual == expected
    left_period(TRIPLE,'BBBABABAABABBA',(2,14))
    assert cell(TRIPLE,(0,0,0),'A') == ((2,1,0),'')
    assert cell(TRIPLE,(2,1,0),'A') == ('halt','')
    assert cell(TRIPLE,(2,1,0),'B') == ((1,2,0),'')
    assert cell(TRIPLE,(1,2,0),'A') == ((3,3,3),'A')
    steady = (3,1,3)
    assert feed(TRIPLE,(0,0,0),P) == (steady,P[:7])
    assert feed(TRIPLE,steady,P) == (steady,'B'+P[:7])
    states = set(product((1,2,3), repeat=3))
    lengths = []
    for s in states:
        for a in 'AB':
            assert cell(TRIPLE,s,a)[0] in states
            w,v = single_output(s,a)
            assert v in states and feed(TRIPLE,s,w) == (v,a)
            lengths.append(len(w))
    assert max(lengths) == 8
    # Each proper prefix of a period, including the transient from blank.
    for n in range(1,33):
        inp = (P*5)[:n]
        s,out = feed(TRIPLE,(0,0,0),inp)
        assert out == inp[:len(out)] and len(out)<n
        if n>=3:
            assert s in states
    src='A'+'BBBABABAABABBA'*40
    assert feed(TRIPLE,(0,0,0),src)[1].startswith('ABAABAAA')
    print('Two cell tables, periodic 3-cell driver and 54 control words verified.')


def check_parity():
    word = [int(c) for c in '1211112']
    m = TapeMachine(PARITY, word, left=1)
    vals = []
    for _ in range(3):
        word,lo = word_sweep(word,PARITY)
        vals.append(lo)
        actual = direct_epoch(m,(1,2))
        assert actual == word
    assert vals == [0,-1,-6]
    assert (m.state,m.tape[m.head]) == ('B',4)
    print(f'Parity counterexample from 1211112 verified, {m.steps} defined steps before B4.')


if __name__ == '__main__':
    rows=Path(__file__).with_name('BB2x5_Rocq_holdouts_37.txt').read_text().splitlines()
    assert len(rows)==len(set(rows))==37
    for i,s in ((3,MIX),(12,TRIPLE),(21,LEFT_RB),(22,LEFT_RA),(36,PARITY)):
        assert rows[i-1]==s
    for line,pref,period,start,width,entry in [
        (8,'','BBABA',1,1,'A'), (11,'','BBBA',2,1,'A'),
        (12,'','BBBABABAABABBA',2,1,'A'), (13,'','BABAB',1,1,'A'),
        (15,'BBBA','BABAABBABBABAAAB',9,1,'A'), (20,'BAAAB','ABA',7,1,'A'),
        (21,'','BAABABABAAABA',2,1,'A'), (22,'','BAABABABAAABA',2,1,'A'),
        (26,'','BBAAAA',2,1,'A'), (31,'','ABAAA',1,2,'B')]:
        left_period(rows[line-1],period,(start,len(period)),width,pref,entry)
    print('Ten infinite blank left-half response streams checked by finite return certificates.')
    check_columns()
    check_parity()
    check_mixed()
