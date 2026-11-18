"""Inspect the only pair of complete survivor gaps with positive corrected charge."""
from itertools import product

from cut100 import SEED, analyze, first_digits
from line34_right import interfaces


def phases(word):
    previous = next((int(x == 2) for x in word if x != 1), 0)
    result = [previous]
    for x in word:
        if x != 1:
            assert previous == (x == 2)
            previous = int(x == 3)
        result.append(previous)
    return result


def classify(word, bits, offset=0):
    """Ignore incomplete end runs. Every gap between complete runs is retained."""
    assert len(word) == len(bits)
    starts = [j for j in range(1,len(bits)) if bits[j] and not bits[j-1]]
    colors = phases(word)
    gaps = []
    for start, end in zip(starts, starts[1:]):
        split = start+1
        while bits[split]:
            split += 1
        x = split-start
        gap = word[split:end]
        q = gap.count(3)
        assert gap.count(1) == q
        assert len(gap) == 3*q + colors[start] - colors[end]
        inc = 3*(1-q)-x
        assert 3-(end-start) == inc-colors[start]+colors[end]
        gaps.append((start,end,q,x,inc))
    winning = []
    i = 0
    while i < len(gaps):
        a,b,q,x,inc = gaps[i]
        if q:
            assert inc <= -1
            i += 1
            continue
        assert tuple(word[a+x:b]) == (2,)
        if i+1 == len(gaps):
            break
        _,e,r,y,other = gaps[i+1]
        assert r >= 1
        total = inc+other
        assert total <= 1
        if total == 1:
            assert (x,y,r) == (1,1,1)
            pattern = ''.join(map(str,word[a:e]))
            assert pattern in ('12113','121132')
            winning.append((a+offset,pattern))
        i += 2
    return winning


def main():
    cases = 0
    for n in range(1,12):
        for source in product((0,1),repeat=n+1):
            word = [1 if a==b else 3 if b else 2 for a,b in zip(source,source[1:])]
            for exterior in (0,1,3):
                bits = [int(b) for _,b in interfaces(tuple(word)+(3,)*exterior)[1:1+n]]
                classify(word,bits)
                cases += 1
    print('Ordinary derivative words and exterior-debt controls checked:', cases)
    word = first_digits(SEED['width'])
    bits = [int(b) for _,b in interfaces(word)[1:]]
    win = classify(word[99:],bits[99:],99)
    assert win
    print('Real epoch 1300, after cut 99:',len(win),'positive groups; earliest',win[:6])
    cfg = (SEED['width'],int(SEED['open_hex'],16),int(SEED['closing_hex'],16))
    _,g,(debt,),_ = analyze(cfg,(100,))
    print('This blank tape has guard debt',g,'and cut-100 debt',debt)


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('enable assertions')
    main()
