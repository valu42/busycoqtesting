"""Replay the cross-scale three-bulk gate, its exit lift and its blank checkpoints."""
import argparse
from fractions import Fraction
from math import ceil
from pathlib import Path
import sys

from bulk_digit_cycles_758 import flags
from check_bb33 import champion_step, first_return
from check_blank_crossings import cuts as early_cuts
from check_confluence import itinerary
from check_power_crossings_758 import windows as power_windows
from next_gate_after_fifth_758 import CUTS as power35_cuts
from power36_followon_758 import CUTS as power36_cuts
from power_gates_758 import coalesce, coarse_return, gate_exits
from target_clock_758 import first_pass, timed_return


TABLE = Path(__file__).with_name('three_bulk_scale_transport_758.tsv')
CYCLES = (
    ((7,), (2,), (4,)), ((0,),), ((1,4,6),), ((2,5),),
    ((0,3),), ((4,1,7),), ((5,),), ((6,), (1,), (3,)),
)


def corridor(m):
    """First and last even starts having the complete word I J^m L^3 R."""
    p = 3**m
    limits = []
    for residue in range(4):
        n1 = (3*residue+3)//2
        n2 = (3*n1+3)//2
        # At n=4i+r the three quotients are 4i+r, 6i+n1, 9i+n2.
        first = (4*p-15-4*residue-4*n1-10*n2+129)//130
        last = (p-3-residue-n1-n2)//19
        limits.append((4*first+residue,4*last+residue))
    first = min(low for low,_ in limits)
    last = max(high for _,high in limits)
    return 2*p+4*first-2*m-6, 2*p+4*last-2*m-4


def exclude_three_bulk_halts():
    # Both launch parities have a=2h-1 with h=3^m or 2*3^m.
    # At n=4i+r the final gap after three bulks is 2h-130i-E_r-15.
    residues = set()
    for r in range(4):
        n1 = (3*r+3)//2
        n2 = (3*n1+3)//2
        e = 4*r+4*n1+10*n2
        residues.update((e+16,e+18))
    assert pow(3,12,65) == 1
    required = {t%130 for t in residues}
    assert all(2*b*pow(3,m,65)%130 not in required for b in (1,2) for m in range(12))


def exit_offsets(m):
    """All j such that the first even exit from a deep start can equal high+2j."""
    p = 3**m
    low,high = corridor(m)
    assert 2*p <= low < high < 3*p-2*m-6-4*(m+10)
    assert high-low > 50*(2*m+20)
    y_end = high//2-p+m+6
    increments = [m+7+flags(y,3)[1].bit_count() for y in range(8)]
    cycles = set()
    seen = set()
    for start in range(8):
        path = []
        y = start
        while y not in seen and y not in path:
            path.append(y)
            y = (y+increments[y])%8
        if y in path:
            cycle = path[path.index(y):]
            cycles.add(frozenset(cycle))
        seen.update(path)
    assert cycles == {frozenset(c) for c in CYCLES[m%8]}
    result = set()
    for cycle in CYCLES[m%8]:
        for i,y in enumerate(cycle):
            delta = increments[y]
            phase = (y+delta)%8
            assert phase == cycle[(i+1)%len(cycle)]
            j0 = (phase-y_end-1)%8+1
            result.update(range(j0,delta+1,8))
    return result


def passage(m, seed):
    """Calculate the exact exit and number of returns using at most 16 phase edges."""
    low,high = corridor(m)
    assert low <= seed <= high-10*(2*m+20)
    count = seed%2
    if count:
        seed += 2*m+5+2*(seed%4 == 3)
    y = seed//2-3**m+m+6
    end = high//2-3**m+m+6
    seen = {}
    checked = 0
    while y <= end:
        phase = y%8
        if phase in seen:
            old,old_count = seen[phase]
            stride = y-old
            copies = (end-y)//stride
            y += copies*stride
            count += copies*(count-old_count)
            # The remaining partial lap begins at this same phase.
            seen.clear()
        seen[phase] = y,count
        y += m+7+flags(phase,3)[1].bit_count()
        count += 1
        checked += 1
    assert checked <= 16
    return high+2*(y-end),count


def timed_passage(m, seed):
    """Sum the quadratic raw-clock polynomial on every phase of the physical cycle."""
    low,high = corridor(m)
    expected = passage(m,seed)
    even,head_cost = timed_return(seed) if seed%2 else (seed,0)
    exit_seed,count,elapsed = first_pass(even,low,high,16,2*m+20)
    assert expected == (exit_seed,count+seed%2)
    return exit_seed,count+seed%2,elapsed+head_cost


