"""Check the power-36 approach to a one-bulk halter and the doubled gate."""
from pathlib import Path
import subprocess

from annular_skip_758 import openings
from check_bb33 import first_return
from double35_frontier_758 import read_table, run_grid, validate
from fourth_clock_758 import timed_return
from power35_inner_skip_758 import direct
from power_gates_758 import coarse_return, coalesce, gate_exits
from power_skip_758 import corridor, skip

POWER = 3**36
START = POWER+112_032
HALTER = 270_170_343_534_598_339
END = HALTER-199_000
WIDTH = 5_000
CUTS = [*range(START,END,10**13),END]
TABLE = Path(__file__).with_name('double36_frontier_758.tsv.gz')
DOUBLED = 300_189_270_594_119_530


def symbolic_census(worker):
    """Reproduce all zero-query receipts and the complementary direct requests."""
    stored = read_table(TABLE,CUTS)
    count = 0
    for i,(a,b) in enumerate(zip(CUTS,CUTS[1:])):
        check = subprocess.run([worker,str(a),str(b)],capture_output=True,text=True)
        if check.returncode == 0:
            row = validate(i,tuple(map(int,check.stdout.split())),CUTS)
            assert row[-1] == 0 and stored.get(i) == row
            count += 1
        else:
            assert check.returncode == 1 and check.stderr.strip() == 'direct trace requested'
    assert count == 10_010
    print(f'{count:,} symbolic windows and {len(CUTS)-1-count:,} requiring exact returns.')


def verify_gate():
    q = HALTER
    assert len(CUTS)-1 == 12008
    assert coalesce(gate_exits(36,1),1455) == (START,1455)
    # Maximal jump count is nondecreasing within each parity class.
    for parity,k in ((0,35),(1,36)):
        for s in (START+(parity-START)%2, END-(END-parity)%2):
            assert openings(s).k == k
    assert 64*((END+50_000)//2)<2**64
    # The original Cover table includes powers up to 3^36. Its greatest
    # possible initial common-jump threshold is attained at an even seed.
    assert (2*(END+3)+4)//4 < POWER
    # After J^36 the gap after one bulk is 2P-10i-9. Only gap
    # three can halt since P=1 mod 5, and its i is odd as required.
    i = (POWER-6)//5
    assert POWER%10 == 1 and 2*POWER-10*i-9 == 3 and i%2
    assert q == 4*i-1+POWER-73 == 9*POWER//5-78 and q%2
    assert first_return(q) is None and first_return(q+2) is None
    even_h = 2*(POWER//3)
    even_first = even_h+4*((2*even_h)//10)-76
    assert even_first == 180_113_562_356_398_866
    try:
        coarse_return(36,even_first-2,2)
    except AssertionError:
        pass
    else:
        raise AssertionError('preceding even seed has the one-bulk word')
    near = 2*POWER-2*36-6
    for s in (even_first,even_first+2,near):
        assert coarse_return(36,s,2)-s == 79+(s&2)
    for parity,first,top in ((0,q+3,near),(1,q+4,near+83)):
        for s in (first,top-(top-parity)%2):
            g = coarse_return(36,s,2)-s
            assert 0<g<=81 and g%2
    assert q+3 <= near-34*(4*36+40)
    # Before the sharp all-parity gate the preceding odd seed is a halter.
    merger,edges = coalesce(range(END,END+WIDTH+1),9601)
    assert (merger,edges) == (270_170_343_534_454_530,9601)
    # The final archived window has the singleton exit END+103.
    singleton,entry_count,entry_time = direct(END+103,merger)
    assert singleton == merger and entry_count == 440
    assert entry_time == 155_819_331_675_901_112_115_483_857_838_995_992_304
    boundary,n0,t0 = direct(merger,q-48)
    assert (boundary,n0,t0) == (q-48,1063,352_866_774_980_705_962_657_849_208_048_208_692_711)
    assert timed_return(boundary) == (q+102,280_792_859_414_564_088_211_790_599_247_683_383)
    left, _ = corridor(36,2)
    s1,n1,t1 = direct(merger,left)
    s2,n2,t2,evaluations = skip(36,2,s1)
    s3,n3,t3 = direct(s2,DOUBLED)
    assert (s1,n1) == (270_170_343_534_599_399,1076)
    assert (s2,n2,evaluations) == (300_189_270_593_997_238,375_236_588_242_473,17)
    assert (s3,n3) == (DOUBLED,461)
    assert coalesce(gate_exits(36,2),1301) == (DOUBLED,1301)
    assert n1+n2+n3 == 375_236_588_244_010
    assert t1+t2+t3 == 54_355_875_010_408_737_199_375_449_280_878_118_887_067_416_077_742


def checkpoint(rows,index,with_clock):
    _,cut,low,high,_,_ = rows[index]
    target,edges = coalesce(range(low,high+1),100_000)
    print(f'From the power-36 checkpoint row {index:,} forces reset {target:,} after {edges:,} distinct merger edges.')
    if with_clock:
        from fifth_blank_clock_758 import timed_extension
        bounds = timed_extension(START,target,[(START,cut,2*10**12)],(0,0))
        print(f'This conditional segment takes between {bounds[0]:,} and {bounds[1]:,} raw transitions.')


if __name__ == '__main__':
    run_grid(CUTS,TABLE,verify_gate,checkpoint,
             f'The complete grid connects the power-36 checkpoint to {DOUBLED:,}.',__doc__)
