"""Pack arbitrary ordinary #758 excursions up to a finite mass, with exact clocks."""
from fractions import Fraction
from functools import cache

from check_bb33 import HALTING_TARGET, champion_step
from timing_758 import branch_cost


EFFECTS = ((5,20),(9,35),(7,26),(7,29))


def aligned(a,c):
    return (a+2*c-1)//2,(c-1)//2


def counters(u,d):
    return 2*u-4*d-1,2*d+1


def bulk_clock(c):
    return (6*c*c+31*c+37)//2 if c%4==1 else 3*c*c+29*c+65


def formal(word,u,d):
    """Evaluate the specified ordinary formulas, allowing unguarded interpolation."""
    raw = 0
    for letter in word:
        if letter == 'J':
            a,c = counters(u,d)
            raw += 3*a*a+5*c+6
            u,d = u+2,3*d-u+1
        else:
            c = 2*d+1
            raw += bulk_clock(c)+bulk_clock(6*((c+1)//4)+5)
            v,b = EFFECTS[d%4]
            u,d = u+v,(9*d+b)//4
    return u,d,raw


@cache
def matrix(word):
    q,a,m = 1,0,1
    for letter in word:
        if letter == 'J':
            q,a = 3*q,3*a-m
        else:
            q,a,m = 9*q,9*a,4*m
    return q,a,m


@cache
def correction(word,residue):
    q,a,m = matrix(word)
    # q is odd; (0,d0) realizes the desired residue even when m=1.
    d0 = residue*pow(q,-1,m)%m
    gain,final_d,c0 = formal(word,0,d0)
    e = m*final_d-q*d0
    def cost(i,j):
        return formal(word,m*i,d0+m*j)[2]
    cu,cd = cost(1,0)-c0,cost(0,1)-c0
    uu,dd = cost(2,0)-2*cu-c0,cost(0,2)-2*cd-c0
    ud = cost(1,1)-cu-cd-c0
    return gain,e,d0,c0,cu,cd,uu,dd,ud


@cache
def call_count(word):
    return len(word)+word.count('P')


@cache
def homogeneous(letter,count):
    return letter*count


def apply(word,u,d):
    if not word:
        return u,d,0
    q,a,m = matrix(word)
    numerator = q*d+a*u
    g,e,base,c0,cu,cd,uu,dd,ud = correction(word,numerator%m)
    y = d-base
    twice = (2*m*m*c0 + 2*m*(cu*u+cd*y) + uu*u*(u-m) + dd*y*(y-m)
             + 2*ud*u*y)
    clock,rem = divmod(twice,2*m*m)
    assert rem == 0 and (numerator+e)%m == 0
    return u+g,(numerator+e)//m,clock


class Atlas:
    def __init__(self,lower,depth):
        if depth < 1 or lower < 65536*3**depth:
            raise ValueError('need depth >=1 and lower >=65536 times 3**depth')
        self.lower = lower
        self.depth = depth
        self.bins = 4096*3**depth
        self.events = dict(full=0, middle=0, ambiguous=0)
        self.routes = {}

    def recipe(self,cell):
        if cell not in self.routes:
            x = Fraction(2*cell+1, 2*self.bins)
            envelope = Fraction(1,self.bins)+Fraction(16,self.lower)
            letters = ''
            for _ in range(self.depth):
                if abs(x-Fraction(1,3)) <= envelope or abs(x-Fraction(2,9)) <= envelope:
                    kind = 'ambiguous'
                    break
                if x > Fraction(1,3):
                    letters += 'J'
                    x = 3*x-1
                elif x < Fraction(2,9):
                    letters += 'P'
                    x = 9*x/4
                else:
                    kind = 'middle'
                    break
                envelope *= 3
            else:
                kind = 'full'
            self.routes[cell] = letters,kind
        return self.routes[cell]

    def packet(self,a,c,stop_at_reset=False):
        """One capped packet or a terminal; returns state, raw clock, counter calls."""
        assert a%2 and c%2
        u,d = aligned(a,c)
        assert u >= self.lower
        word,kind = self.recipe(self.bins*d//u)
        u,d,clock = apply(word,u,d)
        calls = call_count(word)
        self.events[kind] += 1
        if kind == 'full':
            return counters(u,d),clock,calls
        a,c = counters(u,d)
        q = (c+1)//4
        if a <= c:  # J on the low-d side of its entry guard leaves d nearly zero.
            assert kind == 'ambiguous'
            continuation,pure = 'J','P'
        elif a >= 4*q+3:
            # Following the first L the left counter is even. The exact next
            # guard separates P from a terminal or a live reset.
            left,right = a-4*q-3,6*q+5
            if left >= 4*((right+1)//4)+3:
                assert kind == 'ambiguous'
                continuation,pure = 'P','J'
            else:
                return (champion_step(left,right),
                        clock+branch_cost(a,c)+branch_cost(left,right), calls+2)
        else:
            # The aligned odd-left state can only take the exceptional branch.
            assert kind == 'ambiguous' and a==c+2 and c%4==3
            return champion_step(a,c),clock+branch_cost(a,c),calls+1
        rest = self.depth-len(word)-1
        u,d,dt = apply(continuation,u,d)
        if stop_at_reset and continuation=='P' and 2*u-4*d-1 == 1:
            return counters(u,d),clock+dt,calls+2
        u,d,last = apply(homogeneous(pure,rest),u,d)
        calls += len(continuation)+int(continuation=='P')+rest*(1+(pure=='P'))
        return counters(u,d),clock+dt+last,calls

    def through(self,state,cut,stop_at_reset=False):
        """Reach W>=2*cut+1, halt, or optionally the first positive-time reset."""
        a,c = state
        if not 2*self.lower <= a+2*c <= 2*cut or c < 1 or (not c%2 and a != 1):
            raise ValueError('bad starting state or mass range')
        raw = calls = packets = 0
        while a+2*c < 2*cut+1:
            if a%2 and c%2 and a+2*c+18*self.depth < 2*cut+1:
                state,dt,n = self.packet(a,c,stop_at_reset)
                packets += 1
            else:
                # This also handles an even-left state and the initial even-c
                # reset. Near the target it gives the exact first crossing.
                dt = branch_cost(a,c)
                state = champion_step(a,c)
                n = 1
            raw += dt
            calls += n
            if state is None:
                return None,raw,calls,packets
            a,c = state
            if stop_at_reset and a == 1:
                break
        return (a,c),raw,calls,packets


def literal(state,cut,stop_at_reset=False):
    raw = calls = 0
    while state is not None and state[0]+2*state[1] < 2*cut+1:
        raw += branch_cost(*state)
        state = champion_step(*state)
        calls += 1
        if stop_at_reset and state is not None and state[0] == 1:
            break
    return state,raw,calls


def audit():
    from random import Random
    rng = Random(758)
    # Exercise exact guard boundaries, both axes, and random physical angles.
    for depth in (1,2,4,8,16):
        x = max(10**12,65536*3**depth)
        atlas = Atlas(x,depth)
        for u in (x+1, x+115, 3**292):
            targets = [Fraction(0),Fraction(2,9),Fraction(1,3),Fraction(1,2)]
            for pattern in ('J','P','JPP','PJJ','JPJP','JJPPJ'):
                for x0 in (Fraction(2,9),Fraction(1,3)):
                    x1 = x0
                    for op in reversed(pattern):
                        x1 = (x1+1)/3 if op=='J' else 4*x1/9
                    targets.append(x1)
            candidates = [rng.randrange(u//2) for _ in range(35)]
            candidates.extend(u*x0.numerator//x0.denominator+offset
                              for x0 in targets for offset in range(-9,10))
            for d in candidates:
                if 0 <= d <= (u-1)//2:
                    a,c = counters(u,d)
                    state,raw,count = atlas.packet(a,c)
                    s=(a,c)
                    dt=0
                    for _ in range(count):
                        assert s is not None
                        dt += branch_cost(*s)
                        s = champion_step(*s)
                    assert (state,raw) == (s,dt)
        assert min(atlas.events.values()) > 0

    # Independent construction of mixed 144-block ordinary passages.
    from verify_cut import audit_word
    target = HALTING_TARGET
    for i in range(8):
        word = ''.join(rng.choices('JB',k=144))
        d0 = audit_word(target,word)
        state = counters(target,d0)
        atlas = Atlas(target,24)
        count = raw = 0
        for _ in range(6):
            state,dt,steps = atlas.packet(*state)
            count += steps
            raw += dt
        start = counters(target,d0)
        u_end = target+sum(2 if ch=='J' else 5 for ch in word)
        assert (state,raw,count)==literal(start,u_end)
    # Near the lower pair guard, P can itself land back on a=1. One more J
    # in the same packet would otherwise hide that first positive-time reset.
    ax = Atlas(target-100,24)
    for off in range(36):
        u = target+off
        for d in range(2*u//9-8,2*u//9+5):
            start = counters(u,d)
            assert ax.through(start,u+300,True)[:3] == literal(start,u+300,True)
    print('Eight 144-block mixed itineraries each matched literal execution in six packets.')

    p = 3**292
    for seed,depth,delta in ((10**12,5,19000),(p+1_934_340,16,50000),
                             (HALTING_TARGET,32,10000),(HALTING_TARGET-2,32,10000)):
        atlas = Atlas((seed-1)//2,depth)
        got = atlas.through((1,seed),seed+delta)
        assert got[:3] == literal((1,seed),seed+delta)
        print(f'seed {seed}, depth {depth}: {got[2]} elementary calls, '
              f'{got[3]} packets, halt {got[0] is None}; classifications {atlas.events}')


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Enable assertions.')
    audit()
