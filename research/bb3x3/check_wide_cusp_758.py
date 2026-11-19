"""Replay the all-phase cusp cover and the connected succession of outward gates."""
import argparse
from pathlib import Path
import subprocess
import tempfile

from check_bb33 import first_return
from power_ladder_758 import M, P, MANIFEST, merger
from power_gates_758 import coarse_return


HERE = Path(__file__).parent


def read_rows(path):
    return [tuple(map(int,s.split())) for s in path.read_text().splitlines()
            if s and not s.startswith('#')]


def main(full):
    covers=read_rows(HERE/'power_cusp_ranges_758.tsv')
    links=read_rows(HERE/'power_cusp_links_758.tsv')
    gates={r[0]:r for r in read_rows(MANIFEST)}
    assert covers[0][0]==0 and all(x[1]+2==y[0] for x,y in zip(covers,covers[1:]))
    assert all(row[-1]<=5000 for row in covers)
    # The fixed even word has mass gain at most 8+4*291+4+9*5+5.
    for d in (1,covers[-1][1]-1):
        assert coarse_return(M,P+d,1)==first_return(P+d)
    edge=20_000_000_000
    assert covers[-1][1]==gates[731][1] and covers[-1][1]+5000<gates[731][2]
    root,edges=merger(P+edge+1,5000,35_000)
    assert (root-P,edges)==(20_021_397_898,29_962)
    frontier=root-P
    with tempfile.TemporaryDirectory() as folder:
        binary=Path(folder)/'cover'
        subprocess.run(['c++','-O3','-std=c++17',str(HERE/'power_cusp_cover_758.cpp'),
                        '-lgmpxx','-lgmp','-o',str(binary)],check=True)
        def run(*args):
            output=subprocess.run([str(binary),*map(str,args)],check=True,text=True,capture_output=True).stdout
            return tuple(map(int,output.split()))
        # Independent checks use the original first-return implementation.
        for start in (1_934_340,39_000_181,10**10+1,19_999_999_151):
            seed,count=start,0
            while seed<start+500_000:
                seed=first_return(P+seed)-P
                count+=1
            assert run(start,start+500_000,'--link')==(start,start+500_000,seed,count)
        for row in (covers if full else covers[:1]):
            assert run(*row[:2])==row
        for k,source,low,arrival,n,exit_seed,*window in links:
            _,gate_low,high,_,delta,_=gates[k]
            assert source==frontier and low==gate_low<=arrival<high and exit_seed==high+delta
            if window:
                width,joins,span=window
                assert width>0 and joins>0 and span>0
                if full:
                    assert run(source,low,'--stitch',width)==(source,low,arrival,width,n,joins,span)
            elif full:
                assert run(source,low,'--link')==(source,low,arrival,n)
            frontier=exit_seed
    print(f'all-phase upper offset {gates[731][2]-1} and connected checkpoint offset {frontier}')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--all',action='store_true',help='replay the complete wide census and linked intervals')
    args=parser.parse_args()
    if not __debug__:
        parser.error('enable assertions')
    main(args.all)
