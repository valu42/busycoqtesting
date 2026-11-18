#!/usr/bin/env python3
"""Exactly time completed normal epochs of the 424-pair blank register on line 17."""
import argparse
from bisect import bisect_right
from array import array
from dataclasses import dataclass
import json
from pathlib import Path
import sys
import subprocess

from checkpoints import ROOT, atomic_json, checksum, holdouts
sys.path.insert(0, str(ROOT))
from marked_register import lift_period
from prior_frontier import DATA, HEAD, M17, digits, mark_step, periodic_marks


@dataclass
class Counts:
    """Counts of input slots, raw calls, and instructions inside digit pairs."""
    state: tuple
    slots: int = 0
    calls: int = 0
    interior: int = 0

    def add(self, other, copies=1):
        self.slots += copies*other.slots
        self.calls += copies*other.calls
        self.interior += copies*other.interior
        self.state = other.state


def literal_counts(state, word):
    result = Counts(state)
    for bit in word:
        v, p = result.state
        c = bool(p or bit)
        nv, np, out = mark_step(v,p,bit)
        result.calls += (4,3,3)[v] if c else 1
        result.interior += (2,6,4)[v] if c else (2 if v == 2 else 0)
        result.slots += len(out)
        result.state = nv, np
    return result


def word_counts(state, head, period, slots):
    """Evaluate a finite prefix through the initial six possibly nonhomogeneous pairs."""
    result = literal_counts(state, head[:slots])
    whole, tail = divmod(max(0, slots-len(head)), len(period))
    seen = {}
    j = 0
    while j < whole and result.state not in seen:
        seen[result.state] = j, result.slots, result.calls, result.interior
        result.add(literal_counts(result.state, period))
        j += 1
    if j < whole:
        prior, n, c, inner = seen[result.state]
        laps, rem = divmod(whole-j,j-prior)
        result.add(Counts(result.state,result.slots-n,result.calls-c,result.interior-inner),laps)
        for _ in range(rem):
            result.add(literal_counts(result.state,period))
    result.add(literal_counts(result.state, period[:tail]))
    return result


def marked_counts(slots, marks, v=1, pending=False):
    """Exact counts for marks at one-based positions, with a possibly cut-off final C burst."""
    incoming = slots
    emitted = inner = 0
    last = 0
    def ordinary(n):
        nonlocal v, emitted, inner
        rotations,v = divmod(v+n,3)
        emitted += rotations
        inner += 2*rotations
    for t in marks:
        if t > slots:
            break
        if pending or t <= last:
            raise ValueError('overlapping marked bursts')
        ordinary(t-last-1)
        r = v
        take = min(slots-t+1,r+1)
        for _ in range(take):
            incoming += 3 if v==0 else 2
            inner += (2,6,4)[v]
            emitted += 1 if v==0 else 2
            pending = v != 0
            v = (v+2)%3
        last = t+take-1
    if last < slots:
        if pending:
            raise ValueError('unconsumed pending C')
        ordinary(slots-last)
    return Counts((v,int(pending)), emitted, incoming, inner)


def periodic_counts(period, marks, slots):
    """Skip repetitions of a mark period when the trit and pending bit recur."""
    whole, rem = divmod(slots, period)
    result = Counts((1,0))
    seen = {}
    i = 0
    while i < whole and result.state not in seen:
        seen[result.state] = i, result.slots, result.calls, result.interior
        result.add(once_counts(period,marks,result.state))
        i += 1
    if i < whole:
        prior, n, calls, inner = seen[result.state]
        laps, tail = divmod(whole-i,i-prior)
        result.add(Counts(result.state,result.slots-n,result.calls-calls,result.interior-inner),laps)
        for _ in range(tail):
            result.add(once_counts(period,marks,result.state))
    result.add(once_counts(rem,marks,result.state))
    return result


def mark_image(marks, limit, state):
    """Exact prefix of the next mark list. Virtually complete bursts to compute times."""
    v,p = state
    c = v-1
    if p:
        # Pending from the previous pair acts as a mark on the very first slot.
        # Count it here, with the same output timing as any other initial burst.
        if marks and marks[0] <= v+1:
            raise ValueError('initial pending burst overlaps a mark')
        def entries():
            yield 1
            yield from marks
        times = entries()
    else:
        times = iter(marks)
    for t in times:
        if t>limit: break
        x = t+c
        r = x%3
        if r:
            yield (x+5*r)//3
        c += 4*(1+r)


def once_counts(slots, marks, state):
    if not state[1]:
        return marked_counts(slots,marks,state[0])
    finish = min(slots,state[0]+1)
    if marks and marks[0] <= finish:
        raise ValueError('pending input overlaps a mark')
    result = literal_counts(state,bytes(finish))
    if finish < slots:
        result.add(marked_counts(slots-finish,(t-finish for t in marks if t>finish), result.state[0]))
    return result


