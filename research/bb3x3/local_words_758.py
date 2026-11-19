"""Construct a physical realization of any short fine word at a specified cut."""
from itertools import product
from random import Random

from check_bb33 import HALTING_TARGET as H, champion_step
from excursion_power_758 import J, PAIRS

LIMIT = 291
Q = 3**LIMIT
RADIUS = 10**100


def length(symbol):
    return 1 if symbol == J else 2


def gain(symbol):
    return 2 if symbol == J else PAIRS[symbol][0]


def witness(cut_u, word, split, index=0):
    """Return (a,c) at the start of the requested indexed realization."""
    calls = sum(map(length, word))
    assert 0 <= split <= len(word) and calls <= LIMIT
    assert abs(cut_u-H) <= RADIUS and 0 <= index < 3**(LIMIT-calls)
    start_u = cut_u-sum(map(gain, word[:split]))
    if all(s == J for s in word):
        h = 2+(start_u % 2)+2*index
        return 2*h-1, start_u-h+1

    # Compose the congruence on d at the end of each prefix.
    modulus, residue, u = 1, 0, start_u
    for s in word:
        if s == J:
            modulus *= 3
            residue = (3*residue-u+1) % modulus
        else:
            _, b = PAIRS[s]
            modulus *= 9
            residue = (9*residue+b)*pow(4,-1,modulus) % modulus
        u += gain(s)
    assert modulus == 3**calls
    low = (Q+15)//16
    d = low+(residue-low) % modulus + index*modulus
    assert low <= d < low+Q
    for s in reversed(word):
        u -= gain(s)
        if s == J:
            d, rem = divmod(d+u-1,3)
        else:
            _, b = PAIRS[s]
            d, rem = divmod(4*d-b,9)
            assert d % 4 == s
        assert rem == 0 and d >= 0 and u-2*d >= 2
    return 2*u-4*d-1, 2*d+1


def replay(cut_u, word, split, index=0):
    a, c = witness(cut_u,word,split,index)
    cut = None
    for i in range(len(word)+1):
        assert a % 2 == c % 2 == 1 and a > 1 and c > 0
        if i == split:
            assert (a+2*c-1)//2 == cut_u
            cut = a,c
        if i == len(word):
            break
        s = word[i]
        if s == J:
            assert a <= c
            a,c = champion_step(a,c)
        else:
            assert (c-1)//2 % 4 == s
            for _ in range(2):
                assert a >= 4*((c+1)//4)+3
                a,c = champion_step(a,c)
                assert a > 1 and c > 0
    return cut


def main():
    min_u, max_u = H-RADIUS-9*LIMIT, H+RADIUS+9*(LIMIT+1)
    assert 3*Q+100 < min_u and max_u < 2*3**292
    low = (Q+15)//16
    min_h = min_u-2*(low+Q-1)
    assert min_h >= 2*3**289 and 5*min_u >= 18*3**289
    assert (min_u-1)//3 >= low
    assert (low+7)*4**145 >= 7*9**145
    for v,b in PAIRS:
        assert 35 >= b >= 2*v
    letters = (J,0,1,2,3)
    short = 0
    for blocks in range(5):
        for word in product(letters,repeat=blocks):
            index = 3**(LIMIT-sum(map(length,word)))-1
            for split in range(blocks+1):
                cut = H+split
                assert replay(cut,word,split,0) != replay(cut,word,split,index)
                short += 1
    random = Random(758)
    for trial in range(180):
        target = 291-trial%5
        if trial < 5:
            word = [J]*target
        elif trial < 10:
            word = [trial % 4]*(target//2) + [J]*(target%2)
        elif trial < 15:
            word = [J]*(target-2)+[trial%4]
            if trial%2:
                word.reverse()
        else:
            word = []
            remaining = target
            while remaining:
                symbol = J if remaining == 1 else random.choice(letters)
                word.append(symbol)
                remaining -= length(symbol)
        cut = H+random.randint(-RADIUS,RADIUS)
        index = random.randrange(3**(LIMIT-target))
        for split in (0,len(word)//2,len(word)):
            replay(cut,word,split,index)
    print(f"all constants verified, {short} short word/split pairs at both endpoint indices")
    print("540 long word/split replays, up to 291 calls")


if __name__ == '__main__':
    main()
