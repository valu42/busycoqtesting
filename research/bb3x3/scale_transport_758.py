#!/usr/bin/env python3
"""Verify a normalized common-word cover and distinct higher-scale reset paths."""
from fractions import Fraction
from itertools import product
from random import Random

from scale_clauses_758 import BASE, H, PREFIX, check_word
from check_bb33 import champion_step


PERIOD = 32_768
SLOPE = 55_837_100
BETA_LOW, BETA_HIGH = -203_238_392, 106_061_328
BASE_JUMPS = 263
FIXED_SCALE = 240


def prefix(distance):
    """Extend the common prefix algebraically to compute its affine residues."""
    power = 3**292
    a, c, gain = 2*power-1, H-distance+585-power, 4*292
    for i in range(14):
        if i == 8:
            a, c, gain = 3*a+2, c-a+1, gain+4
        q = (c+1)//4
        gain += 9 if c % 4 == 3 else 5
        a, c = a-4*q-3, 6*q+5
    return a+1, gain


def bounds(left, right):
    """Lower-left-counter and upper-left-counter corners for scales 0..240."""
    # Initial X=a+1 after J^(263-n) is a multiple of four.
    power = 3**BASE_JUMPS
    xmin = power*(SLOPE*left+BETA_LOW)//PERIOD
    xmax = -(-power*(SLOPE*right+BETA_HIGH)//PERIOD)
    xmin -= xmin % 4
    xmax += -xmax % 4
    wmin = 2*(H-right*3**FIXED_SCALE)+1+4*293+5*14+4*(BASE_JUMPS-FIXED_SCALE)
    wmax = 2*(H-left)+1+4*293+9*14+4*BASE_JUMPS
    cmin = (wmin-xmax+1)//2
    cmax = (wmax-xmin+2)//2
    cmin -= (cmin+1) % 2
    cmax += (cmax+1) % 2
    assert 1 <= cmin <= cmax
    return (xmin-1, cmax), (xmax-1, cmin)


def ordinary(a, c):
    q = (c+1)//4
    if a >= 4*q+3:
        return "L", (a-4*q-3, 6*q+5)
    if a % 2 == 0:
        return "stop", None  # either a halt or an even-left return
    if a <= c:
        return "J", (3*a+2, c-a+1)
    return "E", None


def shared_cost(left, right):
    x, y = bounds(left, right)
    for step in range(1, 1001):
        p, x = ordinary(*x)
        q, y = ordinary(*y)
        if p != q or p == "E":
            return None
        if p == "stop":
            return step
    raise ValueError("unexpectedly long common word")


def verify_cover():
    offsets = []
    for r in range(0, PERIOD, 2):
        start, gain = prefix(r)
        shifted, next_gain = prefix(r+PERIOD)
        assert shifted-start == SLOPE and gain == next_gain
        offsets.append(PERIOD*start-SLOPE*r)
    assert (min(offsets), max(offsets)) == (BETA_LOW, BETA_HIGH)
    # These endpoint checks imply legality through the common prefix for
    # every odd seed between them. Positive final c checks the next J run.
    for d in (BASE, 3*BASE*3**FIXED_SCALE):
        check_word(H-d, PREFIX)
    good = bad = width = longest = 0
    queue = [(BASE, 3*BASE)]
    while queue:
        left, right = queue.pop()
        cost = shared_cost(left, right)
        if cost is not None:
            good += 1
            width += right-left
            longest = max(longest, cost)
        elif right-left <= 2**14:
            bad += 1
        else:
            middle = (left+right)//2
            queue.extend(((left,middle), (middle,right)))
    assert (good,bad,width,longest) == (27_423,53_333,19_491_376_875,34)
    return width


def launch(z):
    """For D=32768*z, aligned mass u and counter d after J^23 at scale 240."""
    initial, gain = prefix(PERIOD*z)
    k = BASE_JUMPS-FIXED_SCALE
    u = H-PERIOD*z+gain//2+2*k
    h = initial*3**k//2
    return u, (u-h)//2


def witness(word):
    """Integral reset origin near the real center of a prescribed fine word."""
    if not word.startswith("JB"):
        raise ValueError("the two initial blocks must be JB")
    u0, d0 = launch(0)
    u1, d1 = launch(1)
    du = u1-u0
    slope, constant, den, gain = d1-d0, d0, 1, 0
    for letter in word:
        if letter == "J":
            slope = 3*slope-du*den
            constant = 3*constant+(1-u0-gain)*den
            gain += 2
        elif letter == "B":
            slope *= 9
            constant = 9*constant+20*den
            den *= 4
            gain += 5
        else:
            raise ValueError(letter)
    assert slope % 2
    residue = -constant*pow(slope,-1,den) % den
    # Solve d_final=u_final/4 over the reals, then round in the class.
    num = den*(u0+gain)-4*constant
    div = 4*slope-den*du
    if div < 0:
        num, div = -num, -div
    assert div > 0
    width = div*den
    return PERIOD*(residue + den*((2*(num-div*residue)+width)//(2*width)))


def replay(word):
    distance = witness(word)
    scale = 3**FIXED_SCALE
    assert BASE*scale <= distance <= 3*BASE*scale
    u, d = launch(distance//PERIOD)
    a, c = 2*u-4*d-1, 2*d+1
    for letter in word:
        if letter == "J":
            assert a <= c and a % 2 == c % 2 == 1
            a, c = champion_step(a, c)
        else:
            for _ in range(2):
                assert c % 4 == 1 and a >= c+2
                a, c = champion_step(a, c)
        assert a > 1
    assert min(c-1, (a+1)//2) > H//4
    return distance


def verify_witnesses():
    k = BASE_JUMPS-FIXED_SCALE
    p0, gain = prefix(0)
    scale = 3**FIXED_SCALE
    # Even at the outermost residue rounding, there are opposite signs.
    for d, side in ((BASE*scale+PERIOD*4**121, -1),
                    (3*BASE*scale-PERIOD*4**121, 1)):
        u = H-d+gain//2+2*k
        h = Fraction(3**k,2)*(p0 + Fraction(SLOPE*d,PERIOD))
        if side < 0:
            assert h < Fraction(5,27)*u
        else:
            assert h > Fraction(1,3)*u + 8*122+4
    assert (SLOPE*3**k + 2*PERIOD)*3**243 < H//100
    assert H//(10*3**122) > 100 and H-3*BASE*scale > 9*H//10
    rng = Random(758)
    words = ["JB"+"".join(w) for w in product("JB", repeat=10)]
    words += ["JB"+w for w in ("J"*120, "B"*120, "JB"*60, "BJ"*60)]
    words += ["JB"+"".join(rng.choices("JB",k=120)) for _ in range(128)]
    assert len({(len(w),replay(w)) for w in words}) == len(words)


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run without -O for verification.")
    measured = verify_cover()
    verify_witnesses()
    print("Shared coverage:", measured, "out of", 2*BASE, "normalized width.")
    print("Verified high-scale witness construction on 1,156 words.")
