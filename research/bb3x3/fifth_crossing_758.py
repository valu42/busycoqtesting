"""Check the synchronized fifth-pair crossing and its ordinary-passage bound."""
from argparse import ArgumentParser
from pathlib import Path
import subprocess

from check_bb33 import champion_step, first_return
from check_confluence import itinerary

K = 40_486_323_621_582_648
B = 39_752_584_607_270_532
CUT = K - 10**14
END = CUT + 5_000
START_MASS = 79_694_553_903_668_291
E_WORD = "L"*88 + "JLLLR"


def post_exception(mass):
    """Return the reset following the indicated word, or None at a guard failure."""
    assert mass % 12 == 11
    c = (mass-2)//3
    assert c % 4 == 3
    actual = champion_step(c+2,c)
    assert actual == (mass+6,1)
    a,c = actual
    for op in E_WORD:
        if op == "L" and a < 4*((c+1)//4)+3:
            return None
        if op == "J" and not (a % 2 and a <= c):
            return None
        if op == "R" and not (a % 2 == 0 and a <= c):
            return None
        actual = champion_step(a,c)
        assert actual is not None
        a,c = actual
    assert a == 1
    return c


def verify():
    assert B <= CUT and END-B+1 == 633_739_014_317_117
    assert itinerary(B) == itinerary(END) == ("J"*34+"LLLLJLR",198)
    assert itinerary(B+1) == itinerary(END-1) == ("J"*33+"LR",150)

    seed = K-198_990
    for i in range(1_054):
        if i == 1_053:
            assert seed == K-98
        assert seed < K
        next_seed = first_return(seed,batch=False)
        assert next_seed is not None and next_seed > seed
        seed = next_seed
    assert seed == K+118

    # E inputs have mass 11 modulo 12. A live call adds at most nine.
    upper = 2*END+1
    last = upper - 94*9
    first = START_MASS
    assert 2*B+1 < first < last
    assert post_exception(first-12) is None
    for mass in (first,last-(last-11)%12):
        s = post_exception(mass)
        assert s is not None and B <= s <= END and 2*s+1-mass <= 94*9
    # The first states >=first and >=last overshoot by at most eight.
    # Inside this interval a bypass has neither resets nor an E.
    # Discard a possible incomplete LL pair at each end.
    ordinary_calls = (last-first-8)//9
    blocks = (ordinary_calls-2)//2
    horizon = 7_700_000**2
    n = 66
    assert blocks >= horizon+n and 3**n > 9*horizon*K
    print(f"The deep block synchronizes at K-198990 and crosses K-98 to K+118.")
    print(f"A trajectory reaching the pair from below B needs at least "
          f"{blocks:,} consecutive ordinary blocks and 7,700,000 different length-67 fine words.")


def replay(worker):
    for start, end in ((CUT,K-10**11),(K-10**11,K-199_000)):
        line = subprocess.check_output([str(worker),str(start),str(end)],text=True)
        a,b,low,high,blocks,returns = map(int,line.split())
        assert (a,b)==(start,end) and b <= low <= high <= b+5_000
        assert blocks > 0 and returns >= 0
        if start == K-10**11:
            assert low == high == K-198_990
        print(line.strip())


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--worker',type=Path,help='replay both C++ transfers with cross_758_fast')
    args = parser.parse_args()
    if not __debug__:
        parser.error('enable assertions')
    if args.worker:
        replay(args.worker.resolve(strict=True))
    verify()
