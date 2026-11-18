#!/usr/bin/env python3
"""Bound line 17's first visit to +12 and test specified input streams at a cut."""
import argparse
from pathlib import Path
import subprocess

from line17 import DATA, digits, mark_image, mark_step, once_counts, periodic_marks, word_counts
from marked_register import finite_event
from prior_frontier import marks_on_word, pulse_on_tail


DIGITS = digits(DATA)
ROOT_PERIOD = bytes((0, 1, 0, 0))
LOCKED = bytes(int(i in (5, 11, 17, 23)) for i in range(1, 27))
ZERO = bytes((0,))


def initial(i):
    return DIGITS[i][0], DIGITS[i-1][1] if i else 0


def source_slot(state, prefix, period, rank):
    """One-based input that emits the requested one-based output on this ray."""
    if rank < 1 or not period:
        raise ValueError('need a positive rank and nonempty period')
    def inside(start, word, target):
        for index, bit in enumerate(word, 1):
            v, pending, out = mark_step(*start, bit)
            target -= len(out)
            if target <= 0:
                return index
            start = v, pending
        raise ValueError('rank outside the selected word')

    after, output = marks_on_word(state, prefix)
    if rank <= len(output):
        return inside(state, prefix, rank)
    consumed = len(prefix)
    rank -= len(output)
    state = after
    seen, transfers = {}, {}
    while True:
        if state in seen:
            previous, previous_rank = seen[state]
            width = previous_rank-rank
            # Every three valid input slots emit at least one output.
            copies = (rank-1)//width
            consumed += copies*(consumed-previous)
            rank -= copies*width
            seen.clear()
        seen[state] = consumed, rank
        if state not in transfers:
            after, output = marks_on_word(state, period)
            transfers[state] = after, len(output)
        after, width = transfers[state]
        if rank <= width:
            return consumed+inside(state, period, rank)
        consumed += len(period)
        rank -= width
        state = after


def period_layers(start, stop, prefix, period, word_limit):
    """Retain the actual input ray and initial state at each digit."""
    for i in range(start, stop):
        if len(prefix)+len(period) > word_limit:
            raise ValueError(f'period-word budget at pair {i}')
        state = initial(i)
        yield state, prefix, period
        if i+1 < stop:
            prefix, period = periodic_marks(state, prefix, period)


def cut53_period():
    prefix, period = b'', ROOT_PERIOD
    for i in range(53):
        prefix, period = periodic_marks(initial(i), prefix, period)
    if prefix or len(period) != 147740 or period[:26] != LOCKED:
        raise ValueError('unexpected period at cut 53')
    return period


def forced_output(state, known):
    """Extend the known output by up to five letters common to all legal inputs."""
    (v, pending), output = marks_on_word(state, known)
    cool = 2 if known[-1:] == b'\x01' else int(known[-2:-1] == b'\x01')
    def possible(v, pending, cool, needed):
        for bit in (0, 1):
            if bit and (pending or cool):
                continue
            new_v, new_p, letters = mark_step(v, pending, bit)
            if len(letters) >= needed:
                yield bytes(letters[:needed])
            else:
                new_cool = 2 if bit else max(0, cool-1)
                for tail in possible(new_v, new_p, new_cool, needed-len(letters)):
                    yield bytes(letters)+tail
    futures = possible(v, pending, cool, 5)
    common = next(futures)
    for word in futures:
        while not word.startswith(common):
            common = common[:-1]
        if not common:
            break
    return output+common


def cut_limits(target=424, rank=1):
    """Latest input needed at each earlier cut to emit the requested output."""
    if not 53 <= target <= len(DIGITS) or rank < 1:
        raise ValueError('invalid target cut or output rank')
    cut53_period()
    if forced_output((1, 0), LOCKED)[:26] != LOCKED:
        raise ValueError('homogeneous digit does not preserve the locked prefix')

    prefix = LOCKED
    prefixes = {}
    for i in range(53, target):
        if i < 403:
            if initial(i) != (1, 0):
                raise ValueError('unexpected digit in the homogeneous block')
            prefixes[i] = LOCKED
        else:
            prefixes[i] = prefix
            prefix = forced_output(initial(i), prefix)
    limits = {target: rank}
    for i in reversed(prefixes):
        # After the guaranteed input prefix, extending by zero minimizes the
        # cumulative number of emitted slots at this individual digit.
        limits[i] = source_slot(initial(i), prefixes[i], ZERO, limits[i+1])
    return limits


