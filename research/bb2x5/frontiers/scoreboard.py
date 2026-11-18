#!/usr/bin/env python3
"""Generate the 37-row table from the checked-in finite blank runs."""
import argparse
import json
from pathlib import Path
import re

from checkpoints import ROOT, checksum, holdouts
import survey


def display(n):
    digits=str(n)
    if len(digits)<=20: return f'{n:,}'
    # Every displayed power is explicitly approximate. The link retains the exact integer.
    return f'≈ {digits[0]}.{digits[1:6]} × 10^{len(digits)-1}'


def generate():
    machines=holdouts(); best={}; bounds={}
    def consider(i,m,steps,path,label):
        if not 1<=i<=len(machines) or machines[i-1]!=m or steps<0:
            raise ValueError(f'invalid result for line {i}')
        if i not in best or steps>best[i][0]: best[i]=(steps,path,label)
    for name in ('pilot','deep'):
        path=ROOT/'accelerator-results'/f'{name}.json'
        for r in json.loads(path.read_text())['records']:
            loc=path.with_name(r['checkpoint']) if 'checkpoint' in r else path
            consider(r['line'],r['machine'],int(r['steps'],0),loc,'Block simulator')
    for i,m in enumerate(machines,1):
        path=ROOT/'frontiers'/'runs'/f'window-{i:02}.json'; p=survey.load(path,i,m)
        consider(i,m,p['steps'],path,'Moving window')
    # Later runs can supply a larger exact endpoint without changing older files.
    for path in sorted((ROOT/'frontiers'/'runs').glob('stream-*.json')):
        doc=json.loads(path.read_text());p=doc['payload']
        if doc['sha256']!=checksum(p) or p['format']!='bb2x5-longitudinal-v1':
            raise ValueError(f'invalid stream result {path}')
        consider(p['line'],p['machine'],p['steps'],path,'Boundary streams')
    mixed=(ROOT/'mixed-verification.txt').read_text()
    b3=int(re.search(r'lower bound as an integer: (\d+)',mixed).group(1))
    bounds[3]=f'[≥ 10^{len(str(b3))-1}](mixed-verification.txt)'
    a5=json.loads((ROOT/'accelerator-results'/'arithmetic5-100k.json').read_text())['payload']
    if a5['machine']!=machines[4] or a5['state']['tag']!='A': raise ValueError('line 5 identity')
    bits=int(a5['state']['b_hex'],16).bit_length()-1
    bounds[5]=f'[≥ 2^{bits:,}](accelerator-results/arithmetic5-100k.json)'
    bounds[17]='[> 10^36](marked-register.md)'
    lines=['# BB(2,5) simulation table','',
           'Each row follows one machine from the all-zero, two-way-infinite tape. The step counter advances once per defined instruction. The linked result contains the complete checkpoint or its run record. All 37 blank-tape outcomes remain open in these runs.','',
           'The exact endpoint column gives the largest counted run in the sources indexed here. Values marked ≈ abbreviate the exact integer in the linked file. The lower-bound column also credits longer runs where only a minimum raw duration is known.','',
           '| Line | Machine in the November 3 list | Raw steps at exact endpoint | Additional raw lower bound | Endpoint source |',
           '|---:|---|---:|---:|---|']
    for i,m in enumerate(machines,1):
        n,path,label=best[i]; lines.append(f'| {i} | `{m}` | {display(n)} | {bounds.get(i,"—")} | [{label}]({path.relative_to(ROOT)}) |')
    lines+=['','Line 5’s A(4,b) checkpoint contains b consecutive nonzero cells. Starting on blank takes at least one write per such cell, so its 173,754-bit b gives the displayed raw lower bound. Its 8,684,421,216 recurrence events have a separate count. Line 3’s exact lower-bound integer is in its transcript. Line 17’s bound follows from its verified count of header epochs and the distance travelled in each.','',
            'The table tracks this repository. For comparison, Andrew Ducharme reported about 10^17.50888 raw steps for line 13, and LegionMammal978 reported more than 10^1,140,000,000 on line 7. The community lists line 17 as likely to halt, line 13 as a possible halter, and line 26 as likely nonhalting. [Community holdout notes](https://wiki.bbchallenge.org/wiki/BB%282%2C5%29#Unsolved) · [October research report](https://wiki.bbchallenge.org/wiki/TMBR:_October_2026#Holdouts)','',
            'Run `python3 frontiers/scoreboard.py --check` from this directory to check the table against the saved files. [Simulation and continuation commands](frontiers/README.md)']
    return '\n'.join(lines)+'\n'


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',action='store_true');args=p.parse_args()
    table=ROOT/'SIMULATION_TABLE.md'; content=generate()
    if args.check:
        if table.read_text()!=content: p.exit(1,'Simulation table is out of date.\n')
        print('All 37 table rows match the run files.')
    else: table.write_text(content)


if __name__=='__main__': main()
