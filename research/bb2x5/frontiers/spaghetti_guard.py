#!/usr/bin/env python3
"""Count the BBA guard replies on the two reflected spaghetti orbits."""
import argparse
import base64
import json
from itertools import product
from pathlib import Path
import subprocess
import zlib

from checkpoints import atomic_json, checksum
from line19_pair import MACHINES, rule, translate_checkpoint
import survey

FORMAT = 'bb2x5-spaghetti-guards-v1'
DIGITS = (0, 2, 3)
CHANNELS = ('B3','A','B','AA','AB','AAA','AAB')


def first_exits(digit, exit_direction):
    """Possible last (state, digit) of a one-cell A entry, allowing both exterior replies."""
    todo = [('A',digit)]
    seen, ends = set(), set()
    while todo:
        state, symbol = todo.pop()
        if (state,symbol) in seen:
            continue
        seen.add((state,symbol))
        op = rule(MACHINES[19],state,symbol)
        if op == '---':
            continue
        if op[1] == exit_direction:
            ends.add(state+str(symbol))
        else:
            todo.extend((q,int(op[0])) for q in 'AB')
    return ends


def verify_antecedents():
    """Check the control cases that exclude 032 at an actual blank-orbit guard."""
    right_exits = {0:{'A0'},1:{'A1'},2:{'B3'},4:{'B2','B3'}}
    for d,expected in right_exits.items():
        if first_exits(d,'R') != expected:
            raise ValueError('guard predecessor has another possible right exit')
    left_exits = {0:{'A2','A4','B4'},2:{'A2'},3:set()}
    for d,expected in left_exits.items():
        if first_exits(d,'L') != expected:
            raise ValueError('suffix predecessor has another possible left exit')


def verify_short_third_calls():
    """Classify all A-entry B returns in at most seven actual steps."""
    for word in product(DIGITS,repeat=7):
        cells = list(word)
        head, q, elapsed = 0,'A',0
        while head>=0 and elapsed<7:
            op = rule(MACHINES[19],q,cells[head])
            if op=='---':
                break
            cells[head]=int(op[0])
            head+=1 if op[1]=='R' else -1
            q=op[2]
            elapsed+=1
        short_return = head==-1 and q=='B'
        if short_return!=(word[:3]==(0,2,0)) or (short_return and elapsed!=7):
            raise ValueError('short B-return classification failed')


def guard(row):
    cell, seed, digit, stage, *times = map(int, row.split())
    if seed == 0:
        return None
    if len(times) != 3 or not 0 <= stage <= 2 or digit not in DIGITS:
        raise ValueError('invalid guard trace')
    return {'cell': cell, 'entry': seed, 'suffix_digit': digit, 'returns': [t for t in times if t]}


def unpack(line, text, profile=False):
    rows = iter(text.splitlines())
    steps, head, q, direction, blocks, detailed = map(int, next(rows).split())
    if q not in (0, 1) or direction not in (-1, 1):
        raise ValueError('invalid result state')
    counts = {}
    for d in DIGITS:
        digit, seeds, *replies = map(int, next(rows).split())
        if d != digit or len(replies) != 6:
            raise ValueError('invalid reply counts')
        counts[str(d)] = dict(zip(CHANNELS, (seeds,*replies)))
    first, longest = guard(next(rows)), guard(next(rows))
    pending = [guard(next(rows)) for _ in range(int(next(rows)))]
    start = int(next(rows))
    padded = bytes(int(c) for c in next(rows))
    by_word, fresh_left = {}, {}
    for row in rows:
        word,*counters = row.split()
        if (not profile or len(word)!=4 or set(word)-set('023') or word in by_word
                or len(counters)!=len(CHANNELS)+1):
            raise ValueError('unexpected worker profile')
        by_word[word]=dict(zip(CHANNELS,map(int,counters[:-1])))
        fresh_left[word]=int(counters[-1])
    tape = padded.strip(b'\0')
    left = start + len(padded)-len(padded.lstrip(b'\0')) if tape else 0
    scanned = tape[head-left] if left <= head < left+len(tape) else 0
    state = 'AB'[q]
    status = 'halt' if rule(MACHINES[19],state,scanned) == '---' else 'unknown'
    normalized = {'format': survey.FORMAT, 'line': 19, 'machine': MACHINES[19],
                  'steps': steps, 'head': head, 'state': state, 'status': status,
                  'left': left, 'cells': len(tape),
                  'tape_zlib_base64': base64.b64encode(zlib.compress(tape,9)).decode()}
    return {'format': FORMAT, 'configuration': translate_checkpoint(normalized,line),
            'normalized_initial_state': 'A' if line == 19 else 'B',
            'tile_operations': blocks, 'detailed_tile_operations': detailed,
            'counts_by_suffix_digit': counts, 'first_third_return':first,
            'longest_third_call':longest, 'open_guards':pending,
            **({'counts_by_launch_word':by_word, 'fresh_left_launches_by_word':fresh_left} if profile else {})}


