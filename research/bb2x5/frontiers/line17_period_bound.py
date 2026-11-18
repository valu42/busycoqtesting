#!/usr/bin/env python3
"""Bound the first +12 visit using mark counts per period across the homogeneous band."""
import argparse
import json
from pathlib import Path
import subprocess

from line17_edge import DATA, ZERO, cut_limits, forced_output, initial, marks_on_word, source_slot

DEFAULT_ORBIT = 76489417298376469046624256
BAND_END = 403


def ceil_div(n, d):
    return -(-n // d)


def fifth_mark_target(counts_path):
    """Recover the fifth cut-168 mark and invert the stronger suffix prefix."""
    rows = [tuple(map(int, row.split())) for row in counts_path.read_text().splitlines()]
    n, inner = rows[167][2], rows[167][4]
    if n != 29 or inner//2-n != 5:
        raise ValueError('fifth-mark witness requires five marks in 29 cut-168 slots')
    hits = []
    for t in (27, 28, 29):
        prefix = bytes(int(i in (5,11,17,23,t)) for i in range(1,30))
        state, word = marks_on_word((1,0), prefix)
        if (state == rows[168][:2] and len(word) == rows[168][2] and
                sum(word) == rows[168][4]//2-len(word)):
            hits.append((t, prefix))
    if len(hits) != 1 or hits[0][0] != 29:
        raise ValueError('fifth-mark witness does not isolate slot 29')
    # Canonical trit-2 bursts preserve all five positions through cut 403.
    # Three-slot mark separation guarantees two zeros after the last mark.
    known = hits[0][1] + bytes(2)
    layers = []
    for i in range(BAND_END, 424):
        layers.append((initial(i), known))
        known = forced_output(initial(i), known)
    rank = 1
    for state, prefix in reversed(layers):
        rank = source_slot(state, prefix, ZERO, rank)
    return rank


def required_slots(base, period, mark_count, target, prefix_rows, aligned_bounds=False, five_marks=False):
    """Overapproximate the input rank needed at base, minimizing over usable depths."""
    width = BAND_END - base
    powers = [3**i for i in range(width + 1)]
    requirements = [target]*(width+1)
    for i in reversed(range(width)):
        offset = 61 if five_marks and base+i >= 168 else 49
        requirements[i] = 3*requirements[i+1] - offset

    # At depth i, H=2^b 3^(i-a-b) base periods lift to one period P.
    # Each entry lower-bounds its mark count and floor(3^i P/H).
    # Once the second lower bound reaches this cap it remains above it forever.
    cap = max(10**13, 2_000*period)
    states = {(0, 0, mark_count): period}
    best = requirements[0], 0
    seen_slots = prefix_rows[base-1][2]
    for depth in range(1, width + 1):
        new_states = {}
        observed = prefix_rows[base+depth-1] if base+depth <= len(prefix_rows) else (0,0,0,0,0)
        seen_marks = observed[4]//2 - observed[2]
        consumed = 0
        if aligned_bounds and base+depth <= len(prefix_rows):
            n = prefix_rows[base+depth-2][2]
            consumed, rem = divmod(3*observed[2]+observed[0]-n-1, 4)
            if rem or consumed < 0:
                raise ValueError('inconsistent compound-pulse count in homogeneous band')
        for (singles, doubles, marks), scaled in states.items():
            s, t = powers[singles + doubles], 2**doubles
            base_periods = powers[depth-1]*t//s
            # If even a minimal single lift has length >=23, it contains all
            # four guaranteed marks. Every period contains at least one mark.
            minimum = 4 if (scaled + 4*(marks+1)*s//t)*t >= 23*3*s else 1
            if five_marks and base+depth >= 168 and (scaled + 4*(marks+1)*s//t)*t >= 29*3*s:
                minimum = 5
            choices = (
                (1, singles+1, doubles, minimum, 4*(marks+minimum)*s//t),
                (2, singles, doubles+1, marks, 6*marks*s//t),
                (3, singles, doubles, 2*marks, 8*marks*s//t),
            )
            for h, a, b, count, gain in choices:
                length = scaled + gain
                input_periods = h*base_periods
                groups = max(1, ceil_div(seen_slots, period*input_periods))
                # A finite prefix from 'groups' aligned base superperiods
                # emits at most that many child periods by the slot identity.
                count = max(count, ceil_div(seen_marks, groups))
                if aligned_bounds:
                    # Each parent mark has at most h children over h copies.
                    # D counts every parent start and one or two extra pulses
                    # for each child mark. All observed pulses fit in groups D.
                    parents = max(marks, ceil_div(count, h))
                    compounds = max(h*parents + count, ceil_div(consumed, groups))
                    if h == 3:
                        compounds = max(compounds, 3*count)
                    length = max(length, scaled + 4*compounds*s//(h*t))
                length = max(length, ceil_div(observed[2], groups)*powers[depth]//input_periods)
                if length < cap:
                    key = a, b, count
                    new_states[key] = min(length, new_states.get(key, cap))
        states = new_states
        req = requirements[depth]
        scale = powers[depth]
        # The dropped states have H<=scale and scaled length >=cap.
        lost = (scale-1)//2 if aligned_bounds else depth*scale
        bound = ceil_div(req*scale, cap) + scale + lost
        for (a,b,_), scaled in states.items():
            input_periods = 2**b * powers[depth-a-b]
            lost = depth*input_periods
            if aligned_bounds:
                # The root-period overhead for one extra copy per digit is
                # sum(H_j, j<depth). Its maximum for these multiplicities
                # places all triples before the doubles and all singles last.
                triples = powers[depth-a-b]
                lost = (triples-1)//2 + triples*(2**b-1) + a*input_periods
            bound = max(bound, ceil_div(req*scale, scaled) + input_periods + lost)
        best = min(best, (period*bound, depth))
    return best


def run_worker(args, epochs, cut):
    if args.tiled:
        cmd = [str(args.tiled.resolve()), str(epochs), str(args.word_bits), str(args.threads)]
    else:
        cmd = [str(args.packed.resolve()), str(epochs), str(args.word_bits), str(args.finite_slots)]
    raw = subprocess.run(cmd, input=DATA[:2*cut], text=True, capture_output=True)
    if raw.returncode:
        raise ValueError(raw.stderr.strip() or 'native transfer failed')
    rows = [tuple(map(int, line.split())) for line in raw.stdout.splitlines()]
    if len(rows) != cut or any(len(row) != 5 for row in rows):
        raise ValueError('invalid native output')
    return rows


def read_trace(args):
    anchor = json.loads(args.anchor.read_text())
    base = anchor['base_cut']
    period, marks = anchor['period_slots'], anchor['period_marks']
    hroot = anchor['root_period_epochs']
    if anchor['base_slots_after_root_period'] != period:
        raise ValueError('trace anchor must place its first root period on a slot boundary')
    trace = [tuple(map(int,row.split())) for row in args.trace.read_text().splitlines()]
    rows = [tuple(map(int,row.split())) for row in args.counts.read_text().splitlines()]
    if not base <= args.cut <= len(trace) or len(rows)<args.cut:
        raise ValueError('requested cut is missing from trace')
    copies = 0
    for i in range(base-1,args.cut):
        cut, pre, p, k, tail, m = trace[i]
        if cut!=i+1 or pre or p<3 or k<1 or not 1<=m<=p or p*k+tail!=rows[i][2]:
            raise ValueError(f'invalid pure period trace at cut {cut}')
        if cut==base:
            if (p,m)!=(period,marks):
                raise ValueError('period trace disagrees with the independent anchor')
        else:
            # The tile worker has only six states. A positive input period
            # of at least three slots emits at least one slot, so an empty
            # output prefix implies begin=0 in its cycle construction.
            multipliers = []
            for h in range(1, 7):
                compounds, residue = divmod(3*p-h*period, 4)
                if (copies//h == k and not residue and
                        h*marks+m <= compounds <= h*marks+2*m):
                    multipliers.append(h)
            if len(multipliers)!=1:
                raise ValueError(f'ambiguous lift at cut {cut}; choose an earlier cut')
            hroot *= multipliers[0]
        copies, period, marks = k, p, m
    return hroot, rows, period, marks

def read_aligned(args):
    anchor = json.loads(args.anchor.read_text())
    base = anchor['base_cut']
    if not base <= args.cut < BAND_END:
        raise ValueError('choose a cut at or beyond the independently checked anchor')
    header, *lines = args.counts.read_text().splitlines()
    name, n = header.split()
    if name != 'epochs':
        raise ValueError('aligned counts must include their sweep horizon')
    horizon = int(n)
    rows = [tuple(map(int, row.split())) for row in lines]
    cycles = [tuple(map(int, row.split())) for row in args.aligned.read_text().splitlines()
              if row.strip() and not row.startswith('#')]
    if len(cycles) < args.cut or len(rows) < args.cut or any(len(row) != 5 for row in rows):
        raise ValueError('incomplete aligned counts or period table')
    for i in range(base-1, args.cut):
        cut, origin, hroot, prefix, period, marks = cycles[i]
        if cut != i+1 or prefix or not 0 <= origin < horizon or hroot < 1 or not 1 <= marks <= period:
            raise ValueError(f'invalid aligned cycle at cut {cut}')
        count, rem = divmod(horizon-origin, hroot)
        observed = rows[i]
        if (rem or observed[2] != count*period or
                observed[4] != 2*(observed[2] + count*marks)):
            raise ValueError(f'aligned run has different slot or mark totals at cut {cut}')
        if cut == base:
            if (hroot,period,marks) != (anchor['root_period_epochs'], anchor['period_slots'], anchor['period_marks']):
                raise ValueError('aligned cycle disagrees with independently checked anchor')
        else:
            h, rem = divmod(hroot, previous_h)
            compounds, r = divmod(3*period-h*previous_p, 4)
            if (rem or not 1 <= h <= 6 or origin != previous_origin or r or
                    not h*previous_m+marks <= compounds <= h*previous_m+2*marks):
                raise ValueError(f'inconsistent cycle lift at cut {cut}')
        previous_h, previous_p, previous_m, previous_origin = hroot, period, marks, origin
    return hroot, rows, period, marks, origin, horizon


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    engine = parser.add_mutually_exclusive_group(required=True)
    engine.add_argument('--packed', type=Path)
    engine.add_argument('--tiled', type=Path)
    engine.add_argument('--trace', type=Path)
    engine.add_argument('--aligned', type=Path)
    parser.add_argument('--counts', type=Path)
    parser.add_argument('--five-marks-from', type=Path)
    parser.add_argument('--anchor', type=Path)
    parser.add_argument('--cut', type=int, default=95)
    parser.add_argument('--period-epochs', type=int, default=DEFAULT_ORBIT)
    parser.add_argument('--word-bits', type=int, default=2**31)
    parser.add_argument('--finite-slots', type=int, default=2**35)
    parser.add_argument('--threads', type=int, default=2)
    args = parser.parse_args()
    if not 53 <= args.cut < BAND_END or args.period_epochs < 1:
        parser.error('require 53 <= cut < 403 and a positive root epoch period')
    h, base = args.period_epochs, args.cut
    origin = 0
    if args.aligned:
        if not args.counts or not args.anchor:
            parser.error('--aligned requires --anchor and --counts')
        h, first, p, m, origin, horizon = read_aligned(args)
        at_h = p
    elif args.trace:
        if not args.counts or not args.anchor:
            parser.error('--trace requires --anchor and --counts')
        h, first, p, m = read_trace(args)
        at_h = p
    else:
        first = run_worker(args, h, BAND_END)
        second = run_worker(args, 2*h, base)
        if any(a[:2] != b[:2] for a,b in zip(first, second)):
            raise ValueError('proposed period does not return the full prefix state at H and 2H')
        at_h = first[base-1][2]
        p = second[-1][2] - at_h
        interior = second[-1][4] - first[base-1][4]
        if p < 1 or interior % 2 or interior//2 <= p:
            raise ValueError('invalid period output or mark count')
        m = interior//2 - p
    five_marks = args.five_marks_from is not None
    target = fifth_mark_target(args.five_marks_from) if five_marks else cut_limits()[BAND_END]
    rank, depth = required_slots(base, p, m, target, first, aligned_bounds=bool(args.aligned),
                                 five_marks=five_marks)
    epochs = origin + h*(1 + max(0, ceil_div(rank-at_h, p)))
    steps = 2308941 + 14*epochs*(epochs-1) + (74+72*(2**424-1))*epochs
    result = dict(base_cut=base, root_period_epochs=h, base_slots_after_root_period=at_h, period_slots=p,
                          period_marks=m, cut_403_rank=target, bounded_cut=base+depth,
                          base_cut_rank_bound=rank, sweep_deadline=epochs,
                          first_plus12_raw_deadline=steps)
    if five_marks:
        result['fifth_mark_witness_cut'] = 168
    if args.aligned:
        result['root_sweep_origin'] = origin
        result['observed_sweeps'] = horizon
        result['slots_after_first_aligned_period'] = result.pop('base_slots_after_root_period')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
