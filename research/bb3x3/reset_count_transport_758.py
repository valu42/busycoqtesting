"""Bound actual return counts on completed power annuli with a given largest gain."""
from fractions import Fraction as F

from annular_skip_758 import openings
from check_bb33 import champion_step


def width(h, a, b, lower, upper):
    lo, hi = max(a, lower), min(b, upper)
    return h*(1/lo-1/hi) if lo < hi else F(0)


def good_constant(depth=12):
    # Unit scale P=1 for the three launches. The tiny fourth group at the
    # upper edge is charged by its total displacement, not by this sum.
    groups = ((F(1), F(1,3), F(1)), (F(2,3), F(1,3), F(2,3)),
              (F(2), F(66,100), F(1)))
    nodes, total = [(5, 4, 9, 9)], F(0)
    for _ in range(depth):
        children = []
        for a, scale, den, gain in nodes:
            lo, hi = F(a,den), F(a+scale,den)
            total += gain*sum(width(h,lo,hi,lower,upper) for h,lower,upper in groups)
            children.extend(((3*a,scale,3*den,2), (9*a+5*scale,4*scale,9*den,9)))
        nodes = children
    # Every nonempty survivor word starts with P, hence x>=5/9.
    tail = (F(81,25)*F(11,3)*F(4,9)*F(7,9)**(depth-1)
            *(F(2,3)+F(4,9)*9)/(1-F(7,9)))
    return total+tail


def target_example():
    m, p, cap = 291, 3**291, 3**219
    # Exact upper bound for (3P/G)^delta, using delta<3/4.
    assert 3*p//cap == 3**73
    assert 27*44**4 >= 100**4 and 729*55**4 >= 64*100**4 and 44+55<100
    leaves = 3**55
    assert leaves**4 >= (3*p//cap)**3
    # Every initial return seed is at least 2m greater than its predecessor.
    minimum_displacement = 2*p-2*cap
    errors = F(63*p,2*m) + leaves*(36*cap+1188+144) + 2*m+2
    lower = -(-(minimum_displacement-errors)//(2*m+11))
    upper = p//m
    assert 1000*m*lower >= 927*p
    print(f'At exponent {m}, with reset gaps at most 3^219, the interior '
          f'contains {lower:,} to {upper:,} complete returns.')
    return lower,upper


def spot_check():
    # Check the opening classes, minimum gain and elementary accounting on
    # genuine returns in the three main groups at widely separated scales.
    for m in (20,35,291):
        p = 3**m
        for factor in (F(7,6), F(11,6), F(17,7)):
            for parity in (0,1):
                seed = int(p*factor)
                seed += (parity-seed)%2
                launch = openings(seed)
                k = launch.k
                assert k==m if parity else k in (m-1,m)
                for _ in range(10):
                    a,c = 1,seed
                    opening = openings(seed)
                    for step in range(int(opening.even)+opening.k):
                        a,c = champion_step(a,c)
                        assert a>1
                    u0 = (a+2*c-1)//2
                    assert 2*m <= u0-seed <= 2*m+4
                    while a!=1:
                        a,c = champion_step(a,c)
                    assert c>seed+2*m
                    seed=c


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run with assertions enabled.')
    constant=good_constant()
    assert constant < 63
    print(f'Normalized sum of weighted ordinary widths is less than {float(constant):.6f} (rounded).')
    target_example()
    spot_check()
