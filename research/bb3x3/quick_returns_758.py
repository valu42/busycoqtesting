"""Bound long first excursions from every reset seed through a given cutoff."""
from argparse import ArgumentParser
from functools import lru_cache
from fractions import Fraction

from check_bb33 import HALTING_TARGET, champion_step


def cut_tree(upper, depth):
    """Count terminal coarse words starting with P, by the numbers of J and P."""
    three = [3**i for i in range(2*depth+1)]
    four = [4**p for p in range(depth+1)]
    pending = {1: 1}
    leaves = 0
    for n in range(1, depth+1):
        following = {}
        for p, weight in pending.items():
            # R = 4^p / 3^(n+p). A surviving interval then has width < 7.
            if 9*upper*four[p] < 5*three[n+p]:
                leaves += weight
            else:
                following[p] = following.get(p, 0)+weight
                following[p+1] = following.get(p+1, 0)+weight
        pending = following
    assert not pending and leaves >= 1
    return leaves


@lru_cache(maxsize=None)
def budget(t):
    n = 1
    while 9*(t+9*n)*4**n >= 5*9**n:
        n += 1
    return n, cut_tree(t+9*n, n)


def launches(limit):
    for even, b in ((False,1),(True,2)):
        k = 0
        while b*3**k <= limit+4*even+2*k:
            t = min(limit+4*even+2*k, 3*b*3**k-3)
            if t >= 1:
                yield int(even)+k, t
            k += 1


def bound(limit):
    total = calls = groups = 0
    for leading, t in launches(limit):
        n, leaves = budget(t)
        # Four seeds per leaf, at most two per internal E, and one
        # possible E before the first pair. Extra slack costs nothing.
        total += 6*leaves
        calls = max(calls, leading+2*n)
        groups += 1
    return total, calls, groups


def fixed_tail(limit, n):
    """Upper fraction bound beyond 2*n calls after each launch's leading run."""
    starts = list(launches(limit))
    upper_sum = sum(t+9*n for _,t in starts)
    errors = 6*len(starts)*2**(n-1)
    widths = Fraction(2,5)*upper_sum*Fraction(7,9)**(n-1)
    return min(Fraction(1), (errors+widths)/limit)


def layer_tail(n):
    """Exact limiting probability of n ordinary blocks in a complete launch group."""
    assert n >= 1
    intervals = [(Fraction(0), Fraction(1))]
    for _ in range(n-1):
        intervals = [(a/3,b/3) for a,b in intervals]+[
            ((4*a+5)/9,(4*b+5)/9) for a,b in intervals]
    # The initial J run has already ended. The first surviving block must be P.
    intervals = [((4*a+5)/9,(4*b+5)/9) for a,b in intervals]
    return sum((1/a-1/b)/2 for a,b in intervals)


def small_check():
    assert layer_tail(1) == Fraction(2,5)
    for n in range(1,11):
        tail = layer_tail(n)
        ratio = Fraction(7,9)**(n-1)
        assert Fraction(2,9)*ratio <= tail <= Fraction(18,25)*ratio
    # Literal counter transitions, with a fresh initial reset on every run.
    for limit in (100, 1_000, 10_000):
        ceiling, calls, _ = bound(limit)
        overdue = 0
        for seed in range(1,limit+1):
            state = (1,seed)
            for _ in range(calls):
                state = champion_step(*state)
                if state is None or state[0] == 1:
                    break
            else:
                overdue += 1
        assert overdue <= ceiling
    # Compare the grouped count to visiting distinct words on a small tree.
    for t in (5,50,500):
        n, aggregate = budget(t)
        upper = t+9*n
        def descend(j,p):
            if 9*upper*4**p < 5*3**(j+2*p):
                return 1
            return descend(j+1,p)+descend(j,p+1)
        assert aggregate == descend(0,1)


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--limit',type=int,default=HALTING_TARGET)
    parser.add_argument('--small-check',action='store_true')
    args = parser.parse_args()
    if not __debug__ or args.limit < 1:
        parser.error('use a positive cutoff with assertions enabled')
    if args.small_check:
        small_check()
    rare, calls, groups = bound(args.limit)
    print(f'{groups} launch groups. At most {rare:,} of the {args.limit:,} seeds '
          f'can avoid both a halt and a positive-time reset for {calls:,} calls.')
    if args.limit == HALTING_TARGET:
        # Adding direct halts at the first nonpaired bulk increases the per-leaf
        # bound from 6 to 10. Both counts use the identical prefix trees.
        no_return = rare//6*10
        assert rare%6 == 0 and 10**36*no_return < 3*args.limit
        print('Including early halts among exceptions, fewer than 3 in 10^36 '
              'fail to return to a reset within the same budget.')
        assert calls == 1086 and groups == 584 and 5*10**35*rare < args.limit
        for n,reciprocal in ((22,100),(31,1000),(59,10**6),(86,10**9)):
            assert fixed_tail(args.limit,n)*reciprocal < 1
        print('After the leading jumps, the fractions exceeding 44, 62, 118 and '
              '172 further calls are below 1/100, 1/1000, 1/10^6 and 1/10^9.')
        print('Integer lower bound on reciprocal exceptional fraction:',args.limit//rare)
