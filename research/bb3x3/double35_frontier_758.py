"""Verify and extend the blank-orbit window chain above the power-35 gate."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import gzip
from pathlib import Path
import subprocess
import tempfile

from annular_skip_758 import openings
from next_gate_after_fifth_758 import GOAL
from power_gates_758 import coarse_return, coalesce, gate_exits

HERE = Path(__file__).resolve().parent
END = 90_056_781_178_199_398
WIDTH = 5_000
STRIDE = 5*10**12
CUTS = [*range(GOAL, END, STRIDE), END]
TABLE = HERE/'double35_frontier_758.tsv.gz'
HEADER = 'index start end low high blocks calls'


def verify_gate():
    p = 3**35
    # k is nondecreasing with seed within one launch parity.
    for parity,k in enumerate((34,35)):
        for seed in (GOAL+(parity-GOAL)%2, END-(END-parity)%2):
            assert openings(seed).k == k
    boundary = 2*p-2*35-6
    assert END+WIDTH <= boundary-34*(4*35+40)
    for parity,top in enumerate((boundary,boundary+2*35+11)):
        for seed in (END+(parity-END)%2, top-(top-parity)%2):
            assert coarse_return(35,seed,2) > seed
    assert coalesce(gate_exits(35,2),1893) == (2*p+155_534,1893)


def validate(index, row):
    a,b,low,high,blocks,calls = row
    assert 0 <= index < len(CUTS)-1 and [a,b] == CUTS[index:index+2]
    assert b <= low <= high <= b+WIDTH and min(blocks,calls) >= 0
    return row


def read_table(path):
    rows = {}
    with gzip.open(path,'rt') as file:
        assert next(file).strip() == HEADER
        for line in file:
            index,*row = map(int,line.split())
            assert index not in rows
            rows[index] = validate(index,tuple(row))
    return rows


def compute(worker, index):
    output = subprocess.check_output([worker,str(CUTS[index]),str(CUTS[index+1])],text=True)
    return validate(index,tuple(map(int,output.split())))


def save_table(rows, path):
    with tempfile.NamedTemporaryFile(dir=path.parent,delete=False) as tmp:
        with gzip.GzipFile(filename='',fileobj=tmp,mode='wb',mtime=0) as archive:
            archive.write((HEADER+'\n').encode())
            for i,row in sorted(rows.items()):
                archive.write((' '.join(map(str,(i,*row)))+'\n').encode())
    Path(tmp.name).replace(path)


def checkpoint(rows, index, with_clock):
    assert 0 <= index < len(CUTS)-1 and all(i in rows for i in range(index+1))
    _,cut,low,high,_,_ = rows[index]
    seed,edges = coalesce(range(low,high+1),100_000)
    print(f'Row {index:,} forces reset {seed:,} after checking {edges:,} distinct first-return edges.')
    if with_clock:
        from fifth_blank_clock_758 import timed_extension
        from power35_inner_skip_758 import DESTINATION, DESTINATION_CLOCK, PREVIOUS_CLOCK
        start,previous = (DESTINATION,DESTINATION_CLOCK) if cut >= DESTINATION else (GOAL,PREVIOUS_CLOCK)
        bounds = timed_extension(start,seed,[(start,cut,2*10**12)],previous)
        print(f'Raw #758 clock at {seed:,} in [{bounds[0]:,}, {bounds[1]:,}].')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--table',type=Path,default=TABLE)
    parser.add_argument('--worker',type=Path,help='replay rows using a compiled window worker')
    parser.add_argument('--fill',type=Path,metavar='DIR',help='compute missing rows and retain each success in DIR')
    parser.add_argument('--save',type=Path,help='write the combined archive when the selected range finishes')
    parser.add_argument('--jobs',type=int,default=1)
    parser.add_argument('--start',type=int,default=0,help='first index to replay or fill')
    parser.add_argument('--stop',type=int,default=len(CUTS)-1,help='exclusive last index')
    parser.add_argument('--checkpoint',type=int,metavar='INDEX',help='prove an exact merger of the row exits, up to 100,000 edges')
    parser.add_argument('--clock',action='store_true',help='also bound the clock at --checkpoint')
    parser.add_argument('--require-complete',action='store_true')
    args = parser.parse_args()
    if not __debug__ or args.jobs < 1 or not 0 <= args.start <= args.stop < len(CUTS):
        parser.error('enable assertions and supply a valid row range and worker count')
    if args.clock and args.checkpoint is None:
        parser.error('--clock requires --checkpoint')
    rows = read_table(args.table)
    verify_gate()
    if args.fill:
        args.fill.mkdir(parents=True,exist_ok=True)
        for path in args.fill.glob('*.txt'):
            i = int(path.stem)
            row = validate(i,tuple(map(int,path.read_text().split())))
            assert rows.setdefault(i,row) == row
    if args.worker:
        worker = args.worker.resolve()
        def replay(i):
            row = compute(worker,i)
            if args.fill:
                with tempfile.NamedTemporaryFile(mode='w',dir=args.fill,delete=False) as tmp:
                    print(*row,file=tmp)
                Path(tmp.name).replace(args.fill/f'{i:05}.txt')
            return i,row
        # Filling retains every success, including rows completed out of order.
        selected = [i for i in range(args.start,args.stop) if (i not in rows) == bool(args.fill)]
        with ThreadPoolExecutor(args.jobs) as pool:
            for i,row in pool.map(replay,selected):
                assert rows.setdefault(i,row) == row
    if args.save:
        save_table(rows,args.save)
    end = len(CUTS)-1
    frontier = next((i for i in range(end) if i not in rows),end)
    print(f'{len(rows):,}/{end:,} windows, first {frontier:,} consecutive to {CUTS[frontier]:,}.')
    if args.checkpoint is not None:
        if not 0 <= args.checkpoint < frontier:
            parser.error('checkpoint row must belong to the consecutive prefix')
        checkpoint(rows,args.checkpoint,args.clock)
    if frontier == end:
        print(f'The complete grid connects blank to {2*3**35+155_534:,}.')
    elif args.require_complete:
        raise SystemExit(f'Missing window {frontier}')


if __name__ == '__main__':
    main()
