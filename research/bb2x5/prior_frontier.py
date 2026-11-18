"""Finite audits for the BB(2,5) research notes dated 18 November 2026."""
from collections import deque
from functools import cache
from itertools import product
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent
LIST = (ROOT / 'BB2x5_Rocq_holdouts_37.txt').read_text().splitlines()
M10 = '1RB2RB3LA4LA1LA_2LB3RA---4RA1RB'
M17 = '1RB2RA3LB---2LB_2LA0LA4RB0RB1LA'
M22 = '1RB2RA3LA4LA2RB_2LA3RA---0RA1LA'
M26 = '1RB2RB4LA2RA1LA_2LA4RA3LA---3RA'
M31 = '1RB3RB---4RA2RA_2LA2RA3LB4LB1LB'
assert len(set(LIST)) == len(LIST) == 37
assert [LIST[j-1] for j in (10,17,22,26,31)] == [M10,M17,M22,M26,M31]


def parse(machine):
    rows = machine.split('_')
    assert len(rows) == 2
    table = []
    for row in rows:
        assert re.fullmatch(r'(?:(?:[0-4][LR][AB])|---){5}', row)
        ops = []
        for i in range(0, 15, 3):
            a, d, q = row[i:i+3]
            ops.append(None if a == '-' else (int(a), 1 if d == 'R' else -1, int(q == 'B')))
        table.append(tuple(ops))
    return tuple(table)


for line in LIST:
    assert sum(op is None for row in parse(line) for op in row) == 1
T17, T10 = parse(M17), parse(M10)
HEAD = '231302'
DATA = '220312221222' + '02' * 397 + '030202121212121303130222031302221302122212'


def digits(word):
    assert len(word) % 2 == 0
    assert all(a in '102' and b in '23' for a,b in zip(word[::2],word[1::2]))
    return tuple(('102'.index(a), int(b == '3')) for a,b in zip(word[::2],word[1::2]))


def blank17():
    tape = {}
    x = state = right = 0
    for step in range(2308941):
        if step in (252, 2889, 2308940):
            assert state == 0 and min(tape) > x
            row = ''.join(str(tape.get(u,0)) for u in range(x+1,max(tape)+1))
            assert row.startswith(HEAD) and row.endswith('2')
            count = len(digits(row[len(HEAD):-1]))
            assert count == {252:7, 2889:20, 2308940:424}[step]
            print('line 17 blank checkpoint', step, 'head', x, 'digits', count, 'rightmost visited', right)
            if step in (252,2889):
                assert normal_epochs(digits(row[len(HEAD):-1])) == (9 if step==252 else 400)
            if step == 2308940:
                assert row == HEAD + DATA + '2' and (x,right) == (-844,11)
                return
        write, delta, state = T17[state][tape.get(x,0)]
        if write:
            tape[x] = write
        else:
            tape.pop(x, None)
        x += delta
        right = max(right, x)


def pair_trace(word, initial):
    """Enumerate complete two-cell traces. Lower-case b/a return A, X returns B."""
    results = set()
    tasks = [(list(map(int,word)), 0, initial, '')]
    while tasks:
        tape, x, state, trace = tasks.pop()
        for _ in range(80):
            if x < 0:
                results.add((trace, 'L'+'AB'[state]+''.join(map(str,tape))))
                break
            if x == len(tape):
                returns = [(0,'b')] if state else [(0,'a'),(1,'X')]
                for back,label in returns:
                    tasks.append((tape.copy(), x-1, back, trace+label))
                break
            op = T17[state][tape[x]]
            if op is None:
                results.add((trace, 'H'+'AB'[state]+''.join(map(str,tape))))
                break
            tape[x], delta, state = op
            x += delta
        else:
            raise AssertionError('unfinished local trace')
    return results


PAIR = {
    '02': ('b/LA02', '/LA22'),
    '12': ('bba/LA13 bbXb/LA12', '/LA02'),
    '22': ('/LB32','b/LA12'),
    '03': ('bba/LA03 bbXb/LA02','/LA23'),
    '13': ('/HA23','/LA03'),
    '23': ('/LB33','bba/LA13 bbXb/LA12'),
    '32': ('/HA32','b/LA22'),
    '33': ('/HA33','bba/LA23 bbXb/LA22'),
    '2': ('/LB3','b/LB2')}


