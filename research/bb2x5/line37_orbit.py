"""Exact bit-parallel matching sweeps for line 37. Bit 0 is the rightmost cell."""

from argparse import ArgumentParser
from itertools import product
from pathlib import Path

from prior_sweeps import TERNARY_OPEN, word_sweep


def encode(word):
    opens = closes = 0
    for symbol in word:
        opens = (opens << 1) | (symbol == 2)
        closes = (closes << 1) | (symbol == 1)
    return opens, closes


def match(width, opens, closes, cut):
    """Return survivor bits, total unmatched closings, and suffix debt at cut."""
    end_bit = 1 << width
    cut_bit = 1 << (width - cut)
    guard = cut_debt = 0
    while closes:
        # One slot stores a closing until an opening consumes it. The incoming
        # carry of closes + ~opens is the occupancy just before each cell.
        occupied = ((closes + ~opens) ^ closes ^ ~opens)
        guard += bool(occupied & end_bit)
        cut_debt += bool(occupied & cut_bit)
        closes &= occupied     # A closing that met a full slot goes deeper.
        opens &= ~occupied     # An opening that met an empty slot goes deeper.
    return opens, guard, cut_debt


def sweep(width, survivors, guard):
    """Build the next two digit masks, including the left header."""
    assert width and survivors & 1 and guard in (0, 1)
    right = (survivors << 1) | 1
    data_width = width + 1
    mask = (1 << data_width) - 1
    opens = ~(survivors ^ right) & mask
    closes = ~survivors & right
    if guard == 0:
        return data_width + 1, opens | (1 << data_width), closes
    return data_width + 4, opens | (0b1011 << data_width), closes | (0b0100 << data_width)


def audit():
    for n in range(1, 8):
        for prefix in product((1, 2, 3), repeat=n - 1):
            word = prefix + (2,)
            opens, closes = encode(word)
            expected, _ = word_sweep(word, TERNARY_OPEN)
            debt = 0
            for cut in range(n, -1, -1):
                survivors, guard, cut_debt = match(n, opens, closes, cut)
                assert cut_debt == debt
                if cut:
                    debt = max(0, debt + (word[cut-1] == 1) - (word[cut-1] == 2))
            assert guard == debt
            if expected is None:
                assert guard >= 2
            else:
                assert sweep(n, survivors, guard) == (len(expected), *encode(expected))


def run(epochs):
    width, opens, closes = 1, 1, 0  # first sweep of the empty word produces 2
    maximum = resets = 0
    for epoch in range(1, epochs + 1):
        survivors, guard, debt = match(width, opens, closes, min(width, 45))
        if width >= 45:
            maximum = max(maximum, debt)
        if guard >= 2:
            print(f'Halt in sweep from epoch {epoch}, width {width}, guard debt {guard}.')
            return
        if epoch in (1001, epochs):
            print(f'Epoch {epoch}, width {width}, resets in preceding sweeps {resets}, '
                  f'maximum debt at cut 45 so far {maximum}.')
        if epoch < epochs:
            width, opens, closes = sweep(width, survivors, guard)
            resets += guard


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run with assertions enabled.')
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--epochs', type=int, default=1001)
    args = parser.parse_args()
    if args.epochs < 1:
        parser.error('--epochs must be a positive integer')
    assert Path(__file__).with_name('BB2x5_Rocq_holdouts_37.txt').read_text().splitlines()[36] == TERNARY_OPEN
    audit()
    run(args.epochs)
