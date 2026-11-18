"""Finite certificates for isolated exterior readings and for sweeps from one visible prefix."""

import argparse
from collections import deque
from functools import cache
from pathlib import Path

from line35_chronological_strip import ordinary_debt_bound
from line35_guard_stream import (
    ALPHABET, CLOSE, HEADERS, OPEN, packed_successor, prefix_successor, unpack,
)
from line35_isolated_sweep import CUT, Epoch, read_checkpoint
from line37_orbit import match
from prior_sweeps import TERNARY_CLOSE, TapeMachine, direct_epoch, word_sweep


MASK = (1 << CUT) - 1
# Each digit is one exterior debt. These reach an abstract halt if the allowed
# gap in the corresponding theorem is shortened by one sweep.
ESCAPES = {
    4: '040000002010102222200030002222000400000000224',
    5: '0400000002000022002010102220000000000010200040000000000002200000200020000000200000000105',
    None: (0, 0, 0, 11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 2),
}


def seed28():
    machine = TapeMachine(TERNARY_CLOSE)
    for _ in range(15):
        word = direct_epoch(machine, ALPHABET)
    assert len(word) == CUT + 1
    state = Epoch.from_word(15, machine.steps, machine.head, word)
    return ((state.opens >> 1) << CUT) | (state.closes >> 1)


@cache
def transitions(key, ceiling=6):
    opens, closes = key >> CUT, key & MASK
    survivors, internal, _ = match(CUT, opens, closes, CUT)
    count = survivors.bit_count()
    edges = []
    for debt in range(ceiling + 1):
        guard = internal + max(0, debt - count)
        dest = None
        if guard < 6:
            width, o, c = packed_successor(CUT, survivors, guard)
            shift = width - CUT
            dest = ((o >> shift) << CUT) | (c >> shift)
        edges.append((guard, dest))
        survivors &= survivors - 1
    return edges


def permitted(key, peak, wait):
    if wait:
        return transitions(key)[:3]
    if peak is None:
        # Unrestricted pulses are checked on arrival. Include all successful
        # highs and all lows, so a later low that halts still fails the proof.
        peak = max(2, 5 + (key >> CUT).bit_count() - (key & MASK).bit_count())
    return transitions(key, max(6, peak))[:peak+1]


def check_spacing(start, peak, gap, needed):
    # A smaller remaining wait admits every continuation of a larger one.
    waits = {start: 0}
    queue = deque([(start, 0)])
    while queue:
        key, wait = queue.popleft()
        if wait != waits[key]:
            continue
        for debt, (guard, dest) in enumerate(permitted(key, peak, wait)):
            if dest is None:
                raise AssertionError(('unprotected prefix', key, wait, debt, guard))
            after = gap if debt > 2 else max(0, wait - 1)
            if dest not in waits or after < waits[dest]:
                waits[dest] = after
                queue.append((dest, after))

    # Check every certificate edge from scratch, including the seed. A real
    # prefix need only have a remaining wait >= its entry in this table.
    assert waits[start] == 0
    maximum = 0
    for key, wait in waits.items():
        edges = permitted(key, peak, wait)
        needed[key] = max(len(edges) - 1, needed.get(key, 0))
        for debt, (guard, dest) in enumerate(edges):
            maximum = max(maximum, guard)
            after = gap if debt > 2 else max(0, wait - 1)
            assert guard < 6 and dest in waits and waits[dest] <= after
    eligible = sum(wait == 0 for wait in waits.values())
    print('exterior ceiling', peak if peak is not None else 'any successful pulse', 'required intervening lows', gap,
          'certified prefixes', len(waits), 'eligible for a pulse', eligible, 'max guard', maximum)
    return waits, (len(waits), eligible, maximum)


