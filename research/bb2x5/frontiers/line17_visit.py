#!/usr/bin/env python3
"""Locate and time the first visit to a data pair during line 17's 424-pair phase."""
import argparse
from dataclasses import dataclass
from functools import cache
import json
from pathlib import Path
import subprocess

from checkpoints import atomic_json, checksum
import line17
from prior_frontier import HEAD, M17, T17, digits, mark_step


@dataclass(frozen=True)
class Crossing:
    parent: int       # Which incoming raw probe issued this child request?
    clock: int        # Instructions executed in this component up to the crossing
    word: str         # Physical component at that instant


@cache
def probes(trit):
    """(raw entry, normal reply, fixed-register slot) for one 0100 block."""
    script = []
    pending = 0
    for slot,bit in enumerate((0,1,0,0),1):
        if pending or bit:
            script.extend(((1,0,slot),(1,0,slot),(0,int(trit==0),slot)))
            if not trit:
                script.append((1,0,slot))
        else:
            script.append((1,0,slot))
        trit,pending,_ = mark_step(trit,pending,bit)
    return tuple(script)


@cache
def pair_crossings(child_trit):
    """Trace one leading 12, stopping its local clock during child work."""
    child = probes(child_trit)
    tape = [1,2]
    found = []
    clock = 0
    for parent,(state,reply,_) in enumerate(probes(0)):
        x = 0
        while x>=0:
            if x==2:
                entry,answer,_ = child[len(found)]
                if state!=entry:
                    raise ValueError('unexpected pile request')
                found.append(Crossing(parent,clock,''.join(map(str,tape))))
                x,state=1,answer
                continue
            op=T17[state][tape[x]]
            if op is None or clock>=100:
                raise ValueError('invalid pile path')
            tape[x],move,state=op
            x+=move
            clock+=1
        if state!=reply:
            raise ValueError('unexpected pile reply')
    if tape!=[1,2] or len(found)!=len(child):
        raise ValueError('incomplete pile trace')
    return tuple(found)


@cache
def header_crossings(child_trit):
    """Literal header from the head at offset zero through its right cut at seven."""
    child=probes(child_trit)
    tape=dict(enumerate(map(int,HEAD),1))
    x=state=clock=0
    found=[]
    while clock<100:
        if x==7:
            entry,reply,_=child[len(found)]
            if state!=entry:
                raise ValueError('unexpected header request')
            left=min(0,min(tape))
            word=''.join(str(tape.get(i,0)) for i in range(left,7))
            found.append(Crossing(0,clock,word))
            x,state=6,reply
        elif x==-2 and state==0 and tape.get(x,0)==0:
            if len(found)!=len(child) or ''.join(str(tape.get(i,0)) for i in range(-1,7))!=HEAD+'12':
                raise ValueError('invalid final header')
            return tuple(found)
        else:
            op=T17[state][tape.get(x,0)]
            if op is None:
                raise ValueError('header reached an undefined instruction')
            tape[x],move,state=op
            x+=move
            clock+=1
    raise ValueError('unterminated header trace')


def suspended_pile(pairs, child_trit, request):
    """Clock and physical words in left-to-right order before data request."""
    if not pairs:
        header=header_crossings(child_trit)[request]
        return header.clock,header.word,[]
    inner=pair_crossings(child_trit)[request]
    request=inner.parent
    groups=[(inner,1)]
    if pairs>=2:
        regular=pair_crossings(0)
        middle=regular[request]
        groups.append((middle,1))
        request=middle.parent
        if pairs>2:
            outer=regular[request]
            if outer.parent!=request:
                raise ValueError('ordinary pile request does not stabilize')
            groups.append((outer,pairs-2))
    header=header_crossings(0)[request]
    clock=header.clock
    pieces=[]
    for crossing,copies in reversed(groups):
        clock+=copies*crossing.clock
        if pieces and pieces[-1]['word']==crossing.word:
            pieces[-1]['copies']+=copies
        else:
            pieces.append({'word':crossing.word,'copies':copies})
    return clock,header.word,pieces


def event_in_sweep(seed,pair,work=10**7):
    """First physical arrival at the pair within this one sweep, or None."""
    data=digits(seed['register'])
    if not 0<=pair<=len(data) or work<1:
        raise ValueError('invalid data-pair index or work limit')
    tape=list(map(int,seed['register']+seed['terminal']))
    local=0
    for request,(state,reply,slot) in enumerate(probes(data[0][0])):
        x=0
        while x>=0:
            if x==2*pair:
                outside,header,pile=suspended_pile(seed['pile_pairs'],data[0][0],request)
                origin=seed['head']+7+2*seed['pile_pairs']
                return {'sweep':seed['epochs']+1,'register_slot':4*seed['epochs']+slot,
                        'slot_in_sweep':slot,'data_raw_probe':request+1,'steps':seed['steps']+outside+local,
                        'header_pile_steps':outside,'data_steps':local,'head':origin+x,'state':'AB'[state],
                        'tape_left':seed['head']+7-len(header),'header':header,'pile':pile,
                        'data_and_singleton':''.join(map(str,tape))}
            if x>=len(tape) or T17[state][tape[x]] is None:
                raise ValueError('exceptional data path before the requested visit')
            if local>=work:
                raise ValueError('single-sweep literal work budget')
            tape[x],move,state=T17[state][tape[x]]
            x+=move
            local+=1
        if state!=reply:
            raise ValueError('unexpected fixed-register reply')
    return None


