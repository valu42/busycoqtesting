"""Build repeatable ordinary-return intervals and trace one reset chain exactly."""
from dataclasses import dataclass
from fractions import Fraction
import heapq

from check_bb33 import HALTING_TARGET, champion_step, first_return


@dataclass(frozen=True)
class Launch:
    even: bool
    k: int
    h: int

    def state(self, seed):
        t = seed + 4*self.even + 2*self.k
        assert self.h <= t <= 3*self.h-3
        return 2*self.h-1, t-self.h+1


def openings(seed):
    even = seed%2 == 0
    k,h = 0, 2 if even else 1
    while 3*h <= seed + 4*even + 2*k+2:
        k,h = k+1, 3*h
    return Launch(even,k,h)


def runs(low, high, label):
    """Partition integer indices by a nondecreasing, integer-valued label."""
    while low <= high:
        value = label(low)
        if label(high) == value:
            yield low, high, value
            return
        lo,hi = low,high
        while lo+1 < hi:
            mid = (lo+hi)//2
            if label(mid) == value:
                lo = mid
            else:
                hi = mid
        yield low,lo,value
        low = hi


def replay(launch, letters, seed):
    a,c = launch.state(seed)
    for op in letters:
        if op == 'L':
            q = (c+1)//4
            assert a >= 4*q+3
            a,c = a-4*q-3, 6*q+5
        else:
            assert a%2 and a <= c
            a,c = 3*a+2,c-a+1
    return a,c