def header17(stop_at):
    """Run the literal header, supplying A to B probes and B to the selected A probe."""
    tape = {i:int(a) for i,a in enumerate(HEAD,1)}
    x = state = acount = 0
    sent = ''
    for moves in range(200):
        if x == 7:
            sent += 'AB'[state]
            if state == 0:
                acount += 1
                state = int(acount == stop_at)
            else:
                state = 0
            x -= 1
        if x < 0 and state == 0 and tape.get(x,0) == 0:
            assert x == -2 and ''.join(str(tape.get(j,0)) for j in range(x+1,7)) == HEAD+'12'
            return moves,sent
        a,delta,state = T17[state][tape.get(x,0)]
        tape[x] = a
        x += delta
    raise AssertionError('header did not finish')


def mark_step(v, pending, bit):
    assert not (pending and bit)
    if pending or bit:
        return (v+2)%3, int(v != 0), ((0,),(0,1),(0,0))[v]
    return (v+1)%3, 0, (0,) if v == 2 else ()


def normal_epochs(data):
    state=[(v,data[i-1][1] if i else 0) for i,(v,f) in enumerate(data)]
    def reaches_edge(i,bit):
        if i == len(data):
            return True
        v,p,out = mark_step(*state[i],bit)
        state[i] = v,p
        return any(reaches_edge(i+1,next_bit) for next_bit in out)
    for epoch in range(1000):
        if any(reaches_edge(0,bit) for bit in (0,1,0,0)):
            return epoch
    raise AssertionError('small checkpoint failed to reach its terminal')


def artificial17(first_trit):
    row=HEAD+'102'[first_trit]+'2'+'12'*3+'2'
    tape={i:int(a) for i,a in enumerate(row,1) if a!='0'}
    right=max(tape)
    x=state=0
    extension=None
    for n in range(2000):
        if x>right and extension is None:
            assert state==1
            extension=n
        if extension is not None and state==0 and x<min(tape):
            w=''.join(str(tape.get(i,0)) for i in range(x+1,max(tape)+1))
            if w.startswith(HEAD) and w.endswith('2') and len(w[len(HEAD):-1])%2==0:
                try:
                    digits(w[len(HEAD):-1])
                except AssertionError:
                    pass
                else:
                    return 'header',n,extension
        op=T17[state][tape.get(x,0)]
        if op is None:
            return 'halt',n,extension
        a,dx,state=op
        if a:
            tape[x]=a
        else:
            tape.pop(x,None)
        x+=dx
    raise AssertionError('example unfinished')


def check_second_marks(data):
    second = True  # Source 0100 has a mark on slot two.
    pending = False
    tested = []
    for i,(v,f) in enumerate(data):
        if pending:
            tested.append((i,v))
            assert v <= 1 and not (v == 1 and second)
        second = (v == 1) if pending else (v == 0 and second)
        pending = bool(f)
    assert tested == [(2,0),(404,1),(411,1),(412,0),(413,1),(416,0),(417,1),(420,1)]
    print('line 17 initially pending inputs', tested)


def marks_on_word(state,word):
    v,p=state
    out=bytearray()
    for bit in word:
        v,p,emitted=mark_step(v,p,bit)
        out.extend(emitted)
    return (v,p),bytes(out)


def periodic_marks(state,prefix,period):
    state,head=marks_on_word(state,prefix)
    seen={}
    out=bytearray()
    while state not in seen:
        seen[state]=len(out)
        state,w=marks_on_word(state,period)
        out.extend(w)
    cut=seen[state]
    head+=bytes(out[:cut])
    tail=bytes(out[cut:])
    assert tail
    length=(tail+tail).find(tail,1)
    tail=tail[:length]
    n=0
    while n<len(head) and head[-1-n]==tail[(-1-n)%len(tail)]:
        n+=1
    if n:
        shift=(-n)%len(tail)
        head=head[:-n]
        tail=tail[shift:]+tail[:shift]
    return head,tail