def check_one_pulse(before, needed):
    """An exterior of arbitrary height acts once. Only a successful pulse has a future."""
    after = set()
    thresholds = []
    for key in before:
        balance = (key >> CUT).bit_count() - (key & MASK).bit_count()
        fatal = 6 + balance
        thresholds.append(fatal)
        needed[key] = max(needed[key], fatal)
        edges = transitions(key, fatal)
        assert edges[fatal] == (6, None)
        assert all(dest in before for _, dest in edges[:3])
        for guard, dest in edges[3:fatal]:
            assert guard < 6 and dest is not None
            after.add(dest)
    assert (min(thresholds), max(thresholds)) == (7, 33)
    # Saturate under all quiet continuations. Each post-pulse edge must both
    # succeed and re-enter this same finite set, proving the infinite tail.
    first = after.copy()
    queue = deque(after)
    while queue:
        key = queue.popleft()
        for guard, dest in transitions(key)[:3]:
            assert guard < 6 and dest is not None
            if dest not in after:
                after.add(dest)
                queue.append(dest)
    for key in after:
        needed[key] = max(2, needed.get(key, 0))
        assert all(guard < 6 and dest in after for guard, dest in transitions(key)[:3])
    assert (len(before), len(first), len(after)) == (20286, 13262, 71627)
    print('one arbitrary pulse:', len(before), 'pre-pulse prefixes,', len(first),
          'immediate successors,', len(after), 'prefixes closed under all later lows; thresholds',
          min(thresholds), 'through', max(thresholds))


def check_escape(start, peak, gap):
    prefix = unpack(CUT, start >> CUT, start & MASK)
    history = list(map(int, ESCAPES[peak]))
    last_high = -gap - 1
    for t, d in enumerate(history):
        assert d >= 0 and (peak is None or d <= peak)
        if d > 2:
            assert t - last_high > gap
            last_high = t
        word = prefix + (CLOSE,) * d + (OPEN, CLOSE)
        machine = TapeMachine(TERNARY_CLOSE, word, left=1)
        actual = direct_epoch(machine, ALPHABET)
        prefix = prefix_successor(prefix, d)
        if t == len(history) - 1:
            assert actual is None and prefix is None and (machine.state, machine.tape[machine.head]) == ('B', 4)
            assert peak is not None or d <= 2
        else:
            assert actual is not None and prefix == tuple(actual[:CUT])
    label = peak if peak is not None else 'any successful pulse'
    print('one shorter gap', gap, 'admits a', len(history), 'sample abstract B4 at ceiling', label)


def check_all():
    start = seed28()
    needed = {}
    for peak, gap, expected in ((2, 0, (20286, 20286, 3)), (3, 0, (58682, 58682, 5)),
                                (4, 11, (49826, 33968, 5)), (6, 43, (50156, 22599, 5)),
                                (None, 8, (128716, 74687, 5))):
        waits, result = check_spacing(start, peak, gap, needed)
        assert result == expected
        if peak == 2:
            check_one_pulse(waits, needed)
    check_escape(start, 4, 10)
    check_escape(start, 5, 42)
    check_escape(start, None, 7)
    checked = 0
    for key, largest in needed.items():
        prefix = unpack(CUT, key >> CUT, key & MASK)
        edges = transitions(key, largest) if largest > 6 else transitions(key)
        for d in range(largest+1):
            word = prefix + (CLOSE,) * d + (OPEN, CLOSE)
            actual, low = word_sweep(word, TERNARY_CLOSE)
            guard, dest = edges[d]
            assert min(6, guard) == -low and (actual is None) == (dest is None)
            if dest is not None:
                assert tuple(actual[:CUT]) == unpack(CUT, dest >> CUT, dest & MASK)
            checked += 1
    assert checked == 1_603_448
    print('distinct certificate inputs independently checked by word sweep:', checked)


def zero_seam(state):
    """Return a permanent zero-debt suffix length. The empty suffix always qualifies."""
    if state.width < 2 or state.opens & 3 != 2 or state.closes & 3 != 1:
        return 0
    if state.number % 2 == 0:
        return 2
    word = state.digits()
    triples = 0
    for j in range(2, len(word)-2, 3):
        if word[-1-j] != OPEN or word[-3-j] != OPEN:
            break
        triples += 1
    return 3*triples if triples else 2