def part(low, high, parity, depth, weights, scale):
    """Classify seeds 2*i+parity for low<=i<=high; None marks difficult sites."""
    result = []
    def descend(lo, hi, launch, ops, complete, odd):
        if depth is None:
            # At an odd node, a pair has contributed exactly two L letters.
            pairs,jumps = ops.count('L')//2,ops.count('J')
            stop = scale*4**pairs <= 3**(jumps+2*pairs)
        else:
            stop = complete >= depth
        if odd and stop:
            result.append((lo,hi,None))
            return
        def kind(i):
            a,c = replay(launch,ops,2*i+parity)
            if odd and a == 1:
                return 3
            if a >= 4*((c+1)//4)+3:
                return 0
            if a > c:
                return 1
            return 2
        for x,y,j in runs(lo,hi,kind):
            if j == 0:
                descend(x,y,launch,ops+'L',complete+(weights[1] if not odd else 0),not odd)
            elif j == 2 and odd:
                descend(x,y,launch,ops+'J',complete+weights[0],True)
            elif j == 2:
                result.append((x,y,(launch,ops)))
            else:
                result.append((x,y,None))
    for x,y,k in runs(low,high,lambda i: openings(2*i+parity).k):
        launch = openings(2*x+parity)
        assert launch.k == k
        descend(x,y,launch,'',0,True)
    assert result[0][0] == low and result[-1][1] == high
    assert all(a[1]+1 == b[0] for a,b in zip(result,result[1:]))
    return result


def partition(p, n=None, weights=(1,1)):
    """Merge the two parity partitions into half-open cells covering [p,3p]."""
    if p < 100 or (n is not None and n < 1) or min(weights) < 1:
        raise ValueError('require X >= 100 and positive stopping weights and budget')
    low, high = p//2, 3*p//2
    rows = [part(low,high,parity,n,weights,p) for parity in (0,1)]
    cuts = sorted({low, high+1, *(x for row in rows for x,_,_ in row)})
    idx = [0,0]
    for x,y in zip(cuts,cuts[1:]):
        for b,row in enumerate(rows):
            while row[idx[b]][1] < x:
                idx[b] += 1
            assert row[idx[b]][0] <= x <= y-1 <= row[idx[b]][1]
        yield (max(2*x,p),min(2*y,3*p+1),*(row[k][2] for row,k in zip(rows,idx)))


def evaluate(rule, seed):
    launch,ops = rule
    a,c = replay(launch,ops,seed)
    assert not a%2 and a <= c
    return a//2+c+2


def skip_cell(seed, end, rules):
    """Advance to the first reset >=end, bounding residue-cycle evaluations."""
    modulus = 2**(1+max(ops.count('L') for _,ops in rules))
    seen = {}
    count = evaluations = 0
    while seed < end:
        residue = seed%modulus
        if residue in seen:
            old,n = seen[residue]
            gain = seed-old
            assert gain > 0 and gain%modulus == 0
            repeats = (end-1-seed)//gain
            seed += repeats*gain
            count += repeats*(count-n)
            break
        seen[residue] = seed,count
        seed = evaluate(rules[seed%2],seed)
        count += 1
        evaluations += 1
    while seed < end:
        seed = evaluate(rules[seed%2],seed)
        count += 1
        evaluations += 1
    assert evaluations <= 2*modulus
    return seed,count,evaluations


def run(cells, seed):
    calls = steps = 0
    for low,end,*rules in cells:
        if seed >= end:
            continue
        assert seed >= low
        if None in rules:
            while seed < end:
                seed = first_return(seed)
                calls += 1
                steps += 1
                if seed is None:
                    return None,steps,calls
        else:
            seed,n,k = skip_cell(seed,end,rules)
            calls += k
            steps += n
    return seed,steps,calls


def cover(cells, starts):
    """Enclose all live exit resets and record whether the calculation saw any halt."""
    pending = set(starts)
    heap = list(pending)
    heapq.heapify(heap)
    calls = 0
    halt = False

    def push(seed):
        if seed not in pending:
            pending.add(seed)
            heapq.heappush(heap,seed)

    for lo,hi,*rules in cells:
        if not heap or heap[0] >= hi:
            continue
        assert heap[0] >= lo
        if None in rules:
            while heap and heap[0] < hi:
                seed = heapq.heappop(heap)
                pending.remove(seed)
                nxt = first_return(seed)
                calls += 1
                if nxt is None:
                    halt = True
                else:
                    assert nxt > seed
                    push(nxt)
        else:
            gain = max((8*launch.even + 4*launch.k + 4*ops.count('J')
                        + 9*ops.count('L') + 5)//2 for launch,ops in rules)
            while heap and heap[0] < hi:
                pending.remove(heapq.heappop(heap))
            for seed in range(hi,hi+gain):
                push(seed)
    return pending,halt,calls


def audit():
    for p,n,weights in ((497,3,(1,1)),(3**7,4,(1,1)),(3**10,5,(1,1)),(3**7,13,(2,5))):
        cells = list(partition(p,n,weights))
        for low,hi,*rules in cells:
            for seed in range(low,hi):
                rule = rules[seed%2]
                if rule is None:
                    continue
                launch,ops = rule
                a,c = 1,seed
                for _ in range(int(launch.even)+launch.k+len(ops)):
                    a,c = champion_step(a,c)
                    assert a != 1
                assert (a,c) == replay(*rule,seed)
                assert champion_step(a,c) == (1,evaluate(rule,seed))
        end,nsteps,calls = run(cells,p)
        s,count = p,0
        while s is not None and s <= 3*p:
            s = first_return(s)
            count += 1
        assert (end,nsteps) == (s,count)
        print(f'[{p},{3*p}]: {len(cells)} cells; {calls} evaluated of {nsteps} exact returns; end {end}')


def audit_exponent():
    upper_a = Fraction(123651,100000)
    lower_b = Fraction(10686,10000)
    assert upper_a**5-upper_a**3-1 > 0
    assert 4*lower_b**5+3*lower_b**2-9 < 0
    assert (4*upper_a**5)**119 < lower_b**4405


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run with assertions enabled.')
    audit()
    audit_exponent()
    p = 3**9
    starts = range(p,p+41)
    exits,halt,calls = cover(list(partition(p)),starts)
    for seed in starts:
        while seed is not None and seed <= 3*p:
            seed = first_return(seed)
        assert halt if seed is None else seed in exits
    print(f'Adaptive enclosure from 41 seeds at 3^9: {len(exits)} allowed exits; '
          f'{calls} difficult queries; possible halt {halt}')
    p,n = 3**292,8
    cells = list(partition(p,n))
    difficult = sum(h-l for l,h,*r in cells if None in r)
    print(f'3^292 annulus at depth {n}: {len(cells)} cells; '
          f'{float(Fraction(2*p+1-difficult,2*p+1)):.9%} certified for both parities')
    easy = [(lo,min(hi,HALTING_TARGET),r) for lo,hi,*r in cells
            if lo < HALTING_TARGET and None not in r]
    width = sum(hi-lo for lo,hi,_ in easy)
    print(f'From 3^292 to H, depth {n} certifies {len(easy)} intervals covering '
          f'{width/(HALTING_TARGET-p):.9%} of integer positions.')
    lo,hi,rules = max(easy,key=lambda x: x[1]-x[0])
    end,count,evaluations = skip_cell(lo,hi,rules)
    assert end-hi == 188 and evaluations == 204
    print(f'From {lo} to {end}, {count} first returns from {evaluations} evaluations.')
