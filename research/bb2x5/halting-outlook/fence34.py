"""Check the 52-phase moving cut, its necessity for prefix lock, and cap motion."""
import argparse
import json
from collections import Counter
from itertools import product
from pathlib import Path
import sys

from target34_orbit import encode, sweep
from line34_left import digits
from line34_right import interfaces
from prior_sweeps import TERNARY, TapeMachine, direct_epoch, textword, word_sweep


BOUNDARY = "0101110100101001111111011101100111100101011101011001"


def allowance(phase):
    if phase in (2, 13, 40, 46):
        return 0
    if phase in (3, 7, 23, 41):
        return 2
    return 1


def cuts():
    result = [67]
    for phase in range(52):
        result.append(result[-1] + 1 - allowance(phase))
    assert result[-1] == result[0] and (min(result), max(result)) == (66, 68)
    return result


def prefix(config, size):
    width, opens, closes = config
    return digits((opens >> (width-size), closes >> (width-size)), size)


def verify_fence(seed, guards, sizes):
    protected = tuple(seed)
    boundary_bits = []
    cases = literal = 0
    for phase in range(52):
        x, y = sizes[phase:phase+2]
        assert len(protected) == x
        u = allowance(phase)
        assert not u or protected[-u:] == (1,) * u
        undisturbed = protected[:x-u]
        boundary_bits.append(int(interfaces(undisturbed)[-1][1]))
        # All guarded real sweeps using this prefix have the same first y digits as
        # the canonical C^d completion. In computing these digits, suppress any
        # output from the test completion, including a possible terminal append.
        base, low = word_sweep(protected, TERNARY)
        assert low == -guards[phase] and y <= x + 1
        target = tuple(base[:y])
        accepted = []
        for d in range(x + 7):
            trial = protected + (3,) * d
            new, low = word_sweep(trial, TERNARY)
            if new is not None and low == -guards[phase] and tuple(new[:y]) == target:
                accepted.append(d)
            cases += 1
            if d <= allowance(phase) + 1:
                tm = TapeMachine(TERNARY, trial, left=1)
                assert direct_epoch(tm, (1, 2, 3)) == new
                if new is not None:
                    head = -1 if low > -3 else -5
                    assert tm.head == head and tm.state == 'A'
                    assert tm.tape == {head+i+1:v for i,v in enumerate(new)}
                else:
                    assert tm.state == 'B' and tm.tape[tm.head] == 4
                literal += 1
        assert accepted == list(range(allowance(phase)+1))
        protected = target
    assert protected == tuple(seed)
    assert ''.join(map(str,boundary_bits)) == BOUNDARY
    print(f'52-phase prefix closes. {cases} canonical debt cases, {literal} literal full-config checks.')


def residual_update(word, allowance, left_bit):
    """One exact residual-word sweep, or None on loss of the protected prefix."""
    if interfaces(word)[0][0] > allowance:
        return None
    supplied = (1,) * allowance + word
    bits = [bool(left_bit)] + [p[1] for p in interfaces(supplied)[1:]]
    ordinary = tuple(1 if a == b else 3 if b else 2 for a,b in zip(bits,bits[1:]))
    return ordinary + ((2,) if bits[-1] else ())


def check_wave():
    # Bit column alpha=0 (wlog); left of j is arbitrary. Enumerate enough cells
    # for the local assertion and several periods on the right as a matching cap.
    for j in range(4, 8):
        for older in product((0, 1), repeat=4):
            reference = [int(i % 4 == 0) for i in range(22)]
            changed = reference[:]
            changed[j-4:j] = older
            changed[j] ^= 1
            def update(bits):
                ordinary = [1 if l == r else 3 if r else 2
                            for l,r in zip(bits, bits[1:])]
                d = 0
                new = []
                for v in reversed(ordinary):
                    new.append(int(v == 1 and not d))
                    d = max(0, d + (v == 3) - (v == 1))
                # output index i+2 corresponds to the pair bits[i:i+2]
                return [None, None] + list(reversed(new))
            a, b = update(reference), update(changed)
            last = max(i for i in range(2, len(a)) if a[i] != b[i])
            assert last == j + (1 if j % 4 == 2 else 2)
    print('64 defect fronts on the width-four tail give the predicted rightmost successor.')


