"""Clocks by coordinate for BB(2,5) line 13. Use Python with assertions enabled."""
from fractions import Fraction
from pathlib import Path
import json

from pair13 import MACHINE, ROOT, cell, counts


def strip(states, word):
    """Treat the right boundary as a child with its verified return contract."""
    for i, st in enumerate(states):
        states[i], word = cell(st, word)
        assert states[i] is not None, 'halt in tested strip'
    return word


def b_phase(st):
    """The bit that flips on each A entry of an initialized cell."""
    symbol, virgin = st
    assert not virgin and symbol in (1, 2, 4)
    return int(symbol == 4)


def measured_period(k):
    states = [(0, True)] * (4+k)
    strip(states, 'A')
    seen = {}
    phases = []
    emitted = []
    for g in range(4*(2**k)+3):
        key = tuple(states)
        if key in seen:
            start = seen[key]
            end = g
            assert end-start == 2**k
            assert start <= 2**(k+1)-1
            assert len(set(phases[start:end])) == 2**k
            assert None not in phases[start:end]
            period = ''.join(emitted[start:end])
            return start, (period.count('A'), period.count('B'))
        seen[key] = g
        initialized = all(not v and s in (1, 2, 4) for s, v in states[4:])
        phases.append(tuple(b_phase(s) for s in states[4:]) if initialized else None)
        emitted.append(strip(states, 'BABAB'))
    raise AssertionError('period deadline exceeded')


def calendar_bound(h):
    assert h >= 5 and h % 2 == 1
    q = 3 * 2**(h-4)
    requests = 5*q - 4
    return requests, 15*q*q + 16*(h+2)*requests + 5


def run():
    assert (ROOT / 'BB2x5_Rocq_holdouts_37.txt').read_text().splitlines()[12] == MACHINE
    states = [(0, True)]*4
    assert strip(states, 'A') == '' and strip(states, 'BABAB') == 'A'
    settled = tuple(states)
    assert strip(states,'BABAB') == 'BA' and tuple(states) == settled
    inputs = 'BA'
    f, next_f = 2, 3  # Fibonacci bounds F_(k+3) and F_(k+4).
    rates = [Fraction(n) for n in (5,3,3,1)]  # Cut 0..3 entries per steady root group.
    for k in range(33):
        a, b = inputs.count('A'), inputs.count('B')
        assert a%2 and b and a+b <= f
        if k<=9:
            warmup, observed = measured_period(k)
            assert observed == (a,b)
        if k in (0,4,8,12,16,20,24,28,32):
            print(f'cut {4+k}: {a} A, {b} B in {2**k} root groups, Fibonacci bound {f}')
        rates.append(Fraction(a+b, 2**k))
        if k < 32:
            state, output = cell((4, False), inputs*2)
            assert state == (4, False)
            assert (output.count('A'),output.count('B')) == counts(inputs)
            inputs = output
            f, next_f = next_f, f+next_f
    # Starting cuts 0..3 are checked by complete finite-state simulation.
    states = [(0,True)]*4
    strip(states,'A')
    strip(states,'BABAB')
    w='BABAB'
    for st, target in zip(states, rates[:4]):
        assert len(w)==target
        new,w = cell(st,w)
        assert new==st
    # Compare fixed-cut throughput predictions with an independently saved blank trace.
    recorded = json.loads(Path(__file__).with_name('streams-13.json').read_text())
    q = recorded['state']['groups']
    for x in (4, 12, 20, 28, 36):
        observed = recorded['cuts'][x]['entries']
        expected = rates[x] * q
        print(f'cut {x}, q={q}: observed {observed}, steady-rate prediction {float(expected):.3f}')
        if x<=20:
            assert abs(observed-expected) < 100
    R,T = calendar_bound(155)
    print('If unresolved at checkpoint, cell 155 first A (or its halt) by root request',R)
    print('Outer raw-step deadline for that opportunity:',T)


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run without -O')
    run()
