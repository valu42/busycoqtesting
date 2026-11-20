#!/usr/bin/env python3
"""Verify the scale-21 enlargement of the contiguous halting basin."""
import argparse
from fractions import Fraction
from math import comb
from pathlib import Path
import re
import subprocess
import sys

from check_bb33 import champion_step
from dyadic_guard_shadow_758 import guard_counts
from scale_clauses_758 import H, PREFIX, EVEN_WORD, check_word
from scale_transport_758 import PERIOD, SLOPE, prefix
from target_basin_758 import (
    GATES_NEW, NEAR, high_receipts, least_tail_margin, read_tails,
)
from target_shadow_758 import D, POWER, aligned, horizon

HERE = Path(__file__).resolve().parent
OLD_FAR = GATES_NEW[20][1]
NEAR_GATE = 96_235_046_526_296_379_328
FAR = 160_391_744_210_493_965_542
RECENT_RESET = 35_642_609_824_553_458_330
HEADER = (
    "r p last_guard groups directory_bits filter_bits first stop cells "
    "probes atlas_tests image_tests exact_fallbacks survivors"
).split()
EXTRA_GUARDS = [(249, 0, 0), (250, 103, 0), (251, 165, 0), (252, 583, 0)]
EXCEPTIONS = {
    29: (63, 63, 29, 188_136_122_924_663_855,
         1_144_541_009_596_807_477_707_782_023_595),
    30: (63, 64, 30, 777_865_017_584_130_175,
         3_343_848_190_836_621_005_949_279_610_625),
}
EXCEPTION_LENGTHS = {29: 186, 30: 195}
EXCEPTION_CLEARANCES = {
    29: 962_784_278_959_391_660_117_995_150_222_859_267_856_847_373_207_217_987_776_355_610_388_319_041_489,
    30: 11_292_473_431_637_801_390_039_388_297_349_820_517_250_589_757_212_092_534_102_149_802_929_981_073_132,
}
EXCEPTION_ORIGINS = {
    29: [(96_233_342_737_222_047_692, 802, 1899),
         (96_233_342_737_222_047_694, 802, 1901)],
    30: [(93_717_244_529_141_180_700, 812, 1938),
         (93_717_244_529_141_180_702, 812, 1940)],
}
EXPECTED_TOTALS = {
    29: (1_344_904, 11_016_108_664, 180_089_868_609, 7_878_071_241, 4_974_393, 1),
    30: (40_920, 1_340_818_856, 12_175_754_416, 532_630_042, 335_919, 1),
}


def read_chunks(p, text=None):
    """Require a complete, disjoint partition of all r=63, p-pair headers."""
    if text is None:
        text = (HERE / f"target_gap_atlas_p{p}_758.tsv").read_text()
    lines = text.splitlines()
    assert lines and lines[0].split() == HEADER
    rows, exceptions = [], []
    for line in lines[1:]:
        if line.startswith("surviving "):
            match = re.fullmatch(r"surviving r=(\d+) m=(\d+) p=(\d+) N=(\d+) A=(\d+)", line)
            assert match is not None
            exceptions.append(tuple(map(int, match.groups())))
        else:
            rows.append(tuple(map(int, line.split())))
    assert exceptions == [EXCEPTIONS[p]]
    assert all(len(row) == len(HEADER) for row in rows)
    rows.sort(key=lambda row: row[6])
    next_index = 0
    totals = [0] * 6
    for row in rows:
        r, pairs, guard, groups, bits, filter_bits, first, stop, *counts = row
        cells, probes, tests, images, exact, survivors = counts
        assert (r, pairs, guard, groups, bits, filter_bits) == (
            63, p, 248, 12 if p == 29 else 14, 20, 20
        )
        assert first == next_index and first < stop <= first + 4096
        assert cells == stop - first
        assert 0 <= survivors <= exact <= images <= tests
        assert probes > 0 and images > 0
        next_index = stop
        totals = [x + y for x, y in zip(totals, counts)]
    expected_cells = comb(63-p-1, p-1) + comb(63-p-1, p-2)
    assert next_index == totals[0] == expected_cells
    assert totals[-1] == len(exceptions) == 1
    assert tuple(totals) == EXPECTED_TOTALS[p]
    return rows, tuple(totals)


