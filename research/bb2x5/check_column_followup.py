"""Reproduce the two record transitions after the fully timed width-205 checkpoint."""
import argparse
import json
from pathlib import Path
import subprocess

from check_column_records import HERE, LATEST, future_arrivals, rows, verify_endpoint
from column_raw_time import recover
from frontiers.checkpoints import checksum


def load(path):
    doc = json.loads(path.read_text())
    p = doc['payload']
    assert doc['sha256']==checksum(p) and p['steps']==verify_endpoint(p)
    return p


def digits(p):
    u, e = int(p['u'],16), int(p['e'],16)
    return ''.join(str(2*((u>>i)&1)+((e>>i)&1)) for i in range(p['width']))


def resumed(binary, cut, start, end):
    line = subprocess.check_output(
        [binary,'--resume',str(cut),str(end['ticks']),str(start['ticks']),
         str(start['physical_visit_sum']),digits(start)],text=True)
    tick, accounting, visits, width, word = line.split()
    t, n, v, w = map(int,(tick,accounting,visits,width))
    assert t==end['ticks'] and w==end['width'] and word==digits(end)
    assert v-2*w*(n-w)==end['physical_visit_sum']


def small_resumptions(binary):
    # Exercise an endpoint between Q events as well as period boundaries.
    for cut in (3,4):
        s, v, word = recover(binary,cut,1)
        assert s>0
        for t in (2,3,4,16,31):
            expected = subprocess.check_output([binary,str(cut),str(t)],text=True)
            actual = subprocess.check_output(
                [binary,'--resume',str(cut),str(t),'1',str(v),''.join(map(str,word))],text=True)
            assert actual==expected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--records',type=Path)
    parser.add_argument('--clock',type=Path)
    args = parser.parse_args()
    start = load(LATEST)
    records = rows((HERE/'column-records.txt').read_text())
    end = None
    clock = args.clock.resolve() if args.clock else None
    counter = args.records.resolve() if args.records else None
    if clock:
        small_resumptions(clock)
    for depth, partial in ((98,4),(99,0)):
        end = load(HERE/f'frontiers/runs/line26-record{depth}.json')
        tick, old, gap, new, width = next(row for row in records if row[3]==depth)
        assert (tick,old,new,width)==(end['ticks'],start['record_depth'],end['record_depth'],end['width'])
        assert new==old+1+(gap%4 in (1,2))
        assert width==start['width']+(gap+3)//4-(partial+3)//4
        if counter:
            for cut in (17,18):
                assert future_arrivals(counter,cut,old,start['ticks'],1,digits(start))==[(tick,gap-partial)]
        if clock:
            for cut in (17,18):
                resumed(clock,cut,start,end)
        print(f'Tick {tick}: gap {gap} at {old}, record {new}, width {width}.')
        start = end

    maximum_run = 4
    for _ in range(15,end['record_depth']):
        maximum_run += (maximum_run+1)//2
    assert 3*maximum_run<2**53 and end['record_depth']+53<=end['width']
    if counter:
        count=end['width']-end['record_depth']-1
        arrivals=[future_arrivals(counter,cut,60,end['ticks'],count,digits(end)) for cut in (15,17)]
        assert arrivals[0]==arrivals[1] and arrivals[0][-1][0]==end['safe_through_tick']
        print('Guaranteed survival through tick',end['safe_through_tick'])


if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Enable assertions.')
    main()
