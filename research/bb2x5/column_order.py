"""Ordered subsequence counts, the physical checkpoint inverse, and a finite obstruction."""
from itertools import product

from column_tick import tick
from prior_frontier import LIST, M26, parse

PAIRS = ('14','11','44','41')


def scattered_pairs(word):
    counts = [0]*4
    pairs = [[0]*4 for _ in counts]
    for d in word:
        for a,n in enumerate(counts):
            pairs[a][d] += n
        counts[d] += 1
    return counts,pairs


def inverse(word):
    """Return the unique preceding successful aligned upper word, when it exists."""
    u = sum((d//2)<<i for i,d in enumerate(word))
    e = sum((d%2)<<i for i,d in enumerate(word))
    selected = e&~u
    if not selected:
        return None
    stop = selected&-selected
    old_e = e^(~u&(2*stop-1))
    assert old_e < e
    selector = 2*old_e+1
    width = len(word)
    for _ in range(9):
        selected_zero = selector&~u
        stop = selected_zero&-selected_zero
        width -= not stop
        u ^= selector&(2*stop-1)
    if width < max(u.bit_length(),old_e.bit_length()):
        return None
    return tuple(2*((u>>i)&1)+((old_e>>i)&1) for i in range(width))


# Each row is a replacement at the given aligned tick, low pair first.
REPLACEMENTS = {
    8:  ('0102201000','0012210000'),
    16: ('0113330100000','1130303001000'),
    24: ('10033321330000','13303021030003'),
    27: ('200232212301032','022210303222301'),
}


def check_path():
    table = parse(M26)
    tape = {}
    x = state = steps = 0

    def advance(target):
        nonlocal x,state,steps
        start = steps
        while x != target:
            move = table[state][tape.get(x,0)]
            if move is None:
                assert state == 1 and tape[x] == 3
                return steps-start
            symbol,delta,state = move
            if symbol:
                tape[x] = symbol
            else:
                tape.pop(x,None)
            x += delta
            steps += 1
            assert steps-start < 50000
        assert state == 0 and tape.get(x,0) == 0
        return None

    last = max(REPLACEMENTS)
    for t in range(1,last+1):
        guard = 8*t+1
        assert advance(-guard) is None
        assert all(tape.get(i,0) == 4 for i in range(1-guard,1))
        assert ''.join(str(tape[i]) for i in range(1,7)) == '14'*3
        end = max(tape)
        assert tape[end] == 3 and len(tape) == guard+end
        word = tuple(PAIRS.index(str(tape[i])+str(tape[i+1])) for i in range(7,end,2))
        if t==1:
            assert word == (2,1)
        if t in REPLACEMENTS:
            old,new = REPLACEMENTS[t]
            new_word = tuple(map(int,new))
            assert word == tuple(map(int,old))
            assert scattered_pairs(word) == scattered_pairs(new_word)
            for i,d in enumerate(new_word):
                tape[7+2*i],tape[8+2*i] = map(int,PAIRS[d])
            print('tick',t,old,'->',new,'same four single and sixteen ordered-pair counts')
    final_steps = advance(-(8*(last+1)+1))
    assert final_steps is not None
    print('last replacement reaches B3 in',final_steps,'defined instructions at coordinate',x)
    print('total defined instructions along the path with replacements:',steps)


def main():
    assert LIST[25] == M26 == '1RB2RB4LA2RA1LA_2LA4RA3LA---3RA'
    assigned = 0
    for size in range(7):
        for word in product(range(4),repeat=size):
            forward = tick(word)
            if forward is not None:
                assert inverse(forward) == word
            past = inverse(word)
            if past is not None:
                assert tick(past) == word
                assigned += 1
    assert inverse((2,1)) is None
    print('inverse checked on all 5461 words of widths 0..6;',assigned,'have physical predecessors')
    check_path()


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run with assertions enabled.')
    main()