def packed_source_slot(engine, word_bits, cut, rank):
    # Every three input slots emit at least one child slot at every digit.
    horizon = (3**cut*rank+3)//4
    def run(epochs, *mode):
        cmd = [str(Path(engine).resolve()), str(epochs), str(word_bits), '0', *mode]
        proc = subprocess.run(cmd, input=DATA[:2*cut], text=True, capture_output=True)
        if proc.returncode:
            raise ValueError(proc.stderr.strip() or 'packed worker failed')
        return proc.stdout
    root = int(run(horizon, 'select', str(rank)))
    if not 1 <= root <= 4*horizon:
        raise ValueError('selected slot outside the guaranteed horizon')
    # Independently count all earlier sweeps, then propagate up to four slots
    # from their ending states. This also checks positions inside a two-bit output.
    epochs, offset = divmod(root-1, 4)
    rows = [tuple(map(int, row.split())) for row in run(epochs).splitlines()]
    if len(rows) != cut or any(len(row) != 5 for row in rows):
        raise ValueError('incomplete packed rank check')
    def outputs(width):
        word = ROOT_PERIOD[:width]
        for v, pending, _, _, _ in rows:
            _, word = marks_on_word((v, pending), word)
        return rows[-1][2]+len(word)
    if not outputs(offset) < rank <= outputs(offset+1):
        raise ValueError('forward and inverse output ranks differ')
    return root


def edge_bound(cut=53, engine=None, word_bits=2**31):
    if not 53 <= cut <= 403:
        raise ValueError('choose an exact-period cut between 53 and 403')
    bounds = cut_limits()
    rank = bounds[cut]
    if engine:
        root = packed_source_slot(engine, word_bits, cut, rank)
    else:
        layers = list(period_layers(0, cut, b'', ROOT_PERIOD, 2**20))
        root = rank
        for state, head, period in reversed(layers):
            root = source_slot(state, head, period, root)
    epochs = (root+3)//4
    # Count whole virtual sweeps, stopping the physical clock at first entry
    # to the singleton plus one B2 instruction to reach the new blank at +12.
    raw = 2308941 + 14*epochs*(epochs-1) + (74+72*(2**len(DIGITS)-1))*epochs
    return bounds[403], root, epochs, raw


def suffix_event(cut, prefix, period, word_limit=2**20):
    """Exact first +12 event under this specified ray at the chosen cut."""
    if not 0 <= cut < len(DIGITS) or not period or set(prefix+period)-{0, 1}:
        raise ValueError('invalid cut or bit word')
    # Two period copies include every spacing across a repeat boundary.
    marks = [j for j, b in enumerate(prefix+period*2) if b]
    if any(y-x < 3 for x, y in zip(marks, marks[1:])):
        raise ValueError('input marks must be at least three slots apart')
    layers = list(period_layers(cut, len(DIGITS), prefix, period, word_limit))
    first = 1
    for state, head, cycle in reversed(layers):
        first = source_slot(state, head, cycle, first)
    count = first-1
    states = []
    for state, head, cycle in layers:
        result = word_counts(state, head, cycle, count)
        count = result.slots
        states.append(result.state)
    if count:
        raise ValueError('the preceding prefix already visited the singleton')
    flags = [p for _, p in states[1:]]+[DIGITS[-1][1]]
    row = ''.join('102'[v]+str(2+f) for (v, _), f in zip(states, flags))+'2'
    at = first-1
    bit = prefix[at] if at < len(prefix) else period[(at-len(prefix)) % len(period)]
    hit, row = pulse_on_tail(row, bool(bit or states[0][1]))
    if not hit:
        raise ValueError('selected input did not reach coordinate +12')
    return first, row


def possible_symbols(through, marks, cut=403):
    """Propagate a finite mark list and report what its cut-418 bits settle."""
    if not 53 <= cut <= 418:
        raise ValueError('choose an input cut from 53 through 418')
    if through < 0 or any(t < 1 or t > through for t in marks):
        raise ValueError('marks must lie within the supplied prefix')
    if any(b-a < 3 for a, b in zip(marks, marks[1:])):
        raise ValueError('mark positions must be increasing with gaps of at least three')
    known = LOCKED
    for i in range(403, cut):
        known = forced_output(initial(i), known)
    if [t for t in marks if t <= len(known)] != [i for i, bit in enumerate(known[:through], 1) if bit]:
        raise ValueError(f'cut-{cut} prefix differs from the known blank-orbit prefix')
    n = through
    for i in range(cut, 418):
        state = initial(i)
        outputs = once_counts(n, marks, state).slots
        marks = [t for t in mark_image(marks, n, state) if t <= outputs]
        n = outputs
    if n < 9:
        return n, (0, 1, 4)
    if 9 in marks:
        return n, (1,)
    if n < 10:
        return n, (0, 4)
    return n, (0,) if 10 in marks else (4,)