def record(epochs, counts, register=DATA, base_steps=2308940, base_head=-844, start_epoch=0):
    initial = digits(register)
    if len(counts)!=len(initial):
        raise ValueError('incomplete digit tally')
    if counts[-1].slots:
        raise ReachesTerminal('a call reaches the old right boundary; stop before this epoch')
    # Header = 58 + outgoing raw probes. Every ordinary pair contributes its
    # two boundary crossing counts plus its internal moves. At the pile, a
    # reset 12 emits four slots, uses 9 input probes and makes 10 internal
    # moves. The innermost pair emits the data-dependent number of calls.
    new_epoch = start_epoch+epochs
    raw = base_steps + 58*epochs + 14*epochs*(2*start_epoch+epochs-1)
    raw += sum(2*c.calls+c.interior for c in counts)
    pairs = []
    for i,c in enumerate(counts):
        outgoing = counts[i+1].state[1] if i+1<len(counts) else initial[i][1]
        pairs.append('102'[c.state[0]]+str(2+outgoing))
    return {'format':'bb2x5-line17-epochs-v1','machine':M17,'line':17,
            'epochs':new_epoch,'steps':raw,'head':base_head-2*epochs,'state':'A',
            'header':HEAD,'pile_pairs':new_epoch,'register':''.join(pairs),'terminal':'2'}


class ReachesTerminal(ValueError):
    """The cut at the singleton receives a raw probe during the requested interval."""


def advance(seed, epochs, engine):
    """Resume at a physical sweep boundary. Finite arbitrary digit phases are preserved."""
    if not __debug__:
        raise ValueError('the register verifier requires Python assertions')
    if holdouts()[16] != M17 or epochs < 0:
        raise ValueError('invalid machine or additional epoch count')
    if epochs == 0:
        return dict(seed)
    data = digits(seed['register'])
    counts = []
    n = 4*epochs
    head,period = b'',bytes((0,1,0,0))
    # A valid continuation is a suffix of the same periodic source at each early
    # cut. Keep its exact phase until a bounded finite prefix can be materialized.
    cut = 0
    while cut < len(data) and (n > 4000000 or cut < 6):
        state = data[cut][0], data[cut-1][1] if cut else 0
        counts.append(word_counts(state,head,period,n))
        n = counts[-1].slots
        head,period = periodic_marks(state,head,period)
        cut += 1
        if len(head)+len(period)>4000000:
            raise ValueError('resume period budget; choose fewer additional epochs')
    if cut < len(data):
        first = head[:n]
        cycles,tail = divmod(n-len(first),len(period))
        word = first + period*cycles + period[:tail]
        if engine:
            # Input is binary, one 0/1 byte per slot. The suffix can begin with
            # an unfinished burst and digits in any of their physical states.
            proc = subprocess.run([str(Path(engine).resolve()),'resume',seed['register'],str(cut),str(n)],
                                  input=word,capture_output=True)
            if proc.returncode: raise ValueError(proc.stderr.decode().strip() or 'resume worker failed')
            for row in proc.stdout.splitlines():
                v,p,count,calls,inner=map(int,row.split())
                if v not in range(3) or p not in (0,1) or not 0<=count<=2*n or not n<=calls<=4*n or not 0<=inner<=6*n:
                    raise ValueError('invalid native resumed counts')
                counts.append(Counts((v,p),count,calls,inner));n=count
            if len(counts)!=len(data): raise ValueError('incomplete native resumed counts')
        else:
            marks = array('Q',(i for i,bit in enumerate(word,1) if bit))
            for i in range(cut,len(data)):
                state=data[i][0],data[i-1][1]
                c=once_counts(n,marks,state)
                marks=array('Q',(t for t in mark_image(marks,n,state) if t<=c.slots))
                counts.append(c);n=c.slots
    return record(epochs,counts,seed['register'],seed['steps'],seed['head'],seed['epochs'])


