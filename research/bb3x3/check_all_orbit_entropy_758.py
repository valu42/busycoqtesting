#!/usr/bin/env python3
"""Replay the scale-3 cusp construction used in ALL_ORBIT_ENTROPY_758.md."""
from fractions import Fraction
from itertools import product

from check_bb33 import champion_step


UPPER_T = Fraction(251, 250)
DEPTH = 10
EXPONENT = 96


def inverse(letter, x):
    return x/3 if letter == 'J' else (4*x+5)/9


def take(state, letter):
    a, c = state
    if letter == 'J':
        assert a % 2 and c % 2 and a <= c
    elif letter == 'L':
        assert c % 2 and a >= 4*((c+1)//4)+3
    elif letter == 'I':
        assert a == 1 and c % 2 == 0
    elif letter == 'R':
        assert a % 2 == 0 and c % 2 and a <= c
    state = champion_step(a, c)
    assert state is not None
    return state


def odd_path(s, exponent, word):
    state = (1, s)
    for letter in 'J'*exponent + word.replace('P', 'LL'):
        state = take(state, letter)
        assert state[0] > 1


def even_entry(s, exponent):
    state = (1, s)
    for letter in 'I' + 'J'*(exponent-1) + 'LLJLLL':
        state = take(state, letter)
        assert state[0] > 1
    assert state[0] % 4 == 0
    a, dest = take(state, 'R')
    assert a == 1 and dest % 2 and s < dest <= s + 2*exponent+29
    return dest


def check_cusp():
    # The image of (0,1) under seven inverse bulk pairs gives the full
    # range of normalized odd launches used for the factor witnesses.
    assert 1/(1-Fraction(4, 9)**7) < UPPER_T
    for t in (Fraction(1), UPPER_T):
        x = 2/(3*t)
        assert Fraction(5,9) < x < 1
        x = (9*x-5)/4
        assert 0 < x < Fraction(1,3)
        x *= 3
        assert Fraction(5,9) < x < 1
        x = (9*x-5)/4
        assert Fraction(1,3) < x < Fraction(5,9)

    scale = 3**EXPONENT
    for tail in product('JP', repeat=DEPTH):
        word = 'P'*7 + ''.join(tail)
        x = Fraction(1, 2)
        for letter in reversed(word):
            x = inverse(letter, x)
        seed = scale*x.denominator//x.numerator
        odd = seed if seed%2 else seed-1
        assert 1 < Fraction(odd, scale) < UPPER_T
        odd_path(odd, EXPONENT, word)
        odd_path(even_entry(odd-1, EXPONENT), EXPONENT, word)


def check_exceptional_annuli():
    right, decrement = 1, 0
    checked = 0
    # A finite cross-check of the explicit annuli and their guarded bulk run.
    for i in range(1, 190):
        q = (right+1)//4
        decrement += 4*q+3
        right = 6*q+5
        if i%2 == 0:
            continue
        # The two extremal admissible E-input masses satisfy W=11 mod 12.
        low, high = decrement-6, decrement+right-6
        for mass in (low+(11-low)%12, high-(high-11)%12):
            if not low <= mass <= high or mass<11:
                continue
            c = (mass-2)//3
            state = champion_step(c+2, c)
            assert state == (mass+6, 1)
            for _ in range(i):
                state = take(state, 'L')
            state = take(state, 'R')
            assert state[0] == 1
            checked += 1
    assert checked > 150


def check_fine_residues():
    # Guard-independent arithmetic check for a template of seven pairs. Extra
    # precision also retains the high flag on the final unpaired bulk move.
    word = 'PPJPPJPPP'
    pairs, jumps = word.count('P'), word.count('J')
    mod = 4**pairs
    exponent = (1-jumps-5*(pairs+1)//2) % mod
    power = pow(3, exponent, 4*mod)
    labels = {}
    for z in range(2*mod):
        u = 2*z+1+2*exponent
        d = ((u-power)//2) % (2*mod)
        code, high = 0, 0
        for letter in word:
            if letter == 'J':
                d, u = 3*d-u+1, u+2
            else:
                r = d%4
                v = (5,9,7,7)[r]
                b = (20,35,26,29)[r]
                d, u = (9*d+b)//4, u+v
                code = 4*code+r
                high += (v-5)//2
        high += d%2
        gain = exponent+jumps+5*(pairs+1)//2+high
        assert 1 <= gain%mod <= 2*pairs+2
        assert labels.setdefault(code, z%mod) == z%mod
    assert len(labels) == mod


def main():
    if not __debug__:
        raise SystemExit('run without -O to enable the checks')
    check_cusp()
    check_exceptional_annuli()
    check_fine_residues()
    print('Replayed all 1,024 ten-block words from both cusp parities and '
          'checked the exceptional annuli and all seven-pair fine residue codes.')


if __name__ == '__main__':
    main()
