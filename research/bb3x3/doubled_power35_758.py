"""Verify the complete power-35 crossing, its final timed flight and its checkpoint."""
import argparse
from pathlib import Path

from double35_frontier_758 import CUTS, END, TABLE, read_table, verify_gate
from fifth_blank_clock_758 import timed_extension
from power35_inner_skip_758 import direct
from power35_parity_bridges_758 import MERGERS
from power_skip_758 import certify_all_exponents, corridor, skip


POWER = 3**35
SOURCE = 90_056_781_178_199_543
DESTINATION = 2*POWER+155_534
INCOMING_CLOCK = (
    2_638_850_660_075_778_516_888_220_150_868_284_148_565_289_781_271,
    3_951_233_789_304_834_198_184_672_340_620_265_502_586_285_652_949,
)
DURATION = 2_064_800_570_200_302_539_140_344_402_993_658_760_635_001_476_898


def flight(row):
    """Time each of the three consecutive parts of the singleton's trajectory."""
    _, end, low, high, _, _ = row
    assert end == END and low == high == SOURCE
    certify_all_exponents()
    left, _ = corridor(35,2)
    first, n1, t1 = direct(SOURCE,left)
    assert (first,n1,t1) == (90_056_781_178_200_479,12,185_934_390_910_898_828_981_131_948_513_723_836)
    second, n2, t2, evaluations = skip(35,2,first)
    assert (second,n2,evaluations) == (100_063_090_197_998_375,128_286_013_074_332,156)
    last, n3, t3 = direct(second,DESTINATION)
    assert (last,n3,t3) == (DESTINATION,614,24_741_845_703_790_976_128_763_094_172_514_939_194)
    assert n1+n2+n3 == 128_286_013_074_958 and t1+t2+t3 == DURATION
    print(f'{SOURCE:,} reaches {last:,} in {n1+n2+n3:,} first returns and {DURATION:,} raw transitions.')


def clock():
    # The earlier timed merger, the archived grid and the final singleton
    # all lie on the same blank trajectory once every grid row is available.
    start = MERGERS[1807][0]
    assert start == 59_450_686_841_407_190
    lower, upper = timed_extension(start,SOURCE,[(start,END,2*10**12)],INCOMING_CLOCK)
    lower += DURATION
    upper += DURATION
    assert (lower,upper) == (
        11_712_678_510_935_380_362_058_354_962_364_020_304_705_317_061_556,
        15_174_090_093_546_359_518_174_460_234_028_779_946_439_652_299_731,
    )
    print(f'#758 raw clock at the doubled power in [{lower:,}, {upper:,}].')
    print(f'#153 raw clock at the doubled power in [{lower-50_707:,}, {upper-50_707:,}].')
    return lower,upper


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--table',type=Path,default=TABLE)
    parser.add_argument('--gate-only',action='store_true',help='check the singleton flight independently of the preceding grid')
    parser.add_argument('--clock',action='store_true',help='bound raw time from blank through the complete grid and gate')
    args = parser.parse_args()
    if not __debug__ or (args.gate_only and args.clock):
        parser.error('enable assertions and use the full grid when requesting the blank clock')
    rows = read_table(args.table)
    last = len(CUTS)-2
    if last not in rows:
        parser.error('missing final grid row')
    if not args.gate_only and len(rows) != last+1:
        parser.error(f'the blank connection requires all {last+1:,} validated rows')
    verify_gate()
    flight(rows[last])
    if not args.gate_only:
        print(f'All {len(rows):,} consecutive grid rows connect blank to reset {DESTINATION:,}.')
    if args.clock:
        clock()


if __name__ == '__main__':
    main()
