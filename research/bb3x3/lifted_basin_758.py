"""Exactly classify the original twelve-million-reset window at every lifted H."""
from functools import cache
import argparse

from check_758_lifts import BASE_M, COARSE, D, H, OFFSET, PERIOD, check_family
from check_758_moving_seeds import check_guards, return_constant
from check_bb33 import champion_step

WIDTH = 12_000_000
INNER = 3_403_055
MOD = 32_768
BITS = 136
MASK = (1 << BITS)-1
PAIR = ((5,20), (9,35), (7,26), (7,29))
EXPECTED = (0,0,12,0,6,0,4,8,2,4,2,2,2,2,2,4,2,4,2,2,2,2,2,4)
TOTAL = (26,10,20,4,10,4,8,10,4,6,4,4,4,4,4,6,4,6,4,4,4,4,4,6)


def prefix_at_base(distance, validate=False):
    """Return h and the bounded correction g immediately after the extra bulk."""
    power = 3**BASE_M
    a,c = 2*power-1,H-distance+2*BASE_M-power+1
    for index,letter in enumerate(COARSE+'L'):
        if validate:
            assert min(a,c) > 1
            if letter == 'J':
                assert a <= c and a%2 == c%2 == 1
            else:
                assert a >= 4*((c+1)//4)+3
        if letter == 'J':
            a,c = 3*a+2,c-a+1
        else:
            group = (c+1)//4
            a,c = a-4*group-3,6*group+5
    return (a+1)//2, (a+2*c-1)//2-H+distance-2*BASE_M


@cache
def headers():
    table = tuple(prefix_at_base(i) for i in range(0,MOD,2))
    for i,(h,g) in enumerate(table):
        assert prefix_at_base(2*i+MOD) == (h+2*D,g)
        assert 37 <= g <= 65
    for d in (4, WIDTH):
        prefix_at_base(d, validate=True)
    return table


def header(distance):
    h,g = headers()[(distance % MOD)//2]
    return h + (distance//MOD)*2*D,g


def alignment(distance):
    h,g = header(distance)
    p,q,r = h*D,3**15,0
    while p>q:
        q *= 3
        r += 1
    assert 0 <= r <= 21 and q < 3*p < 3*q
    return h,g,p,q,r


def check_all_offsets():
    """Certify every denominator, endpoint, hole and uniform comparison margin."""
    check_family()
    check_guards()
    maximum = 0
    for d in range(4,WIDTH+1,2):
        _,_,p,q,_ = alignment(d)
        count = 0
        while True:
            assert 0 < p < q
            if 3*p < q:
                p *= 3
            elif 9*p > 5*q:
                p,q = 9*p-5*q,4*q
            else:
                assert 3*p > q and 9*p < 5*q
                break
            count += 1
            assert count <= 58
        maximum = max(maximum,count)
    assert maximum == 58
    # Denominators at most 3^(15+21) 4^58. The norm error grows by at most
    # a factor 4 after an additive allowance of 32 for an exact grouped block.
    assert 3**BASE_M > 1000*(2*BASE_M+WIDTH+1000)*4**58 * 3**36*4**58
    print('All 5,999,999 odd offsets had a strict ordinary return; maximum 58 blocks.')


class Lift:
    def __init__(self,m):
        self.m = m
        self.z = ((pow(3,m+15,MASK+1)-OFFSET)*pow(D,-1,MASK+1)) & MASK
        self.powers = [pow(3,m-r,MASK+1) for r in range(22)]
        self.even = {d: 2*m+return_constant(m,d-2*m) for d in range(1,64,2)}
        assert all(2*m+21 <= gain <= 2*m+31 for gain in self.even.values())

    def gain(self,d):
        """Exact first-return increment at distance d≥3."""
        assert 3 <= d <= WIDTH
        if d%2:
            return self.even[d%64]
        h,g,p,q,r = alignment(d)
        gain = 2*self.m+g+2*(self.m-r)
        u = (self.z-d+g+2*(self.m-r)) & MASK
        low_d = ((u-self.powers[r]*h) & MASK)//2
        for _ in range(59):
            if 3*p < q:
                low_d = 3*low_d-u+1
                u += 2
                p *= 3
                gain += 2
            elif 9*p > 5*q:
                v,b = PAIR[low_d%4]
                assert (9*low_d+b)%4 == 0
                low_d = (9*low_d+b)//4
                gain += v
                u += v
                p,q = 9*p-5*q,4*q
            else:
                assert 3*p>q and 9*p<5*q
                result = gain+5+2*(low_d%2)
                assert 4*self.m-60 <= result <= 4*self.m+610
                return result
        raise AssertionError('Word exceeds the verified length.')

    def parents(self,d):
        for gain in set(self.even.values()):
            parent = d+gain
            if parent <= WIDTH and parent%2 and self.gain(parent) == gain:
                yield parent
        lo = max(4,d+4*self.m-60)
        hi = min(WIDTH,d+4*self.m+610)
        for parent in range(lo+lo%2,hi+1,2):
            if parent-self.gain(parent) == d:
                yield parent

    def basin(self):
        found = {0,2}
        queue = [0,2]
        while queue:
            d = queue.pop()
            for parent in self.parents(d):
                assert parent > d and parent not in found
                queue.append(parent)
                found.add(parent)
        return found


def directly_check(m, distances):
    """Independent full-size integer replay at selected offsets."""
    alg = Lift(m)
    power = 3**m
    target = (power*3**15-OFFSET)//D-2*m
    for d in sorted(set(distances)):
        if d%2:
            q = power//3
            a,c = 4*q-1,target-d-2*q+2*(m-1)+5
        else:
            a,c = 2*power-1,target-d-power+2*m+1
            for letter in COARSE+'L':
                assert (a<=c) == (letter=='J')
                a,c = champion_step(a,c)
                assert a>1
            # Test the skipped jump batch independently, with the original
            # positive-right guard for the last J of the proposed count.
            _,_,_,_,r = alignment(d)
            k = m-r
            h = (a+1)//2
            assert h*(power//3**r) <= (a+2*c-1)//2+2*k
            a,c = (a+1)*(power//3**r)-1,c-h*(power//3**r-1)+2*k
        while a != 1:
            nxt = champion_step(a,c)
            assert nxt is not None
            a,c = nxt
        assert c == target-d+alg.gain(d)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--quick',action='store_true',help='skip the six-million-direction enumeration')
    parser.add_argument('--dense',action='store_true',help='independently scan every start at the first two exponents')
    args = parser.parse_args()
    if not __debug__:
        parser.error('enable assertions')
    if not args.quick:
        check_all_offsets()
    for k in range(1,25):
        m = BASE_M+k*PERIOD
        lift = Lift(m)
        seeds = lift.basin()
        count = sum(d>=INNER for d in seeds)
        assert (len(seeds),count)==(TOTAL[k-1],EXPECTED[k-1])
        if k == 1:
            assert max(seeds)==3_401_471
            directly_check(m,(seeds-{0,2}) | {4,6,111,123_456,INNER,WIDTH})
        print(f'k={k:2d}  full={len(seeds):2d}  original interval={count:2d}')
    directly_check(BASE_M,[4,6,111,123_456,INNER,WIDTH])
    if args.dense:
        for m, counts in ((BASE_M,(10_837_487,8_596_946)),(BASE_M+PERIOD,(26,0))):
            lift = Lift(m)
            captured = bytearray(WIDTH+1)
            captured[0] = captured[2] = 1
            for d in range(3,WIDTH+1):
                after = d-lift.gain(d)
                if after >= 0:
                    captured[d] = captured[after]
            assert (sum(captured),sum(captured[INNER:])) == counts
            print(f'm={m}: dense scan verified {counts}.')
    assert 2*(BASE_M+25*PERIOD) > WIDTH
    print('At k≥25 only the two direct seeds halt before passing H_m.')


if __name__ == '__main__':
    main()
