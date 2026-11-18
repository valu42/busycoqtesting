"""Check phase slips on blank and perturbations of the cut-100 proof hypotheses."""
from collections import deque
import json

from cut100 import CUT, HERE, SEED, WIDTHS, allowance, first_digits
from line34_left import digits
from prior_sweeps import TapeMachine, direct_epoch
from target34_orbit import TERNARY, analyze, encode


def compare_blank():
    """Compare two genuine blank tapes at an offset of eleven 52-sweep cycles."""
    run = json.loads((HERE / 'cut100-250000.json').read_text())
    assert run['machine'] == TERNARY and run['end_epoch'] == 250000
    pulses = set(run['pulse_epochs'])
    disagreements = [(t, t in pulses) for t in range(8000, 250000)
                     if (t in pulses) != (t-572 in pulses)]
    early = [t for t, actual in disagreements if actual]
    late = [t for t, actual in disagreements if not actual]
    assert early == [13138, 21510, 32742, 39398, 221658, 247762]
    assert late == [t+52 for t in early]
    print('572-sweep pulse forecast advances by 52 at:', early)
    assert 221658 - 39451 == 182207
    print('Consecutive correct holdout forecasts between the fourth and fifth slips:', 182207)

    history = deque()
    config = (SEED['width'], int(SEED['open_hex'],16), int(SEED['closing_hex'],16))
    clock = SEED['raw_steps']
    for t in range(1300, 13139):
        out, _, (d,), _ = analyze(config, (100,))
        assert out is not None
        if len(history) == 572:
            other, old_clock, old_d = history.popleft()
            if t in (12395, 13138):
                n, o, c = config
                m, a, b = other
                length = min(n, m)
                different = ((o >> (n-length)) ^ (a >> (m-length))) | ((c >> (n-length)) ^ (b >> (m-length)))
                common = length - different.bit_length()
                if t == 12395:
                    assert (old_clock, clock, common) == (303317491, 333379833, 201)
                else:
                    assert (old_d, d, common) == (1, 2, 89)
                print(f'Blank epochs {t-572}, {t}: common prefix {common}, cut-100 inputs {old_d}, {d}.')
        history.append((config, clock, d))
        config, _, ticks = out
        clock += ticks


def changed_tape():
    """A single cell substitution at a real seed makes both proposed conditions fail."""
    seed_word = list(first_digits(SEED['width']))
    assert seed_word[CUT] == 1
    seed_word[CUT] = 2
    tape = TapeMachine(TERNARY, seed_word, head=SEED['head'], left=SEED['head']+1)
    config = encode(seed_word)
    head = SEED['head']
    elapsed = 0
    pulses = []
    for t in range(1300, 1314):
        phase = t % 52
        out, g, (inner, d100), _ = analyze(config, (WIDTHS[phase], CUT))
        assert out is not None and inner <= allowance(phase)
        assert g == (0 if phase % 13 == 0 else 2 if phase % 13 == 12 else 1)
        if d100 >= 2:
            n,o,c = config
            first = digits((o >> (n-103), c >> (n-103)), 3)
            assert d100 == 2
            pulses.append((t, ''.join(map(str,first)), elapsed))
        successor, shift, ticks = out
        raw_word = direct_epoch(tape, (1,2,3))
        head -= shift
        elapsed += ticks
        assert raw_word is not None and tape.state == 'A'
        assert tape.steps == elapsed and tape.head == head and encode(raw_word) == successor
        assert tape.tape == {head+1+i:v for i,v in enumerate(raw_word)}
        config = successor
    assert [v[0] for v in pulses] == [1309,1313] and pulses[0][1] != '323'
    print('Changed 101st digit 1 to 2 at epoch 1300. Pulses (epoch, first three digits, elapsed raw steps):', pulses)
    print('All 14 altered sweeps agree with literal tape and raw clock through:', elapsed)


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('enable assertions')
    compare_blank()
    changed_tape()
