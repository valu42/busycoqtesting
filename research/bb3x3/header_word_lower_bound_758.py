"""Exact numerical bounds for HEADER_WORD_LOWER_BOUND_758.md."""
from fractions import Fraction

from check_bb33 import HALTING_TARGET, champion_step
from scale_transport_758 import prefix


def move(a, c):
    if a <= c:
        return 'J' if a % 2 else 'R'
    if a >= 4*((c+1)//4)+3:
        return 'L'
    return 'terminal or exceptional'


def main():
    divisor = 13_959_275
    unit = Fraction(3**307, divisor)
    mesh = Fraction(2*divisor**2, 3**154)
    maximum = 32768/mesh
    assert 10**4 < 5*maximum/9 < maximum < 252*10**61
    assert mesh*unit > maximum+1220
    assert Fraction(4, 27)*120/15 > 1
    assert 449**11*3**8 < 1000**11
    assert 551**11*9**8 < 1000**11*4**8
    assert (120*mesh)**8 * (10**41)**11 < 1
    assert prefix(0)[0] == 0 and prefix(32768)[0] == 4*divisor

    distance = 2519807940164222286326480224696064445884526387481856382330434770
    seed = HALTING_TARGET-distance
    a, c = 1, seed
    opening = 'J'*292+'L'*8+'J'+'L'*6
    word = opening+'J'*153+'L'*357+'R'
    for index, letter in enumerate(word):
        assert c % 2 and move(a,c) == letter
        assert index == 0 or a != 1
        if index == len(opening):
            h0 = (a+1)//2
            numerator = 4**77-3**154+divisor*h0
            assert numerator == 22835963083295358096932575511191922154683810565
            assert numerator % 10 == 5
        a, c = champion_step(a,c)
    assert len(word) == 818 and (a,c) == (1,seed+2160)
    assert 3**(307-157-2) > divisor*(distance+2000) >= 3**(307-158-2)
    print('Over 10^41 distinct returning words; 818-call witness, seed gain 2160.')


if __name__ == '__main__':
    main()
