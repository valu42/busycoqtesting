#!/usr/bin/env python3
"""Advance a checked-in holdout to an exact raw step or a bounded work stop."""
import argparse
import base64
import itertools
import json
from pathlib import Path
import subprocess
import zlib

from checkpoints import atomic_json, checksum, holdouts

FORMAT='bb2x5-window-v1'


def pack(line, machine, result):
    lines=iter(result.splitlines())
    status,work=next(lines).split()
    if next(lines)!=machine or status not in ('unknown','halt'):
        raise ValueError('wrong native result header')
    steps,head,state=map(int,next(lines).split())
    if steps<0 or abs(head)>steps or (steps-head)%2 or state not in (0,1):
        raise ValueError('invalid native state')
    cells=bytearray(); left=0
    for row in lines:
        x,n,s=map(int,row.split())
        if n<=0 or not 1<=s<=4 or x < -steps or x+n-1>steps:
            raise ValueError('invalid native tape run')
        if not cells: left=x
        if x<left+len(cells): raise ValueError('overlapping tape runs')
        cells.extend(bytes(x-left-len(cells)))
        cells.extend(bytes([s])*n)
    payload={'format':FORMAT,'line':line,'machine':machine,'steps':steps,'head':head,
             'state':'AB'[state],'status':status,'left':left,'cells':len(cells),
             'tape_zlib_base64':base64.b64encode(zlib.compress(cells,9)).decode()}
    verify_state(payload,machine)
    return payload,int(work)


def verify_state(p,machine):
    if p['format']!=FORMAT or p['machine']!=machine or p['state'] not in ('A','B'):
        raise ValueError('checkpoint machine/format mismatch')
    cells=zlib.decompress(base64.b64decode(p['tape_zlib_base64'],validate=True))
    steps,head,left=p['steps'],p['head'],p['left']
    if (len(cells)!=p['cells'] or (cells and (max(cells)>4 or not cells[0] or not cells[-1]))
            or (not cells and left!=0) or steps<0 or abs(head)>steps or (steps-head)%2
            or left< -steps or left+len(cells)-1>steps):
        raise ValueError('invalid tape or coordinates')
    symbol=cells[head-left] if 0<=head-left<len(cells) else 0
    row=machine.split('_')['AB'.index(p['state'])]
    halt=row[3*symbol:3*symbol+3]=='---'
    if p['status']!=('halt' if halt else 'unknown'):
        raise ValueError('status disagrees with scanned instruction')
    return cells


def load(path,line,machine):
    doc=json.loads(Path(path).read_text());p=doc['payload']
    if doc['sha256']!=checksum(p) or p['line']!=line:
        raise ValueError('checkpoint identity or checksum mismatch')
    verify_state(p,machine)
    return p


def native_input(machine,p):
    if p is None: return f'{machine}\n0 0 0\n'
    cells=verify_state(p,machine)
    x=p['left'];rows=[machine,f"{p['steps']} {p['head']} {'AB'.index(p['state'])}"]
    for symbol,group in itertools.groupby(cells):
        n=sum(1 for _ in group)
        if symbol: rows.append(f'{x} {n} {symbol}')
        x+=n
    return '\n'.join(rows)+'\n'


def advance(engine,line,machine,p,target,work,width):
    cp=subprocess.run([str(Path(engine).resolve()),str(width),str(target),str(work)],
                      input=native_input(machine,p),capture_output=True,text=True)
    if cp.returncode: raise RuntimeError(cp.stderr.strip() or 'native worker failed')
    return pack(line,machine,cp.stdout)


def save(path,p):
    atomic_json(path,{'payload':p,'sha256':checksum(p)})


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--engine',type=Path,required=True)
    parser.add_argument('--line',type=int,choices=range(1,38),required=True)
    parser.add_argument('--target',type=int,required=True,help='absolute raw step target, up to 2^60')
    parser.add_argument('--work',type=int,default=10**9,help='maximum number of window or single-step operations')
    parser.add_argument('--width',type=int,default=8,choices=range(2,11))
    parser.add_argument('--resume',type=Path)
    parser.add_argument('--checkpoint',type=Path,required=True)
    args=parser.parse_args();machine=holdouts()[args.line-1]
    try:
        p=load(args.resume,args.line,machine) if args.resume else None
        state,used=advance(args.engine,args.line,machine,p,args.target,args.work,args.width)
        save(args.checkpoint,state)
        print(json.dumps({'line':args.line,'status':state['status'],'steps':state['steps'],'work':used}))
    except (ValueError,OSError,RuntimeError,KeyError,zlib.error) as error:
        parser.exit(2,f'Window simulation stopped: {error}\n')


if __name__=='__main__':
    main()
