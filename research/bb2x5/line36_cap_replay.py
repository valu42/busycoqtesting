"""Verify an untrusted exported right-potential table without running relaxation."""
import sys
from pathlib import Path

from prior_frontier import LIST
from prior_sweeps import PARITY, TapeMachine, direct_epoch

WIDTH = 42
MASK = (1<<WIDTH)-1
VISIBLE = MASK >> 1


def successors(cap):
    # Left-to-right matching. A set bit of stack is an unmatched opening.
    # Of the openings already scanned, the nearest has the lowest set bit.
    stack = debt = 0
    bit = 1<<(WIDTH-1)
    while bit:
        if cap&bit:
            if stack:
                stack &= stack-1
            else:
                debt += 1
        else:
            stack |= bit
        bit >>= 1
    assert cap and stack

    positions = cap
    monomers = previous = 0
    while positions:
        digit = positions & -positions
        j = digit.bit_length()-1
        monomers += (j-previous)&1
        previous = j
        positions -= digit
    final_gap = (WIDTH-previous)&1
    monomers += final_gap
    runs = stack
    odd = 0
    while runs:
        runs >>= (runs & -runs).bit_length()-1
        length = ((runs+1) & ~(runs)).bit_length()-1
        odd += length&1
        runs >>= length
    whole = monomers-debt-odd
    # For a prepended opening, only the sentinel gap, the outgoing debt,
    # or the parity of the initial survivor run can change.
    if debt:
        paid = debt-1+odd
    else:
        initial_run = WIDTH-(MASK ^ stack).bit_length()
        paid = odd+1-2*(initial_run&1)
    before_opening = monomers+1-2*final_gap-paid
    cheap = min(whole,before_opening)
    assert cheap >= 0
    image = stack ^ (stack >> 1)
    if not cap&1:
        return ((((image<<1)|1)&MASK,cheap),)
    if debt:
        return ((image,cheap),)
    return ((image,whole),(image^(1<<(WIDTH-1)),cheap))


def read_table(path):
    table = {}
    with Path(path).open() as stream:
        for line in stream:
            cap,h = map(int,line.split())
            assert 0 <= cap <= VISIBLE and -21 <= h <= 0 and cap not in table
            table[cap] = h
    return table


def check(table):
    assert LIST[35] == PARITY == '1RB2LA1LA4RA2LA_0LA3RB3LB2RB---'
    tm = TapeMachine(PARITY)
    for _ in range(32):
        word = direct_epoch(tm,(1,2))
        assert word is not None
    assert len(word) == 92
    seed = int(''.join('1' if d == 2 else '0' for d in word[-41:]),2)
    assert seed in table
    cache = [{} for _ in range(8)]

    def potential(phase,cap):
        if phase == 8:
            # A missing possible next block is a certificate failure.
            return table[cap&VISIBLE]
        known = cache[phase]
        if phase and cap in known:
            return known[cap]
        h = 0
        for nxt,c in successors(cap):
            h = min(h,3*c-1+potential(phase+1,nxt))
        assert -21 <= h <= 0
        if phase:
            known[cap] = h
        return h

    for cap,h in table.items():
        assert h <= potential(0,cap)
        assert h <= potential(0,cap|(1<<41))
    print('Independent table replay passed:',len(table),'boundary entries,',
          sum(map(len,cache)),'intermediate phase/cap pairs, seed',seed,'potential',table[seed])


if __name__ == '__main__':
    if not __debug__ or len(sys.argv) != 2:
        raise SystemExit('Run with assertions enabled and the exported TSV path.')
    check(read_table(sys.argv[1]))