def branch_witnesses():
    """Lift three conditional right-edge histories through all 350 equal pairs."""
    period = cut53_period()
    width = 403-53
    power = 3**width
    weights = (power-1)//2
    carry = 0
    survivors = []
    for slot, bit in enumerate(period, 1):
        if bit:
            delta, child = finite_event(slot+carry, width)
            carry += delta
            if child is not None:
                survivors.append(child)
    if survivors != [5, 11, 17, 23]:
        raise ValueError('unexpected surviving marks from the first cut-53 period')
    for gap in (5, 7, 8):
        # The fifth cut-403 mark is at 28 in every example.
        at, row = suffix_event(403, LOCKED+ZERO, bytes((1,))+bytes(gap-1))
        c, previous = carry, len(period)
        for child in range(28, at+1, gap):
            slot = power*child-5*weights-c
            delta, emitted = finite_event(slot+c, width)
            if slot-previous < 3 or (emitted, delta) != (child, 8*weights):
                raise ValueError('invalid separated cut-53 preimage')
            c += delta
            previous = slot
        yield gap, at, row[-13:]


def bits(text):
    if set(text)-set('01'):
        raise ValueError('a bit word may contain only 0 and 1')
    return bytes(map(int, text))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    bound = sub.add_parser('bound', help='compute an upper bound for the true blank orbit')
    bound.add_argument('--cut', type=int, default=53)
    bound.add_argument('--packed-engine', type=Path)
    bound.add_argument('--word-bits', type=int, default=2**31)
    case = sub.add_parser('suffix', help='evaluate a specified finite prefix and repeating tail')
    case.add_argument('--cut', type=int, default=403)
    case.add_argument('--prefix', default='')
    case.add_argument('--period', required=True)
    case.add_argument('--word-limit', type=int, default=2**20)
    sub.add_parser('branches', help='check three continuations of the first true cut-53 period')
    decision = sub.add_parser('decide', help='check the two decisive slots from a finite prefix at an earlier cut')
    decision.add_argument('--cut', type=int, default=403, help='input cut from 53 through 418')
    decision.add_argument('--through', type=int, required=True, help='number of known slots at the input cut')
    positions = decision.add_mutually_exclusive_group(required=True)
    positions.add_argument('--marks', nargs='*', type=int, help='all one-based marks through that slot')
    positions.add_argument('--marks-file', type=Path, help='whitespace-separated positions, in increasing order')
    args = parser.parse_args()
    try:
        if not __debug__:
            raise ValueError('the register verifier requires assertions')
        if args.command == 'bound':
            local, root, epochs, raw = edge_bound(args.cut, args.packed_engine, args.word_bits)
            print(f'First +12 visit by cut-403 slot {local}, root slot {root}, sweep {epochs}, raw step {raw}.')
        elif args.command == 'branches':
            for gap, slot, word in branch_witnesses():
                print(f'Cut-403 gap {gap}, first +12 on cut-403 slot {slot}, cells -1 through 11 = {word}.')
        elif args.command == 'decide':
            marks = args.marks if args.marks_file is None else list(map(int, args.marks_file.read_text().split()))
            n, symbols = possible_symbols(args.through, marks, args.cut)
            print(f'The supplied prefix emits {n} slots at cut 418. The remaining candidate symbols at -1 are {symbols}.')
        else:
            slot, row = suffix_event(args.cut, bits(args.prefix), bits(args.period), args.word_limit)
            left = -837+2*args.cut
            print(f'For the supplied stream, B first enters +12 on cut-{args.cut} slot {slot}.')
            print(f'Cells {left} through 11 at arrival: {row}')
    except (AssertionError, ValueError, OSError) as exc:
        parser.exit(2, f'Edge calculation stopped: {exc or "invalid marked stream or literal return"}\n')


if __name__ == '__main__':
    main()
