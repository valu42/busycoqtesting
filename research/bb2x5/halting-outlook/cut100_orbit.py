"""Measure the line-34 signal at cut 100 on the exact blank computation."""
import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

from fence34 import allowance, cuts
from target34_orbit import analyze, TERNARY

HERE = Path(__file__).resolve().parent
START = 1300
SPLITS = (8000, 125000)
BUDGET = 250000


def record(stop, output):
    seed = json.loads((HERE / 'fence34-seed.json').read_text())
    old = json.loads((HERE / 'target34_checkpoint.json').read_text())
    assert seed['machine'] == old['machine'] == TERNARY == '1RB2LA4RA1LA3LA_0LA2RB3RB2LB---'
    assert seed['epoch'] == START and seed['state'] == old['state'] == 'A'
    config = (seed['width'], int(seed['open_hex'], 16), int(seed['closing_hex'], 16))
    steps, head = seed['raw_steps'], seed['head']
    xs = cuts()
    pulse_epochs = []
    first_positions = Counter()
    pulse_times = []
    phase_hist = [Counter(), Counter(), Counter()]
    snapshots = []
    previous = None
    first_breach = None
    signal = sha256()
    for epoch in range(START, stop):
        phase = epoch % 52
        result, guard, (inner, outer), _ = analyze(config, (xs[phase], 100))
        if result is None:
            raise RuntimeError(f'Physical guard reaches B4 in sweep starting at {epoch}, clock {steps}')
        if first_breach is None and (outer > 2 or
                (outer == 2 and previous is not None and epoch - previous < 42)):
            first_breach = (epoch, outer, previous)
        if first_breach is None:
            assert inner <= allowance(phase) and guard == (0 if phase % 13 == 0 else 2 if phase % 13 == 12 else 1)
        signal.update(outer.to_bytes(4, 'little'))
        block = (epoch >= SPLITS[0]) + (epoch >= SPLITS[1])
        phase_hist[block][phase, outer] += 1
        if outer >= 2:
            previous = epoch
            pulse_epochs.append(epoch)
            pulse_times.append(steps)
            width, opens, closes = config
            balance = 0
            for j in range(100, width):
                bit = 1 << (width - j - 1)
                balance += bool(closes & bit) - bool(opens & bit)
                if balance == 2:
                    first_positions[j + 1 - 100] += 1
                    break
        config, shift, ticks = result
        steps += ticks
        head -= shift
        if epoch + 1 == old['completed_sweeps']:
            assert (steps, head, config) == (old['steps'], old['head'],
                (old['width'], int(old['opens_hex'], 16), int(old['closes_hex'], 16)))
        if epoch + 1 in (*SPLITS, stop):
            snapshots.append({'epoch': epoch + 1, 'steps': steps, 'head': head, 'width': config[0]})
    gaps = Counter(b - a for a, b in zip(pulse_epochs, pulse_epochs[1:]))
    time_gaps = [b-a for a,b in zip(pulse_times, pulse_times[1:])]
    doc = {'machine': TERNARY, 'start_epoch': START, 'end_epoch': stop, 'raw_steps': steps,
           'state': 'A', 'head': head, 'width': config[0], 'opens_hex': hex(config[1]),
           'closes_hex': hex(config[2]), 'bit_zero': 'rightmost; remaining occupied digits are neutral',
           'snapshots': snapshots, 'histogram_splits': list(SPLITS),
           'outer_debt_by_phase': [[[p, d, n] for (p,d),n in sorted(part.items())] for part in phase_hist],
           'pulse_epochs': pulse_epochs, 'raw_intervals_between_pulses': (
               [min(time_gaps),max(time_gaps)] if time_gaps else []),
           'pulse_gap_histogram': dict(sorted(gaps.items())),
           'first_two_deficit_prefix_lengths': dict(sorted(first_positions.items())),
           'first_42_gap_contract_violation': first_breach,
           'signal_sha256_unsigned32_le': signal.hexdigest()}
    if output:
        output.write_text(json.dumps(doc, indent=2)+'\n')
    print('Boundaries:', snapshots)
    print('Pulse counts by segment:', [sum(n for (_, d),n in part.items() if d >= 2) for part in phase_hist])
    print('Pulse phases:', sorted({t % 52 for t in pulse_epochs}), 'gaps:', dict(sorted(gaps.items())))
    print('First prefix lengths reaching two:', dict(first_positions), 'raw intervals:', doc['raw_intervals_between_pulses'])
    print('First contract violation:', first_breach, 'signal SHA-256:', signal.hexdigest())
    return doc


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--through', type=int, default=BUDGET)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if not __debug__ or args.through <= START:
        parser.error('enable assertions and choose an endpoint after the seed')
    record(args.through, args.output)
