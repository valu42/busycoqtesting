"""Verify the unrestricted even-header classes with more than 28 pairs."""
import argparse
from itertools import combinations
from pathlib import Path
import subprocess

from target_shadow_758 import D

TABLE = Path(__file__).with_name('even_header_entry_758.tsv')


def progressions(r):
    """Unrestricted even h gives N = -A modulo 2 D 3^(m-r)."""
    for m in (r,r+1):
        modulus = 2*D*3**(m-r)
        for pairs in range(29,m//2+1):
            blocks = m-pairs
            jumps = m-2*pairs
            residues = set()
            # The word starts with P; an overshoot also ends in P.
            for places in combinations(range(1,blocks-int(m>r)),jumps):
                jump_positions = set(places)
                a,scale = 0,1
                for i in range(blocks):
                    if i in jump_positions:
                        a *= 3
                    else:
                        a,scale = 9*a+5*scale,4*scale
                assert scale == 4**pairs and a%10 == 5
                residues.add((-a)%modulus)
            for residue in sorted(residues):
                yield r,m,pairs,residue,modulus


def tail(n,q,limit=400):
    depth = 0
    while depth <= limit:
        assert 0 < n < q and n%2
        if 3*n<q:
            n *= 3
            depth += 1
        elif 9*n>5*q:
            n,q = 9*n-5*q,4*q
            depth += 2
        else:
            assert 3*n>q and 9*n<5*q
            return depth
    raise ValueError('tail exceeds verification limit')


def verify(worker=None):
    specs = [s for r in (57,58,59) for s in progressions(r)]
    assert len(specs) == 445 and specs[0] == (57,58,29,79_179_505,83_755_650)
    with TABLE.open() as f:
        assert next(f).strip() == 'r m p residue modulus witness max_calls'
        recorded = [tuple(map(int,line.split())) for line in f]
    assert len(recorded) == len(specs)
    for spec,row in zip(specs,recorded):
        assert row[:5] == spec and len(row)==7
        r,m,p,residue,modulus,n,depth = row
        assert 0<n<4**p and n%modulus == residue
        assert tail(n,4**p) == depth <= 188
    if worker:
        query = ''.join(' '.join(map(str,s))+'\n' for s in specs)
        result = subprocess.check_output([worker,'--progressions'],input=query,text=True)
        assert [tuple(map(int,l.split())) for l in result.splitlines()] == recorded
    return [max(row[-1] for row in recorded if row[0]==r) for r in (57,58,59)]


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('run without -O for verification')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--worker',type=Path,help='compiled dyadic_survival_758.cpp, to repeat the exact searches')
    args = parser.parse_args()
    print('Maximum high-pair tail at each exponent 57, 58, 59:',verify(args.worker.resolve() if args.worker else None))
