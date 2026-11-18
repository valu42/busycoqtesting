"""Derive the seed of the reduced cap checker and independently audit its local cost."""
from functools import cache
from itertools import product
from pathlib import Path
import subprocess
import sys

from line36_tiles import survivors
from prior_frontier import LIST
from prior_sweeps import PARITY, TapeMachine, direct_epoch


@cache
def loss(word):
    # Independent optimum over monomer/dimer tilings by prefix length.
    best = [0] + [len(word)+1]*len(word)
    for j,digit in enumerate(word):
        best[j+1] = min(best[j+1],best[j]+1)
        if digit == '1' and j+1 < len(word):
            best[j+2] = min(best[j+2],best[j])
    bits,debt = survivors(word)
    odd_runs = sum(len(run)%2 for run in ''.join('1' if b else '0' for b in bits).split('0'))
    result = best[-1]-odd_runs-debt
    assert result >= 0
    return result


def main():
    assert __debug__ and LIST[35] == PARITY == '1RB2LA1LA4RA2LA_0LA3RB3LB2RB---'
    if len(sys.argv) not in (2,3):
        raise SystemExit('Pass the compiled checker path and optionally an output TSV path.')
    prefixes = [''.join(w) for n in range(6) for w in product('12',repeat=n)]
    comparisons = 0
    for n in range(1,9):
        for digits in product('12',repeat=n):
            cap = ''.join(digits)
            sharp = min(loss(cap),loss('1'+cap))
            assert min(loss(x+cap) for x in prefixes) == sharp
            assert all(loss(x+'2'+cap) >= loss(cap) for x in prefixes)
            comparisons += len(prefixes)
    print('Tested the exact minimum over prefixes in',comparisons,'cap/prefix pairs.',flush=True)
    tm = TapeMachine(PARITY)
    for _ in range(32):
        word = direct_epoch(tm,(1,2))
        assert word is not None
    assert len(word) == 92
    seed = 0
    for digit in word[-41:]:
        seed = (seed<<1) | (digit == 2)
    print('Literal epoch 32, width',len(word),'and 41-bit seed',seed,flush=True)
    subprocess.run([str(Path(sys.argv[1]).resolve()),str(seed),*sys.argv[2:]],check=True)


if __name__ == '__main__':
    main()
