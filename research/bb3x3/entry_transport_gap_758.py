#!/usr/bin/env python3
"""Two exact reset-origin examples delimiting possible entry arguments.

Neither starting reset is asserted to lie on the blank trajectory.
"""
from check_bb33 import champion_step
from target_bridge_even_758 import FAR, H


def first_return(seed, budget=2000):
    a, c = 1, seed
    for calls in range(1, budget+1):
        result = champion_step(a, c)
        assert result is not None
        a, c = result
        if a == 1:
            return calls, c
    raise AssertionError('finite example exceeded its verification budget')


def verify():
    boundary = H-FAR
    seed = boundary-586
    a, c = 1, seed
    crossed = None
    for calls in range(1, 598):
        result = champion_step(a, c)
        assert result is not None
        a, c = result
        if crossed is None and a%2 and c%2 and (a+2*c-1)//2 >= boundary:
            h, u = (a+1)//2, (a+2*c-1)//2
            expected_numerator = 9*3**292-5*boundary-10
            assert expected_numerator%4 == 0
            assert calls == 294 and u == boundary+3
            assert h == expected_numerator//4 and c == boundary+4-h
            assert h%2 == 0 and h%3 != 0 and len(str(h)) == 140
            assert h > 2*((H-FAR)//(2*3**(307-88)))
            crossed = calls
        if a == 1:
            assert calls == 597 and c == boundary+644 and crossed == 294
            break
    assert first_return(seed) == (597, boundary+644)
    print('A reset 586 below the basin crosses with a 140-digit even primitive h; '
          'its first return is 303 calls after that crossing, inside the basin.')

    power = 3**292
    assert power+8153 < H
    assert first_return(power+4137) == (299, power+4744)
    assert first_return(power+4139) == (299, power+4744)
    assert first_return(power+4742) == (1105, power+8153)
    assert first_return(power+4744) == (1105, power+8153)
    # The two 1105-call starts are siblings merging at their first bulk.
    images = []
    for offset in (4742, 4744):
        a, c = 1, power+offset
        for _ in range(292):
            assert a%2 and c%2 and a <= c
            a, c = champion_step(a, c)
        assert a > c
        images.append(champion_step(a, c))
    assert images[0] == images[1]
    print('Two 299-call first returns feed a 1105-call excursion; '
          'the sibling origin merges at its first bulk.')


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run without -O for verification.')
    verify()