def departure(m,j):
    """State at the small right counter after the two bulks and jump or exception."""
    p = 3**m
    _,high = corridor(m)
    s = high+2*j
    a,c = 4*p-1,s-2*p+2*m+5
    for _ in range(2):
        assert a >= 4*((c+1)//4)+3
        a,c = champion_step(a,c)
    assert a%2 and a < 4*((c+1)//4)+3
    state = champion_step(a,c)
    assert state is not None and state[0] > 1
    return state


def bulk_end(state):
    """Count the pure bulks and recognize an immediate live reset at the end."""
    a,c = state
    x = (c+1)//4+3
    n = 0
    while a >= 4*x-9:
        a -= 4*x-9
        c = 6*x-13
        x = 3*x//2
        n += 1
    return n, n%2 == 1 and a <= c


def exceptional_band(m, numerator=26, denominator=5, precision=1000):
    """Test the whole mass band by enclosing its odd endpoints; bulk costs are fixed."""
    p = 3**m
    divisor = precision*denominator
    low = ((precision-1)*numerator*p)//divisor
    high = ((precision+1)*numerator*p+divisor-1)//divisor
    low -= (low-1)%2
    high += (1-high)%2
    n0,live0 = bulk_end((low+6,1))
    n1,live1 = bulk_end((high+6,1))
    return n0 == n1 and live0 and live1


def one_bulk_band(m):
    """Check both parity words at both ends of the entrance to the doubled gate."""
    p = 3**m
    low,high = (183*p+99)//100,195*p//100
    # itinerary omits the first call: I for evens and the first J for odds.
    word = 'J'*(m-1)+'LR'
    for parity in (0,1):
        for seed in (low+(parity-low)%2, high-(high-parity)%2):
            assert itinerary(seed)[0] == word
            assert coarse_return(m,seed,2) == first_return(seed) <= seed+2*m+9


def finite_orbit_choice(m):
    """Give the whole-band orbit dichotomy explicit constants on the archived scales."""
    p = 3**m
    low,high = corridor(m)
    for a,b in ((5,1),(113,20),(92,25)):
        if not exceptional_band(m,a,b,10_000):
            continue
        center = Fraction(a*p,b)
        radius = center/10_000
        # A central exceptional call reaches a reset before leaving the full band.
        # The odd endpoints below already checked have this same pure-bulk count.
        w = int(center)
        n,live = bulk_end((w+(1-w)%2+6,1))
        assert live and 9*(n+2) < radius/2
        assert center+radius < Fraction(566*p,100)
        assert 60_000*(radius-26) > 18*p
        smallest = (center-radius-1)/2
        largest = (center+radius-1)/2
        if (a,b) == (92,25):
            assert 100*smallest >= 183*p and 100*largest <= 185*p
            last = 195*p//100
            gain = 2*m+9
            cut = (19*p+9)//10
            assert largest < cut < cut+gain <= min(last,2*p-2*m-6-34*(4*m+40))
        else:
            assert low <= smallest and largest <= high-10*(2*m+20)
            # Allow one short return for an odd entrant.
            largest += 2*m+7
            last,gain = high,2*m+20
        assert 200*m*(last-largest) >= p*gain
        if m == 36:
            assert (a,b,n) == (92,25,93)
            assert ceil(center+radius) == 552_403_492_718_746_061
            assert ceil((radius-26)/18) == 3_068_601_432_738
            assert ceil((last-largest)/gain) == 203_491_265_058_954
            assert coalesce(gate_exits(36,2),1301) == (300_189_270_594_119_530,1301)
        return
    raise AssertionError('no exceptional band covered this exponent')


def verify_bands(m):
    one_bulk_band(m)
    finite_orbit_choice(m)
    assert any(exceptional_band(n) for n in range(m,m+3))
    assert any(exceptional_band(n,a,b,10_000) for n in (m,m+1) for a,b in ((5,1),(113,20)))


def lift(m):
    p = 3**m
    delta = (3**72-1)*p
    low,high = corridor(m)
    low2,high2 = corridor(m+72)
    assert 65*(low2-low+144) == 162*delta
    assert 19*(high2-high+144) == 54*delta
    old,new = exit_offsets(m),exit_offsets(m+72)
    assert old <= new and len(new)-len(old) == 9*sum(map(len,CYCLES[m%8]))
    counts = [0,0]
    for j in sorted(old):
        a,c = departure(m,j)
        a2,c2 = departure(m+72,j)
        assert c == c2 and 19*(a2-a) == 108*delta
        assert abs(19*a-108*p) <= 19*40*(m+10) and 1 <= c <= 27*(m+10)
        n0, return0 = bulk_end((a,c))
        n1, return1 = bulk_end((a2,c2))
        a3,c3 = departure(m+144,j)
        assert c3 == c and 19*(a3-a) == 108*(3**144-1)*p
        _, return2 = bulk_end((a3,c3))
        assert return0 or return1 or return2
        extra = n1-n0
        assert extra in (195,196)
        counts[extra-195] += 1
    return counts


def blank_cut(m):
    if m <= 30:
        cuts = early_cuts('prefix')
    elif m == 31:
        cuts = early_cuts('second')
    elif m in (32,33):
        cuts = [b for _,b in power_windows('power33' if m == 32 else 'power34')]
    else:
        cuts = power35_cuts if m == 34 else power36_cuts
    low,high = corridor(m)
    return next(s for s in cuts if low <= s and s+5000 <= high-10*(2*m+20))


def verify(m, expected):
    low,high = corridor(m)
    verify_bands(m)
    # Endpoint order already proves every intervening guard. Check sharpness
    # independently with the unbatched word evaluator at its four edges.
    word = 'J'*m+'LLLR'
    assert all(itinerary(s)[0] == word for s in (low,high))
    assert all(itinerary(s)[0] != word for s in (low-2,high+2))
    offsets = exit_offsets(m)
    count,steps,checkpoint = expected
    assert len(offsets) == count
    for seed in (low,low+1):
        end,n,raw = timed_passage(m,seed)
        assert (end-high)//2 in offsets and n > 0 and raw > 0
    # Independently walk the final short stretch with the original scalar rules.
    for start in (high-10*(2*m+20), high-10*(2*m+20)-1):
        end,n = passage(m,start)
        s = start
        for _ in range(n):
            assert s <= high
            s = first_return(s)
        assert s == end > high
    assert coalesce((high+2*j for j in offsets),steps) == (checkpoint,steps)
    if m <= 35:
        blank_cut(m)
    return lift(m)


def main():
    # The user-requested exact clock can have arbitrarily many decimal digits.
    if hasattr(sys,'set_int_max_str_digits'):
        sys.set_int_max_str_digits(0)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--all',action='store_true',help='replay all 273 mergers and their lifted departures')
    parser.add_argument('--bands',action='store_true',help='check all 273 finite passage alternatives without replaying their mergers')
    parser.add_argument('--m',type=int,help='replay a single archived exponent from 20 to 292')
    parser.add_argument('--passage',type=int,metavar='EXPONENT',help='compute an exact crossing and raw time at any exponent >= 20')
    parser.add_argument('--seed',type=int,help='deep entrance for --passage (defaults to the lower edge)')
    args = parser.parse_args()
    if not __debug__ or sum((args.all,args.bands,args.m is not None,args.passage is not None)) > 1:
        parser.error('enable assertions and choose at most one selector')
    if args.seed is not None and args.passage is None:
        parser.error('--seed requires --passage')
    if args.passage is not None:
        m = args.passage
        if m < 20:
            parser.error('the corridor theorem begins at exponent 20')
        low,high = corridor(m)
        seed = low if args.seed is None else args.seed
        if not low <= seed <= high-10*(2*m+20):
            parser.error('the chosen entrance is outside the deep interval')
        end,count,raw = timed_passage(m,seed)
        print(f'm={m}, entrance {seed}, exit {end}, first returns {count}, raw steps {raw}.')
        return
    if args.m is not None and not 20 <= args.m <= 292:
        parser.error('the merger table covers exponents 20 through 292')
    with TABLE.open() as stream:
        assert next(stream).split() == ['m','exits','merger_edges','reset']
        data = [tuple(map(int,line.split())) for line in stream]
    assert [m for m,*_ in data] == list(range(20,293))
    table = {m:(count,steps,seed) for m,count,steps,seed in data}
    assert sum(row[0] for row in table.values()) == 12_621
    assert sum(row[1] for row in table.values()) == 1_403_139
    assert max(row[1] for row in table.values()) == 20_347
    exclude_three_bulk_halts()
    # Exact margins needed to compare the two cumulative bulk thresholds.
    assert 1003*3**195 < 999*2**195*3**72
    assert 998*3**196 > 1003*2**196*3**72
    assert 1_000_000*(20+10) <= 3**20
    # 195.08 < log_(3/2)(3^72) < 195.09 and (3/2)^0.01 > 1.003.
    assert 3**19508 < 2**19508*3**7200 and 3**19509 > 2**19509*3**7200
    assert 2*1003**100 < 3*1000**100
    assert 3**2709 < 2**2709*3**1000 and 3**2710 > 2**2710*3**1000
    assert 3**301*100**1000 < 2**301*113**1000
    assert 3**302*100**1000 > 2**302*113**1000
    assert 3**755*92**1000 < 2**755*125**1000
    assert 3**756*92**1000 > 2**756*125**1000
    assert 2*5001**1000 < 3*5000**1000
    if args.bands:
        for m in table:
            verify_bands(m)
        print(f'Verified finite passage alternatives at all {len(table)} power scales.')
        return
    chosen = ([args.m] if args.m is not None else range(20,293) if args.all else range(20,36))
    totals = [0,0]
    for m in chosen:
        counts = verify(m,table[m])
        totals = [a+b for a,b in zip(totals,counts)]
        if args.m is not None:
            print(f'm={m}: {table[m][0]} exits merge at {table[m][2]} in {table[m][1]} edges.')
    print(f'Replayed {len(chosen)} scale mergers. Lifted departures with 195/196 extra bulks: {totals}.')


if __name__ == '__main__':
    main()
