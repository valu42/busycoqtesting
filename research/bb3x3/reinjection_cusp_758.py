#!/usr/bin/env python3
"""Audit the first-cusp reduction and genuine long-reinjection families.

The uniform proofs are in REINJECTION_758.md. This standard-library checker
stops at unresolved J/E inputs and makes no blank-tape decision.
"""
from fractions import Fraction
from itertools import product

from check_bb33 import champion_step
from uniform_parity_passage_758 import source_bounds, prefix
from scale_clauses_758 import check_word

K = Fraction(2187, 2059)
WEIGHTS = (320, 608, 1040, 1688, 2660, 4118)


def verify_constants():
    m, p = 20, 3**20
    assert p >= 4000*m*Fraction(3, 2)**3
    assert Fraction(46656, 2059)*p > 332500*m+8414
    low_c6 = Fraction(729, 64)*((K-1)*p-493)-7
    assert Fraction(3, 2)*low_c6+Fraction(7, 2) > 16000
    assert Fraction(-2059*501+14232, 64) > -15896
    assert 2*K*p > 51000*m+967
    assert 16*Fraction(3, 2)**(3*m) > 2*K*p+1027*m+73
    assert (Fraction(54, 49)-K)*p > 518*m+505
    assert (512000*K*m-44040)/6177 > 2*m
    assert 42*m-7 > Fraction(31*m+63, 2)
    assert (Fraction(3645, 8)*m+495)/(2*m+20) < 228
    assert 24666 < 58500*m
    lane_weights = (81, 135, 171, 195, 211)
    for index, weight in enumerate(lane_weights, 1):
        assert 36*weight == 8236-2*WEIGHTS[5-index]
    assert 8236-2*WEIGHTS[-1] == 0
    assert len({sum(w*b for w,b in zip(lane_weights,bits))
                for bits in product((0,1), repeat=5)}) == 32


def verify_lanes():
    m, p = 20, 3**20
    low_z = 2187*p//2059+51
    low_z += (1-low_z) % 2
    lanes = set()
    for z in range(low_z, low_z+128, 2):
        seed = z-2*m
        a,c,bits = prefix(seed,m)
        u,h = (a+2*c-1)//2,(a+1)//2
        constant = 20835+18*sum(w*e for w,e in zip((81,135,171,195,211),bits[1:]))
        lanes.add(constant)
        assert 1995*u+64*h == 2187*p+constant
        assert u % 2 == 0 and h % 6 == 0
        translated_a,translated_c,translated_bits = prefix(seed+128,m)
        translated_u = (translated_a+2*translated_c-1)//2
        translated_h = (translated_a+1)//2
        assert translated_bits == bits
        assert (translated_u-u,translated_h-h) == (128,-3990)
        if bits[0]:
            other_a,other_c,other_bits = prefix(seed+2,m)
            assert (other_a,other_c) == (a,c)
            assert other_bits == (0,)+bits[1:]
    assert len(lanes) == 32


def capture(m):
    p, b, n, d = 3**m, 3, 27, 8
    while p*d*16 >= 4000*m*n*81:
        b, n, d = b+4, n*81, d*16
    assert 4000*m <= Fraction(p*d, n) < 20250*m
    lo, hi = source_bounds(m, b)
    assert lo-K*p > 2*m
    assert lo-K*p < Fraction(3645, 8)*m-6
    assert hi-lo >= 42*m-7 > Fraction(31*m+63, 2)
    return b, lo, hi


