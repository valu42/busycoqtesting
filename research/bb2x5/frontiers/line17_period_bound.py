#!/usr/bin/env python3
"""Bound the first +12 visit using mark counts per period across the homogeneous band."""
import argparse
import json
from pathlib import Path
import subprocess

from line17_edge import DATA, cut_limits

DEFAULT_ORBIT = 76489417298376469046624256
BAND_END = 403


def ceil_div(n, d):
    return -(-n // d)


def required_slots(base, period, mark_count, target, prefix_rows):
    """Overapproximate the input rank needed at base, minimizing over usable depths."""
    width = BAND_END - base
    powers = [3**i for i in range(width + 1)]
    # Repeatedly applying the inherited inverse bound R -> 3R-49.
    def required_after(depth):
        return ((2*target - 49)*powers[width - depth] + 49)//2

    # At depth i, H=2^b 3^(i-a-b) base periods lift to one period P.
    # Each entry lower-bounds its mark count and floor(3^i P/H).
    # Once the second lower bound reaches this cap it remains above it forever.
    cap = max(10**13, 2_000*period)
    states = {(0, 0, mark_count): period}
    best = required_after(0), 0
    seen_slots = prefix_rows[base-1][2]
    for depth in range(1, width + 1):
        new_states = {}
        observed = prefix_rows[base+depth-1] if base+depth <= len(prefix_rows) else (0,0,0,0,0)
        seen_marks = observed[4]//2 - observed[2]
        for (singles, doubles, marks), scaled in states.items():
            s, t = powers[singles + doubles], 2**doubles
            base_periods = powers[depth-1]*t//s
            # If even a minimal single lift has length >=23, it contains all
            # four guaranteed marks. Every period contains at least one mark.
            minimum = 4 if (scaled + 4*(marks+1)*s//t)*t >= 23*3*s else 1
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
                length = max(length, ceil_div(observed[2], groups)*powers[depth]//input_periods)
                if length < cap:
                    key = a, b, count
                    new_states[key] = min(length, new_states.get(key, cap))
        states = new_states
        req = required_after(depth)
        scale = powers[depth]
        # The dropped states have H<=scale and scaled length >=cap.
        bound = ceil_div(req*scale, cap) + (depth+1)*scale
        for (a,b,_), scaled in states.items():
            input_periods = 2**b * powers[depth-a-b]
            bound = max(bound, ceil_div(req*scale, scaled) + (depth+1)*input_periods)
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

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    engine = parser.add_mutually_exclusive_group(required=True)
    engine.add_argument('--packed', type=Path)
    engine.add_argument('--tiled', type=Path)
    engine.add_argument('--trace', type=Path)
    parser.add_argument('--counts', type=Path)
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
    if args.trace:
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
    target = cut_limits()[BAND_END]
    rank, depth = required_slots(base, p, m, target, first)
    epochs = h*(1 + max(0, ceil_div(rank-at_h, p)))
    steps = 2308941 + 14*epochs*(epochs-1) + (74+72*(2**424-1))*epochs
    print(json.dumps(dict(base_cut=base, root_period_epochs=h, base_slots_after_root_period=at_h, period_slots=p,
                          period_marks=m, cut_403_rank=target, bounded_cut=base+depth,
                          base_cut_rank_bound=rank, sweep_deadline=epochs,
                          first_plus12_raw_deadline=steps), indent=2))


if __name__ == '__main__':
    main()
