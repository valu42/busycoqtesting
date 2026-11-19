#!/usr/bin/env python3
"""Recover exact reset seeds for prescribed ordinary itineraries of #758."""
from fractions import Fraction
from itertools import product
from random import Random

from check_bb33 import HALTING_TARGET, champion_step


LEADING = 291


def witness(word, leading=LEADING):
    """Find a reset seed for a fine word beginning with a pair of (b) moves."""
    if not word or word[0] != "B":
        raise ValueError("the word must start with B")
    power = 3**leading
    # At each stage, u = t + gain and d = (slope*t + constant)/den.
    gain, slope, constant, den = 0, 1, -power, 2
    for letter in word:
        if letter == "J":
            slope = 3 * slope - den
            constant = 3 * constant + (1 - gain) * den
            gain += 2
        elif letter == "B":
            slope *= 9
            constant = 9 * constant + 20 * den
            den *= 4
            gain += 5
        else:
            raise ValueError(letter)

    # Impose integrality at all phases, then choose the solution closest
    # to the real root of d_final = u_final/4.
    residue = -constant * pow(slope, -1, den) % den
    numerator = den * gain - 4 * constant
    denominator = 4 * slope - den
    spacing = den * denominator
    assert spacing > 0
    index = (2 * (numerator - residue * denominator) + spacing) // (2 * spacing)
    t = residue + den * index
    return t - 2 * leading


