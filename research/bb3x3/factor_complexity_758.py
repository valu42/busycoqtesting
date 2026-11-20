#!/usr/bin/env python3
"""Check the determinant identity and the finite word-count bounds for #758."""
from itertools import product
from math import isqrt

from check_bb33 import HALTING_TARGET as H
from excursion_power_758 import J, PAIRS


def symbol_step(point, symbol):
    u, d = point
    if symbol == J:
        return u+2, 3*d-u+1
    gain, offset = PAIRS[symbol]
    assert d % 4 == symbol
    return u+gain, (9*d+offset)//4


def area(points):
    (x,y), (u,v), (s,t) = points
    return (u-x)*(t-y) - (s-x)*(v-y)


def audit_determinants():
    # Work on the integer congruence class for an entire fine word. Guards
    # are unnecessary for the algebraic identity. Physical guards are required
    # before using an observed loop to certify infinite continuation.
    for size in range(1, 5):
        for word in product(range(5), repeat=size):
            pairs = sum(letter != J for letter in word)
            den = 4**pairs
            num = 3**(size+pairs)
            # Exact d mod den at each chosen u. Pull all symbols back from
            # d_final = 0 modulo 1, increasing the modulus by four at a pair.
            def initial(u):
                before = []
                for letter in word:
                    before.append(u)
                    u += 2 if letter == J else PAIRS[letter][0]
                residue, modulus = 0, 1
                for letter, u in reversed(list(zip(word, before))):
                    if letter == J:
                        residue = (residue+u-1)*pow(3,-1,modulus) % modulus
                    else:
                        modulus *= 4
                        b = PAIRS[letter][1]
                        residue = (4*residue-b)*pow(9,-1,modulus) % modulus
                assert modulus == den
                return residue
            points = [(7,initial(7)), (11,initial(11)+den), (20,initial(20)+4*den)]
            start = area(points)
            for symbol in word:
                points = [symbol_step(p,symbol) for p in points]
            final = area(points)
            assert den*final == num*start and final % num == 0


def verify_passage(width, clearance, horizon, n):
    # Thresholds are 2B+1 and 2U+1-clearance. An entry can overshoot
    # its lower edge by eight. Drop a possible half block at each end.
    calls = (2*(width-1)-clearance-7+8)//9
    blocks = (calls-2)//2
    assert blocks >= horizon+n
    assert 3**n > 9*horizon*H
    assert isqrt(horizon)**2 == horizon
    # F^2+2F < T if F is smaller than this integer square root.
    return n+1, isqrt(horizon), blocks


def main():
    audit_determinants()
    gate = 10**10*3**74
    band_width = gate//2-39_000_000+1
    # The exceptional branch returns after 785 bulk decrements and one
    # even-left return following E. All tested strips lie in its annulus.
    total, right = 0, 1
    for _ in range(785):
        q = (right+1)//4
        total += 4*q+3
        right = 6*q+5
    assert total-6 <= 2*(H-3*gate//2)+1
    assert 2*H+1 <= total+right-6
    for name, width, horizon, n in (
        ("scale 74", band_width, 10**44, 400),
        ("scale-74 midpoint", gate//4-39_004_000+1, (7*10**21)**2, 400),
        ("original joined interval", 11_177_973_024_732, 10**12, 324),
        ("enlarged joined interval", 33_533_925_880_304, 1_900_000**2, 321),
        ("scale-10 halting corridor", 362_166_436_260_267, 6_300_000**2, 323),
        ("scale-20 joined interval", 53_463_914_736_827_918_796, 2_437_300_755**2, 334),
        ("scale-21 joined interval", 160_391_744_210_490_562_488, 4_221_528_741**2, 335),
        ("scale-19 joined interval", 17_821_304_912_273_704_228, 1_407_176_247**2, 333),
    ):
        length, count, blocks = verify_passage(width, 5458, horizon, n)
        print(f"{name}: at least {blocks:,} complete ordinary blocks. "
              f"At least {count:,} distinct length-{length} fine words.")


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run without -O so that verification checks execute.")
    main()
