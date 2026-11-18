"""Check the line-26 record walk against sparse counters and saved physical time."""
import argparse
import json
from pathlib import Path
import subprocess

from column_phases import lift, p_step, q_step
from column_raw_time import recover, literal_check, physical_trips
from frontiers.checkpoints import checksum, holdouts

HERE = Path(__file__).resolve().parent
CHECKPOINT = HERE/'frontiers/runs/line26-record96.json'
MACHINE = '1RB2RB4LA2RA1LA_2LA4RA3LA---3RA'


def rows(text):
    return [tuple(map(int,line.split())) for line in text.splitlines()
            if line and not line.startswith('#')]


def gap_walk():
    for b in range(257):
        u, e, wraps = 0, 1, 0
        for _ in range(b):
            u, stop = p_step(u,e)
            wraps += stop == 0
        e, stop = q_step(u,e)
        jump = stop-1
        assert jump == 1 + (b%4 in (1,2))
        assert wraps == (b+3)//4
        assert wraps-jump == (b+1)//4-1
        assert e >> jump == 1 and u >> jump == 0
        assert 2*(u%2)+(e%2) == (3 if b%2 else 0)
        if jump == 2:
            assert 2*((u>>1)%2)+((e>>1)%2) == 2


def root_replay(records, limit):
    u = e = width = 0
    previous = 3
    old_width = 0
    result = []
    for tick in range(1,limit+1):
        for _ in range(9):
            u, stop = p_step(u,e)
            width += stop == 0
        e, stop = q_step(u,e)
        depth = 3+stop-1
        assert depth < width
        if tick == 1:
            assert (width,depth) == (5,4)
        elif depth > previous:
            # Recover b uniquely from wrap count, jump length and the low parity.
            delta = width-old_width
            candidates = [b for b in range(max(0,4*delta-3),4*delta+1)
                          if 1+(b%4 in (1,2))==depth-previous and
                          b%2==(u>>(previous-3))%2]
            b, = candidates
            result.append((tick,previous,b,depth,width))
        if tick == 1 or depth>previous:
            previous,old_width = depth,width
    assert result == [r for r in records if r[0]<=limit]


def phase_window(gaps, start, count):
    """Return each record margin relative to the starting margin."""
    u,e,width = 0,1,0
    result = []
    current = 0
    index = start
    while len(result)<count:
        for _ in range(gaps[index]):
            u,stop = p_step(u,e)
            width += stop==0
        e,stop = q_step(u,e)
        if stop-1>current:
            current = stop-1
            result.append(width-current)
        index = (index+1)%len(gaps)
    return result


def verify_endpoint(payload):
    tick, width = payload['ticks'], payload['width']
    u,e = int(payload['u'],16),int(payload['e'],16)
    assert payload['machine']==holdouts()[25]==MACHINE
    assert payload['head']==-8*tick-1 and payload['state']=='A'
    assert max(u,e).bit_length()<=width
    last = (e&~u) & -(e&~u)
    assert last.bit_length()-1==payload['record_depth']
    return (192*tick*tick-8*tick+3*payload['physical_visit_sum']
            +u.bit_count()+2*e.bit_count()+7*width-3*width*width+5)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--records', type=Path, help='compiled column_records.cpp')
    parser.add_argument('--clock', type=Path, help='compiled column_raw_time.cpp')
    parser.add_argument('--extended', action='store_true', help='replay the large endpoint on two cuts')
    args = parser.parse_args()
    if args.extended and not (args.records and args.clock):
        parser.error('--extended needs both binaries')
    records = rows((HERE/'column-records.txt').read_text())
    doc = json.loads(CHECKPOINT.read_text())
    p = doc['payload']
    assert checksum(p)==doc['sha256'] and verify_endpoint(p)==p['steps']
    assert records[-1]==(p['ticks'],94,14,p['record_depth'],p['width'])
    run_bound = 4  # The enumerated cyclic maximum at cut 15.
    for _ in range(15, p['record_depth']):
        run_bound += (run_bound+1)//2
    assert 3*run_bound < 2**52 and p['record_depth']+52 <= p['width']
    gap_walk()
    root_replay(records,200000)
    previous_tick, previous, width = 1,4,5
    gains = []
    for tick,old,b,new,size in records:
        assert tick>previous_tick and old==previous
        assert new==old+1+(b%4 in (1,2)) and size==width+(b+3)//4
        assert size>new
        gains.append(size-new-(width-old))
        previous_tick,previous,width = tick,new,size
    minima = [min(sum(gains[i:i+h]) for i in range(len(gains)-h+1)) for h in range(1,7)]
    assert (len(gains),minima)==(61,[-1,-2,-2,-1,-1,1])
    period=[9]
    for _ in range(3):
        period=lift(period)
    assert phase_window(period,1,6)[-1]==13
    assert phase_window(period,14,6)[-1]==-4
    print('61 record transitions; minimum gains over windows of lengths 1..6:',minima)
    print('Cut 6 six-record gain: true start +13; shifted start -4.')
    if args.records:
        binary=args.records.resolve()
        checks=[(3,35),(13,60)]
        if args.extended:
            checks.extend([(17,96),(18,96)])
        for cut,target in checks:
            output=subprocess.check_output([binary,str(cut),str(target)],text=True)
            seed=int(output.splitlines()[1].split()[2])
            assert rows(output)==[r for r in records if seed<r[0] and r[1]<target]
    if args.clock:
        binary=args.clock.resolve()
        literal_check(binary)
        physical_trips(binary)
        if args.extended:
            for cut in (17,18):
                steps,visits,word=recover(binary,cut,p['ticks'])
                u=sum((digit//2)<<i for i,digit in enumerate(word))
                e=sum((digit%2)<<i for i,digit in enumerate(word))
                assert (steps,visits,len(word),hex(u),hex(e))==(
                    p['steps'],p['physical_visit_sum'],p['width'],p['u'],p['e'])
                print('Full tape and clock match at calendar cut',cut)


if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Enable assertions.')
    main()
