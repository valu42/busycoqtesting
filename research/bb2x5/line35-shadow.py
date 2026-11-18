"""A nonblank line-35 tape shadows 888 guard observations, then reaches B4."""
import argparse

from line35_timed import sweep, unpack
from prior_sweeps import TapeMachine, TERNARY_CLOSE, word_sweep

BLOCK = '12323112321132311123213121323112111311211311213'
COPIES = 1358


def encode_large(word):
    return (len(word), *(int(bytes(49 if x == d else 48 for x in word), 2)
                         for d in (1, 2)))


def main(literal):
    blank_word = []
    for _ in range(400):
        blank_word, _ = word_sweep(blank_word, TERNARY_CLOSE)
    planted = blank_word + list(map(int, BLOCK)) * COPIES + [2]
    true = encode_large(blank_word)
    altered = encode_large(planted)
    raw_time = 0
    head = 0
    for epoch in range(400, 1288):
        true, _, d, _, cut8 = sweep(*true)
        altered, dt, alt_d, _, alt_cut8 = sweep(*altered)
        assert true is not None and altered is not None
        assert (d, cut8) == (alt_d, alt_cut8)
        raw_time += dt
        head -= 1 if d <= 2 else 4
    assert raw_time == 196821912
    _, _, true_guard, _, true_cut8 = sweep(*true)
    dest, _, guard, _, cut8 = sweep(*altered)
    assert dest is None and guard == 6 and true_guard < 6
    print('888 matching guard and cut-8 readings; genuine and altered at 1288:',
          (true_guard, true_cut8), (guard, cut8))
    if literal:
        machine = TapeMachine(TERNARY_CLOSE, planted, left=1)
        expected = 282627758
    else:
        machine = TapeMachine(TERNARY_CLOSE, unpack(*altered), head=head, left=head+1)
        expected = 282627758 - raw_time
    while machine.steps <= expected and machine.step():
        pass
    assert machine.steps == expected and machine.head == -920
    assert machine.state == 'B' and machine.tape[machine.head] == 4
    print('altered halt at B4, head -920, after 282627758 defined steps')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--literal', action='store_true',
                        help='replay all steps from the planted word using the literal interpreter')
    if not __debug__:
        parser.error('assertions must be enabled')
    main(parser.parse_args().literal)
