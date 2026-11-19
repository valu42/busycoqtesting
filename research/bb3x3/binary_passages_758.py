"""Verify two finite lower bounds for the binary jump indicator."""
from fractions import Fraction

from after_target_758 import EDGE
from check_bb33 import HALTING_TARGET as H


def log_ceil(x, a=3, b=1):
    """Smallest n >= 0 such that (a/b)^n >= x, by exact comparison."""
    terms = 0
    numerator = denominator = 1
    while numerator < x*denominator:
        numerator *= a
        denominator *= b
        terms += 1
    return terms


def phase_bound(q):
    """Number of bounded states on a fixed-denominator central span."""
    m = log_ceil(7*q+1)
    counts = [1,1]
    for _ in range(2,m+1):
        counts.append(counts[-1]+4*counts[-2])
    return m+2+counts[m]+4*counts[m-1]


def ordinary_passage(low, high):
    """Minimum number of aligned ordinary blocks across a missed interval."""
    total, right = 0, 1
    for _ in range(785):
        q = (right+1)//4
        total += 4*q+3
        right = 6*q+5
    assert total-6 <= 2*low+1 <= 2*high+1 <= total+right-6
    # The first crossing enters at most eight beyond the lower threshold.
    # Trimming 5,458 at the upper end excludes E; trim both half-pairs.
    minimum_calls = (2*(high-low)-5458-8)//9
    return (minimum_calls-2)//2


def post_target():
    t, u, k = 10**135, 2*H, 300_000_000
    m = log_ceil(144*t+1)
    future = log_ceil(u+1,3,2)
    n = m+future+4
    assert n == 1085
    assert EDGE+647 < u
    assert ordinary_passage(H+1,EDGE+647) > t+4*n
    outer = 2**(m+4)*k
    repeated = (t-outer)//(outer+1)
    qmax = 9*t
    three = log_ceil(qmax)+1
    pairs = log_ceil(qmax,4)+1
    jumps = log_ceil(u+1)+1
    growing = log_ceil(2*qmax*(u+7),9,4)+3
    core = repeated-(three+(pairs+1)*(jumps+1)+2*growing+10)
    assert core > 0
    # A candidate q <= 9t supplies at most phase_bound(q) positions.
    # Enough room exists at this fixed q to choose a span with 9s < q.
    lo, hi = 1,qmax
    assert phase_bound(lo) < core <= phase_bound(hi)
    while hi-lo > 1:
        mid = (lo+hi)//2
        if phase_bound(mid) < core:
            lo = mid
        else:
            hi = mid
    s = min(core//2,(hi-1)//9)
    fine = log_ceil(144*s+1)
    past = max(fine,log_ceil(qmax+1))
    assert past+3 <= n
    inner = 2**(fine+4)*k
    inner_run = (s-past-2-inner)//(inner+1)
    maximum_run = log_ceil(2*(u+2)*9*s*qmax,9,4)+2
    assert inner_run > maximum_run
    print(f'Post-target: K={k:,} leads to an inner run of at least {inner_run:,}; '
          f'the maximum is {maximum_run:,}. Binary word length {n}.')


def halting_corridor():
    limit = 44
    far = 905_416_090_650_670
    near = 543_249_654_390_404
    assert ordinary_passage(H-far,H-near) > 40_000_000_000_000
    # A reference before J has integer deviation span at most q after trimming
    # 100 more blocks. An unbounded deviation cannot persist 1,000 calls.
    qmax = 3**limit
    assert 4*qmax*4**100 < 3*9**100
    assert (qmax*(H+7))*2**1000 < 3**1000
    assert (2*H+7)*2**1000 < 3**1000
    peak = Fraction(0)
    for length in range(3,limit+1):
        for pairs in range(1,(length-1)//2+1):
            jumps = length-2*pairs
            weight = (4**pairs//2)*(2*jumps+7*pairs+1)
            peak = max(peak,Fraction(weight,length))
    ceiling = limit*peak+(limit+2)*20_000
    assert ceiling < far-near-15_000
    print(f'Scale 10: at most {int(ceiling):,} mass-coordinate units '
          f'under K <= {limit}; more than {far-near-15_000:,} are required.')


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run with assertions enabled.')
    post_target()
    halting_corridor()