def replay(epochs, periodic_cut=45, mark_budget=10000000, engine=None):
    """Replay from the independently checked 424-pair entry. All slot numbers are one-based."""
    if not __debug__:
        raise ValueError('the register verifier requires Python assertions')
    if epochs < 0 or not 6 <= periodic_cut <= 70 or mark_budget < 1:
        raise ValueError('invalid epoch target or work limits')
    if holdouts()[16] != M17:
        raise ValueError('line 17 encoding mismatch')
    data = digits(DATA)
    counts = []
    n = 4*epochs
    head, period = b'', bytes((0,1,0,0))
    for i,(v,_) in enumerate(data[:6]):
        state = v, data[i-1][1] if i else 0
        count = word_counts(state,head,period,n)
        counts.append(count)
        n = count.slots
        head,period = periodic_marks(state,head,period)
    if head:
        raise ValueError('expected pure periodic input at digit six')
    marks = array('Q',(i for i,bit in enumerate(period,1) if bit))
    length = len(period)
    # Python handles arbitrary-precision early slot counts. The optional native
    # period lifter takes over once the projected counts fit its integer type.
    handoff = periodic_cut
    for i in range(6,periodic_cut):
        if engine and n <= (2**64-1)//16:
            handoff = i
            break
        if data[i] != (1,0) or data[i-1][1]:
            raise ValueError('expected homogeneous register')
        c = periodic_counts(length,marks,n)
        counts.append(c)
        n = c.slots
        if len(marks)*3 > mark_budget: raise ValueError('period mark budget')
        length,marks,_ = lift_period(length,marks,0)
    tail_start = periodic_cut
    if engine:
        # Each digit up to 402 has v=1 and receives a clear initial flag.
        width = 403-handoff
        if any(data[i] != (1,0) or data[i-1][1] for i in range(handoff,403)):
            raise ValueError('invalid native homogeneous band')
        proc = subprocess.run([str(Path(engine).resolve()),str(n),str(length),str(width),str(mark_budget),
                               '65536',str(periodic_cut-handoff)],
                              input=' '.join(map(str,marks)),text=True,capture_output=True)
        if proc.returncode: raise ValueError(proc.stderr.strip() or 'native mark worker failed')
        rows = proc.stdout.splitlines()
        if len(rows) != width+1 or rows[-1].split()[:1] != ['marks']:
            raise ValueError('incomplete native output')
        for row in rows[:-1]:
            v,p,slots,calls,inner = map(int,row.split())
            if v not in range(3) or p not in (0,1) or not n <= calls <= 4*n or not 0 <= slots <= 2*n or not 0 <= inner <= 6*n:
                raise ValueError('invalid native counts')
            counts.append(Counts((v,p),slots,calls,inner))
            n = slots
        finite = array('Q',map(int,rows[-1].split()[1:]))
        tail_start = 403
    else:
        whole, tail = divmod(n,length)
        size = whole*len(marks) + bisect_right(marks,tail)
        if size > mark_budget:
            raise ValueError('finite mark budget')
        finite = array('Q',(base+t for base in range(0,n,length) for t in marks if base+t<=n))
    for i in range(tail_start,len(data)):
        state = data[i][0], data[i-1][1]
        c = once_counts(n,finite,state)
        counts.append(c)
        finite = array('Q',(t for t in mark_image(finite,n,state) if t<=c.slots))
        n = c.slots
    return record(epochs,counts)


def save(path, state):
    atomic_json(path,{'payload':state,'sha256':checksum(state)})


def load(path):
    doc = json.loads(Path(path).read_text())
    p = doc['payload']
    if doc['sha256']!=checksum(p) or (p['format'],p['line'],p['machine'])!=('bb2x5-line17-epochs-v1',17,M17):
        raise ValueError('invalid line 17 checkpoint')
    if (p['epochs']<0 or p['pile_pairs']!=p['epochs'] or p['head'] != -844-2*p['epochs']
            or p['steps'] < 2308940 or p['steps']%2 != p['head']%2
            or p['state']!='A' or p['header']!=HEAD or p['terminal']!='2'
            or not isinstance(p['register'],str) or len(p['register'])!=848
            or set(p['register'][::2])-set('102') or set(p['register'][1::2])-set('23')):
        raise ValueError('invalid line 17 boundary')
    return p


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--epochs',type=int,required=True)
    parser.add_argument('--cut',type=int,default=45)
    parser.add_argument('--mark-budget',type=int,default=10000000)
    parser.add_argument('--engine',type=Path,help='optional native finite mark worker')
    parser.add_argument('--resume',type=Path,help='start at this saved boundary; --epochs remains an absolute target')
    parser.add_argument('--checkpoint',type=Path,required=True)
    args=parser.parse_args()
    try:
        if args.resume:
            seed = load(args.resume)
            result = advance(seed,args.epochs-seed['epochs'],args.engine)
        else:
            result = replay(args.epochs,args.cut,args.mark_budget,args.engine)
        save(args.checkpoint,result)
        print(f"Line 17 at {result['epochs']} epochs and {result['steps']} raw steps.")
    except (ValueError, OverflowError, OSError) as exc:
        parser.exit(2,f'Replay stopped: {exc}\n')


if __name__=='__main__': main()