def erased_width(survivors, count):
    """Number of rightmost prefix cells through the count-th erased surviving opening."""
    if count == 0:
        return 0
    total = survivors.bit_count()
    assert 0 < count <= total
    lo, hi = 1, survivors.bit_length()
    while lo < hi:
        mid = (lo + hi) // 2
        if total - (survivors >> mid).bit_count() >= count:
            hi = mid
        else:
            lo = mid + 1
    return lo


def forecast(m, width, opens, closes, ancestry, limit, includes_terminal=False):
    """Inputs are the left width before a zero seam and a visible prefix of that width.

    'ancestry' counts earlier successful sweeps, capped at five. Every subsequent
    right-boundary survivor is free. With an empty seam, the permanent terminal
    closing is outside the ordinary-cell rule. Unseen symbols are never read.
    """
    if not (0 <= width <= m and limit > 0 and 0 <= ancestry <= 5):
        raise ValueError('invalid prefix, ancestry or forecast length')
    guards = []
    for _ in range(limit):
        gap = m - width
        recent = min(gap, max(0, 25 - width)) if ancestry == 5 else gap
        exceptional = recent + int(includes_terminal and gap > recent)
        bound = exceptional + ordinary_debt_bound(gap - exceptional)
        survivors, internal, _ = match(width, opens, closes, width)
        spare = survivors.bit_count()
        maximum = internal + max(0, bound - spare)
        if maximum >= 6:
            return guards, 'allowance reaches six', (width, gap, bound, maximum)
        if bound > spare:
            # Every guard in this interval succeeds. Further outcomes can have
            # different headers, so this particular common-prefix proof ends here.
            guards.append((internal, maximum))
            return guards, 'last safe header can vary', (width, gap, bound, maximum)
        guards.append((internal, internal))
        header = len(HEADERS[internal])
        # If width=0 and bound=0, the header is the entire known successor.
        if width:
            lost = erased_width(survivors, bound)
            _, o, c = packed_successor(width, survivors, internal)
            opens, closes = o >> (1+lost), c >> (1+lost)
            width += header - lost
        else:
            width, opens, closes = 1, 0, 1  # head digit 2 at guard zero
        m += header + 1
        ancestry = min(5, ancestry + 1)
    return guards, 'requested horizon certified', (width, m-width, None, None)


def checkpoint_forecast(path, widths, limit):
    state, origin, _ = read_checkpoint(path)
    seam = zero_seam(state)
    m = state.width - seam
    # An externally supplied epoch-v1 file makes a claim about prior blank
    # ancestry. Experimental checkpoints can certify future ordinary ancestry anew.
    ancestry = min(5, state.number - 1) if origin['kind'] == 'checkpoint' else 0
    for x in widths or sorted({(m+4)//5, m//2, max(0, m-28), m}):
        if not 0 <= x <= m:
            raise ValueError('visible prefix must end before the zero-debt seam')
        guards, why, stop = forecast(m, x, state.opens >> (state.width-x), state.closes >> (state.width-x),
                                     ancestry, limit, includes_terminal=seam == 0)
        print('epoch', state.number, 'fixed zero-debt suffix', seam, 'visible', x, 'of', m,
              'certified sweeps', len(guards), 'outcome', why, 'final calculation', stop)
        yield x, guards


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--checkpoint', type=Path, help='forecast from a known prefix of a reached checkpoint')
    parser.add_argument('--prefix', type=int, action='append', help='visible cells, repeatable')
    parser.add_argument('--limit', type=int, default=256, help='maximum forecast horizon')
    args = parser.parse_args()
    if not __debug__:
        parser.error('run certificate checks with assertions enabled')
    if args.checkpoint:
        try:
            list(checkpoint_forecast(args.checkpoint, args.prefix, args.limit))
        except (ValueError, KeyError, OSError) as exc:
            parser.error(str(exc))
    elif args.prefix or args.limit != 256:
        parser.error('--prefix and --limit apply to a checkpoint')
    else:
        check_all()


if __name__ == '__main__':
    main()
