"""Line 26. Scalar gap rules, the two infinite tails, and literal nonblank witnesses."""
from itertools import product

from column_frontier import ordinary_period
from prior_frontier import LIST, M26, parse


def lift(gaps):
    """Emit one full scalar period from four traversals of a cut >= 3."""
    u = e = pending = 0
    output = []
    for _ in range(4):
        for gap in gaps:
            pending += (2-e) * ((gap+1-u)//2)
            u ^= gap % 2
            if u or e:
                output.append(pending)
                pending = 0
            e ^= 1-u
    assert (u,e,pending) == (0,0,0)
    return output


def max_q_run(gaps):
    # Every period used here begins with a nonempty P gap, so no run straddles it.
    assert gaps and gaps[0] > 0
    run = largest = 0
    for gap in gaps:
        run = 1 if gap else run+1
        largest = max(largest,run)
    return largest


def p_step(u,e):
    """Signed or nonnegative counters. Return new u and the one-based stop depth.

    A zero depth denotes a pass through all columns (a positive-tail wrap).
    """
    mask = 2*e+1
    common = mask & u
    stop = common & -common
    return u ^ (mask & (2*stop-1)), stop.bit_length()


def q_step(u,e):
    """Zero depth here means a carry through the entire negative tail."""
    common = ~(u|e)
    stop = common & -common
    return e ^ (~u & (2*stop-1)), stop.bit_length()


def audit_periods():
    word = 'aadd'
    for _ in range(3):
        _,word = ordinary_period(word)
    assert word == 'aaabbbd'
    gaps = [9]
    maxima = []
    for cut in range(3,16):
        assert len(gaps) == 3**(cut-3) and sum(gaps) == 9*len(gaps)
        maxima.append(max_q_run(gaps))
        if cut <= 9:
            assert word.endswith('d')
            actual = [2*w.count('a')+w.count('b') for w in word[:-1].split('d')]
            assert actual == gaps
            _,word = ordinary_period(word)
        if cut < 15:
            gaps = lift(gaps)
    assert all(b <= a+(a+1)//2 for a,b in zip(maxima,maxima[1:]))
    assert maxima[-1] == 4
    bound = maxima[-1]
    for _ in range(15,78):
        bound += (bound+1)//2
    assert bound == 524409302061 and 3*bound < 2**41
    print('maximum consecutive Q, cuts 3..15:',maxima)
    print('upper bound at cut 78:',bound)
    for _ in range(78,84):
        bound += (bound+1)//2
    assert bound == 5973349706294 and 3*bound < 2**45
    epochs = 8*(54306954019-1)
    assert 5+2*epochs*(epochs+1) == 377503392604154203337765
    print('upper bound at cut 84:',bound,'first forced increase by cut',84+45)

    for k in range(1,7):
        mask = (1<<k)-1
        u = e = 0
        seen = set()
        passed_p = passed_q = 0
        for _ in range(4**k):
            assert (u,e) not in seen
            seen.add((u,e))
            # Process one tick on k columns and count its actual scalar output.
            incoming, danger = 9,1
            for i in range(k):
                a,b = (u>>i)&1,(e>>i)&1
                emitted = (2-b)*((incoming+1-a)//2)
                a ^= incoming & 1
                u ^= ((u>>i & 1) ^ a) << i
                passed = danger and (a or b)
                if danger and not a:
                    e ^= 1<<i
                incoming,danger = emitted,passed
            passed_p += incoming
            passed_q += danger
        assert (u,e) == (0,0) and len(seen) == 4**k
        assert (passed_p,passed_q) == (9*3**k,3**k)
    print('one cycle on all paired residues verified through 6 columns')


def audit_plateaux():
    checked = 0
    for g,r,s in product(range(12),range(1,12),range(12)):
        u = e = wraps = high = 0
        for _ in range(g):
            u,depth = p_step(u,e)
            wraps += depth == 0
        assert wraps == (g+1)//2
        for token in 'Q'*r+'P'+'Q'*s+'P':
            if token == 'P':
                u,depth = p_step(u,e)
                if depth == 0:
                    break
            else:
                e,depth = q_step(u,e)
                high = max(high,depth-1)
        assert high == ((2*r+s) if g % 2 else r).bit_length()-1
        checked += 1
    print('plateau formula checked on',checked,'gap triples')


def negative_tail(count):
    u = e = -1
    tick = depth = 0
    records = []
    while len(records) < count:
        tick += 1
        for _ in range(9):
            u,stop = p_step(u,e)
            assert u < 0 and stop > 0
            depth = max(depth,stop)
        e,stop = q_step(u,e)
        assert e < 0
        if stop == 0:
            records.append((tick,depth))
    return records


def check_short_suffix(k,spare,ticks):
    """Every assignment of the upper pairs must fail no later than tick `ticks`."""
    low = (1<<k)-1
    for high_u, high_e in product(range(1<<spare),repeat=2):
        u = low | (high_u<<k)
        e = low | (high_e<<k)
        for _ in range(ticks):
            for _ in range(9):
                u,depth = p_step(u,e)
                assert 0 < depth <= k
            e,depth = q_step(u,e)
            if depth > k+spare:
                break
        else:
            raise AssertionError('short suffix survived')


def check_zero_prefix_traps():
    # Read the actual eight-epoch output from the physical machine at each
    # checkpoint, then restart the same phase with the translated left guard.
    from column_tick import raw_tick, tick
    blank_three = raw_tick(raw_tick((2,1)))
    permuted = (0,1,0,2,3,3)
    assert blank_three == (3,3,2,1,0,0) and sorted(blank_three) == sorted(permuted)
    assert raw_tick(permuted) is None
    print('blank third word 332100 and its immediately halting permutation 010233')
    actual = (2,1)
    for _ in range(1,4096):
        actual = tick(actual)
    assert tuple(actual.count(i) for i in range(4)) == (43,7,3,6)
    # Compute the first Q through the low 43 zeros by individual P subtraction
    # at the root. No width truncation and no external calendar are needed.
    mask = (1<<43)-1
    u = e = g = time = 0
    while True:
        time += 1
        for _ in range(9):
            u,depth = p_step(u,e)
            if not depth or depth > 43:
                # At the final lower pair just one productive operation emits.
                # It sends one P when e is set there, and two otherwise.
                g += 2-((e>>42)&1)
        if (u|e)&mask == mask:
            break
        e,_ = q_step(u,e)
    assert time == 305189
    assert (g+1)//2 == 86 and g <= (2**6-1)*2**7
    print('tick-4096 multiplicities (43,7,3,6), permuted tape halts at tick',time,
          'after',g,'safe tokens at cut 46')
    print('zero-prefix traps (low zeros, leading Ps, high all-ones, first Q tick):')
    gaps = [9]
    for k in range(7):
        g = gaps[0]
        b = g.bit_length()
        assert (1<<b) > g and (not b or (1<<(b-1)) <= g)
        assert (max(gaps)+1)*2**k <= 10*3**k
        word = (0,)*k + (3,)*b
        u = e = n = total = 0
        while True:
            n += 1
            # Count individual P emitted just beyond the k lowest pairs.
            passes = 9
            for i in range(k):
                uu,ee = (u>>i)&1,(e>>i)&1
                emitted = (2-ee)*((passes+1-uu)//2)
                u ^= (passes%2)<<i
                passes = emitted
            total += passes
            j = 0
            while j < k and ((u|e)>>j)&1:
                if not ((u>>j)&1):
                    e ^= 1<<j
                j += 1
            word = raw_tick(word)
            if j == k:
                assert word is None and total == g
                break
            e ^= 1<<j
            assert word is not None
        print(k,g,b,n)
        if k < 6:
            nxt = lift(gaps)
            assert max(nxt) <= max(gaps)+(max(gaps)+1)//2
            gaps = nxt


def check_color_symmetry():
    # Sign-extended masks make these identities valid on the zero and one tails.
    def mirror(u,e):
        return 2*~e,~u

    for u,e in product(range(-16,16),repeat=2):
        x,y = mirror(u,e)
        # P becomes Q with precisely the same stop coordinate.
        v,depth = p_step(u,e)
        yy,mirrored_depth = q_step(x,y)
        assert mirror(v,e) == (x,yy) and depth == mirrored_depth
        # Q becomes two Ps. The first stops one column higher, or passes
        # through every column. The second stops at the new bottom cell.
        f,depth = q_step(u,e)
        xx,first = p_step(x,y)
        xx,second = p_step(xx,y)
        assert mirror(u,f) == (xx,y) and second == 1
        assert first == (depth+1 if depth else 0)
        assert mirror(x,y) == (2*u,2*e+1)
    print('two-color conjugacy on 1024 signed counter pairs, including through-passes')
    def decrement(word,parity):
        result = list(word)
        for i in range(parity,len(word),2):
            if i and word[i-1]:
                continue
            result[i] ^= 1
            if word[i]:
                break
        return tuple(result)
    for length in range(9):
        for tail in product((0,1),repeat=length):
            x = decrement(tail,0)
            y = decrement(tail,1)
            assert decrement((0,)+tail,0) == (1,)+y
            assert decrement((1,)+tail,0) == (0,)+tail
            assert decrement((0,)+tail,1) == (0,)+x
            assert decrement((1,)+tail,1) == (1,)+decrement(x,0)
    print('four binary section rules on all 511 tails of length at most eight')


def raw_witness(k,spare,step_limit):
    # A reads the virgin blank at -1. Cell 0 starts the one-cell leading 4 run.
    # Three 14 pairs fix the root phase. The upper spare pairs are also 14 here.
    word = '4' + '14'*3 + '41'*k + '14'*spare + '3'
    tape = dict(enumerate(map(int,word)))
    table = parse(M26)
    x,state = -1,0
    for steps in range(step_limit):
        symbol = tape.get(x,0)
        move = table[state][symbol]
        if move is None:
            assert (state,symbol) == (1,3)
            return steps,x
        tape[x],direction,state = move
        x += direction
    raise AssertionError('literal witness did not halt by the supplied bound')


def main():
    assert LIST[25] == M26 == '1RB2RB4LA2RA1LA_2LA4RA3LA---3RA'
    audit_periods()
    audit_plateaux()
    check_zero_prefix_traps()
    check_color_symmetry()
    records = negative_tail(11)
    assert records[:8] == [(1,4),(6,8),(18,10),(58,15),(217,20),(596,24),
                           (1792,28),(6793,32)]
    print('successive negative-tail passes (tick, sufficient low width):',records)
    for spare in range(4):
        tick,k = records[(1<<spare)-1]
        check_short_suffix(k,spare,tick)
        print('every suffix of',spare,'pairs fails by tick',tick,'above',k,'all-one pairs')
    for k,spare,cap in [(8,1,20000),(15,2,1000000)]:
        steps,x = raw_witness(k,spare,cap)
        print('literal nonblank witness: k',k,'spare',spare,'defined steps',steps,'B3 at',x)


if __name__ == '__main__':
    main()
