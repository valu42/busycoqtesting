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
LATEST = HERE/'frontiers/runs/line26-width205.json'
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


def anchored_calendars(records):
    by_old = {old: b for _, old, b, _, _ in records}
    gaps = [9]
    for j in range(3, 16):
        first, second = gaps[0], gaps[1 % len(gaps)]
        assert (j in by_old) == (first % 2 == 0)
        if j in by_old:
            assert second == by_old[j]
        next_gaps = lift(gaps)
        increase = 1 if first % 2 else (second + 1) // 2
        assert next_gaps[0] == first + increase
        gaps = next_gaps


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


def future_arrivals(binary, cut, target, tick, count, digits):
    result = subprocess.check_output(
        [binary, '--arrivals', str(cut), str(target), str(tick), str(count), digits],
        text=True)
    return rows(result)


def small_arrivals(binary):
    # Tick 1 has full digits 00021. Use individual P and Q updates at cut 3.
    for target in (4, 5):
        n = target - 3
        u, e = 1, 2
        expected = []
        safe = 0
        tick = 1
        while len(expected) < 20:
            tick += 1
            for _ in range(9):
                old_u, old_e = u, e
                u, _ = p_step(u, e)
                # Count the number of scalar P leaving this finite prefix.
                tokens = 1
                for i in range(n):
                    ui, ei = (old_u >> i) & 1, (old_e >> i) & 1
                    tokens = (2-ei)*((tokens+1-ui)//2)
                safe += tokens
            e, stop = q_step(u, e)
            if stop > n:
                expected.append((tick, safe))
                safe = 0
        assert future_arrivals(binary, 3, target, 1, 20, '00021') == expected


def verify_endpoint(payload):
    tick, width = payload['ticks'], payload['width']
    u,e = int(payload['u'],16),int(payload['e'],16)
    assert payload['machine']==holdouts()[25]==MACHINE
    assert payload['head']==-8*tick-1 and payload['state']=='A'
    assert max(u,e).bit_length()<=width
    last = (e&~u) & -(e&~u)
    assert last.bit_length()-1==payload.get('last_stop',payload['record_depth'])
    return (192*tick*tick-8*tick+3*payload['physical_visit_sum']
            +u.bit_count()+2*e.bit_count()+7*width-3*width*width+5)


def check_continuation(start, end, arrivals):
    cut = 74
    u, e = int(start['u'],16)>>cut, int(start['e'],16)>>cut
    width = start['width']
    pending = 0
    previous = start['ticks']
    for tick, gap in arrivals:
        assert tick > previous and gap >= 0
        previous = tick
        for _ in range(gap):
            # Count scalar safe output at the old record cut 96.
            sent = 1
            for i in range(start['record_depth'] - cut):
                sent = (2-((e>>i)&1))*((sent+1-((u>>i)&1))//2)
                if not sent:
                    break
            pending += sent
            u, stop = p_step(u,e)
            width += stop == 0
        e, stop = q_step(u,e)
        assert cut+stop-1 < start['record_depth']
    assert len(arrivals)==215 and arrivals[107][0]==1052754703428
    assert (tick, width, pending)==(end['ticks'],end['width'],4)
    assert (u,e)==(int(end['u'],16)>>cut,int(end['e'],16)>>cut)
    assert cut+stop-1==end['last_stop']


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
    latest = json.loads(LATEST.read_text())
    end = latest['payload']
    assert checksum(end)==latest['sha256'] and verify_endpoint(end)==end['steps']
    future = rows((HERE/'column-cut74.txt').read_text())
    check_continuation(p, end, future)
    run_bound += (run_bound+1)//2
    assert 3*run_bound < 2**52 and 97+52 <= end['width']
    gap_walk()
    anchored_calendars(records)
    root_replay(records,200000)
    previous_tick, previous, width = 1,4,5
    gains = []
    for tick,old,b,new,size in records:
        assert tick>previous_tick and old==previous
        assert new==old+1+(b%4 in (1,2)) and size==width+(b+3)//4
        assert size>new
        gains.append(size-new-(width-old))
        previous_tick,previous,width = tick,new,size
    total = residue = 0
    for n, (_, _, b, j, w) in enumerate(records, 1):
        total += b
        residue += (b+1)%4
        assert 4*(w-j-1) == total-3*n-residue
        assert 2*total >= 15*n
        if n==2:
            assert 2*total == 15*n
    assert (total,residue)==(715,104)
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
        small_arrivals(binary)
        u, e = int(end['u'], 16), int(end['e'], 16)
        digits = ''.join(str(2*((u>>i)&1)+((e>>i)&1)) for i in range(end['width']))
        guards = [future_arrivals(binary, cut, 60, end['ticks'], 108, digits)
                  for cut in (15,17)]
        assert guards[0]==guards[1] and len(guards[0])==108
        assert guards[0][-1][0]==end['safe_through_tick']
        print('Next 108 cut-60 arrivals give physical survival through tick', guards[0][-1][0])
        checks=[(3,35),(13,60)]
        if args.extended:
            checks.extend([(17,96),(18,96)])
        for cut,target in checks:
            output=subprocess.check_output([binary,str(cut),str(target)],text=True)
            seed=int(output.splitlines()[1].split()[2])
            assert rows(output)==[r for r in records if seed<r[0] and r[1]<target]
        if args.extended:
            u, e = int(p['u'], 16), int(p['e'], 16)
            digits = ''.join(str(2*((u>>i)&1)+((e>>i)&1)) for i in range(p['width']))
            arrivals = [future_arrivals(binary, cut, 74, p['ticks'], 215, digits)
                        for cut in (17,18)]
            assert arrivals[0] == arrivals[1] == future
            print('Both calendars match all 215 cut-74 arrivals through tick', end['ticks'])
    if args.clock:
        binary=args.clock.resolve()
        literal_check(binary)
        physical_trips(binary)
        if args.extended:
            for cut, checkpoint in ((17,p),(18,p),(17,end),(18,end)):
                steps,visits,word=recover(binary,cut,checkpoint['ticks'])
                u=sum((digit//2)<<i for i,digit in enumerate(word))
                e=sum((digit%2)<<i for i,digit in enumerate(word))
                assert (steps,visits,len(word),hex(u),hex(e))==(
                    checkpoint['steps'],checkpoint['physical_visit_sum'],checkpoint['width'],
                    checkpoint['u'],checkpoint['e'])
                print('Full tape and clock match at calendar cut',cut,'tick',checkpoint['ticks'])


if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Enable assertions.')
    main()
