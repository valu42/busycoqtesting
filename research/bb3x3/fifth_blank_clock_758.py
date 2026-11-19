"""Clock bounds conditional on the two crossing chains to the fifth candidate."""
from after_fourth_758 import CHECKPOINT as FOURTH
from crossing_clock_758 import DENOMINATOR, REACH, potential_numerator, segment_bounds
from fifth_crossing_758 import B, CUT, K
from fourth_clock_758 import timed_return
from power_gates_758 import coarse_return
from survey_next_power_758 import END as GATE_START

POWER = 3**34
GATE_CUT = 2*POWER - 2*34 - 6
DOUBLE = 2*POWER + 32_211
MERGER = K - 198_990
# crossing_clock_758.verify() independently checks these exact bounds.
FOURTH_CLOCK = (
    75_287_784_527_483_315_086_258_653_649_976_784_825_150_292_446,
    111_828_955_391_337_651_168_241_433_086_744_445_106_293_997_533,
)


def timed_extension(start, end, intervals, previous):
    lower, upper = previous
    upper += (potential_numerator(end) - potential_numerator(start)) // DENOMINATOR
    prev_end = start
    for a, b, stride in intervals:
        assert prev_end <= a < b <= end
        covered = 0
        for lo in range(a, b, stride):
            credit, saving, width = segment_bounds(lo, min(lo+stride, b), 8)
            lower += credit
            upper -= saving
            covered += width
        print(f'{a}..{b}: common words cover {covered:,} of {b-a:,}.', flush=True)
        prev_end = b
    return lower, upper


def verify():
    assert REACH == 100_000
    assert GATE_START < GATE_CUT < DOUBLE
    for p in (0, 1):
        for s in (GATE_START+(p-GATE_START)%2, GATE_CUT-(GATE_CUT-p)%2):
            assert 0 < coarse_return(34, s, 2)-s <= 77
    double_clock = timed_extension(FOURTH, DOUBLE, [
        (FOURTH, GATE_START, 2*10**12),
        (GATE_START, GATE_CUT, 2*10**12),
    ], FOURTH_CLOCK)
    assert double_clock == (
        436_590_138_305_704_593_768_270_142_045_164_683_395_939_731_420,
        591_416_369_869_847_300_273_717_980_051_936_619_126_590_565_585,
    )
    print('Doubled power:', *double_clock, flush=True)
    fifth_clock = timed_extension(DOUBLE, MERGER, [
        (DOUBLE, B, 2*10**12),
        (B, CUT, 2*10**12),
        (CUT, K-199_000, 2*10**12),
    ], double_clock)
    # The local certificate fixes this exact reset, ten above the final cut.
    seed = MERGER
    suffix = 0
    for i in range(1054):
        if i == 1053:
            assert seed == K-98
        seed, elapsed = timed_return(seed)
        suffix += elapsed
    assert seed == K+118
    assert elapsed == 21_237_958_453_334_090_217_030_746_043_349_705
    assert suffix == 20_265_035_542_707_572_423_545_951_432_277_768_588
    fifth_clock = tuple(t+suffix for t in fifth_clock)
    assert fifth_clock == (
        780_097_594_928_235_085_876_608_753_788_495_923_896_535_100_790,
        1_087_329_834_257_228_132_394_519_759_902_747_657_856_948_305_426,
    )
    print('Exact merger-to-crossing duration:', suffix)
    print('First reset after fifth pair:', *fifth_clock, flush=True)
    return double_clock, fifth_clock


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Enable assertions to verify the bounds.')
    verify()
