"""Exact finite certificates for the line 34 boundary at cell 100. Python 3.10+."""
import argparse
from collections import Counter, deque
from functools import cache
import json
import subprocess
from pathlib import Path

from fence34 import BOUNDARY, allowance, cuts
from line34_left import digits
from target34_orbit import TERNARY, TapeMachine, analyze, encode
from prior_sweeps import direct_epoch, word_sweep

HERE = Path(__file__).resolve().parent
CUT = 100
WIDTHS = cuts()
SEED = json.loads((HERE / 'fence34-seed.json').read_text())
assert SEED['machine'] == TERNARY == '1RB2LA4RA1LA3LA_0LA2RB3RB2LB---'


def first_digits(count):
    shift = SEED['width'] - count
    return digits((int(SEED['open_hex'], 16) >> shift,
                   int(SEED['closing_hex'], 16) >> shift), count)


def pack(word):
    """Encode ordinary digits by adjacent binary pairs, using zero for an all-opening word."""
    word = tuple(word)
    previous = next((int(v == 2) for v in word if v != 1), 0)
    bits = previous
    for v in word:
        if v == 3:
            assert previous == 0
            previous = 1
        elif v == 2:
            assert previous == 1
            previous = 0
        bits = 2 * bits + previous
    return bits


def unpack(code, width):
    opens = ~(code ^ (code >> 1))
    closes = code & ~(code >> 1)
    return digits((opens, closes), width)


class Collar:
    """Retain ordinary cells from the periodic cut through the fixed outer boundary."""

    def __init__(self, extra, local_only=False):
        self.extra = extra
        self.local_only = local_only
        self.end = CUT + extra
        self.start = (0, pack(first_digits(self.end)[WIDTHS[0]:]))

    @cache
    def edges(self, state):
        phase, code = state
        width = self.end - WIDTHS[phase]
        u = allowance(phase)
        mask = (1 << width) - 1
        opens = ~(code ^ (code >> 1)) & mask
        closes = code & ~(code >> 1) & mask
        # In the three-cell calculation, cut 100 lies at the start of this suffix.
        extra_mask = (1 << self.extra) - 1
        tail_balance = (opens & extra_mask).bit_count() - (closes & extra_mask).bit_count()
        motif = self.extra == 3 and opens & 7 == 0 and closes & 7 == 5
        cap = 1 if self.local_only and not motif else 2
        intrinsic = tail_debt = 0
        while closes:
            slots = (closes + ~opens) ^ closes ^ ~opens
            intrinsic += (slots >> width) & 1
            tail_debt += (slots >> self.extra) & 1
            closes &= slots
            opens &= ~slots

        result = []
        # If the exterior sends z, the three-cell split gives
        # d100 = max(h(tail), z - balance(tail)).
        for exterior in range(tail_balance + cap + 1):
            d100 = max(tail_debt, exterior - tail_balance)
            if d100 > cap:
                break
            successor = None
            if intrinsic <= u:
                supplied = ((1 << (u - intrinsic)) - 1) << (width + intrinsic)
                new = ((int(BOUNDARY[phase]) << (width + u)) | supplied | opens) >> 1
                if new == (1 << (width + u)) - 1:
                    new = 0
                successor = ((phase + 1) % 52, new)
            result.append((d100, successor))
            if opens:
                opens &= opens - 1
            else:
                intrinsic += 1
        return tuple(result)


def gap_graph(collar, gap, witness=False, exempt_local=False):
    """For each word and phase, the largest attainable cooldown age includes smaller ages."""
    wait = gap - 1
    ages = {collar.start: wait}
    pending = deque([collar.start])
    if witness:
        traces = [(-1, -1)]
        trace_for = {collar.start: 0}
    while pending:
        state = pending.popleft()
        age = ages[state]
        if witness:
            trace = trace_for[state]
        for d, successor in collar.edges(state):
            local = exempt_local and (state[1] & 15) == 5
            if d == 2 and age < wait and not local:
                continue
            if successor is None:
                if not witness:
                    raise AssertionError('unprotected transition')
                word = [d]
                while trace:
                    trace, digit = traces[trace]
                    word.append(digit)
                return tuple(reversed(word))
            new_age = 0 if d == 2 else min(wait, age + 1)
            if new_age > ages.get(successor, -1):
                ages[successor] = new_age
                pending.append(successor)
                if witness:
                    trace_for[successor] = len(traces)
                    traces.append((trace, d))
    assert not witness
    return ages


