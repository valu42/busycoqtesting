#!/usr/bin/env python3
"""Search for a two-sided finite-automaton TM invariant using Z3.

Both side automata read the tape from blank infinity toward the head. State
zero loops on zero. An abstract configuration is (left DFA state, TM state,
scanned bit, right DFA state). Constraints require the blank start, exclude
halts, and close under every possible inverse image when popping a side.
The transition tables themselves are synthesized, rather than selected from
a predefined family. Breadth-first label bounds break naming symmetries.

UNVERIFIED research: SAT is a candidate, even after the independent Python
least-fixed-point check. Replay a positive certificate in Coq before claiming
nonhalting. UNSAT concerns only this finite template and these state counts;
a timeout is UNKNOWN. No result here is a machine classification.

Dependency: z3-solver (tested with 5.3.1.0). AI-assisted research by Codex.
"""
import argparse
from collections import deque
import json
import math
from pathlib import Path
import time

import z3


def parse(machine):
    flat = machine.strip().replace('_', '')
    if len(flat) != 36:
        raise ValueError('expected six binary states')
    result = []
    for i in range(0, 36, 3):
        item = flat[i:i+3]
        if item == '---':
            result.append(None)
        elif item[0] in '01' and item[1] in 'LR' and item[2] in 'ABCDEF':
            result.append((int(item[0]), item[1], ord(item[2])-65))
        else:
            raise ValueError('invalid transition: ' + item)
    return result


def check_closure(table, ld, rd):
    """Independent of the solver's Boolean invariant; compute its least closure."""
    for dfa in (ld, rd):
        assert dfa and dfa[0][0] == 0
        assert all(len(row) == 2 and all(type(x) is int and 0 <= x < len(dfa)
                                        for x in row) for row in dfa)
    seen = {(0, 0, 0, 0)}
    queue = deque(seen)
    while queue:
        l, q, bit, r = queue.popleft()
        op = table[2*q+bit]
        if op is None:
            raise ValueError('candidate closure contains a halting configuration')
        write, direction, state = op
        for scanned in (0, 1):
            if direction == 'L':
                successors = ((l1, state, scanned, rd[r][write])
                              for l1 in range(len(ld)) if ld[l1][scanned] == l)
            else:
                successors = ((ld[l][write], state, scanned, r1)
                              for r1 in range(len(rd)) if rd[r1][scanned] == r)
            for nxt in successors:
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append(nxt)
    return len(seen)


def synthesize(machine, nl=4, nr=4, seconds=30):
    table = parse(machine)
    for n in (nl, nr):
        if n < 2 or n & (n-1):
            raise ValueError('DFA sizes must be powers of two, at least two')
    bl, br = nl.bit_length()-1, nr.bit_length()-1
    left_sort, right_sort = z3.BitVecSort(bl), z3.BitVecSort(br)
    li = lambda i: z3.BitVecVal(i, bl)
    ri = lambda i: z3.BitVecVal(i, br)
    solver = z3.Solver()
    solver.set(timeout=max(1, int(seconds*1000)))
    ld = [z3.Array('left'+str(b), left_sort, left_sort) for b in (0, 1)]
    rd = [z3.Array('right'+str(b), right_sort, right_sort) for b in (0, 1)]
    allowed = [[z3.Array('ok'+str(q)+str(b), z3.BitVecSort(bl+br), z3.BoolSort())
                for b in (0, 1)] for q in range(6)]

    def ok(q, bit, l, r):
        return z3.Select(allowed[q][bit], z3.Concat(l, r))

    for tabs, n, cast in ((ld, nl, li), (rd, nr, ri)):
        solver.add(z3.Select(tabs[0], cast(0)) == cast(0))
        for i in range(n):
            for bit in (0, 1):
                solver.add(z3.ULE(z3.Select(tabs[bit], cast(i)),
                                  cast(min(n-1, 2*i+bit))))
    solver.add(ok(0, 0, li(0), ri(0)))
    for q in range(6):
        for bit in (0, 1):
            op = table[2*q+bit]
            for l in range(nl):
                for r in range(nr):
                    if op is None:
                        solver.add(z3.Not(ok(q, bit, li(l), ri(r))))
                        continue
                    write, direction, state = op
                    for scanned in (0, 1):
                        if direction == 'L':
                            src = ok(q, bit, z3.Select(ld[scanned], li(l)), ri(r))
                            dst = ok(state, scanned, li(l), z3.Select(rd[write], ri(r)))
                        else:
                            src = ok(q, bit, li(l), z3.Select(rd[scanned], ri(r)))
                            dst = ok(state, scanned, z3.Select(ld[write], li(l)), ri(r))
                        solver.add(z3.Implies(src, dst))
    start = time.monotonic()
    result = solver.check()
    out = {'machine': machine, 'left': nl, 'right': nr, 'result': str(result),
           'solver_seconds': round(time.monotonic()-start, 3),
           'z3_version': z3.get_version_string()}
    if result == z3.sat:
        model = solver.model()
        out['ldfa'] = [[model.eval(z3.Select(ld[b], li(i)), model_completion=True).as_long()
                        for b in (0, 1)] for i in range(nl)]
        out['rdfa'] = [[model.eval(z3.Select(rd[b], ri(i)), model_completion=True).as_long()
                        for b in (0, 1)] for i in range(nr)]
        out['closure_states'] = check_closure(table, out['ldfa'], out['rdfa'])
        out['status'] = 'candidate requiring Coq replay'
    elif result == z3.unknown:
        out['reason'] = solver.reason_unknown()
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group()
    source.add_argument('--machine')
    source.add_argument('--input', type=Path)
    parser.add_argument('--index', type=int, default=1)
    parser.add_argument('--left', type=int, default=4)
    parser.add_argument('--right', type=int, default=4)
    parser.add_argument('--seconds', type=float, default=30)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--selftest', action='store_true')
    args = parser.parse_args()
    if not math.isfinite(args.seconds) or args.seconds <= 0:
        parser.error('--seconds must be finite and positive')
    for n in (args.left, args.right):
        if n < 2 or n & (n-1):
            parser.error('DFA sizes must be powers of two, at least two')
    if args.selftest:
        controls = [('1RA1RA_------_------_------_------_------', 'sat'),
                    ('1RB1RB_1LA1LA_------_------_------_------', 'sat'),
                    ('------_------_------_------_------_------', 'unsat'),
                    ('1RB1RB_------_------_------_------_------', 'unsat')]
        for machine, expected in controls:
            assert synthesize(machine, 4, 4, 5)['result'] == expected
        # The independent checker must reject a spurious certificate too.
        try:
            check_closure(parse(controls[2][0]), [[0, 0]], [[0, 0]])
        except ValueError:
            pass
        else:
            raise AssertionError('invalid certificate accepted')
        out = {'status': 'selftest passed', 'controls': len(controls)}
    else:
        if args.input:
            tables = [s.strip() for s in args.input.read_text().splitlines() if s.strip()]
            if not 1 <= args.index <= len(tables):
                parser.error('--index is outside the input list')
            machine = tables[args.index-1]
        elif args.machine:
            machine = args.machine
        else:
            parser.error('provide --machine, --input, or --selftest')
        try:
            out = synthesize(machine, args.left, args.right, args.seconds)
        except ValueError as e:
            parser.error(str(e))
        if args.input:
            out['index'] = args.index
    text = json.dumps(out) + '\n'
    if args.output:
        args.output.write_text(text)
    print(text, end='')


if __name__ == '__main__':
    main()
