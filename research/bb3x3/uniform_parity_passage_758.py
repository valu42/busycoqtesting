"""Audit the parameterized mixed-word passage at the 2187/2059 cusp.

The proof for every admitted (m,b) is in UNIFORM_PARITY_PASSAGE_758.md.
This small checker verifies its rational constants and selected exact examples;
it does not replace the proof by an exponent or fine-word census.
"""
from argparse import ArgumentParser
from fractions import Fraction

from check_bb33 import champion_step, first_return
from scale_clauses_758 import check_word


KAPPA = Fraction(2187, 2059)
WEIGHTS = (320, 608, 1040, 1688, 2660, 4118)


def ceil_fraction(x):
    return -((-x.numerator) // x.denominator)


def source_bounds(m, b):
    """Exact rational z=s+2m bounds; every integer seed in them is admitted."""
    if m < 20 or b < 3 or b % 4 != 3:
        raise ValueError("require m>=20 and b>=3 congruent to 3 modulo 4")
    p, n, d = 3**m, 3**b, 2**b
    if p*d < 1000*n:
        raise ValueError("require 3^m/(3/2)^b >= 1000")
    low = Fraction(6561*n*p - 44040*n + (3584+576*b)*d,
                   6177*n - 128*d)
    high = Fraction(2187*n*p - 25498*n + (2720+160*b)*d,
                    2059*n - 64*d)
    return low, high


def source_interval(m, b):
    low, high = source_bounds(m, b)
    return ceil_fraction(low)-2*m, high.numerator//high.denominator-2*m


def corridor(m):
    p = 3**m
    return 2187*p//2059-2*m-500, 54*p//49-2*m-504


def prefix(seed, m):
    """Apply J^m L^6 J, returning the state and the six exact carry bits."""
    assert seed % 2
    p, z = 3**m, seed+2*m
    a, c = 1, seed
    for _ in range(m):
        assert a % 2 == c % 2 == 1 and a <= c
        a, c = champion_step(a, c)
        assert a > 1
    assert (a, c) == (2*p-1, z-p+1)
    carries = []
    for _ in range(6):
        carries.append(((c+7)//2) % 2)
        assert a >= 4*((c+1)//4)+3
        a, c = champion_step(a, c)
        assert a > 1
    assert a % 2 == c % 2 == 1 and a <= c
    a, c = champion_step(a, c)
    weighted = sum(w*e for w, e in zip(WEIGHTS, reversed(carries)))
    assert 64*c == 2059*z-2187*p+14232+weighted
    assert a+2*c == 2*z+35+4*sum(carries)
    assert a % 4 == 3 and c > 0
    return a, c, tuple(carries)


def verify_constants():
    """Rational inequalities used in the proof, with no exponent census."""
    r0 = Fraction(27, 8)
    assert sum(WEIGHTS) == 10434
    for j, w in enumerate(WEIGHTS, 1):
        assert w == 64*(6*Fraction(3, 2)**j-4)
    # b/r <= 3/r0 for every integer b>=3, since (b+1)/(3b/2)<=1.
    max_lower_correction = (3584+576*3)/r0
    min_lower_denominator = 6177-128/r0
    assert 128*KAPPA*1000-44040 > 0
    assert 64*KAPPA*1000-25498 > 0
    assert 128*KAPPA/min_lower_denominator < Fraction(9, 400)
    assert (-44040+max_lower_correction)/min_lower_denominator < -6
    assert 64*KAPPA/2059 > Fraction(33, 1000)
    assert Fraction(-25498, 2059) > -13
    assert Fraction(21, 2000)*1000-7 == Fraction(7, 2)
    assert (128*KAPPA*1000-44040)/6177 > 14
    assert (2720+160*3)/r0 < 25498
    assert 2187*r0/(2059*r0-64) == Fraction(59049, 55081)
    assert Fraction(59049, 55081) < Fraction(27, 25)
    assert 3*r0*min(WEIGHTS) > 256
    assert r0*min(WEIGHTS) > 128
    # The following inequalities persist for m>=20: replacing m by m+1
    # triples their exponential side and increases their positive linear side.
    m, p = 20, 3**20
    assert (665*(Fraction(2, 25)*p+1)+7685)/32 < 2*p-2
    assert Fraction(27, 1225)*p > Fraction(31*m+1073, 2)
    # Uniform even-corridor guard checks, using z in [kappa P-501,54P/49-505].
    zl, zh = KAPPA*p-501, Fraction(54, 49)*p-505
    assert 6*p-5*zh-62 > 4
    assert 18*p-19*zl <= 94
    assert 49*zh-54*p <= -616
    assert 162*p-155*zl <= 678
    # At least one captured lift per old residue cycle, for every m>=2200.
    qlo, qhi = 1000*Fraction(81, 16)**2, 1000*Fraction(81, 16)**3
    assert Fraction(21, 2000)*qlo-7 > 256
    assert 64*KAPPA*qhi/(2059-64/r0) < 4400
    assert 3**20*2**11 >= 1000*3**11  # hence b_max-8>=3
    assert (KAPPA-Fraction(24, 23))*p > 4*m+20
    assert 2187-2059*KAPPA == 0
    assert 2059*20-26650 > 64
    assert 6305*Fraction(24, 23) > 6561


def audit_example(m, b):
    low, high = source_bounds(m, b)
    first, last = source_interval(m, b)
    p, r = 3**m, Fraction(3, 2)**b
    q = p/r
    assert b < 3*m
    assert low > KAPPA*p+14
    assert high < Fraction(27, 25)*p
    assert high-low >= Fraction(21, 2000)*q-7 >= Fraction(7, 2)
    assert first < last
    c, e = corridor(m)
    even_word = 'I'+'J'*(m-1)+'LLJLR'
    for seed in (c+c%2, e-1-(e-1)%2):
        gain = check_word(seed, even_word)
        assert gain in range(2*m+14, 2*m+21, 2)
    samples = {first, last, (first+last)//2}
    samples |= {first+(1-first)%2, last-(last-1)%2}
    for seed in sorted(samples):
        if seed % 2:
            a, right, _ = prefix(seed, m)
            start_mass = a+2*right
            start_right = right
            high_carries = 0
            for _ in range(b):
                high_carries += ((right+7)//2) % 2
                assert a >= 4*((right+1)//4)+3
                a, right = champion_step(a, right)
                assert a > 1
            assert a % 4 == 2 and a <= right
            assert r*(start_right+7)-7 <= right <= r*(start_right+13)-13
            assert a+2*right == start_mass+5*b+4*high_carries
            state = champion_step(a, right)
            assert state[0] == 1
            nxt = state[1]
            gain = check_word(seed, 'J'*m+'L'*6+'J'+'L'*b+'R')
            assert nxt == seed+gain and nxt % 2 == 0
            assert gain <= 2*m+(9*b+63)//2
        else:
            gain = check_word(seed, even_word)
            nxt = seed+gain
            assert nxt % 2 == 0
        assert c <= nxt < e
        assert first_return(seed) == nxt
    return m, b, first, last, e, e+2*m+20


def largest_b(m):
    b = 3
    while 3**m*2**(b+4) >= 1000*3**(b+4):
        b += 4
    return b


def seam_audit(m):
    """Classify the old finite exit enclosure; this is not a blank phase claim."""
    c, e = corridor(m)
    bands = [(b, *source_interval(m, b)) for b in range(3, largest_b(m)+1, 4)]
    captured, uncaptured = set(), set()
    hits = set()
    for start in range(c+(1-c)%2, c+2*m+41, 2):
        seed, seen, hit = start, set(), None
        while seed % 2:
            assert seed not in seen and len(seen) < 10000
            seen.add(seed)
            for b, lo, hi in bands:
                if lo <= seed <= hi:
                    hit = b, seed
                    hits.add(hit)
            nxt = first_return(seed)
            assert nxt is not None and seed < nxt < e
            seed = nxt
        (captured if hit else uncaptured).add(start)
    return m, len(captured), len(uncaptured), tuple(sorted(hits))


def incoming_witness(m):
    """Construct a captured lift on one selected old-corridor residue cycle.

    The full intervening flight is certified by the positive periodic map,
    not simulated return by return. Only its entrance, last old return and
    mixed return are replayed here.
    """
    assert m >= 2200
    p, b = 3**m, largest_b(m)-8
    low, high = source_interval(m, b)
    entrance = 24*p//23
    gains = {}
    def charge(residue):
        if residue in gains:
            return gains[residue]
        right = (residue+2*m-p+1) % 256
        high_bits = 0
        for _ in range(7):
            high_bits += right % 4 == 3
            right = 6*((right+1)//4)+5
        gains[residue] = 2*m+20+2*high_bits
        return gains[residue]
    path, positions, residue = [], {}, 1
    while residue not in positions:
        positions[residue] = len(path)
        path.append(residue)
        residue = (residue+charge(residue)) % 256
    cycle = path[positions[residue]:]
    assert cycle
    old_word = 'J'*m+'L'*7+'R'
    new_word = 'J'*m+'L'*6+'J'+'L'*b+'R'
    _, edge = corridor(m)
    y = low+(cycle[0]-low) % 256
    assert low <= y <= high and y % 2
    last = y-gains[cycle[-1]]
    assert last > entrance and last+2*m < KAPPA*p-20
    assert last+check_word(last, old_word) == y
    stride = sum(gains[r] for r in cycle)
    assert stride > 0 and stride % 256 == 0
    periods = (y-entrance)//stride
    assert periods > 0
    point, index = y-periods*stride, 0
    for _ in range(len(cycle)):
        previous_index = (index-1) % len(cycle)
        previous = point-gains[cycle[previous_index]]
        if previous < entrance:
            break
        point, index = previous, previous_index
    else:
        raise AssertionError('a whole backwards period still fit')
    assert entrance <= point <= entrance+2*m+34
    assert point % 256 == cycle[index]
    assert point+2*m <= KAPPA*p-20
    assert check_word(point, old_word) == gains[point % 256]
    nxt = y+check_word(y, new_word)
    assert nxt % 2 == 0 and nxt < edge
    return m, b, len(cycle), stride, point-entrance, y-(2187*p//2059-2*m)


def verify():
    verify_constants()
    rows = []
    for m in (20, 35, 36, 100, 292, 1000):
        for b in sorted({3, 7, largest_b(m)}):
            rows.append(audit_example(m, b))
    return rows


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--seam-audit', action='store_true',
                        help='classify the inherited m=35,36 cusp exit enclosures')
    parser.add_argument('--incoming-audit', action='store_true',
                        help='construct a captured lift on one cycle at m=2200,2201')
    args = parser.parse_args()
    if not __debug__:
        parser.error('enable assertions')
    rows = verify()
    print('Verified rational constants and', len(rows), 'selected parameter examples.')
    for m in (35, 36):
        row = next(row for row in rows if row[0] == m and row[1] == largest_b(m))
        print('Example m,b,source_first,source_last,output_low,output_high:', *row)
    if args.seam_audit:
        for m in (35, 36):
            print('Inherited seam m,captured,uncovered,(b,seed) hits:', seam_audit(m))
    if args.incoming_audit:
        for m in (2200, 2201):
            print('Incoming m,b,cycle length,stride,entrance offset,cusp offset:',
                  *incoming_witness(m))