def fresh_at(seed,pair):
    past=line17.deepest_probe(seed['register'])
    return past is None or past[0]<pair


def make_record(before,pair,event):
    payload={'format':'bb2x5-line17-first-visit-v1','line':17,'machine':M17,'pair':pair,
             'before':{'payload':before,'sha256':checksum(before)},'arrival':event}
    return {'payload':payload,'sha256':checksum(payload)}


def locate(seed,pair,through,engine,word_bits,finite_slots,work=10**7,miss_checkpoint=None):
    data=digits(seed['register'])
    width=len(data)
    if not 0<=pair<=width or through<seed['epochs'] or not fresh_at(seed,pair):
        raise ValueError('need a boundary at or before the search horizon and before the first visit')
    if not 16<=word_bits<=2**32 or not 0<=finite_slots<2**60 or work<1:
        raise ValueError('invalid work budget')
    epochs=through-seed['epochs']
    if not epochs:
        if miss_checkpoint is not None: line17.save(miss_checkpoint,seed)
        return None
    relative_slot=1
    if pair:
        mode='first' if miss_checkpoint is None else 'scan'
        proc=subprocess.run([str(Path(engine).resolve()),str(epochs),str(word_bits),str(finite_slots),mode],
                            input=seed['register'][:2*pair],text=True,capture_output=True)
        if proc.returncode: raise ValueError(proc.stderr.strip() or 'slot locator failed')
        rows=proc.stdout.splitlines()
        selected=rows.pop()
        if selected=='none':
            if miss_checkpoint is not None:
                counts=line17.native_counts(rows,4*epochs,pair)
                if counts[-1].slots:
                    raise ValueError('worker reported a miss after emitting a slot')
                # Every deeper pair had zero input and retains its starting phase.
                counts.extend(line17.Counts((data[i][0],data[i-1][1])) for i in range(pair,width))
                end=line17.record(epochs,counts,seed['register'],seed['steps'],seed['head'],seed['epochs'])
                if not fresh_at(end,pair): raise ValueError('miss changed the target trit')
                line17.save(miss_checkpoint,end)
            return None
        relative_slot=int(selected)
    if not 1<=relative_slot<=4*epochs:
        raise ValueError('first slot outside the finite search')
    whole=(relative_slot-1)//4
    before=line17.advance_packed(seed,whole,engine,word_bits,finite_slots) if whole else dict(seed)
    if not fresh_at(before,pair):
        raise ValueError('target was visited before the selected sweep')
    event=event_in_sweep(before,pair,work)
    if event is None or event['register_slot']!=4*seed['epochs']+relative_slot or event['state']!='B':
        raise ValueError('slot selection and physical first arrival disagree')
    return make_record(before,pair,event)


def verify(doc,work=10**7):
    p=doc['payload']
    if doc['sha256']!=checksum(p) or (p['format'],p['line'],p['machine'])!=('bb2x5-line17-first-visit-v1',17,M17):
        raise ValueError('invalid first-visit record')
    before=line17.validate(p['before'])
    if not fresh_at(before,p['pair']):
        raise ValueError('target already visited at starting boundary')
    event=event_in_sweep(before,p['pair'],work)
    if event is None or event['state']!='B' or make_record(before,p['pair'],event)!=doc:
        raise ValueError('physical first-visit replay differs')
    return event


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='command',required=True)
    find=sub.add_parser('find',help='locate the first visit to a pair after the large register was initialized')
    find.add_argument('--pair',required=True,type=int,help='zero-based fixed pair, or 424 for the singleton')
    find.add_argument('--through',required=True,type=int,help='inclusive absolute sweep horizon')
    find.add_argument('--resume',type=Path,help='an earlier ordinary-sweep boundary')
    find.add_argument('--packed-engine',type=Path,required=True)
    find.add_argument('--word-bits',type=int,default=2**28)
    find.add_argument('--finite-slots',type=int,default=10**11)
    find.add_argument('--literal-work',type=int,default=10**7)
    find.add_argument('--output',type=Path,required=True)
    find.add_argument('--miss-checkpoint',type=Path,help='save the complete ordinary endpoint if the target stays untouched')
    check=sub.add_parser('check',help='replay the arrival from its recorded pre-sweep boundary')
    check.add_argument('record',type=Path)
    check.add_argument('--literal-work',type=int,default=10**7)
    args=parser.parse_args()
    try:
        if not __debug__: raise ValueError('the register verifier requires assertions')
        if args.command=='check':
            doc=json.loads(args.record.read_text())
        else:
            seed=line17.load(args.resume) if args.resume else line17.replay(0,6)
            doc=locate(seed,args.pair,args.through,args.packed_engine,args.word_bits,args.finite_slots,
                       args.literal_work,args.miss_checkpoint)
            if doc is None:
                print(f'Pair {args.pair} received no input through sweep {args.through}.')
                return
        e=verify(doc,args.literal_work)
        if args.command=='find': atomic_json(args.output,doc)
        print(f"First visit to pair {doc['payload']['pair']} in sweep {e['sweep']}, "
              f"at raw step {e['steps']}, {e['state']} at coordinate {e['head']}.")
    except (ValueError,KeyError,IndexError,OSError,OverflowError) as exc:
        parser.exit(2,f'First-visit check stopped: {exc}\n')


if __name__=='__main__': main()
