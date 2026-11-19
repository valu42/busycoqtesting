"""Post-gate first-return words at s=2*3^m-2m-4 across exponents."""
from bisect import bisect_right
from collections import Counter
from fractions import Fraction
from math import log

from check_bb33 import champion_step
from power_gates_758 import coarse_return


def exit_seed(m):
    return 2*3**m - 2*m - 4


def audit_entrance(m):
    """Check a trajectory entering the gate below 1.92 times the power."""
    p = 3**m
    last, stride = exit_seed(m), 4*m+16
    q = (last-192*p//100 + stride-1)//stride
    start = last-q*stride
    assert 191*p <= 100*start <= 192*p and q > 0
    for s in (start, last-stride):
        t = coarse_return(m,s,2)
        assert t == s+2*m+9
        assert coarse_return(m,t,2) == s+stride
    a,c = 1,last
    for _ in range(m+1):
        a,c = champion_step(a,c)
    assert (a,c) == (4*p-1,1)


def bulk_sequence(limit):
    """Right coordinate and cumulative left consumption for uninterrupted bulks."""
    right, debit = [1], [0]
    while debit[-1] <= limit:
        q = (right[-1]+1)//4
        debit.append(debit[-1]+4*q+3)
        right.append(6*q+5)
    return right,debit


def outcome(m, right, debit, max_blocks):
    """Classify the first nonbulk action and then up to max_blocks coarse blocks."""
    supply = 4*3**m-1
    n = bisect_right(debit,supply)-1
    a,c = supply-debit[n],right[n]
    if a == 1:
        return 'seam reset'
    if a >= c+1:
        return 'seam boundary'
    if n % 2:
        assert a%2 == 0 and champion_step(a,c)[0] == 1
        return 'bulk then reset'
    assert a%2 and a <= c
    a,c = champion_step(a,c)
    prefix = ''
    for _ in range(max_blocks+1):
        if a == 1:
            return 'seam reset'
        assert a%2 and c%2
        if a <= c:
            prefix += 'J'
        elif a >= 4*((c+1)//4)+3:
            a,c = champion_step(a,c)
            if a <= c:
                assert not a%2 and champion_step(a,c)[0] == 1
                return prefix+'R'
            if a < 4*((c+1)//4)+3:
                return 'terminal boundary'
            prefix += 'P'
        else:
            return 'exceptional boundary'
        a,c = champion_step(a,c)
    return 'long'


def interval(word):
    lo,hi = Fraction(1,3),Fraction(5,9)
    for letter in reversed(word):
        if letter == 'J':
            lo,hi = lo/3,hi/3
        elif letter == 'P':
            lo,hi = (4*lo+5)/9,(4*hi+5)/9
        else:
            raise ValueError(letter)
    return lo,hi


def density(word):
    lo,hi = interval(word)
    return log((3-lo)/(3-hi))/(2*log(1.5))


def main():
    if not __debug__:
        raise SystemExit('Use Python with assertions enabled.')
    for m in (20,34,292):
        audit_entrance(m)
    last = 2000
    right,debit = bulk_sequence(4*3**last)
    counts = Counter(outcome(m,right,debit,12) for m in range(20,last+1))
    total = last-19
    print(f'Bulk then immediate reset: {counts["bulk then reset"]}/{total}; limiting density 1/2')
    for word in ('','J','P','JJ','JP','PJ','PP'):
        print(f'{word+"R"}: {counts[word+"R"]}/{total}; limiting density {density(word):.7f}')


if __name__ == '__main__':
    main()
