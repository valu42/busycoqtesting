#!/usr/bin/env python3
"""Build a certified blank-orbit pulse period and advance complete line-17 checkpoints."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

from checkpoints import atomic_json
from line17 import Counts, DATA, M17, digits, literal_counts, load, native_counts, record, replay, save


def file_hash(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(4 << 20), b''):
            digest.update(chunk)
    return digest.hexdigest()


def metadata_path(period):
    return period.with_name(period.name + '.json')


def build(args):
    period = args.period.resolve()
    with tempfile.TemporaryDirectory(dir=period.parent) as folder:
        tmp = Path(folder) / 'period'
        command = [str(args.engine.resolve()), str(args.cut), str(args.word_bits), str(args.threads),
                   'export-coded', str(tmp)]
        run = subprocess.run(command, input=DATA+'\n', text=True, capture_output=True, env=native_env())
        if run.returncode:
            raise ValueError(run.stderr.strip() or 'period export failed')
        header, *text_rows = run.stdout.splitlines()
        name, cut, origin, root, slots, marks = header.split()
        if name != 'period' or int(cut) != args.cut or int(root) <= 0:
            raise ValueError('invalid period export')
        rows = native_counts(text_rows, 4*int(root), args.cut)
        if (rows[-1].slots, rows[-1].interior//2 - rows[-1].slots) != (int(slots), int(marks)):
            raise ValueError('exported prefix counts disagree with its word')
        meta = dict(format='bb2x5-line17-coded-period-v1', machine=M17, cut=args.cut,
                    origin=int(origin), root_period=int(root), slots=int(slots), marks=int(marks),
                    sha256=file_hash(tmp), prefix=[[*r.state, r.slots, r.calls, r.interior] for r in rows])
        os.replace(tmp, period)
        atomic_json(metadata_path(period), meta)
        print(f'Cut {args.cut} has {slots} slots and {marks} marks per {root} sweeps.')


def verified_period(period):
    meta = json.loads(metadata_path(period).read_text())
    if (meta.get('format') != 'bb2x5-line17-coded-period-v1' or meta['machine'] != M17
            or meta['sha256'] != file_hash(period)):
        raise ValueError('period identity or checksum mismatch')
    return meta


def lifted_metadata(meta, result, initial):
    name, copies, source_slots, source_marks, state, slots, calls, interior = result.split()
    copies, source_slots, source_marks, state, slots, calls, interior = map(
        int, (copies, source_slots, source_marks, state, slots, calls, interior))
    if (name != 'lift' or copies not in range(1, 7) or state != initial
            or (source_slots, source_marks) != (meta['slots'], meta['marks']) or interior % 2):
        raise ValueError('inconsistent physical period lift')
    cut = meta['cut'] + 1
    root = copies*meta['root_period']
    prefix = [[v, p, copies*n, copies*c, copies*i] for v,p,n,c,i in meta['prefix']]
    prefix.append([state//2, state%2, slots, calls, interior])
    rows = native_counts([' '.join(map(str, row)) for row in prefix], 4*root, cut)
    start = digits(replay(meta['origin'],6)['register'])
    from line17 import check_pulse_balances
    check_pulse_balances(root, start[:cut], rows)
    return {**meta, 'cut': cut, 'root_period': root, 'slots': slots,
            'marks': interior//2-slots, 'prefix': prefix}


def lift(args):
    period, output = args.period.resolve(), args.output.resolve()
    if len({period, metadata_path(period), output, metadata_path(output)}) != 4:
        raise ValueError('lifted source needs its own destination')
    meta = verified_period(period)
    cut = meta['cut']
    if not 0 < cut < 424:
        raise ValueError('the source must have another physical pair')
    seed = digits(replay(meta['origin'],6)['register'])
    initial = 2*seed[cut][0]+seed[cut-1][1]
    with tempfile.TemporaryDirectory(dir=output.parent) as folder:
        tmp = Path(folder)/'period'
        command = [str(args.engine.resolve()), 'lift', str(period), str(initial), str(args.threads), str(tmp)]
        run = subprocess.run(command, capture_output=True, text=True, env=native_env())
        if run.returncode:
            raise ValueError(run.stderr.strip() or 'period lift failed')
        new = lifted_metadata(meta, run.stdout, initial)
        new['sha256'] = file_hash(tmp)
        os.replace(tmp, output)
        atomic_json(metadata_path(output), new)
        print(f"Cut {new['cut']} has {new['slots']} slots and {new['marks']} marks per {new['root_period']} sweeps.")


def native_env():
    env = os.environ.copy()
    env.setdefault('OMP_WAIT_POLICY', 'PASSIVE')
    return env


def blank_totals_at_origin(epoch):
    # The blank orbit has an origin two sweeps into the 424-pair phase.
    if epoch > 1000:
        raise ValueError('provide cumulative counts for this saved starting checkpoint')
    from prior_frontier import marks_on_word
    word = bytes((0, 1, 0, 0))*epoch
    pending = 0
    original = []
    for trit, flag in digits(DATA):
        state = trit, pending
        row = literal_counts(state, word)
        original.append((*row.state, row.slots, row.calls, row.interior))
        _, word = marks_on_word(state, word)
        pending = flag
    return original


def read_seed_counts(path, seed):
    header, *lines = path.read_text().splitlines()
    if header != f'epochs {seed["epochs"]}':
        raise ValueError('cumulative counts start at a different sweep')
    rows = native_counts(lines, 4*seed['epochs'], 424)
    if record(seed['epochs'], rows) != seed:
        raise ValueError('cumulative counts do not reconstruct the supplied physical seed')
    return [(*r.state, r.slots, r.calls, r.interior) for r in rows]


def atomic_text(path, text):
    with tempfile.NamedTemporaryFile('w', dir=path.parent, delete=False) as file:
        tmp = Path(file.name)
        try:
            file.write(text)
            file.flush()
            os.fsync(file.fileno())
        except BaseException:
            tmp.unlink(missing_ok=True)
            raise
    try:
        os.replace(tmp, path)
    finally:
        tmp.unlink(missing_ok=True)


def checkpoint_interval(path, meta, seed, begin, end, counts_before, args):
    header, *tail = path.read_text().splitlines()
    expected = f"base {begin} {end} {meta['slots']} {meta['marks']}"
    if header != expected:
        raise ValueError('wrong physical interval')
    cycles = end-begin
    delta = cycles*meta['root_period']
    prefix = [Counts((v,p), cycles*n, cycles*c, cycles*i) for v,p,n,c,i in meta['prefix']]
    rows = prefix + native_counts(tail, cycles*meta['slots'], 424-meta['cut'])
    found = record(delta, rows, seed['register'], seed['steps'], seed['head'], seed['epochs'])
    if counts_before is not None:
        totals = [Counts(r.state, r.slots+a[2], r.calls+a[3], r.interior+a[4])
                  for a,r in zip(counts_before, rows)]
        if record(found['epochs'],totals) != found:
            raise ValueError('interval and cumulative physical reconstructions differ')
        text = [f'epochs {found["epochs"]}']
        text += [' '.join(map(str,(*r.state, r.slots, r.calls, r.interior))) for r in totals]
        atomic_text(args.counts,'\n'.join(text)+'\n')
    save(args.checkpoint, found)
    return found


def phase_index(args, period, meta):
    path = args.index.resolve()
    sidecar = metadata_path(path)
    identity = dict(format='bb2x5-line17-phase-index-v1', source_sha256=meta['sha256'],
                    digits=args.digits)
    if path.exists() or sidecar.exists():
        cached = json.loads(sidecar.read_text())
        if cached != {**identity, 'sha256': file_hash(path)}:
            raise ValueError('phase index checksum, depth or source mismatch')
        return path
    with tempfile.TemporaryDirectory(dir=path.parent) as folder:
        tmp = Path(folder)/'index'
        command = [str(args.engine.resolve()), 'index', str(period), str(args.digits),
                   str(args.threads), str(tmp)]
        run = subprocess.run(command, capture_output=True, text=True, env=native_env())
        if run.returncode:
            raise ValueError(run.stderr.strip() or 'phase indexing failed')
        checksum = file_hash(tmp)
        os.replace(tmp, path)
        atomic_json(sidecar, {**identity, 'sha256': checksum})
    return path


def advance(args):
    if not __debug__:
        raise ValueError('run with Python assertions enabled')
    outputs = [p.resolve() for p in (args.checkpoint, args.counts) if p is not None]
    period = args.period.resolve()
    if args.index:
        outputs += [args.index.resolve(), metadata_path(args.index.resolve())]
    if (len(set(outputs)) != len(outputs)
            or any(path in (period, metadata_path(period)) for path in outputs)):
        raise ValueError('period, index, checkpoint and counts need distinct files')
    if args.seed_counts and not args.counts:
        raise ValueError('seed counts require a cumulative counts destination')
    meta = verified_period(period)
    seed = load(args.seed) if args.seed else replay(meta['origin'], 6)
    root = meta['root_period']
    begin, remainder = divmod(seed['epochs']-meta['origin'],root)
    if begin < 0 or remainder or args.epochs < seed['epochs']:
        raise ValueError('the seed must be aligned to the source period and precede the target')
    cut = meta['cut']
    data = digits(seed['register'])
    actual_prefix = [(v, data[i-1][1] if i else 0) for i,(v,_) in enumerate(data[:cut])]
    if len(meta['prefix']) != cut or actual_prefix != [tuple(row[:2]) for row in meta['prefix']]:
        raise ValueError('the physical seed has a different periodic prefix')
    before = None
    if args.counts:
        before = read_seed_counts(args.seed_counts,seed) if args.seed_counts else blank_totals_at_origin(seed['epochs'])
    copies = (args.epochs-seed['epochs']+root-1)//root
    if before is not None and args.seed_counts is None:
        origin_rows = [Counts((v, p), n, c, i) for v, p, n, c, i in before]
        if record(seed['epochs'], origin_rows) != seed:
            raise ValueError('blank counts do not reconstruct the supplied physical seed')
    if not copies:
        if before is not None:
            atomic_text(args.counts,'epochs '+str(seed['epochs'])+'\n'+''.join(' '.join(map(str,r))+'\n' for r in before))
        save(args.checkpoint,seed)
        return
    last = begin
    with tempfile.TemporaryDirectory(dir=period.parent) as folder:
        dest = str(Path(folder)/'period-')
        command = [str(args.engine.resolve()),'virtual',str(period),str(cut),str(args.digits),
                   str(begin),str(copies),str(args.threads),dest,str(args.phase_batch)]
        if args.index:
            command.append(str(phase_index(args,period,meta)))
        with subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
                              text=True, env=native_env()) as proc:
            try:
                proc.stdin.write(seed['register']+'\n')
                proc.stdin.close()
                for message in proc.stderr:
                    parts = message.split()
                    if len(parts) >= 3 and parts[0] == 'base' and parts[2] == 'physical':
                        end = int(parts[1])
                        if end != last+1:
                            raise ValueError('missing completed interval')
                        path=Path(dest+str(end)+'.counts')
                        found=checkpoint_interval(path,meta,seed,begin,end,before,args)
                        path.unlink()
                        last=end
                        print(f'{found["epochs"]} sweeps, {found["steps"]} raw instructions',flush=True)
                    else:
                        print(message.rstrip(),flush=True)
                if proc.wait() or last != begin+copies:
                    raise ValueError('the worker stopped before its requested endpoint')
            except BaseException:
                if proc.poll() is None:
                    proc.terminate()
                raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_subparsers(dest='action',required=True)
    for name in ('build','lift','advance'):
        sub = modes.add_parser(name)
        sub.add_argument('--engine',type=Path,required=True)
        sub.add_argument('--period',type=Path,required=True)
        sub.add_argument('--threads',type=int,default=4)
        if name=='build':
            sub.add_argument('--cut',type=int,default=110)
            sub.add_argument('--word-bits',type=int,default=640_000_000_000)
        elif name=='lift':
            sub.add_argument('--output', type=Path, required=True)
        else:
            sub.add_argument('--epochs',type=int,required=True,help='absolute minimum sweep count')
            sub.add_argument('--digits',type=int,default=5,help='adjacent virtual digits, 1 through 7')
            sub.add_argument('--phase-batch',type=int,default=1,help='source copies per disk pass, 1 through 32')
            sub.add_argument('--index',type=Path,help='reuse or create a checksummed stripe index')
            sub.add_argument('--seed',type=Path)
            sub.add_argument('--seed-counts',type=Path)
            sub.add_argument('--counts',type=Path,help='also save cumulative counts from blank')
            sub.add_argument('--checkpoint',type=Path,required=True)
    args = parser.parse_args()
    try:
        {'build':build, 'lift':lift, 'advance':advance}[args.action](args)
    except (ValueError, OSError, RuntimeError, OverflowError) as exc:
        parser.exit(2,f'Line 17 stopped: {exc}\n')


if __name__=='__main__':
    main()