def locked_marks(data):
    head,cycle=b'',bytes([0,1,0,0])
    for i in range(53):
        state=(data[i][0],data[i-1][1] if i else 0)
        head,cycle=periodic_marks(state,head,cycle)
    assert not head and len(cycle)==147740
    wanted=[5,11,17,23]
    assert [j for j,bit in enumerate(cycle[:25],1) if bit]==wanted
    _,out=marks_on_word((1,0),cycle[:25])
    assert [j for j,bit in enumerate(out[:23],1) if bit]==wanted
    assert all(data[i]==(1,0) for i in range(53,403))
    print('line 17 first four marked slots at every cut from 53 to 403:',wanted)


def force_prefix(v, pending, known, target):
    """All valid continuations respecting start spacing and the known input prefix."""
    frontier = [(v,pending,0,0,0)]
    seen = set(frontier)
    while frontier:
        v,p,cool,i,j = frontier.pop()
        if j >= len(target):
            continue
        alphabet = (known[i],) if i < len(known) else (0,1)
        for bit in alphabet:
            if bit and (p or cool):
                continue
            w,p2,out = mark_step(v,p,bit)
            n = min(len(out), len(target)-j)
            assert out[:n] == target[j:j+n]
            key = (w,p2,2 if bit else max(0,cool-1),min(i+1,len(known)),j+n)
            if key not in seen:
                seen.add(key)
                frontier.append(key)
    # Every three valid input slots emit a slot, so termination of a live branch
    # always means that the specified output prefix has been emitted.


def pulse_on_tail(row, special):
    """Concrete TM on a finite suffix, stopping at its first right extension."""
    tape = list(map(int,row))
    requests = [1,1,0] if special else [1]
    for index, entering in enumerate(requests):
        x = 0
        state = entering
        for _ in range(10000):
            if x == len(tape):
                assert state == 1
                return True, ''.join(map(str,tape))
            if x < 0:
                break
            op = T17[state][tape[x]]
            assert op is not None
            tape[x], delta, state = op
            x += delta
        else:
            raise AssertionError('unfinished raw request')
        if entering:
            assert state == 0
        elif state:
            assert index == 2
            requests.append(1)
    return False, ''.join(map(str,tape))


def right_events(data, prefix):
    start = (DATA[2*418:]+'2', data[417][1], 0, 0)
    frontier, seen, events = [start], {start}, set()
    while frontier:
        row,p,cool,i = frontier.pop()
        v = '102'.index(row[0])
        alphabet = (prefix[i],) if i<len(prefix) else (0,1)
        for a in alphabet:
            if a and (p or cool):
                continue
            special = bool(a or p)
            edge,new = pulse_on_tail(row,special)
            if edge:
                events.add(new)
                continue
            digits(new[:-1])
            assert new[-1] == '2'
            key = (new,int(special and v!=0),2 if a else max(0,cool-1),min(i+1,len(prefix)))
            if key not in seen:
                seen.add(key)
                frontier.append(key)
    return events


def walk_right_piece(word, head, state):
    tape = {i:int(a) for i,a in enumerate(word)}
    x = head
    for n in range(1000):
        if x < 0:
            return n,state,''.join(str(tape.get(j,0)) for j in range(max(tape)+1))
        op = T17[state][tape.get(x,0)]
        assert op is not None
        a,delta,state = op
        tape[x] = a
        x += delta
    raise AssertionError('unterminated right boundary trace')


def audit17():
    blank17()
    assert artificial17(0)==('header',225,64) and artificial17(1)==('halt',1477,748)
    for w,row in PAIR.items():
        for state,traces in enumerate(row):
            assert pair_trace(w,state) == {tuple(t.split('/')) for t in traces.split()}
    assert [header17(j) for j in (1,2,3)] == [(65,'BBBABBB'),(67,'BBBABBABB'),(69,'BBBABBABBAB')]
    data = digits(DATA)
    check_second_marks(data)
    locked_marks(data)
    prefixes = ['0','01000','00001000','010001000','0000001000','0001000','0001000','01000000']
    prefixes = [tuple(map(int,w)) for w in prefixes]
    for i,(src,dst) in enumerate(zip(prefixes,prefixes[1:]),411):
        force_prefix(data[i][0],data[i-1][1],src,dst)
    events = right_events(data,prefixes[-1])
    assert events == {s+'444040444444' for s in '014'}
    assert walk_right_piece('444040444444',12,1) == (55,0,'1213031302222')
    returns = [walk_right_piece(a+'1213031302222',0,0) for a in '014']
    assert returns == [(9,1,'30203031302222'),(71,0,'120222022202122'),(1,1,'21213031302222')]
    print('line 17 first-edge words in cells -1 through 11', sorted(events))
    print('line 17 return 55 steps later: A at -1, cells 0 through 12 = 1213031302222')