def scan_bulk(a, c, bulk_limit):
    """Execute legal bulks only; J/E endpoints are returned without execution."""
    assert a >= 0 and c >= 1 and c % 2 == 1
    calls = bulks = 0
    while True:
        if a == 1:
            return 'reset', c, calls, bulks
        threshold = 4*((c+1)//4)+3
        if a >= threshold:
            assert bulks < bulk_limit, 'bulk bound exhausted'
            nxt = champion_step(a, c)
            assert nxt is not None
            a, c = nxt
            bulks += 1
            calls += 1
            continue
        if a % 2 == 0 and a <= c:
            nxt = champion_step(a, c)
            assert nxt is not None and nxt[0] == 1
            return 'reset', nxt[1], calls+1, bulks
        if a <= c:
            assert a > 1 and a % 2 == c % 2 == 1
            return 'J', (a,c), calls, bulks
        if a == c+2 and c % 4 == 3:
            return 'E', (a,c), calls, bulks
        assert champion_step(a, c) is None
        return 'halt', None, calls+1, bulks


def verify_scanner_controls():
    controls = (
        ((11,1), ('reset',11,2,2)),  # bulk lands on a=1: no extra step
        ((9,1), ('halt',None,2,1)),  # terminal after one bulk
        ((23,1), ('E',(13,11),2,2)), # stop before exceptional restart
        ((21,1), ('J',(11,11),2,2)), # stop before ordinary jump
        ((3,1), ('reset',7,2,1)),    # a=0 followed by allowed R
        ((1,7), ('reset',7,0,0)),    # already on the reset axis
    )
    for start, expected in controls:
        assert scan_bulk(*start, bulk_limit=10) == expected


def one_passage(seed, m):
    """Stop at a reset, halt, or first post-header J/E; never assume return."""
    p, z = 3**m, seed+2*m
    assert seed % 2 == 1 and -501 < z-K*p < 500*m
    a, c, calls = 1, seed, 0
    for _ in range(m):
        assert a % 2 == c % 2 == 1 and a <= c
        a, c = champion_step(a, c)
        calls += 1
        assert a > 1
    assert (a, c) == (2*p-1, z-p+1)
    bits = []
    for _ in range(6):
        bits.append(((c+7)//2) % 2)
        assert a >= 4*((c+1)//4)+3
        a, c = champion_step(a, c)
        calls += 1
        assert a > 1
    assert a % 4 == 3
    if a > c:
        assert a >= 4*((c+1)//4)+3
        a, c = champion_step(a, c)
        calls += 1
        assert a % 2 == 0 and 0 <= a < 16000 < c
        nxt = champion_step(a, c)
        assert nxt[0] == 1
        return 'reset', nxt[1], calls+1, None
    a, c = champion_step(a, c)
    calls += 1
    assert 1 <= c < 17000*m and a > c
    assert a+2*c == 2*z+35+4*sum(bits)
    assert 64*c == 2059*z-2187*p+14232+sum(w*e for w,e in zip(WEIGHTS,reversed(bits)))
    u,h = (a+2*c-1)//2,(a+1)//2
    constant = 20835+18*sum(w*e for w,e in zip((81,135,171,195,211),bits[1:]))
    assert 1995*u+64*h == 2187*p+constant
    assert u % 2 == 0 and h % 6 == 0
    header_right = c
    kind, result, extra_calls, bulks = scan_bulk(a,c,bulk_limit=3*m)
    assert bulks < 3*m
    return kind, result, calls+extra_calls, header_right


def reduce_entrance(seed, m):
    p = 3**m
    cusp, end = 2187*p//2059-2*m-500, 54*p//49-2*m-504
    assert cusp <= seed <= cusp+2*m+40
    b, lo, hi = capture(m)
    calls = 0
    for attempts in range(1, 230):
        if seed % 2 == 0:
            assert cusp <= seed < end
            return 'even', attempts-1, calls
        z = seed+2*m
        if lo <= z <= hi:
            word = 'J'*m+'L'*6+'J'+'L'*b+'R'
            nxt = seed+check_word(seed, word)
            assert nxt % 2 == 0 and cusp <= nxt < end
            calls += len(word)
            assert len(word) <= 4*m+8
            return 'capture', attempts, calls
        assert z < lo
        kind, result, count, header_right = one_passage(seed, m)
        assert count <= 4*m+8
        calls += count
        if kind != 'reset':
            assert kind in {'halt','J','E'}
            return kind, attempts, calls
        assert 2*m+20 <= result-seed <= Fraction(31*m+63,2)
        seed = result
    raise AssertionError('the proved outer rank did not terminate')




KAPPA = Fraction(2187, 2059)
CYCLE = (225, 31, 97, 157)
OFFSETS = (22, 26, 20, 28)
BITS = ('0000001', '1000011', '0000000', '0111100')


def verify_residue_family():
    assert pow(3, 4480, 2059 * 256) == 1
    assert 4480 % 128 == 0
    m, p = 20, 3**20
    q = 2187*p // 2059
    assert 2187*p % 2059 == 1895
    assert q % 256 == 124
    for index, residue in enumerate(CYCLE):
        c = (residue+2*m-p+1) % 256
        bits = []
        for _ in range(7):
            bits.append(((c+7)//2) % 2)
            c = 6*((c+1)//4)+5
        assert ''.join(map(str, bits)) == BITS[index]
        assert 20+2*sum(bits) == OFFSETS[index]
        assert (residue+2*m+OFFSETS[index]) % 256 == CYCLE[(index+1) % 4]
    # Exponential corridor margin holds at m=20 and grows thereafter.
    assert (KAPPA-Fraction(24, 23))*p > 4*m+20


def verify_family_member(m):
    assert m >= 4500 and m % 4480 == 20
    p = 3**m
    q = 2187*p // 2059
    a = 24*p // 23
    cusp = q-2*m-500
    y = q-2*m+141
    x = y-(2*m+28)
    assert 2187*p % 2059 == 1895 and q % 256 == 124
    assert y % 256 == 225 and x % 256 == 157
    assert a < x < cusp < y <= cusp+2*m+40
    assert Fraction(x+2*m) < KAPPA*p-20
    old_word = 'J'*m+'L'*7+'R'
    assert x+check_word(x, old_word) == y
    left, right, bits = prefix(y, m)
    assert bits == (0,)*6
    assert (left, right) == (2*q-9141, 4729)
    assert left+2*right == 2*q+317
    # Backtrack many complete residue cycles arithmetically, then at most
    # three individual predecessors, as in the analytical entrance proof.
    stride = 8*m+96
    assert stride % 256 == 0
    periods = (y-a)//stride
    point, index = y-periods*stride, 0
    for _ in range(4):
        previous_index = (index-1) % 4
        previous = point-(2*m+OFFSETS[previous_index])
        if previous < a:
            break
        point, index = previous, previous_index
    else:
        raise AssertionError('a complete additional cycle fits')
    assert a <= point <= a+2*m+28
    assert point % 256 == CYCLE[index]
    assert point+2*m <= KAPPA*p-20
    assert check_word(point, old_word) == 2*m+OFFSETS[index]
    # Replaying the entrance and the final edge checks guards. The huge
    # middle flight follows from the cycle and the proved corridor bounds.
    return {'m': m, 'mass_bits': (left+2*right).bit_length(),
            'incoming_offset': point-a, 'cusp_offset': y-cusp,
            'fixed_right': right}


def verify_reinjection_intervals():
    xi = Fraction(81, 145)
    scale = Fraction(4, 729)
    assert (4*xi+405)/729 == xi
    for n in (1, 2, 3, 8):
        low = xi+scale**n*(Fraction(1, 3)-xi)
        high = xi+scale**n*(Fraction(5, 9)-xi)
        assert 0 < low < high < 1
        assert high-low == Fraction(2, 9)*scale**n
        for start in ((3*low+high)/4, (low+high)/2, (low+3*high)/4):
            x = start
            for _ in range(n):
                assert Fraction(5, 9) < x < 1
                x = (9*x-5)/4
                for _ in range(4):
                    assert 0 < x < Fraction(1, 3)
                    x *= 3
            assert Fraction(1, 3) < x < Fraction(5, 9)
    return 4



def audit():
    verify_constants()
    verify_lanes()
    verify_scanner_controls()
    total = 0
    stops = set()
    for m in (20, 35, 36, 292, 4500):
        p = 3**m
        cusp = 2187*p//2059-2*m-500
        for seed in sorted({cusp, cusp+1, cusp+2*m+39, cusp+2*m+40, cusp+m}):
            kind, attempts, calls = reduce_entrance(seed, m)
            assert attempts <= 229 and calls <= 229*(4*m+8)
            stops.add(kind)
            total += 1
    verify_residue_family()
    for m in (4500, 8980):
        verify_family_member(m)
    intervals = verify_reinjection_intervals()
    print("Verified first-cusp constants, 32 lanes, and six scalar stopping controls.")
    print("Focused entrance reductions:", total, "outcomes:", sorted(stops))
    print("Verified two genuine incoming lifts and", intervals, "reinjection cylinders.")


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run without -O for verification.")
    audit()
