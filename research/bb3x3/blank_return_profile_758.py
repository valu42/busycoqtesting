"""Exact return-length census on the blank orbit near the fourth pair."""
from collections import Counter
from after_fourth_758 import CHECKPOINT, EVEN_END, ODD_END, cross, increments
from check_bb33 import champion_step
from exact_fourth_758 import LOW, MERGER


def profile():
    counts = Counter()
    def literal(seed):
        a,c = 1,seed
        n = 0
        while True:
            state = champion_step(a,c)
            assert state is not None
            a,c = state
            n += 1
            if a == 1:
                assert c > seed
                counts[n] += 1
                return c

    seed = MERGER
    for _ in range(425):
        seed = literal(seed)
    assert seed == LOW+208
    bands = []
    def corridor(seed,end,word):
        table = increments(seed,end,word)
        seed, number = cross(seed,end,*table)
        calls = 1+len(word)  # itinerary() omits the opening update.
        counts[calls] += number
        bands.append((number,calls))
        return seed
    seed = corridor(seed,ODD_END,'J'*33+'L'*7+'R')
    while seed % 2:
        seed = literal(seed)
    seed = corridor(seed,EVEN_END,'J'*33+'LLJLR')
    while seed < CHECKPOINT:
        seed = literal(seed)
    assert seed == CHECKPOINT
    assert bands == [(3_746_008_362_829,42),(7_792_944_006_905,39)]
    assert counts.total() == 11_538_952_370_487 and max(counts) == 134
    assert sum(k*v for k,v in counts.items()) == 461_257_167_560_842
    return counts,bands


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run without -O.')
    counts,bands = profile()
    print('Fixed-word bands',bands)
    print('Return-length histogram',sorted(counts.items()))
    print('First returns',counts.total(),'counter calls',sum(k*v for k,v in counts.items()))
