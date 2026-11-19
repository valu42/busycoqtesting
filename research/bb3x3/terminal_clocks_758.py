"""Exact #758 terminal-family clocks and conditional clocks from the blank tape."""
from fractions import Fraction

from after_fourth_758 import CHECKPOINT
from check_758_lifts import BASE_M, D, FINE, H, OFFSET, PERIOD, tail_states
from check_bb33 import champion_step
from exact_fourth_758 import MERGER
from fifth_crossing_758 import K
from mass_clock_758 import block_size, raw_lower_bound
from timing_758 import branch_cost


def formal_tail_cost(power):
    """Evaluate the fixed tail polynomial on a rational argument, without guards."""
    p = Fraction(power)
    z = (3**15*p-OFFSET)/D
    cost = 0
    for (a, c), rule in zip(tail_states(p, z), FINE+"D"):
        if rule == "J":
            cost += 3*a*a+5*c+6
        elif rule == "B":
            cost += (6*c*c+31*c+37)/2
        elif rule == "C":
            cost += 3*c*c+29*c+65
        else:
            assert rule == "D"
            cost += (6*c*c+43*c+75)/2
    return cost


def leading_clock(m, seed, power):
    return (3*power**2-17*power+14)//2+(5*seed+9)*m+5*m*m


def clock_at_lift(m, coeffs):
    assert m >= BASE_M and (m-BASE_M) % PERIOD == 0
    p = 3**m
    z, remainder = divmod(3**15*p-OFFSET, D)
    seed = z-2*m
    assert remainder == 0 and seed % 2
    a, c = 2*p-1, z-p+1
    assert c > 2 and c % 4 == 1 and a >= c+2 and z-2 >= p
    assert champion_step(a, c) == champion_step(a, c-2)

    q0, q1, q2 = coeffs
    tail = (q2*p+q1)*p+q0
    assert tail.denominator == 1
    total = leading_clock(m, seed, p)+tail.numerator
    sibling = total+(3*(z-p)+4)//2-10*m
    direct = 0
    for rule in FINE+"D":
        direct += branch_cost(a,c)
        state = champion_step(a,c)
        if rule == "D":
            assert state is None and a == c+3 and c % 4 == 3
        else:
            assert state is not None
            a,c = state
    assert direct == tail
    return seed, total, sibling


def literal_clock(seed, expected_calls):
    a,c = 1,seed
    raw = 0
    for t in range(1, expected_calls+1):
        raw += branch_cost(a,c)
        state = champion_step(a,c)
        if state is None:
            assert t == expected_calls
            return raw,a+2*c
        a,c = state
    raise AssertionError("expected terminal")


def fast_block_size(target):
    limit = (target+8)//5
    lo,hi = 0,2*limit.bit_length()
    while lo < hi:
        j = (hi+lo)//2
        if 3**j >= limit << j:
            hi = j
        else:
            lo = j+1
    return 5*((lo+7)//5)


def remaining_lower(target, origin):
    size = fast_block_size(target)
    p,d = (target-2)//5, 9*size//5
    n = (target-origin)//(9*size)
    return 3*(n*p*p - p*d*n*(n+1)+d*d*(n*(n+1)*(2*n+1)//6))


def integral_numerator(mass):
    return mass**3+45*mass**2+585*mass


def prefix_bounds(seed):
    target = 2*seed+1
    start = 2*MERGER+1
    end = 2*CHECKPOINT+1
    # From fourth_clock_758.verify(): two consecutive, exact elapsed clocks.
    known = (12_009_315_348_729_165_034_617_066_232_977_846_431_994_862_719
             + 868_964_390_669_458_400_613_660_337_140_973_728_114_577_608)
    assert target >= end
    lower = raw_lower_bound(start)+known+remaining_lower(target,end)
    upper = 2+(integral_numerator(start)-integral_numerator(2)
               +integral_numerator(target)-integral_numerator(end))//36+known
    return lower,upper


def scientific_outward(value, up, precision=5):
    digits = ((value.bit_length()-1)*30103)//100000+1
    power = 10**(digits-1)
    while value < power:
        digits -= 1
        power //= 10
    while value >= 10*power:
        digits += 1
        power *= 10
    step = 10**(digits-precision)
    first, rem = divmod(value,step)
    if up and rem:
        first += 1
    if first == 10**precision:
        first //= 10
        digits += 1
    first = str(first)
    return first[0]+"."+first[1:]+"e"+str(digits-1)


def verify():
    v0,v1,v2 = map(formal_tail_cost,(0,1,2))
    q2 = (v2-2*v1+v0)/2
    coeffs = v0,v1-v0-q2,q2
    assert formal_tail_cost(10) == sum(c*10**i for i,c in enumerate(coeffs))
    for time_target in (10**5,H):
        assert fast_block_size(time_target) == block_size(time_target)
        assert remaining_lower(time_target,2) == raw_lower_bound(time_target)

    for m in (BASE_M, BASE_M+PERIOD):
        seed,total,sibling = clock_at_lift(m,coeffs)
        if m == BASE_M:
            assert seed == H
            direct, terminal_mass = literal_clock(seed,307)
            other, second_mass = literal_clock(seed-2,307)
            assert direct == total and other == sibling
            assert second_mass == terminal_mass == 2*H+1258
        base_lo,base_hi = prefix_bounds(seed)
        sib_lo,sib_hi = prefix_bounds(seed-2)
        lo,hi = min(base_lo+total,sib_lo+sibling),max(base_hi+total,sib_hi+sibling)
        print(f"m={m}  suffix [{scientific_outward(total,False)}, "
              f"{scientific_outward(sibling,True)}]; blank total "
              f"[{scientific_outward(lo,False)}, {scientific_outward(hi,True)}]")
    small = [literal_clock(seed,69)[0] for seed in (K,K+2)]
    small_bounds = [prefix_bounds(seed) for seed in (K,K+2)]
    lo = min(bounds[0]+cost for bounds,cost in zip(small_bounds,small))
    hi = max(bounds[1]+cost for bounds,cost in zip(small_bounds,small))
    print(f"K5 suffix {small}; blank total "
          f"[{scientific_outward(lo,False)}, {scientific_outward(hi,True)}]")
    print(f"fixed tail polynomial coefficients (constant, linear, quadratic): {coeffs}")


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run with assertions enabled.")
    verify()