def validate(p, line):
    config = p['configuration']
    if (line not in MACHINES or p['format'] != FORMAT or config['line'] != line
            or p['normalized_initial_state'] != ('A' if line == 19 else 'B')):
        raise ValueError('wrong spaghetti orbit')
    survey.verify_state(config,MACHINES[line])
    end = config['steps']
    if not 0 <= p['detailed_tile_operations'] <= p['tile_operations'] <= end+1:
        raise ValueError('invalid operation counts')
    counts = p['counts_by_suffix_digit']
    if set(counts) != {str(n) for n in DIGITS}:
        raise ValueError('invalid digit breakdown')
    for g in [*p['open_guards'],p['first_third_return'],p['longest_third_call']]:
        if g is None:
            continue
        times = [g['entry'],*g['returns']]
        if (g['suffix_digit'] not in DIGITS or not 0 < times[0] < end
                or abs(g['cell']) > times[0] or (times[0]-g['cell']) % 2
                or any(b <= a or (b-a) % 2 or b >= end for a,b in zip(times,times[1:]))):
            raise ValueError('invalid guard location or clock')
    for d in DIGITS:
        c = counts[str(d)]
        if set(c) != {'B3','A','B','AA','AB','AAA','AAB'} or any(type(v) is not int or v<0 for v in c.values()):
            raise ValueError('invalid guard counters')
        for stage,(parent,a,b) in enumerate((('B3','A','B'),('A','AA','AB'),('AA','AAA','AAB'))):
            pending = sum(g['suffix_digit']==d and len(g['returns'])==stage for g in p['open_guards'])
            if c[parent] != c[a]+c[b]+pending:
                raise ValueError('inconsistent guard flow')
    if 'counts_by_launch_word' in p:
        profile = p['counts_by_launch_word']
        for word,c in profile.items():
            if (len(word)!=4 or set(word)-set('023') or set(c)!=set(CHANNELS)
                    or any(type(v) is not int or v<0 for v in c.values())):
                raise ValueError('invalid launch word counts')
        if 'fresh_left_launches_by_word' in p:
            fresh = p['fresh_left_launches_by_word']
            if set(fresh)!=set(profile) or any(type(v) is not int or not 0<=v<=profile[w]['B3']
                                                 for w,v in fresh.items()):
                raise ValueError('invalid fresh-left profile')
        for d in DIGITS:
            for channel in CHANNELS:
                total = sum(c[channel] for word,c in profile.items() if word[0]==str(d))
                if total!=counts[str(d)][channel]:
                    raise ValueError('launch word counts do not sum to digit counts')
    if counts['2']['B3']:
        raise ValueError('witness contradicts blank-orbit 032 exclusion')
    third = sum(c['AAA']+c['AAB'] for c in counts.values())
    for g in [p['first_third_return'],p['longest_third_call']]:
        if bool(third) != (g is not None) or (g and len(g['returns'])!=3):
            raise ValueError('missing or incomplete third return')
    return p


def load(path,line):
    document = json.loads(Path(path).read_text())
    p = document['payload']
    if checksum(p) != document['sha256']:
        raise ValueError('guard checkpoint checksum mismatch')
    return validate(p,line)


def replay(engine,line,target,profile=False):
    seed = 'A' if line == 19 else 'B'
    command = [str(Path(engine).resolve()),seed,str(target)]
    if profile:
        command.append('profile')
    result = subprocess.run(command, text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError(result.stderr.strip())
    return validate(unpack(line,result.stdout,profile),line)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--engine',required=True,type=Path)
    parser.add_argument('--line',type=int,choices=MACHINES,required=True)
    parser.add_argument('--target',type=int,required=True)
    parser.add_argument('--profile',action='store_true',help='also count each four-symbol launch prefix')
    parser.add_argument('--checkpoint',type=Path,required=True)
    args = parser.parse_args()
    verify_antecedents()
    verify_short_third_calls()
    p = replay(args.engine,args.line,args.target,args.profile)
    atomic_json(args.checkpoint,{'payload':p,'sha256':checksum(p)})
    print(json.dumps({'steps':p['configuration']['steps'],'counts_by_suffix_digit':p['counts_by_suffix_digit']}))


if __name__ == '__main__':
    main()
