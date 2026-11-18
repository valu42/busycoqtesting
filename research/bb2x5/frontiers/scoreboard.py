#!/usr/bin/env python3
"""Generate the 37-row table from the checked-in finite blank runs."""
import argparse
import json
import re
from decimal import Decimal

from checkpoints import ROOT, checksum, holdouts
from longitudinal import DRIVERS, Driver
import survey
import line7
import line5_timed

RUNS = ROOT / 'frontiers' / 'runs'
COMMUNITY = 'https://wiki.bbchallenge.org/wiki/BB%282%2C5%29#Unsolved'
OCTOBER = 'https://wiki.bbchallenge.org/wiki/TMBR:_October_2026#Holdouts'


def display(n):
    if n < 10**20:
        return f'{n:,}'
    mantissa, exponent = format(Decimal(n), '.5E').split('E')
    return f'≈ {mantissa} × 10^{int(exponent)}'


def generate():
    machines = holdouts()
    best = {}

    def consider(line, machine, steps, path, label):
        if not 1 <= line <= len(machines) or machines[line-1] != machine or steps < 0:
            raise ValueError(f'invalid result for line {line}')
        if line not in best or steps > best[line][0]:
            best[line] = steps, path, label

    for name in ('pilot', 'deep'):
        path = ROOT/'accelerator-results'/f'{name}.json'
        for record in json.loads(path.read_text())['records']:
            loc = path.with_name(record['checkpoint']) if 'checkpoint' in record else path
            consider(record['line'], record['machine'], int(record['steps'], 0), loc, 'Block simulator')
    for line, machine in enumerate(machines, 1):
        path = RUNS/f'window-{line:02}.json'
        p = survey.load(path, line, machine)
        consider(line, machine, p['steps'], path, 'Moving window')
    for line in DRIVERS:
        path = RUNS/f'stream-{line:02}.json'
        p = Driver(line).load(path)
        consider(line, p['machine'], p['steps'], path, 'Boundary streams')

    path = RUNS/'line7-calls.json'
    p = line7.load(path)
    consider(7, p['machine'], int(p['steps_hex'], 16), path, 'Batched suffix calls')

    from line4_orbit import blank_returns
    path = RUNS/'line4-return.json'
    doc = json.loads(path.read_text())
    p = doc['payload']
    b, steps = next(pair for k, pair in enumerate(blank_returns(p['returns']), 1) if k == p['returns'])
    if doc['sha256'] != checksum(p) or (int(p['b']), int(p['steps'])) != (b, steps):
        raise ValueError('line 4 return differs from its timed recurrence')
    consider(4, p['machine'], steps, path, 'Timed A(6,b) returns')

    path = RUNS/'line5-timed.json'
    timed = line5_timed.load(path)
    consider(5, timed['machine'], int(timed['steps_hex'],16), path, 'Timed A/B returns')

    mixed = (ROOT/'mixed-verification.txt').read_text()
    b3 = int(re.search(r'lower bound as an integer: (\d+)', mixed).group(1))
    a5 = json.loads((ROOT/'accelerator-results'/'arithmetic5-100k.json').read_text())['payload']
    if (a5['machine'] != machines[4] or a5['state']['tag'] != 'A'
            or (int(a5['rounds_hex'],16), a5['state']['a_hex'], a5['state']['b_hex'], a5['macro_events_hex'])
            != (timed['rounds'], timed['a_hex'], timed['b_hex'], timed['events_hex'])):
        raise ValueError('line 5 identity')
    exponent = int(a5['state']['b_hex'], 16).bit_length()-1
    bounds = {3: f'[≥ 10^{len(str(b3))-1}](mixed-verification.txt)',
              5: f'[≥ 2^{exponent:,}](accelerator-results/arithmetic5-100k.json)',
              17: '[> 10^36](marked-register.md)',
              37: '[≥ 39,999,600,001](line37-header.md)'}
    reports = {7: ('> 10^1,140,000,000', OCTOBER), 13: ('≈ 10^17.50888', COMMUNITY),
               14: ('≥ 5 × 10^13', COMMUNITY), 15: ('≥ 2 × 10^13', COMMUNITY),
               19: ('≥ 4 × 10^13', COMMUNITY)}
    lines = ['# BB(2,5) simulation table', '',
             'Each row starts on the all-zero, two-way-infinite tape. One raw step is one defined Turing-machine instruction. All 37 runs are still open.', '',
             'The endpoint column gives the largest exact raw count indexed in this repository. Follow its source for the full integer and configuration or run record. ≈ marks a shortened display. Bounds, externally reported simulations and exact repository counts have separate columns.', '',
             '| Line | Machine in the November 3 list | Raw steps at exact endpoint | Additional raw lower bound | Other reported raw steps | Endpoint source |',
             '|---:|---|---:|---:|---:|---|']
    for line, machine in enumerate(machines, 1):
        n, path, label = best[line]
        report = f'[{reports[line][0]}]({reports[line][1]})' if line in reports else '—'
        lines.append(f'| {line} | `{machine}` | {display(n)} | {bounds.get(line, "—")} | {report} | [{label}]({path.relative_to(ROOT)}) |')
    lines += ['', 'Line 3’s transcript gives its lower bound in full. Line 5’s timed replay reaches the same A(4,b) and recurrence count as the earlier checkpoint, which contains b consecutive nonzero cells. Each required a write, so its 173,754-bit b gives the displayed bound. The 8,684,421,216 recurrence events have a separate count. Line 17’s bound uses the distance travelled in its verified header epochs. On line 37 the successful sweeps from epochs 1 through 199,999 each traverse the old word, whose width starts at one and grows by at least two per sweep. Summing the minimum widths gives 199,999² raw steps.', '',
              'The community describes line 7 as expected to halt, line 13 as a possible halter, line 17 as likely to halt and line 26 as likely nonhalting. [Community holdout notes]('+COMMUNITY+') · [October research report]('+OCTOBER+')', '',
              'Run `python3 frontiers/scoreboard.py --check` from this directory to verify the table. [Simulation and continuation commands](frontiers/README.md)']
    return '\n'.join(lines)+'\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    table = ROOT/'SIMULATION_TABLE.md'
    content = generate()
    if args.check:
        if table.read_text() != content:
            parser.exit(1, 'Simulation table is out of date.\n')
        print('All 37 table rows match the run files.')
    else:
        table.write_text(content)


if __name__ == '__main__':
    main()
