#!/usr/bin/env python3
"""Exact affine-period test for odd/odd excursions of #758/#153."""
from fractions import Fraction
from itertools import product

from check_bb33 import HALTING_TARGET as H, champion_step


# A pair of ordinary bulk moves uses the input residue d=(c-1)/2 mod 4.
PAIRS = ((5,20), (9,35), (7,26), (7,29))
J = 4


def period_data(word):
    """u'=u+V, d'=(Q*d+A*u+C)/M and the invariant line d=lambda*u+gamma."""
    V, Q, A, C, M = 0, 1, 0, 0, 1
    for symbol in word:
        if symbol == J:
            Q, A, C = 3*Q, 3*A-M, 3*C+(1-V)*M
            V += 2
        else:
            v, b = PAIRS[symbol]
            Q, A, C, M = 9*Q, 9*A, 9*C+b*M, 4*M
            V += v
    slope = Fraction(-A, Q-M)
    intercept = (M*slope*V-C)/(Q-M)
    return V, Q, A, C, M, slope, intercept


def verify_algebra():
    from math import gcd
    assert 3**292 > H//2+8
    for length in range(1, 6):
        for word in product(range(5), repeat=length):
            v, q, a, b, m, slope, intercept = period_data(word)
            assert gcd(q,m) == 1 and 0 <= slope <= Fraction(1,2)
            assert -7 <= intercept <= 0
            scale = (q-m)**2
            assert (scale*slope).denominator == (scale*intercept).denominator == 1
            # Verify the defect identity at three affinely independent points.
            for u, d in ((0,0), (1,0), (0,1)):
                d1 = Fraction(q*d+a*u+b, m)
                z = scale*(d-slope*u-intercept)
                z1 = scale*(d1-slope*(u+v)-intercept)
                assert m*z1 == q*z
            if word[0] != J:
                assert slope.numerator % 4 == 0
            if any(x != J for x in word):
                assert gcd(slope.denominator, 6) == 1


def ud(a,c):
    assert a % 2 == c % 2 == 1
    return (a+2*c-1)//2, (c-1)//2


def segments(seed):
    """Split one true first-return excursion at E; an incomplete bulk pair ends a segment."""
    a, c = 1, seed
    if c % 2 == 0:
        a, c = champion_step(a,c)
    word, states = [], [ud(a,c)]
    while True:
        q = (c+1)//4
        if a >= 4*q+3:
            symbol = ((c-1)//2) % 4
            a,c = champion_step(a,c)
            q = (c+1)//4
            if a < 4*q+3:
                yield word, states, None
                final = champion_step(a,c)
                assert final is not None and final[0] == 1
                yield [], [], final[1]
                return
            a,c = champion_step(a,c)
        elif a <= c:
            symbol = J
            a,c = champion_step(a,c)
        else:
            yield word, states, None
            assert c % 4 == 3 and a == c+2
            a,c = champion_step(a,c)
            word, states = [], [ud(a,c)]
            continue
        word.append(symbol)
        states.append(ud(a,c))
        if a == 1:
            yield word, states, c
            return


def translation(word, start, end):
    """Test for a mixed ordinary affine translation along this observed fine word."""
    u, d = start
    u1, d1 = end
    numerator, denominator = d1-d, u1-u
    if not 0 < 2*numerator < denominator:
        return False
    # Propagate the proposed direction with denominator held fixed. At a P
    # phase divisibility must survive, since all its cyclic denominators are odd.
    initial = numerator
    for symbol in word:
        if symbol == J:
            if 3*numerator <= denominator:
                return False
            numerator = 3*numerator-denominator
        else:
            if numerator % 4 or 9*numerator >= 2*denominator:
                return False
            numerator = 9*numerator//4
    if numerator != initial:
        return False
    v, _, _, _, _, slope, intercept = period_data(word)
    assert v == denominator and d == slope*u + intercept
    return True


def probe(word, states, check_powers):
    """Check every translation candidate, and optionally all mixed or pure word powers."""
    n = len(word)
    largest = [0,0]
    length = [0]
    for symbol in word:
        length.append(length[-1]+(1 if symbol == J else 2))
    for i in range(n):
        u, d = states[i]
        for j in range(i+1,n+1):
            v, e = states[j]
            if 0 < 2*(e-d) < v-u:
                assert not translation(word[i:j], states[i], states[j])
        if check_powers:
            for size in range(1,(n-i)//3+1):
                w = word[i:i+size]
                if w != word[i+size:i+2*size]:
                    continue
                k = i+2*size
                while k+size <= n and w == word[k:k+size]:
                    k += size
                if k == i+2*size:
                    continue
                score = (length[i+size]-length[i])*((k-i)//size-2)
                largest[0] = max(largest[0],score)
                if J in w and any(x != J for x in w):
                    largest[1] = max(largest[1], score)
                assert 2*3**score < states[k][0] + 14
    return largest


def coarse_pj_candidates(limit, repeats):
    """All deviations permitting this many bulk-pair/J copies at masses u<=limit."""
    # e'=(27/4)*e + c, with 225<=c<=1503/4.
    reach = Fraction(4,27)**repeats
    low = -4*limit*reach - Fraction(1503,23)*(1-reach)
    high = Fraction(15,2)*limit*reach - Fraction(900,23)*(1-reach)
    first = -((-low.numerator)//low.denominator)
    last = high.numerator//high.denominator
    possible = []
    for error in range(first,last+1):
        e = error
        drift = 0
        for _ in range(repeats):
            v,b = PAIRS[(3*e) % 4]
            assert (9*e+23*b) % 4 == 0
            e = 3*((9*e+23*b)//4-9*v)+15
            drift += v+2
        # Among integral d, the largest feasible u maximizes every guard margin.
        u = limit-drift
        u -= (u+pow(4,-1,23)*error) % 23
        d = (4*u+error)//23
        assert 23*d == 4*u+error
        a, c = 2*u-4*d-1, 2*d+1
        if min(a,c) < 1:
            continue
        for _ in range(repeats):
            for _ in range(2):
                if a < 4*((c+1)//4)+3:
                    break
                a,c = champion_step(a,c)
            else:
                if a % 2 and a <= c:
                    a,c = champion_step(a,c)
                    continue
            break
        else:
            assert (a+2*c-1)//2 == u+drift <= limit
            possible.append(error)
    return possible


def verify_coarse():
    assert coarse_pj_candidates(H,170) == []
    assert coarse_pj_candidates(H,169) == [-61,-46]
    smaller = 3_706_040_379_353_000
    assert coarse_pj_candidates(smaller,21) == []
    assert coarse_pj_candidates(smaller,20) == [-61,-46]


def check_blank():
    seed = 2*3**32-20
    assert seed == 3_706_040_377_703_662
    largest = [0,0]
    hits = [None,None]
    for _ in range(8192):
        source = seed
        for word, states, result in segments(source):
            if word:
                current = probe(word, states, True)
                for i, val in enumerate(current):
                    if val > largest[i]:
                        largest[i], hits[i] = val, source
            if result is not None:
                assert result > source
                seed = result
        assert seed != source
    assert seed == 3_706_040_379_351_922
    assert largest == [30,3] and hits == [3_706_040_377_703_662, 3_706_040_378_103_754]
    print("First 8192 returns from the blank checkpoint:", seed, largest, hits)
    return seed,largest,hits


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run without -O to execute the checks.")
    verify_algebra()
    verify_coarse()
    check_blank()
