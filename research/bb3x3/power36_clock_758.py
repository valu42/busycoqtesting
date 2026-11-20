#!/usr/bin/env python3
"""Bound the raw clocks at the fully connected power-36 blank checkpoint."""
import argparse

from crossing_clock_758 import DENOMINATOR, REACH, certify_potential
from doubled_power35_758 import clock as previous_clock
from fifth_blank_clock_758 import timed_extension
from power36_final_758 import START, GATE, TARGET, verify as verify_bridge
from power_gates_758 import coarse_return


# Independently reproduced by doubled_power35_758.clock().
PREVIOUS = (
    11_712_678_510_935_380_362_058_354_962_364_020_304_705_317_061_556,
    15_174_090_093_546_359_518_174_460_234_028_779_946_439_652_299_731,
)
EXPECTED = (
    39_169_625_267_626_016_222_638_085_861_124_527_996_579_493_163_120,
    52_818_905_771_297_598_690_448_450_091_510_656_735_026_479_051_906,
)
ENCODING_OFFSET = 50_707
GATE_CUT = 3**36-2*36-4


def verify(replay_previous=False):
    # A timing estimate conditional on an unconnected grid is not a blank
    # theorem.  Complete receipt and gate verification comes first.
    assert verify_bridge() == TARGET
    assert START == 2*3**35+155_534
    assert TARGET == 3**36+112_032
    assert START < GATE < GATE_CUT < TARGET
    assert REACH == 100_000 and DENOMINATOR == 1058
    # The unchanged worker allows at most 256 packed groups and 5,000
    # subsequent groups, each costing at most two counter calls.  Forty
    # calls enclose either launch or odd normalization.  The symbolic
    # range worker instead permits at most 10,000 subsequent calls.
    packed_calls = 40+2*(256+5000)+40
    symbolic_calls = 40+10_000+40
    assert 9*max(packed_calls, symbolic_calls)//2 < REACH
    for parity, cap in ((0, 101), (1, 77)):
        for seed in (GATE+(parity-GATE)%2,
                     GATE_CUT-(GATE_CUT-parity)%2):
            gain = coarse_return(36, seed, 1)-seed
            assert 0 < gain <= cap < REACH and gain%2 == 1
    certify_potential()
    if replay_previous:
        assert previous_clock() == PREVIOUS
    lower, upper = timed_extension(START, TARGET, [
        (START, GATE, 10**13),
        (GATE, GATE_CUT, 10**13),
    ], PREVIOUS)
    assert (lower, upper) == EXPECTED
    assert lower-ENCODING_OFFSET > 39_169_625_267*10**39
    assert upper < 52_818_905_772*10**39
    print(f'#758 raw clock at A(1,{TARGET:,}) lies in [{lower:,}, {upper:,}].')
    print(f'#153 raw clock lies in [{lower-ENCODING_OFFSET:,}, '
          f'{upper-ENCODING_OFFSET:,}].')
    return lower, upper


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run without -O for verification.')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--replay-previous', action='store_true',
                        help='also recompute the incoming doubled-power clock')
    args = parser.parse_args()
    verify(args.replay_previous)