def replay(seed, word, leading=LEADING):
    a, c = 1, seed
    for _ in range(leading):
        assert a % 2 == c % 2 == 1 and a <= c
        a, c = champion_step(a, c)
    assert a + 1 == 2 * 3**leading
    for letter in word:
        if letter == "J":
            assert a % 2 == c % 2 == 1 and a <= c
            a, c = champion_step(a, c)
        else:
            assert letter == "B"
            for _ in range(2):
                assert c % 4 == 1 and a >= c + 2
                a, c = champion_step(a, c)
        assert a > 1
    u, d = (a + 2 * c - 1) // 2, (c - 1) // 2
    assert 10 * min(d, u // 2 - d) >= 3**leading
    return seed


def shortlist(blocks, leading, parity, mass_limit=HALTING_TARGET):
    """Necessary seed interval from at most 397 coarse post-launch blocks."""
    if not blocks or blocks[0] != "P" or parity not in (0, 1):
        raise ValueError("expected a first bulk pair and an entry parity")
    # u=t+gain, h=(a+1)/2. Bound the translation separately for each residue.
    ratio, weight = Fraction(1), Fraction(0)
    low, high = Fraction(0), Fraction(0)
    min_gain = max_gain = 0
    for move in blocks[:397]:
        if move == "P":
            weight += ratio * Fraction(5, 9)
            low += ratio * Fraction(5*min_gain + 20, 9)
            high += ratio * Fraction(5*max_gain + 34, 9)
            min_gain += 5
            max_gain += 9
            ratio *= Fraction(4, 9)
        elif move == "J":
            min_gain += 2
            max_gain += 2
            ratio /= 3
        else:
            raise ValueError(move)
    h = (1 if parity else 2)*3**leading
    shift = 2*leading + (0 if parity else 4)
    lower = (h - high - ratio*mass_limit)/weight - shift
    upper = (h - low)/weight - shift
    first = max(1, -((-lower.numerator)//lower.denominator))
    first += (parity-first) % 2
    return range(first, min(mass_limit, upper.numerator//upper.denominator) + 1, 2)


def exceptional_shortlist(initial_pairs, blocks, mass_limit=HALTING_TARGET):
    """Possible c for the exceptional origin A(c+2,c), c=3 mod 4."""
    if initial_pairs < 0 or not blocks or blocks[0] != "J":
        raise ValueError("expected the first J after ordinary bulk pairs")
    d, initial_gain = 0, 0
    residues = ((5, 20), (9, 35), (7, 26), (7, 29))
    for _ in range(initial_pairs):
        v, b = residues[d % 4]
        d = (9*d + b)//4
        initial_gain += v

    ratio, weight = Fraction(1), Fraction(0)
    low, high = Fraction(0), Fraction(0)
    min_gain = max_gain = 0
    for move in blocks[:397]:
        if move == "J":
            weight += ratio/3
            low += ratio*(min_gain - 1)/3
            high += ratio*(max_gain - 1)/3
            min_gain += 2
            max_gain += 2
            ratio /= 3
        elif move == "P":
            low -= ratio*35/9
            high -= ratio*20/9
            min_gain += 5
            max_gain += 9
            ratio *= Fraction(4, 9)
        else:
            raise ValueError(move)
    # At the first J, t=9+6*j+initial_gain for the pre-E counter c=4*j+3.
    lower = ((d-high-ratio*mass_limit/2)/weight - initial_gain - 9)/6
    upper = ((d-low)/weight - initial_gain - 9)/6
    first = max(0, -((-lower.numerator)//lower.denominator))
    last = upper.numerator//upper.denominator
    return range(4*first+3, 4*last+4, 4)


def compare(seed, word):
    """Monotone comparison of a same-parity reset seed to a coarse itinerary."""
    a, c = 1, seed
    if c % 2 == 0:
        a, c = champion_step(a, c)
    for index, letter in enumerate(word):
        if letter == "L":
            if a < 4 * ((c + 1) // 4) + 3:
                return 1
        elif letter == "J":
            if a % 2 == 0:
                raise ValueError("J requested at an even-left phase")
            if a > c:
                return -1
        elif letter == "R":
            if a % 2 or index != len(word)-1:
                raise ValueError("R must finish the word at an even-left phase")
            if a > c:
                return -1
        else:
            raise ValueError(letter)
        a, c = champion_step(a, c)
    return 0


def origins(first, last, word):
    """Exact inclusive range of same-parity reset seeds for a coarse J/L word."""
    if first < 1 or last < first or (last-first) % 2:
        raise ValueError("require a nonempty positive same-parity seed interval")

    def boundary(strict):
        lo, hi = 0, (last-first)//2 + 1
        while lo < hi:
            mid = (lo + hi)//2
            result = compare(first + 2*mid, word)
            if result < 0 or (strict and result == 0):
                lo = mid + 1
            else:
                hi = mid
        return lo

    left, right = boundary(False), boundary(True)
    return range(first + 2*left, first + 2*right, 2)


def check_long_origin():
    leading = 292
    s = 3**leading + 4742
    # Exactly the state after the leading Js. The first counter fixes the
    # leading length, and the final J guard implies all its predecessors.
    a, c = 2 * 3**leading - 1, 5327
    blocks = []
    while True:
        if a >= 4*((c+1)//4) + 3:
            a, c = champion_step(a, c)
            if a < 4*((c+1)//4) + 3:
                assert a % 2 == 0 and a <= c
                break
            a, c = champion_step(a, c)
            blocks.append("P")
        else:
            assert a % 2 == 1 and a <= c
            a, c = champion_step(a, c)
            blocks.append("J")
        assert a > 1 and a + 2*c < 2*HALTING_TARGET
    assert len(blocks) == 411 and blocks.count("P") == 400
    candidates = shortlist(blocks, leading, 1)
    assert list(candidates) == [s-2, s, s+2]
    word = "J"*leading + "".join(blocks).replace("P", "LL")
    assert list(origins(candidates[0], candidates[-1], word)) == [s, s+2]


def check_exceptional_origin():
    # Generate integer histories from the original map, then invert them.
    histories = 0
    for j in range(1, 200):
        origin = 4*j+3
        a, c = champion_step(origin+2, origin)
        blocks = []
        for _ in range(80):
            if a >= 4*((c+1)//4) + 3:
                a, c = champion_step(a, c)
                if a < 4*((c+1)//4) + 3:
                    break
                a, c = champion_step(a, c)
                blocks.append("P")
            elif a <= c:
                a, c = champion_step(a, c)
                blocks.append("J")
            else:
                break
        if "J" in blocks:
            first = blocks.index("J")
            assert origin in exceptional_shortlist(first, blocks[first:], 10_000)
            histories += 1
    assert histories > 50
    # The archimedean width including the unknown final d is strictly below six.
    assert Fraction(123, 25) + Fraction(1, 2)*Fraction(4, 9)**396*HALTING_TARGET < 6


def check_even_corridor():
    upper = HALTING_TARGET - 3_403_055
    lower = HALTING_TARGET - 64_000_000
    word = "J"*291+"LLJLLJLR"
    matches = origins(2, HALTING_TARGET-1, word)
    start = matches.start
    assert start == int(
        "2139765206074066056917952753139324985798572811650448401273625479927612"
        "3044548507478515077163843523468268930744915669252491365804261929780506"
    )
    assert list(matches[-1:]) == [HALTING_TARGET-1]
    assert compare(start-2, word) < 0
    assert compare(start, word) == compare(HALTING_TARGET-1, word) == 0
    # The largest seed has the smallest left counter along each common prefix.
    a, c = champion_step(1, HALTING_TARGET-1)
    for _ in word[:-1]:
        assert a > 1
        a, c = champion_step(a, c)
    assert a > 1
    assert champion_step(a, c)[0] == 1
    max_gain = (8 + 4*word.count("J") + 9*word.count("L") + 5)//2
    assert max_gain == 615 and lower-1+max_gain <= upper
    min_age = (2*(upper-start)+5+8)//9
    assert min_age > 109 * 10**134
    return start, min_age


def verify():
    power = 3**LEADING
    assert 8*3**291 > 2*HALTING_TARGET
    assert 3**282 * 1_000 < power
    assert 4**141 + 8 * 141 + 4 < power//100
    assert 2*power + 5*141 < HALTING_TARGET
    assert power > 1_010 * 3**141
    assert 9 * HALTING_TARGET * 4**397 < 5 * 9**397

    rng = Random(758)
    words = ["B" + "".join(w) for w in product("BJ", repeat=10)]
    words += ["B" + "B"*140, "B" + "J"*140, "B" + "BJ"*70, "B" + "JB"*70]
    words += ["B" + "".join(rng.choices("BJ", k=140)) for _ in range(128)]
    starts = {}
    for word in words:
        s = witness(word)
        assert 3 <= s < HALTING_TARGET
        replay(s, word)
        if len(word) == 141:
            assert s in shortlist(word.replace("B", "P"), LEADING, 1)
        assert (len(word), s) not in starts
        starts[len(word), s] = word

    for start in (1, 2):
        base = range(start, 401, 2)
        for size in range(1, 6):
            # Grouped words always request J at an odd-left phase.
            for symbols in product("JB", repeat=size):
                word = "".join(symbols).replace("B", "LL")
                expected = [s for s in base if compare(s, word) == 0]
                assert expected == list(origins(base[0], base[-1], word))
    check_long_origin()
    check_exceptional_origin()
    check_even_corridor()
    print("Verified the 411-block reset inverse and 1,156 reset witnesses.")


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Use Python without -O for verification.")
    verify()