def spatial_graph(collar):
    seen = {collar.start}
    queue = deque([collar.start])
    while queue:
        for _, successor in collar.edges(queue.popleft()):
            assert successor is not None
            if successor not in seen:
                seen.add(successor)
                queue.append(successor)
    return seen


def literal_case(phase, prefix, middle, z, predicted, extra):
    """Realize one input as a finite tape ending in z closings. Check the complete sweep."""
    raw = (*prefix, *middle, *(3,) * z)
    tm = TapeMachine(TERNARY, raw, left=1)
    actual = direct_epoch(tm, (1, 2, 3))
    timed, guard, _, _ = analyze(encode(raw), ())
    assert (timed is None) == (actual is None)
    if actual is not None:
        new, shift, ticks = timed
        assert tm.state == 'A' and (tm.head, tm.steps) == (-shift, ticks)
        assert tm.tape == {tm.head + 1 + j: v for j, v in enumerate(actual)}
        assert new == encode(actual)
    else:
        assert tm.state == 'B' and tm.tape[tm.head] == 4
    target_guard = 0 if phase % 13 == 0 else 2 if phase % 13 == 12 else 1
    target, _ = word_sweep(prefix, TERNARY)
    x = WIDTHS[phase + 1]
    keep = actual is not None and guard == target_guard and tuple(actual[:x]) == tuple(target[:x])
    assert keep == (predicted is not None)
    if keep:
        assert tuple(actual[x:CUT+extra]) == unpack(predicted[1], CUT + extra - x)


def crosscheck(collar, states, ages=None, gap=42, exempt_local=False):
    """Use a scalar right-to-left stack on every graph edge, including final certificate closure."""
    references = [first_digits(WIDTHS[0])]
    for phase in range(51):
        out, _ = word_sweep(references[-1], TERNARY)
        references.append(tuple(out[:WIDTHS[phase + 1]]))
    literal = Counter()
    edge_count = 0
    for state in sorted(states):
        phase, code = state
        width = collar.end - WIDTHS[phase]
        u = allowance(phase)
        middle = unpack(code, width)
        tail = middle[CUT-WIDTHS[phase]:]
        cap = 1 if collar.local_only and tail != (3,2,3) else 2
        entries = collar.edges(state)
        accepted = 0
        for z in range(len(tail) + cap + 1):
            debt = z
            bits_right_first = []
            for j, cell in enumerate(reversed(middle)):
                if j == len(tail):
                    d100 = debt
                bits_right_first.append(int(cell == 1 and debt == 0))
                debt = max(0, debt + (cell == 3) - (cell == 1))
            if d100 > cap:
                break
            d, successor = entries[z]
            accepted += 1
            assert d == d100
            if debt <= u:
                bits = [int(BOUNDARY[phase]), *([1] * (u - debt)), *([0] * debt), *reversed(bits_right_first)]
                word = tuple(1 if a == b else 3 if b else 2 for a,b in zip(bits,bits[1:]))
                assert successor == ((phase + 1) % 52, pack(word[:-1]))
            else:
                assert successor is None
            if ages is not None:
                age = ages[state]
                if d == 2 and age < gap-1 and not (exempt_local and tail == (3,2,3)):
                    continue
                assert successor in ages and ages[successor] >= (0 if d == 2 else min(gap-1, age + 1))
            else:
                assert successor in states
            edge_count += 1
            if not literal[phase, z]:
                literal_case(phase, references[phase], middle, z, successor, collar.extra)
                literal[phase, z] += 1
        assert accepted == len(entries)
    return edge_count, sum(literal.values())


def replay_abstract_witness(word, collar):
    """Reconstruct each old prefix directly, then check its forced canonical completion literally."""
    p = 0
    prefix = first_digits(WIDTHS[p])
    middle = first_digits(CUT)[WIDTHS[p]:]
    state = collar.start
    for t, d in enumerate(word):
        assert d < 3 and state == (p, pack(middle))
        _, successor = collar.edges(state)[d]
        literal_case(p, prefix, middle, d, successor, 0)
        whole, _ = word_sweep((*prefix, *middle, *(3,)*d), TERNARY)
        if t + 1 == len(word):
            assert successor is None
            break
        assert successor is not None
        state = successor
        p = (p+1) % 52
        prefix, middle = tuple(whole[:WIDTHS[p]]), tuple(whole[WIDTHS[p]:CUT])
    return p


