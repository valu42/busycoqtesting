"""Verify the append clock and the failure of a local debt bound for line 34."""
from collections import Counter
from itertools import product
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from prior_sweeps import TERNARY, TapeMachine, direct_epoch, textword, word_sweep
from target34_orbit import encode, sweep


def trailing_openings(word):
    for count, digit in enumerate(reversed(word)):
        if digit != 1:
            return count
    return len(word)


def interfaces(word):
    """At cut i: debt of word[i:] and survivor bit of cell i−1."""
    debt = 0
    result = [(0, False)] * (len(word) + 1)
    for i in range(len(word) - 1, -1, -1):
        digit = word[i]
        result[i + 1] = (debt, digit == 1 and not debt)
        debt = max(0, debt + (digit == 3) - (digit == 1))
    result[0] = (debt, debt == 1)
    return result


def check_clock(word, previous_header, successor):
    """Check one successful step; the predicted suffix has material coordinates."""
    n = trailing_openings(word)
    if n:
        assert successor[-n-1:] == [3] + [1] * (n - 1) + [2]
    elif word and word[-1] == 2:
        n = trailing_openings(word[:-1])
        if n:
            assert successor[-n-1:] == [3] + [1] * (n - 1) + [2]
        elif len(word) >= 2 and word[-2] == 3:
            assert successor[-1] == 1
            if len(word) >= 3:
                assert successor[-2:] == [1, 1]
            if previous_header is not None:
                pairs = interfaces(word)
                last = next((i for i in range(len(word), 0, -1)
                             if pairs[i][1]), 0)
                if last and last >= previous_header:
                    tail = word[last:]
                    assert tail.count(1) == tail.count(3)
                    assert tail.count(2) - tail.count(3) in (0, 1)
                    assert trailing_openings(successor) == len(tail) - 1
                    return True
                assert trailing_openings(successor) >= len(word) - previous_header - 1
                return False
    return None