def verify_residues():
    residues, starts = set(), []
    assert PERIOD == 32768 and SLOPE == 4*D
    for distance in range(0, PERIOD, 2):
        twice_h, gain = prefix(distance)
        shifted, shifted_gain = prefix(distance+PERIOD)
        assert shifted-twice_h == 4*D and gain == shifted_gain
        assert twice_h % 4 == 0
        residues.add((twice_h//2) % (2*D))
        starts.append((distance, twice_h//2))
    assert len(residues) == 8192
    return starts


def verify_exception(p, starts):
    r, m, pairs, numerator, origin = EXCEPTIONS[p]
    assert r == 63 and m in (r, r+1) and pairs == p
    assert 0 < numerator < 4**p and numerator % 10 == 5

    # Independently decode the alleged angular header backwards. The final
    # letter is determined by its residue modulo three.
    a, depth, pair_count, reversed_word = origin, m, p, []
    while depth:
        if a % 3 == 0:
            a //= 3
            depth -= 1
            reversed_word.append("J")
        else:
            assert pair_count > 0 and depth >= 2
            a -= 5*4**(pair_count-1)
            assert a >= 0 and a % 9 == 0
            a //= 9
            depth -= 2
            pair_count -= 1
            reversed_word.append("P")
    word = reversed_word[::-1]
    assert a == pair_count == 0 and word[0] == "P"
    assert m-(1 if word[-1] == "J" else 2) < r

    a, b, triple, elapsed, minimum = numerator, 4**p, 1, 0, None
    while True:
        gap = min(9*a, 3*abs(3*a-b), abs(9*a-5*b), 9*(b-a))
        assert gap > 0
        margin = Fraction(gap, 9*triple)
        minimum = margin if minimum is None else min(minimum, margin)
        if 3*a < b:
            a, triple, elapsed = 3*a, 3*triple, elapsed+1
        elif 9*a > 5*b:
            a, b, triple, elapsed = 9*a-5*b, 4*b, 9*triple, elapsed+2
        else:
            break
        assert elapsed <= 243
    assert elapsed == EXCEPTION_LENGTHS[p]
    clearance = POWER*minimum/(D*3**m)
    assert clearance > NEAR_GATE+2000
    assert int(clearance) == EXCEPTION_CLEARANCES[p]

    divisor = 3**(m-r)*D
    h0, remainder = divmod(numerator+origin, divisor)
    assert remainder == 0 and h0 > 0 and h0 % 2 == 0
    distances = []
    for residue, base_h in starts:
        quotient, remainder = divmod(h0-base_h, 2*D)
        if remainder == 0:
            distances.append(residue+PERIOD*quotient)
    assert sorted(distances) == [d for d, _, _ in EXCEPTION_ORIGINS[p]]
    for distance, calls, gain in EXCEPTION_ORIGINS[p]:
        assert OLD_FAR < distance < NEAR_GATE
        seed = H-distance
        a, c = 1, seed
        for used in range(1, 861):
            a, c = champion_step(a, c)
            if a == 1:
                break
        else:
            raise AssertionError("exception did not return in the certified bound")
        assert (used, c-seed) == (calls, gain)
        assert calls == len(PREFIX)+(307-r)+m+elapsed+2
        assert H-FAR <= c <= H-NEAR
    return elapsed, int(clearance)


def verify(*, worker=None, threads=1, inherit=True):
    if inherit:
        # Keep the inherited proof at its explicit scale even if its default
        # is enlarged in a later change. This is the archived scale-20 proof.
        subprocess.run(
            [sys.executable, str(HERE / "target_basin_758.py"), "--scale", "20"],
            check=True, stdout=subprocess.PIPE, text=True,
        )
    assert FAR == 3*OLD_FAR-8
    assert NEAR_GATE == 3*GATES_NEW[20][0]+4
    word = PREFIX + "J"*(264-21) + "LR"
    for distance in (NEAR_GATE, FAR):
        assert 0 < check_word(H-distance, word) < 4000
    for distance in (NEAR_GATE-2, FAR+2):
        try:
            check_word(H-distance, word)
        except AssertionError:
            pass
        else:
            raise AssertionError("the claimed corridor endpoint is not sharp")
    for distance in (OLD_FAR+2, NEAR_GATE-2):
        check_word(H-distance, PREFIX)
        assert 307-aligned(distance)[2] == 63
    for distance in (OLD_FAR+1, FAR-1):
        assert 0 < check_word(H-distance, EVEN_WORD) < 4000
    assert horizon(NEAR_GATE-2) == 248
    assert list(guard_counts(63, NEAR_GATE-2, 252)) == EXTRA_GUARDS
    assert all(ancestors == 0 for _, _, ancestors in EXTRA_GUARDS)

    # The old p<=28 exhaustion and its complete exceptional-tail ledger are
    # inherited. The larger cut only divides its aligned clearance by three.
    margin = least_tail_margin(read_tails(28))
    clearance = POWER*margin/(D*3**64)
    assert clearance > NEAR_GATE+2000
    assert int(clearance) == 79_762_309_749_986_306_880_633_296_187_060_457_963_034_068_453_186_124_314_406_566
    starts = verify_residues()

    totals = {}
    for p in (29, 30):
        expected, totals[p] = read_chunks(p)
        verify_exception(p, starts)
        if worker is not None:
            cells = totals[p][0]
            command = [str(Path(worker).resolve()), "63", str(p), str(threads),
                       "0", str(cells), str(12 if p == 29 else 14), "20"]
            result = subprocess.run(command, text=True, stdout=subprocess.PIPE)
            assert result.returncode == 1, (
                f"p={p}: worker exited {result.returncode}; expected status 1 for "
                "the one separately verified budget survivor"
            )
            assert read_chunks(p, result.stdout) == (expected, totals[p])
    inherited = high_receipts()
    for p in (31, 32):
        guard, cells, *_rest, survivors = inherited[63, p]
        assert guard == 248 and survivors == 0
        assert cells == comb(63-p-1, p-1) + comb(63-p-1, p-2)

    # Every ordinary gap excursion finishes in at most 860 counter calls;
    # the fixed-word corridors take fewer. W grows by at most nine per call.
    calls = len(PREFIX) + (307-63) + 64 + 243 + 2
    assert calls == 860 and 9*calls < 2*4000
    assert OLD_FAR-NEAR > 4000
    assert RECENT_RESET == (2*(FAR-NEAR)+2)//9
    assert 9*RECENT_RESET < 2*(FAR-NEAR)+3
    return {
        "far": FAR,
        "seeds": FAR-NEAR+1,
        "new_seeds": FAR-OLD_FAR,
        "calls": calls,
        "recent_reset": RECENT_RESET,
        "long_tail_clearance": int(clearance),
        "headers": totals,
    }


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run without -O to enable verification.")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--worker", type=Path, help="rerun the complete new header exhaustion")
    parser.add_argument("--threads", type=int, default=1, choices=range(1, 10))
    args = parser.parse_args()
    result = verify(worker=args.worker, threads=args.threads)
    for p, totals in result["headers"].items():
        print(f"p={p}: cells, probes, atlas tests, image tests, exact fallbacks, budget survivors = {totals}")
        print(f"The one budget survivor returns after {EXCEPTION_LENGTHS[p]} tail calls and passes exact physical clearance and origin checks.")
    print(f"All {result['seeds']:,} reset seeds with {NEAR:,} <= H-s <= {FAR:,} halt.")
    print(f"The enlargement adds {result['new_seeds']:,} seeds; every new gap return takes at most {result['calls']} counter calls.")
    print(f"A reset within {result['recent_reset']:,} calls before the upper mass crossing is sufficient.")
