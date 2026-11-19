"""Check every odd primitive guard contact at the nine-mass crossing H-10,000,000."""
from collections import Counter
from fractions import Fraction
from functools import cache
from itertools import product
from math import comb

from check_bb33 import champion_step
from halting_collar_758 import FAR
from odd_header_entry_758 import read_table
from scale_clauses_758 import H
from target_basin_758 import NEAR
from target_shadow_758 import C, D, POWER

CROSSING = H-10_000_000


@cache
def primitive_return(v, mass):
    """Follow only the original counter map, including the seed when v=1."""
    a,c = 2*v-1,mass-v+1
    for calls in range(618):
        if a == 1:
            assert H-FAR <= c <= H-NEAR
            return calls,c-mass
        state = champion_step(a,c)
        assert state is not None
        a,c = state
    raise AssertionError((v,mass,'no basin return within 617 calls'))


def verify():
    ties = read_table('odd_header_ties_758.tsv','r h')
    assert len(ties) == 264 and CROSSING%2
    cases = Counter()
    max_calls = max_gain = (0,0,0,0)
    for _,v in ties:
        for u in range(CROSSING,CROSSING+9):
            if u%2 != v%2:
                continue
            h,j = v,0
            while h <= u:
                w = u-2*j
                assert w>=v>0 and w%2 and 2*v-1>0
                # Every one of the j inverse jumps exists: its forward
                # guard is output h <= output u, preserved on dividing h
                # by three and subtracting two from u.
                calls,gain = primitive_return(v,w)
                assert v==1 or calls>j
                cases[(u-h+1)%4] += 1
                max_calls = max(max_calls,(calls,v,u-CROSSING,j))
                max_gain = max(max_gain,(gain,v,u-CROSSING,j))
                h *= 3
                j += 1
    assert set(cases)=={1,3} and sum(cases.values())==350_095
    assert primitive_return.cache_info().currsize==71_075
    assert max_calls==(617,14_041_887_462_289,8,227)
    assert max_gain==(1341,14_041_887_462_289,8,227)
    print(f'{sum(cases.values()):,} states, with odd right residues {dict(cases)}.')
    print('71,075 primitive predecessors. Maximum 617 calls and 1,341 gain from a predecessor.')


def ordinary_word(v, distance):
    """Read the exact first return word at a primitive predecessor."""
    w = H-distance
    a,c = 2*v-1,w-v+1
    word = []
    for _ in range(800):
        if a==1:
            return ''.join(word)
        assert c%2
        if a<=c:
            letter = 'J' if a%2 else 'R'
        else:
            assert a >= 4*((c+1)//4)+3
            letter = 'L'
        word.append(letter)
        a,c = champion_step(a,c)
    raise AssertionError('long ordinary word')


def outer_interval():
    near,far = 61_410_569_303_845_097_640,FAR-FAR%2
    ties = read_table('odd_header_ties_758.tsv','r h')
    bounds = []
    for _,v in ties:
        if v==1:
            continue
        word = ordinary_word(v,near)
        assert ordinary_word(v,far)==word
        assert word.endswith('LR')
        groups = word[:-2].replace('LL','P')
        assert set(groups)<={'J','P'}
        bounds.append(2*groups.count('J')+9*groups.count('P')+7)
    assert max(bounds)==1243 and near-1243>=NEAR
    v = 120_423_828_604_033
    assert ordinary_word(v,near-2)!=ordinary_word(v,near)
    print(f'{far-near+1:,} mass levels in the outer interval. Largest word gain bound {max(bounds):,}.')


def word_count():
    """Count guaranteed distinct complete words from a single odd primitive."""
    v,r = 14_365_291,30
    k,s = 307-r,239
    angle = Fraction(D*v,3**r)
    x = angle
    first = ''
    while x != Fraction(5,9):
        if x < Fraction(1,3):
            first += 'J'
            x *= 3
        else:
            assert x > Fraction(5,9)
            first += 'LL'
            x = (9*x-5)/4
    assert len(first)==r-2 and first.count('L')==26
    contraction = Fraction(4**14,3**r)
    slope = angle/contraction
    shift = Fraction(C,D)-2*k
    U = Fraction(POWER,D)

    # A target direction in (5/9,1) is obtained to within error by taking
    # the nearest even integer distance. The physical guard test adds the
    # much smaller aligned clearance requirement (FAR+2600)/U.
    def ideal_distance(x):
        return U*x/(3**s*slope)-shift

    assert NEAR+2488 < ideal_distance(Fraction(5,9))-1
    assert ideal_distance(1)+1 < FAR
    error = (slope+14/contraction)*3**s/U
    need = error+(FAR+2600)/U
    total = 0
    for n in range(50):
        included = sum(comb(n,p) for p in range(n+1)
                       if Fraction(4,81)*Fraction(1,3)**(n-p)*Fraction(4,9)**p > need)
        total += included
    assert Fraction(4,81)*Fraction(4,9)**49 <= need
    assert total==3_544_067_762_102
    # Literal tests include the endpoints of a sparse selection of long
    # words and every five-letter word. The binomial proof covers the rest.
    probes = ['J'*35,'P'*48,'JP'*20,'P'*30+'J'*10]
    probes.extend(''.join(w) for w in product('JP',repeat=5))
    for word in probes:
        x = Fraction(4,9)
        for letter in reversed('P'+word):
            x = x/3 if letter=='J' else (4*x+5)/9
        margin = Fraction(4,81)*Fraction(1,3)**word.count('J')*Fraction(4,9)**word.count('P')
        assert margin > need
        distance = 2*round(ideal_distance(x)/2)
        assert ordinary_word(v,distance) == 'J'*k+first+'LL'+'J'*s+('P'+word).replace('P','LL')+'LR'
    print(f'At least {total:,} distinct complete first-return words inside the collar for v={v:,}.')


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('run without -O for verification')
    verify()
    outer_interval()
    word_count()