def check_small_rings():
    # Use a forward opening stack on three copies; positive total balance means
    # any closing that can reach a middle-copy opener does so within one period.
    for n in range(1, 12):
        next_mask = []
        for old in range(1 << n):
            b = tuple(bool(old & (1 << i)) for i in range(n))
            word = tuple(1 if b[(i-2)%n] == b[(i-1)%n] else 3 if b[i-1] else 2
                         for i in range(n))
            stack = []
            for j, symbol in enumerate(word * 3):
                if symbol == 1:
                    stack.append(j)
                elif symbol == 3 and stack:
                    stack.pop()
            next_mask.append(sum(1 << (j-n) for j in stack if n <= j < 2*n))
        accepted = []
        for old in range(1 << n):
            v = old
            for _ in range(52):
                v = next_mask[v]
            if v == old:
                accepted.append(old)
        expected = {(1 << n)-1}
        if n % 4 == 0:
            expected.update(sum(1 << j for j in range(r,n,4)) for r in range(4))
        assert set(accepted) == expected
    print('Independent three-copy opening-stack enumeration covers widths 1 through 11.')


def main(epochs):
    listed = Path(__file__).resolve().parents[1] / 'BB2x5_Rocq_holdouts_37.txt'
    assert listed.read_text().splitlines()[33] == TERNARY == '1RB2LA4RA1LA3LA_0LA2RB3RB2LB---'
    sizes = cuts()
    config = (0,0,0)
    clock = head = 0
    observed = Counter()
    prefixes = []
    guards = []
    for epoch in range(epochs):
        phase = epoch % 52
        x = sizes[phase]
        result, guard, d, _ = sweep(config, x)
        assert result is not None
        if epoch == 78:
            start = prefix(config, 17)
            assert start == (1,) * 16 + (3,)
            tm = TapeMachine(TERNARY)
            for _ in range(78):
                assert direct_epoch(tm, (1,2,3)) is not None
            assert (tm.steps, tm.head, tm.state) == (clock, head, 'A')
            assert len(tm.tape) == config[0]
            assert encode([tm.tape[head+i+1] for i in range(config[0])]) == config
        if epoch == 1300:
            stored = json.loads(Path(__file__).with_name('fence34-seed.json').read_text())
            assert stored['machine'] == TERNARY and stored['state'] == 'A'
            assert (stored['raw_steps'], stored['head'], stored['epoch']) == (clock, head, epoch)
            assert config == (stored['width'], int(stored['open_hex'],16), int(stored['closing_hex'],16))
            for _ in range(clock - tm.steps):
                assert tm.step()
            assert (tm.steps, tm.head, tm.state) == (clock, head, 'A')
            full_word = digits(config[1:], config[0])
            assert tm.tape == {head+1+i:v for i,v in enumerate(full_word)}
            residual = full_word[x:]
            print('literal epoch 1300: raw steps', clock, 'head', head, 'width', config[0],
                  'protected prefix', textword(prefix(config, x)))
        if epoch >= 1300:
            assert d <= allowance(phase)
            p = prefix(config, x)
            if epoch < 1352:
                prefixes.append(p)
                guards.append(guard)
            else:
                assert p == prefixes[phase] and guard == guards[phase]
            observed[allowance(phase),d] += 1
        config, shift, ticks = result
        if 1300 <= epoch < 1820:
            residual = residual_update(residual, allowance(phase), int(BOUNDARY[phase]))
            assert residual is not None and residual == digits(config[1:], config[0])[sizes[phase+1]:]
        clock += ticks
        head -= shift
    print(min(520, epochs-1300), 'whole residual words matched the full model')
    verify_fence(prefixes[0], guards, sizes)
    print('guard cycle', guards[:13])
    assert guards == guards[:13] * 4
    print('input epochs 1300 through', epochs-1, '; (allowance, actual debt) counts',
          sorted(observed.items()), '; final raw step', clock)
    check_wave()
    check_small_rings()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--epochs', type=int, default=50000)
    args = parser.parse_args()
    if not __debug__ or args.epochs < 1352:
        parser.error('enable assertions and supply at least 1352 epochs')
    main(args.epochs)
