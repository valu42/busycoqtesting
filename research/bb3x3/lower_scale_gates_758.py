#!/usr/bin/env python3
"""Verify the halting corridors at scales 7..10 and the gap at scale 7."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import re
import subprocess

from scale_clauses_758 import BASE, EVEN_WORD, H, PREFIX, check_word, first_change

HERE = Path(__file__).resolve().parent
# Each row lists the exact bounds of the simple odd word and the bridge stride.
GATES = {
    6: (6_706_785_856_672, 11_177_976_427_786, None),
    7: (20_120_357_570_016, 33_533_929_283_358, 10**11),
    8: (60_361_072_710_048, 100_601_787_850_074, 2*10**11),
    9: (181_083_218_130_136, 301_805_363_550_222, 10**12),
    10: (543_249_654_390_404, 905_416_090_650_670, 2*10**12),
}
RECEIPT = re.compile(r'nodes (\d+) returns (\d+) halts (\d+) remaining (\d+) '
                     r'maxgain (\d+)(?: exits (\d+)\.\.(\d+))?')


def corridor(n):
    near, far, _ = GATES[n]
    assert first_change(n) == near
    word = PREFIX + "J"*(264-n) + "LR"
    for d in (near, far):
        assert 0 < check_word(H-d, word) <= 1_184
    for d in (near+1,far-1):
        assert 0 < check_word(H-d, EVEN_WORD) <= 615
    assert near < BASE*3**n < far
    try:
        check_word(H-far-2, word)
    except AssertionError:
        return
    raise AssertionError("far endpoint is not sharp")


def bridges(n):
    start, _, step = GATES[n]
    stop = GATES[n-1][1]
    return [(d, max(d-step,stop)) for d in range(start,stop,-step)]


def universal_bands():
    start, stop = GATES[6][1], GATES[7][0]
    return [(a,min(a+250_000_000_000,stop)) for a in range(start,stop,250_000_000_000)]


def run():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--worker',type=Path,default=HERE/'gateway_758')
    p.add_argument('--through',type=int,choices=range(7,11),default=10)
    p.add_argument('--jobs',type=int,default=1)
    p.add_argument('--row',type=int,help='one-based row of the selected calculation')
    p.add_argument('--universal',action='store_true',help='check every start in the gap at scale 7')
    p.add_argument('--endpoints',action='store_true',help='verify corridor endpoints only')
    args=p.parse_args()
    if not __debug__ or args.jobs<1: p.error('enable assertions and use a positive worker count')
    for n in range(7,args.through+1):
        corridor(n)
    if args.endpoints:
        print('Verified corridor endpoints through scale',args.through)
        return
    names = HERE/'lower_scale_bridges_758.tsv'
    archived = [tuple(map(int, line.split())) for line in names.read_text().splitlines()]
    expected = [(n, far, near) for n in range(7,11) for far,near in bridges(n)]
    assert [record[:3] for record in archived] == expected
    for n,far,near,nodes,returns,halts,count,gain,lo,hi in archived:
        assert nodes > 0 and returns >= 0 and halts >= 0 and count > 0 and gain > 0
        assert near-5_000 <= lo <= hi < near
    if args.universal:
        manifest = [tuple(map(int, line.split())) for line in
                    (HERE/'universal_gap7_758.tsv').read_text().splitlines()]
        assert [row[:2] for row in manifest] == universal_bands()
        assert all(nodes == 2*leaves-1 and leaves > 0 for _,_,nodes,leaves in manifest)
        jobs=manifest
    else:
        jobs=[r for r in archived if r[0] <= args.through]
    if args.row is not None:
        if not 1<=args.row<=len(jobs): p.error('row is outside this calculation')
        jobs=jobs[args.row-1:args.row]
    worker=str(args.worker.resolve(strict=True))

    def replay(row):
        if args.universal:
            near,far,_,_=row
            out=subprocess.check_output([worker,'--universal',str(far),str(near)],text=True)
            assert tuple(map(int,out.split())) == row
        else:
            _,far,near,*receipt=row
            out=subprocess.check_output([worker,str(far),str(near)],text=True)
            m=RECEIPT.fullmatch(out.strip())
            assert m is not None and int(m[1])>0
            assert (int(m[4])==0)==(m[6] is None)
            assert [int(x) for x in m.groups() if x is not None] == receipt
            if m[6] is not None:
                assert near-5_000<=int(m[6])<=int(m[7])<near
        return far,near
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        for i,(far,near) in enumerate(pool.map(replay,jobs),1):
            print(f'{i}/{len(jobs)} checked distances {far} through {near}',flush=True)


if __name__=='__main__':
    run()
