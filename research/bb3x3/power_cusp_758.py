"""Classify reset origins in a short shell above 3^m after its common bulk prefix."""
from argparse import ArgumentParser
from functools import lru_cache

from annular_skip_758 import runs
from check_bb33 import champion_step, first_return
from continue_after_target_758 import bulk_table
from power_gates_758 import coarse_return


BITS = 12
TABLE = bulk_table(BITS)
FACTOR = 3**BITS


def bulk_prefix(a, c, count):
    """Apply a proven common bulk run. The left counter decreases every call."""
    for _ in range(count // BITS):
        y = (c+7)//2
        high, low = divmod(y, 1 << BITS)
        small, gain = TABLE[low]
        nxt = 2*(high*FACTOR+small)-7
        a, c = a+2*(c-nxt)+gain, nxt
    for _ in range(count % BITS):
        q = (c+1)//4
        a, c = a-4*q-3, 6*q+5
    assert a > 1
    return a,c


def common_pairs(m, distance):
    p = 3**m
    q = 0
    left, right = 4*(2*distance+2*m+14),p
    assert left <= right
    while left*9 <= right*4:
        left *= 9
        right *= 4
        q += 1
    assert q >= 1
    return q


def partition(m, distance, depth, start=None):
    """Return the odd-seed partition in d/2 coordinates, endpoints inclusive."""
    p = 3**m
    assert m >= 20 and distance >= 1 and 2*distance+2*m <= p//1000
    qi = common_pairs(m,distance)
    lower = distance if start is None else start
    assert 0 <= lower <= 2*distance
    low, high = (lower+1)//2,distance

    @lru_cache(maxsize=8192)
    def opening(i):
        return bulk_prefix(2*p-1,2*i+2*m+1,2*qi)

    def replay(i,word):
        a,c = opening(i)
        for op in word:
            if op == 'L':
                q = (c+1)//4
                assert a >= 4*q+3
                a,c = a-4*q-3,6*q+5
            else:
                assert a%2 and a <= c
                a,c = 3*a+2,c-a+1
        return a,c

    def descend(lo,hi,word,odd,completed):
        if completed == depth and odd:
            yield lo,hi,None
            return
        def kind(i):
            a,c = replay(i,word)
            if a == 1:
                return 3
            if a >= 4*((c+1)//4)+3:
                return 0
            return 1 if a > c else 2
        for l,h,choice in runs(lo,hi,kind):
            if choice == 0:
                yield from descend(l,h,word+'L',not odd,completed+int(not odd))
            elif choice == 2 and odd:
                yield from descend(l,h,word+'J',True,completed+1)
            else:
                yield l,h,word if choice == 2 else None

    result = list(descend(low,high,'',True,0))
    assert result[0][0] == low and result[-1][1] == high
    assert all(x[1]+1 == y[0] for x,y in zip(result,result[1:]))
    for i in (low,(low+high)//2,high):
        seed = p+2*i
        a,c = 1,seed
        for _ in range(m+2*qi):
            a,c = champion_step(a,c)
            assert a > 1
        assert (a,c) == opening(i)
    # Both endpoints of the even word suffice by counter ordering.
    for ends in (p+lower,p+2*distance):
        seed = ends-ends%2
        assert coarse_return(m,seed,1) == first_return(seed)
    for l,h,word in result[::max(1,len(result)//32)]:
        if word is not None:
            i=(l+h)//2
            a,c = replay(i,word)
            assert a%2 == 0 and a <= c
            assert first_return(p+2*i) == a//2+c+2
    return qi,result


def report(m,distance,depth):
    qi,cells=partition(m,distance,depth)
    total=sum(h-l+1 for l,h,_ in cells)
    hard=sum(h-l+1 for l,h,r in cells if r is None)
    print(f'm={m} D={distance} n={depth} common_L={2*qi} cells={len(cells)} '
          f'hard={hard}/{total} ({hard/total:.4%})')
    return qi,len(cells),hard,total


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--m',type=int,default=292)
    parser.add_argument('--distance',type=int)
    parser.add_argument('--depth',type=int,default=8)
    args = parser.parse_args()
    if not __debug__ or args.depth < 1:
        parser.error('enable assertions and use a positive depth')
    if args.distance is not None:
        report(args.m,args.distance,args.depth)
    else:
        for d in (2_000_000,2_000_000_000_000,10**80):
            report(args.m,d,args.depth)
