"""Line 26: first dangerous carry, a scalar fixed-point criterion, and width certificates."""
from collections import Counter
from itertools import product

from prior_frontier import LIST
from prior_sweeps import COUNTER, column_token, feed_columns
from verify import arithmetic26


def transfer(state, word):
    emitted = []
    for token in word:
        state, child = column_token(state,token)
        if child:
            emitted.append(child)
    return state,''.join(emitted)


def ordinary_period(word):
    state = initial = (1,0)
    emitted = []
    for h in range(1,5):
        state, out = transfer(state,word)
        emitted.append(out)
        if state == initial:
            return h,''.join(emitted)
    raise AssertionError('ordinary period failed to close')


def first_d_count(word):
    gap = word[:word.index('d')]
    return gap.count('a') + (gap.count('b')+1)//2


def discrepancy(word):
    height = low = high = 0
    for c in word:
        height += 6 if c == 'd' else -1
        low = min(low,height)
        high = max(high,height)
    assert height == 0
    return high-low


def floors(stop):
    """Sum floor(j/6) over 0 <= j < stop."""
    q,r = divmod(stop,6)
    return 3*q*(q-1) + q*r


def phase_bound(word, phase, u):
    """Sum the number of dangerous tokens before each of the next u+1 safe ones."""
    rotated = word[phase:] + word[:phase]
    dangers = 0
    counts = []
    for c in rotated:
        if c == 'd':
            dangers += 1
        else:
            counts.append(dangers)
    q,r = divmod(u+1,len(counts))
    return (q*sum(counts) + len(counts)*dangers*q*(q-1)//2
            + sum(counts[:r]) + r*q*dangers)


def cut_lengths(cycles, periods, repetitions):
    """Exact number of virtual arrivals at each cut following complete root cycles."""
    counts = [4*cycles]
    for k,h in enumerate(repetitions):
        lap, rem = divmod(counts[-1],h*len(periods[k]))
        _, tail = transfer((1,0),(periods[k]*h)[:rem])
        counts.append(lap*len(periods[k+1])+len(tail))
    return counts


def audit_discrepancy():
    # Cross-check the extent of every cyclic interval over one period, and the
    # prefix-sum gain formula against processing the next safe tokens individually.
    for word in ('aaabbbd','aadbdbabaaaabb'):
        if word.count('d')*7 != len(word):
            continue
        c = discrepancy(word)
        for phase in range(len(word)):
            p = s = d = 0
            w = word[phase:] + word[:phase]
            records = []
            for token in w*7:
                if token=='d':
                    d += 1
                else:
                    s += 1
                    records.append(d)
                p = max(p,6*d-s)
            assert p <= c
            for u in range(len(records)):
                actual = sum(records[:u+1])
                assert phase_bound(word,phase,u) == actual
                assert actual <= floors(c+u+1)-floors(c)

    # Compare the high-bit update independent of the root word.
    for width in range(4):
        for pairs in product(product(range(2),repeat=2),repeat=width):
            u = sum((1-o)<<i for i,(o,_) in enumerate(pairs))
            e = sum(v<<i for i,(_,v) in enumerate(pairs))
            for token in 'abd':
                cols = list(pairs)
                live = feed_columns(cols,token)
                if token == 'd':
                    stop = (~(u|e)) & ((u|e)+1)
                    after = e ^ (~u & (2*stop-1))
                    assert 1 <= after-e <= u+1
                    assert live == (after < 1<<width)
                elif len(cols)==width:
                    after_u = sum((1-o)<<i for i,(o,_) in enumerate(cols))
                    assert 0 <= after_u < u
                else:
                    assert live and len(cols)==width+1


def audit_orbit():
    assert LIST[25] == COUNTER == '1RB2RB4LA2RA1LA_2LA4RA3LA---3RA'
    periods = ['aadd']
    repetitions = []
    for k in range(12):
        h,word = ordinary_period(periods[-1])
        repetitions.append(h)
        periods.append(word)
        if k >= 3:
            scale = 3**(k-2)
            assert h==4 and Counter(word)=={'a':3*scale,'b':3*scale,'d':scale}
    ps = list(map(first_d_count,periods))
    assert ps == [2,2,3,5,5,9,9,10,10,12,17,17,18]
    print('first-danger counts p(0) through p(12):',ps)
    cs = {k:discrepancy(periods[k]) for k in range(3,10)}
    print('cyclic discrepancy, cuts 3 through 9:',list(cs.values()))
    u = e = m = 0
    first_d = []
    records = []
    square_misses = uniform_recovers = 0
    width_changes = 0
    for cycles in range(1,131073):
        previous_width = m
        for c in 'aadd':
            if c == 'd':
                stop = (~(u|e)) & ((u|e)+1)
                highest = stop.bit_length()-1
                if highest >= len(first_d):
                    first_d.extend([m]*(highest+1-len(first_d)))
            u,e,m = arithmetic26(u,e,m,c)
            assert e < 1<<m
        if m == previous_width:
            continue
        width_changes += 1
        old_ok = 2*(e//2+(u//4)**2) < 1<<m
        if old_ok:
            continue
        square_misses += 1
        any_bound = any(((e>>k) + floors((u>>k)+c+1)-floors(c) < 1<<(m-k))
                        for k,c in cs.items() if k<=m)
        if any_bound:
            uniform_recovers += 1
        else:
            counts = cut_lengths(cycles,periods[:10],repetitions[:9])
            options = []
            for k in range(3,min(9,m)+1):
                phase = counts[k] % len(periods[k])
                high_e = (e>>k)+phase_bound(periods[k],phase,u>>k)
                if high_e < 1<<(m-k):
                    options.append((k,phase,high_e))
            records.append((cycles,u,e,m,options))
    assert first_d[:len(ps)] == ps
    assert all(v>k for k,v in enumerate(first_d))
    chain=[0]
    while chain[-1]<len(first_d):
        chain.append(first_d[chain[-1]])
    print('ordinary p evaluated at every cut subsequently reached by a d:',first_d)
    print('iteration of p starting at zero through this sample:',chain)
    print(f'{width_changes} cycles increased width; the square bound missed {square_misses}.')
    print(f'Phase-independent period bounds recover {uniform_recovers} of those misses.')
    print('remaining checkpoint and (cut, phase, high E bound):',records)
    assert width_changes == 73 and square_misses == 23 and uniform_recovers == 22
    assert len(records)==1 and records[0][0]==17 and records[0][-1]


if __name__ == '__main__':
    audit_discrepancy()
    audit_orbit()