def audit22_semantics():
    table=parse(M22)
    period='BAABABABAAABA'
    cell=used=0
    snapshots=[]
    for j in range(1,16):
        state=0
        while True:
            cell,delta,state=table[state][cell]
            if delta==1:
                break
            assert state==0
            state=int(period[used%13]=='B')
            used+=1
            assert used<j
        assert 'AB'[state]==period[(j-1)%13]
        snapshots.append((cell,used))
    assert snapshots[1][0]==snapshots[14][0] and snapshots[14][1]-snapshots[1][1]==13
    results={}
    for start in range(5):
        for q in (0,1):
            cell,state,out=start,q,''
            while True:
                op=table[state][cell]
                if op is None:
                    results[start,q]=None
                    break
                cell,delta,state=op
                if delta<0:
                    assert state==0
                    results[start,q]=(cell,out)
                    break
                out+='AB'[state]
                state=0
    expected=[((3,'BA'),(2,'')),((3,'A'),(4,'A')),((3,''),None),((4,''),(3,'ABA')),((3,'B'),(1,''))]
    assert all(results[i,q]==expected[i][q] for i in range(5) for q in (0,1))


def left10():
    seq = 'BBA'+'AB'*16
    cell = used = 0
    trace = []
    for j in range(1,9):
        q = 0
        while True:
            cell,delta,q = T10[q][cell]
            if delta == 1:
                break
            assert q == 0
            q = int(seq[used]=='B')
            used += 1
            assert used < j
        assert 'AB'[q] == seq[j-1]
        trace.append((cell,used))
    assert trace == [(1,0),(2,0),(4,1),(3,2),(2,4),(4,5),(2,6),(4,7)]


def interior10(s, word):
    out = bytearray()
    for a in word:
        if a == 0:
            if s == 0:
                out.append(1)
            s = (s+1)%3
        else:
            out.extend(b'\1\1' if s == 2 else b'\0')
            s = (s+2)%3
    return s,bytes(out)


def rotate_image(s,word):
    start = s
    blocks = []
    for _ in range(3):
        s,out = interior10(s,word)
        blocks.append(out)
        if s == start:
            return b''.join(blocks)
    raise AssertionError('phase failed to return')


