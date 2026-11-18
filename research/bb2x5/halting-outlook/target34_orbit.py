"""Exact timed blank sweeps for line 34. Bit zero denotes the rightmost cell."""
import argparse
from collections import Counter
from itertools import product
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from prior_sweeps import TERNARY, TapeMachine, word_sweep


def encode(word):
    masks = []
    for color in (1, 3):
        bits = ''.join('1' if digit == color else '0' for digit in word)
        masks.append(int(bits or '0', 2))
    return len(word), masks[0], masks[1]


def read_header(debt):
    guard = (1, 2, 3)[debt % 3]
    raw = (guard,) if debt < 3 else (1, 3, 4, guard, 3)
    carry = carries = 0
    digits = []
    alphabet = (3, 1, 2)
    for cell in raw:
        base = 0 if cell == 4 else alphabet.index(cell) + 1
        carry, index = divmod(base + carry, 3)
        digits.append(alphabet[index])
        carries += carry
    return (*encode(digits), carry, carries)


HEADERS = [read_header(i) for i in range(6)]


def analyze(config, cuts):
    width, opens, closes = config
    mask = (1 << width) - 1
    guard = distance = layers = 0
    positions = [1 << (width - min(cut, width)) for cut in cuts]
    debts = [0] * len(cuts)
    while closes:
        occupied = ((closes + ~opens) ^ closes ^ ~opens)
        guard += (occupied >> width) & 1
        for i, bit in enumerate(positions):
            debts[i] += bool(occupied & bit)
        distance += ((occupied >> 1) & mask).bit_count()
        layers += 1
        closes &= occupied
        opens &= ~occupied
    if guard >= 6:
        return None, guard, debts, layers
    header, header_open, header_close, carry, header_carries = HEADERS[guard]
    # The old left neighbor and current survivor determine each data digit.
    preceding = (opens >> 1) | (carry << (width-1)) if width else 0
    emitted = int(bool(opens & 1)) if width else carry
    data_open = ~(opens ^ preceding) & mask
    data_close = opens & ~preceding
    successor = (width + header + emitted, ((header_open << width) | data_open) << emitted,
                 ((header_close << width) | data_close) << emitted)
    out_time = width + 2 + 2 * distance + (16 if guard >= 3 else 0) + 2 * max(0, guard - 3)
    back_time = width + header + 2 * (opens.bit_count() + header_carries + emitted)
    return (successor, header, out_time + back_time), guard, debts, layers


def sweep(config, cut=9):
    result, guard, debts, layers = analyze(config, (cut,))
    return result, guard, debts[0], layers


def audit():
    assert (HERE.parent / 'BB2x5_Rocq_holdouts_37.txt').read_text().splitlines()[33] == TERNARY
    tallies = Counter()
    for n in range(8):
        for word in product((1, 2, 3), repeat=n):
            result, guard, debt, _ = sweep(encode(word), n//2)
            target, low = word_sweep(word, TERNARY)
            bal = peak = 0
            for digit in word[n//2:]:
                bal += (digit == 3) - (digit == 1)
                peak = max(peak, bal)
            assert debt == peak and min(guard, 6) == -low
            machine = TapeMachine(TERNARY, word, left=1)
            if result is None:
                assert target is None
                for _ in range(1000):
                    if not machine.step():
                        break
                else:
                    raise AssertionError('halt did not occur within the test budget')
                assert (machine.state, machine.tape[machine.head]) == ('B', 4)
            else:
                next_word, header, ticks = result
                assert next_word == encode(target)
                for _ in range(ticks):
                    assert machine.step()
                assert machine.state == 'A' and machine.head == -header
                assert machine.tape == {1-header+i: c for i,c in enumerate(target)}
            tallies[guard] += 1
    machine = TapeMachine(TERNARY)
    config = (0,0,0)
    for _ in range(180):
        (config, header, ticks), _, _, _ = sweep(config)
        head = machine.head - header
        for _ in range(ticks):
            assert machine.step()
        assert (machine.state, machine.head) == ('A', head)
        width = config[0]
        assert len(machine.tape) == width
        assert config == encode([machine.tape[k] for k in range(head+1,head+1+width)])
    print('Raw-clock and complete-configuration checks:', dict(sorted(tallies.items())),
          'and 180 blank epochs to step', machine.steps, file=sys.stderr)


def record(epochs, path):
    config = (0, 0, 0)
    clock = head = 0
    phases = [set() for _ in range(13)]
    blocks = []
    summary = Counter()
    largest = (-1, None)
    deepest = (-1, None)
    cut_hits = Counter()
    cut12_hits = Counter()
    least_margin = None
    samples = []
    for epoch in range(epochs):
        result, guard, (debt, debt12), layers = analyze(config, (9,12))
        if result is None:
            raise RuntimeError(f'B4 detected in epoch {epoch} from a blank checkpoint at {clock} steps')
        if config[0] >= 9:
            cut_hits[debt] += 1
            if debt > largest[0]:
                largest = (debt, epoch)
        if config[0] >= 12:
            cut12_hits[debt12] += 1
            shift = config[0] - 12
            balance = (config[1] >> shift).bit_count() - (config[2] >> shift).bit_count()
            margin = 6 + balance - debt12
            assert balance >= 0 and margin > 0
            if least_margin is None or margin < least_margin[0]:
                least_margin = (margin, epoch)
        if layers > deepest[0]:
            deepest = (layers, epoch)
        if epoch >= 52:
            phases[epoch % 13].add(guard)
        summary[guard] += 1
        (config, header, ticks) = result
        clock += ticks
        head -= header
        if epoch + 1 in (52, 78, 1000, 10000, 50000, 100000, epochs):
            samples.append(dict(epoch=epoch+1, width=config[0], clock=clock, head=head,
                                sweep_cost=ticks, cut9_record=largest, depth_record=deepest))
        if (epoch+1) % 25000 == 0 or epoch+1 == epochs:
            blocks.append(dict(through_epoch=epoch+1, guard_histogram=dict(sorted(summary.items())),
                               cut9_histogram=dict(sorted(cut_hits.items())),
                               cut12_histogram=dict(sorted(cut12_hits.items())),
                               least_cut12_margin_and_first_epoch=least_margin))
    doc = dict(machine=TERNARY, start='blank', completed_sweeps=epochs, steps=clock,
               head=head, state='A', width=config[0], opens_hex=hex(config[1]),
               closes_hex=hex(config[2]), bit_zero='rightmost; other cells within width are neutral',
               histogram_blocks='cumulative; input epochs 0 through through_epoch-1; cut histograms exclude widths shorter than each cut',
               blocks=blocks, guard_by_epoch_mod_13_from_52=[sorted(s) for s in phases], samples=samples)
    if path is not None:
        path.write_text(json.dumps(doc, indent=2) + '\n')
    print(json.dumps({k:v for k,v in doc.items() if not k.endswith('_hex')}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--epochs', type=int, default=1000)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if not __debug__ or args.epochs < 1:
        parser.error('use assertions and a positive sweep budget')
    audit()
    record(args.epochs, args.output)