def main():
    listed = Path(__file__).resolve().parents[1] / 'BB2x5_Rocq_holdouts_37.txt'
    assert listed.read_text().splitlines()[33] == TERNARY == '1RB2LA4RA1LA3LA_0LA2RB3RB2LB---'
    # Include resets and explicit halt controls on arbitrary initial tapes.
    literal = failure = 0
    for length in range(8):
        for digits in product((1, 2, 3), repeat=length):
            word = list(digits)
            successor, low = word_sweep(word, TERNARY)
            tm = TapeMachine(TERNARY, word, left=1)
            assert direct_epoch(tm, (1, 2, 3)) == successor
            literal += 1
            if successor is None:
                failure += 1
                assert (tm.state, tm.tape[tm.head]) == ('B', 4)
                continue
            header = 1 if low > -3 else 5
            assert (tm.head, tm.state) == (-header, 'A')
            assert tm.tape == {tm.head + 1 + i: x for i, x in enumerate(successor)}
            assert len(successor) == len(word) + header + bool(trailing_openings(word))
            check_clock(word, None, successor)
    print(f'{literal} one-sweep inputs checked literally; {failure} halted')

    tm = TapeMachine(TERNARY)
    raw = {}
    for epoch in range(1, 81):
        occupied = direct_epoch(tm, (1, 2, 3))
        assert tm.state == 'A' and occupied is not None
        assert tm.tape == {tm.head + 1 + i: x for i, x in enumerate(occupied)}
        if epoch in (2, 4, 9, 12, 18, 80):
            raw[epoch] = (tm.steps, tm.head, len(occupied))
    assert raw == {2: (8, -2, 2), 4: (32, -4, 5), 9: (171, -9, 11),
                   12: (302, -12, 15), 18: (692, -18, 22), 80: (14152, -80, 100)}
    print('literal blank endpoints (steps, head, width):', raw)

    word = []
    previous_header = None
    appends = []
    residue_checks = Counter()
    example_words = {}
    witness = bytes(map(int, '23213232131232131232131'))
    factors = {(witness * 2)[i:i + 17] for i in range(len(witness))}
    sources = {}
    for epoch in range(1501):
        if epoch in (839, 854, 1500):
            example_words[epoch] = word
        if epoch <= 854 and len(sources) != len(factors):
            occupied = bytes(word)
            for factor in factors - sources.keys():
                where = occupied.find(factor)
                if where >= 0:
                    sources[factor] = (epoch, where)
        if epoch == 1500:
            break
        n = trailing_openings(word)
        if n:
            if appends:
                assert epoch == appends[-1][0] + appends[-1][1] + 1
            appends.append((epoch, n))
        successor, low = word_sweep(word, TERNARY)
        assert successor is not None
        certified = check_clock(word, previous_header, successor)
        if certified is not None:
            residue_checks[certified] += 1
        previous_header = 1 if low > -3 else 5
        word = successor

    print('through epoch 1500: width', len(word), 'appending sweeps', len(appends),
          'terminal run lengths', sorted(Counter(r for _, r in appends).items()))
    print('return-to-open steps with/without the local residue hypothesis:',
          residue_checks[True], residue_checks[False])
    assert all(r >= 2 for e, r in appends if e >= 4)
    assert len(sources) == len(factors) == 22
    print('22 distinct length-17 factors at the 23 offsets of the period all occur by epoch',
          max(e for e, _ in sources.values()))
    phase_sources = {}
    phase_word = []
    for epoch in range(3182):
        if epoch % 13 == 854 % 13:
            occupied = bytes(phase_word)
            for factor in factors - phase_sources.keys():
                offset = occupied.find(factor)
                if offset >= 0:
                    phase_sources[factor] = (epoch, offset)
        if len(phase_sources) == len(factors):
            break
        phase_word, _ = word_sweep(phase_word, TERNARY)
        assert phase_word is not None
    assert len(phase_sources) == len(factors) and epoch == 3181
    print('all period factors occur in genuine phase 9 modulo 13 by epoch', epoch)

    original = example_words[839]
    assert len(original) == 1025
    a, b, copies = 856, 879, 493
    assert textword(original[a:b]) == '11112113232111111131211'
    altered = original[:a] + copies * original[a:b] + original[b:]
    machine = TapeMachine(TERNARY, altered, left=1)
    for epoch in range(839, 854):
        pairs = interfaces(original)
        assert pairs[a] == pairs[b]
        assert pairs[9][0] == interfaces(altered)[9][0]
        timed, guard, _, _ = sweep(encode(altered))
        assert timed is not None
        enc, displacement, ticks = timed
        old_head = machine.head
        for _ in range(ticks):
            assert machine.step()
        original, low = word_sweep(original, TERNARY)
        altered, low_alt = word_sweep(altered, TERNARY)
        assert original is not None and altered is not None and low == low_alt == -guard
        assert encode(altered) == enc and machine.head == old_head - displacement
        assert machine.state == 'A' and machine.tape == {
            machine.head + 1 + i: x for i, x in enumerate(altered)}
        header = 1 if low > -3 else 5
        a += header
        b += header
        assert altered == original[:a] + copies * original[a:b] + original[b:]
    assert (a, b) == (871, 894) and original == example_words[854]
    assert bytes(original[a:b]) == witness
    original_bytes, altered_bytes = bytes(original), bytes(altered)
    observed = factors | {original_bytes[i:i+17] for i in range(len(original)-16)}
    assert all(altered_bytes[i:i+17] in observed for i in range(len(altered)-16))
    assert interfaces(original)[9][0] == 0 and interfaces(altered)[9][0] == 10
    assert word_sweep(original, TERNARY)[0] is not None
    assert word_sweep(altered, TERNARY) == (None, -6)
    failed, guard, cut_debt, _ = sweep(encode(altered))
    assert failed is None and (guard, cut_debt) == (6, 10)
    print('15 full configurations matched the timed implementation through raw step', machine.steps)
    while machine.steps <= 6_685_289 and machine.step():
        pass
    assert (machine.steps, machine.state, machine.head, machine.tape[machine.head]) == (
        6_685_289, 'B', -17, 4)
    print('493-copy tape: 15 shadowed sweeps; cut-9 debt jumps from 0 to 10;',
          'literal B4 after 6685289 steps, head -17')


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Enable assertions.')
    main()