def trim_period(q):
    for prime in (2,3):
        while len(q)%prime==0 and q[:len(q)//prime]*prime==q:
            q=q[:len(q)//prime]
    return q


def seed10():
    # BBAB^omega, under its first frontier passage, gives (BAA)^omega.
    # After the first B the old digit 1 receives B A B^omega.
    # Evaluate the finite prefix and the state-return period independently.
    # The input from the left half to old cell 0 is BBA(AB)^omega.
    s,p = interior10(2,bytes([1,1,0]));z,q = interior10(s,bytes([0,1]))
    assert z == s and p==bytes([1,1,0,1]) and q==bytes([1,1])
    # At the next frontier the finite prefix after the first B is BA.
    s,p = interior10(0,bytes([1,0]));q=rotate_image(s,bytes([1]))
    s,p = interior10(2,p);q=rotate_image(s,q)
    assert (p+q*4) == (bytes([1,0,0])*((len(p)+4*len(q)+2)//3))[:len(p)+4*len(q)]
    assert len(q)%3==0
    pos,q = 3,bytes([1,0,0])
    while pos < 13:
        t = (q*3).index(1)
        assert t<3
        n=(t+1)%len(q)
        q=q[n:]+q[:n]
        if t!=1:
            q=rotate_image(0 if t==0 else 2,q)
        q=trim_period(rotate_image(2,q))
        pos += 1 if t==1 else 2
    assert pos==13 and len(q)==54816
    return q


def audit10():
    left10()
    # Compare the states at new rightmost coordinates against the elementary TM.
    actual = []
    tape = {}
    head = state = furthest = 0
    while furthest < 27:
        write,delta,state = T10[state][tape.get(head,0)]
        tape[head] = write
        head += delta
        if head > furthest:
            actual.append(state)
            furthest = head
    expected = [1]
    sample = bytes([1,1,0]) + bytes([1])*1500
    while len(expected)<27:
        t = sample[:3].index(1)
        expected += [1] if t == 1 else [0,1]
        sample = sample[t+1:]
        if t!=1:
            _,sample = interior10(0 if t==0 else 2,sample)
        _,sample = interior10(2,sample)
    assert expected[:27] == actual
    # A different supplied input with the same all-B tail does halt.
    sample = bytes([1])*4 + bytes([0]) + bytes([1])*1450
    alternative_edge = 1
    while sample[:3] != bytes([0,0,0]):
        t = sample[:3].index(1)
        sample = sample[t+1:]
        if t!=1:
            _,sample = interior10(0 if t==0 else 2,sample)
        _,sample = interior10(2,sample)
        alternative_edge += 1 if t==1 else 2
    assert alternative_edge == 49
    q=seed10()
    w=q*(2500000//len(q))
    x=13
    while len(w)>=3:
        t=w[:3].find(b'\1')
        assert t>=0,('line 10 frontier halt',x)
        w=w[t+1:]
        if t!=1:
            _,w = interior10(0 if t==0 else 2,w)
        _,w = interior10(2,w)
        x += 1 if t==1 else 2
    assert x==150
    print('line 10 last established edge in the Python prefix audit',x)


def audit26():
    def column(w):
        o,e=1,0
        out=[]
        for a in w:
            if a=='d':
                if not o or e:
                    out.append('d')
                e ^= o
            else:
                if a=='a' or o:
                    out.append('ab'[e])
                o ^= a=='b'
        assert out[0]=='a'
        return ''.join(out[1:])
    for l in range(1,9):
        for w in map(''.join,product('ab',repeat=l)):
            b=w.count('b')
            r=w.count('a')+(b+1)//2-1
            out=column(w+'dd')
            assert out.startswith('a'*r+'d') and out.count('d') == (2 if b%2 else 1)
    w='aadd'*65000
    count=0
    while w:
        assert w[0]!='d'
        w=column(w)
        count+=1
    assert count==71
    print('line 26 nonempty finite input prefixes, columns 0 through 70')


def audit31():
    # Here A and B are interchanged for comparison to the right edge on line 10.
    def image(phase,w):
        out=bytearray()
        for bit in w:
            if bit:
                out.append(int(phase!=0))
                phase=(phase-1)%3
            else:
                if phase==0:
                    out.append(1)
                phase=(phase+1)%3
        return bytes(out)
    # Verify the negative-half stream on a two-cell block in the original states.
    table=parse(M31)
    tape=[0,0]
    used=0
    source=(0,1,0,0,0)
    snapshots=[]
    for n in range(6):
        x,state=1,1
        for _ in range(200):
            tape[x],delta,state=table[state][tape[x]]
            x+=delta
            if x==2:
                break
            if x<0:
                assert state==1 and used<n
                state=source[used%5]
                used+=1
                x=0
        else:
            raise AssertionError('left block unfinished')
        assert state==source[n%5]
        snapshots.append((tuple(tape),used))
    assert snapshots[0][0]==snapshots[5][0] and snapshots[5][1]-snapshots[0][1]==5
    w=image(2,bytes([1,0,1,1,1])*200000)
    x=1
    while w:
        t=w[:3].find(b'\1')
        if t<0 and len(w)<3:
            break
        assert t!=2
        n=3 if t<0 else t+1
        w=image(2,image(0 if t==0 else 1,w[n:]))
        x+=2
    assert x==59
    print('line 31 finite edge audit reached coordinate',x)


if __name__ == '__main__':
    if len(sys.argv)==2 and sys.argv[1]=='--period10':
        print(''.join('AB'[a] for a in seed10()))
    else:
        audit17()
        audit10()
        audit26()
        audit31()
        audit22_semantics()
        from pullback22 import verify as check22
        check22()