def main(fast=False):
    short = Collar(0)
    ages = gap_graph(short, 42)
    assert len(ages) == 62992
    print(f'42-sweep gap sufficient: {len(ages)} reachable (phase, word) pairs.')
    witness = gap_graph(short, 41, witness=True)
    peaks = [i for i, value in enumerate(witness) if value == 2]
    assert min(b-a for a,b in zip(peaks,peaks[1:])) == 41
    phase = replay_abstract_witness(witness, short)
    print(f'41-sweep input fails the prefix test at update {len(witness)}, phase {phase}; double-input offsets {peaks}.')
    print('Abstract input (offset zero is epoch 1300):', ''.join(map(str,witness)))
    # The chosen 41-gap oracle word is already impossible for one extra physical cell.
    actual = first_digits(CUT + 1)
    for t, d in enumerate(witness):
        q = actual[CUT]
        if q == 3 and d == 0:
            break
        z = d-1 if q == 3 else d if q == 2 else d+1 if d else 0
        updated, _ = word_sweep((*actual, *(3,)*z), TERNARY)
        actual = tuple(updated[:CUT+1])
    assert (t, q, d) == (24, 3, 0)
    print('Oracle witness rejected by physical digit 101 at offset 24: C requires at least one debt.')
    if not fast:
        print('Allowed gap edges and literal canonical sweeps:', crosscheck(short, ages, ages))
    literal = Collar(3, local_only=True)
    states = spatial_graph(literal)
    assert len(states) == 148081
    print(f'Three-cell local criterion sufficient: {len(states)} reachable (phase, word) pairs.')
    if not fast:
        print('Allowed three-cell edges and literal canonical sweeps:', crosscheck(literal, states))
    # With the next three physical digits present, 323 can certify a double immediately.
    # All other doubles require a gap from the last double, including the last local one.
    hybrid = Collar(3)
    combined = gap_graph(hybrid, 89, exempt_local=True)
    assert len(combined) == 258932
    print('Local doubles unrestricted; other doubles after at least 89 sweeps:', len(combined), 'pairs.')
    if not fast:
        print('Allowed combined edges and literal canonical sweeps:',
              crosscheck(hybrid, combined, combined, 89, True))


def wide(executable):
    allowances = ''.join(str(allowance(p)) for p in range(52))
    for k in (3, 8, 9):
        seed = first_digits(CUT+k)
        middle = ''.join(map(str,seed[WIDTHS[0]:]))
        result = subprocess.run([str(executable.resolve()), middle, allowances, BOUNDARY],
                                check=True, text=True, capture_output=True)
        print(result.stdout, end='')
        if k == 3:
            assert '148081 states' in result.stdout
        elif k == 8:
            assert '2248242 states' in result.stdout and '3=1408' in result.stdout
        else:
            assert 'loss at update 159, phase 2' in result.stdout
            inputs = [int(s) for s in result.stdout.splitlines()[1].split(':')[1].split()]
            assert len(inputs) == 159
            prefix = seed[:WIDTHS[0]]
            middle_word = seed[WIDTHS[0]:]
            for t, z in enumerate(inputs):
                phase = t % 52
                tail = middle_word[-k:]
                running = high = 0
                for cell in tail:
                    running += (cell == 3) - (cell == 1)
                    high = max(high,running)
                assert max(high, z+running) <= max(1,high)
                raw = (*prefix, *middle_word, *(3,)*z)
                out, guard, (inner,), _ = analyze(encode(raw), (WIDTHS[phase],))
                assert (inner > allowance(phase)) == (t == len(inputs)-1)
                letters, _ = word_sweep(raw, TERNARY)
                if t == len(inputs)-1:
                    assert out is not None and letters is not None
                    print('Nine-cell oracle: prefix test lost with physical guard debt', guard)
                    break
                x = WIDTHS[phase+1]
                target, _ = word_sweep(prefix, TERNARY)
                assert tuple(letters[:x]) == tuple(target[:x])
                prefix, middle_word = tuple(letters[:x]), tuple(letters[x:CUT+k])



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fast', action='store_true', help='skip the independent scalar check of every allowed edge')
    parser.add_argument('--wide', type=Path, help='run the independently checked spatial-window worker')
    args = parser.parse_args()
    if not __debug__:
        parser.error('enable assertions')
    if args.wide:
        wide(args.wide)
    else:
        main(args.fast)
