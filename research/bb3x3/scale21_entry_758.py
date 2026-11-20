#!/usr/bin/env python3
"""Transport the ordinary-state entry certificates across the scale-21 band.

The final verifier requires the completed scale-21 basin verifier. Geometry
and physical-return checks alone do not establish that basin dependency.
"""
import argparse
from pathlib import Path

from check_bb33 import champion_step
from dyadic_guard_shadow_758 import GUARDS, guard_counts
from entry_transport_758 import MAX_H, MAX_R, classify_left, inconclusive_bound
from filtered_entry_758 import inverse_cylinder
from target_basin_758 import least_tail_margin, read_tails
from target_shadow_758 import C, D, POWER, horizon
from wider_even_entry_758 import (
    FAR as OLD_FAR, H, MAX_CALLS, MAX_H as RECTANGLE_H, NEAR, TRIM,
    verify as verify_rectangle,
)

HERE = Path(__file__).resolve().parent
FAR = 160_391_744_210_493_965_542
MIN_MASS = H-FAR
MAX_MASS = H-NEAR-TRIM
SHADOW_UPPER = FAR+600
LAST_GUARD = MAX_R+189
TRANSPORT_R = MAX_R-1
TRANSPORT_MAX_H = 2*(MIN_MASS//(2*3**(307-TRANSPORT_R)))


def accepts(h, u):
    """Sufficient entry condition, subject to the verified scale-21 basin."""
    return (isinstance(h, int) and isinstance(u, int)
            and 2 <= h <= MAX_H and not h%2 and not u%2
            and MIN_MASS <= u <= MAX_MASS and classify_left(h).accepted)


def verify_geometry():
    assert FAR == 3*OLD_FAR-8 and MAX_R == 88 and LAST_GUARD == 277
    assert MAX_H == 2*(MIN_MASS//(2*3**219)) == 2*(3**88//(2*D))
    assert RECTANGLE_H == 2*(MIN_MASS//(2*3**247))
    assert 3**219*MAX_H <= MIN_MASS
    assert 2*3**293 > MAX_MASS+2*293
    assert 0 < C < 594*D and NEAR+TRIM > 2*292
    assert horizon(SHADOW_UPPER) == 247
    assert min(3**219,3**58) > D*(FAR+2600)

    # General scale/depth transport: shift every new history depth by one.
    # The old error bound then contains the new one, and 2*p <= depth only
    # becomes weaker. The existing R88 certificate gives the R87 fallback.
    assert horizon(OLD_FAR+600) == 248
    assert FAR+2600 < 3*(OLD_FAR+2600)
    assert TRANSPORT_R == 87
    assert TRANSPORT_MAX_H == 23_157_213_388_888_358_048_127_426_440_224_170
    for depth in range(248,277):
        for _, t in GUARDS:
            new = D*(FAR+2600)//3**(307-depth-t)
            old = D*(OLD_FAR+2600)//3**(307-(depth+1)-t)
            assert new <= old

    margin = least_tail_margin(read_tails(28))
    assert POWER*margin > D*3**89*(FAR+2600)
    # The one longer r60 high-pair tail is an independent exact dependency.
    exception = least_tail_margin({29: {247582280329091635: 198}})
    assert POWER*exception > D*3**61*(FAR+2600)
    assert 61+198 == 259 <= LAST_GUARD
    assert 247+61+198+2 == 508 <= MAX_CALLS
    assert 307+1+243+2 == MAX_CALLS and 9*MAX_CALLS//2 == TRIM


def read_shadow_receipt():
    lines = (HERE/'scale21_entry_guard_758.tsv').read_text().splitlines()
    assert lines[0].split() == ['depth','candidates','possible_cut_ancestors']
    rows = [tuple(map(int,line.split())) for line in lines[1:]]
    assert [row[0] for row in rows] == list(range(248,LAST_GUARD+1))
    assert all(count >= 0 and ancestors == 0 for _,count,ancestors in rows)
    assert rows[-1] == (277,764_815_183_667_524,0)
    # Recount all candidate integer distances independently of reverse paths.
    for depth, candidates, _ in rows:
        count = 0
        for b,t in GUARDS:
            denominator = 3**t
            radius = D*(FAR+2600)//3**(307-depth-t)
            for p in range(1,depth//2+1):
                low = max(1,(b*4**p-radius+denominator-1)//denominator)
                high = min(4**p-1,(b*4**p+radius)//denominator)
                count += max(0,(high-5)//10-(low-6)//10)
        assert count == candidates
    return rows


def physical_return(h,u):
    assert accepts(h,u)
    a,c = 2*h-1,u-h+1
    for calls in range(1,MAX_CALLS+1):
        result = champion_step(a,c)
        assert result is not None
        a,c = result
        if a == 1:
            assert u < c <= u+TRIM and H-FAR <= c <= H-NEAR
            return calls,c
    raise AssertionError('accepted state exceeded its first-return bound')


def boundary_checks():
    lower = MIN_MASS+MIN_MASS%2
    upper = MAX_MASS-MAX_MASS%2
    # Include a mass just outside the former scale-20 band.
    former = H-OLD_FAR-1
    assert former%2 == 0 and lower < former < upper
    masses = (lower,former,upper)
    hs = {2,RECTANGLE_H,RECTANGLE_H+2,MAX_H-2,MAX_H,2*(MAX_H//4),
          2_636_868_592_263_816_134_566}
    a,p,m = inverse_cylinder('P'+'J'*32+'P'*27)
    assert (p,m) == (28,88)
    hs.add(2*((a+4**(p-1))//(2*D)))
    count = 0
    reasons = set()
    for h in sorted(hs):
        decision = classify_left(h)
        if not decision.accepted:
            continue
        reasons.add(decision.reason)
        for u in masses:
            physical_return(h,u)
            count += 1
    assert reasons == {'complete rectangle','ordinary return by the cut','covered dyadic tail'}
    assert not accepts(2,lower-2) and not accepts(2,upper+2)
    assert not accepts(3,lower) and not accepts(2,lower+1)
    print(f'{count} accepted physical replays cover the new lower edge, old boundary and upper edge.')


def verify(replay_shadow=False):
    # This is intentionally a required gate, not an optional assumption.
    from target_gap_21_758 import FAR as BASIN_FAR, NEAR as BASIN_NEAR, verify as verify_basin
    assert (BASIN_FAR,BASIN_NEAR) == (FAR,NEAR)
    verify_basin()
    verify_rectangle()
    verify_geometry()
    rows = read_shadow_receipt()
    if replay_shadow:
        assert list(guard_counts(MAX_R,SHADOW_UPPER,LAST_GUARD)) == rows
    boundary_checks()
    cylinders,bound = inconclusive_bound()
    masses = MAX_MASS//2-(MIN_MASS-1)//2
    assert masses == 80_195_872_105_245_280_000
    rectangle_states = masses*(RECTANGLE_H//2)
    filtered_states = masses*(MAX_H//2-bound)
    assert rectangle_states == 121_768_354_998_108_739_585_604_304_504_361_494_240_000
    assert filtered_states == 2_785_667_018_390_042_971_352_885_981_204_136_291_108_270_980_923_840_000
    print(f'Scale21 physical shadow reaches depth {LAST_GUARD}; '
          f'the last guard has {rows[-1][1]:,} candidate distances and no cut ancestors.')
    print(f'All {rectangle_states:,} states in the full r60 rectangle halt.')
    print(f'The unchanged R88 predicate certifies at least {filtered_states:,} ordinary states; '
          f'{cylinders:,} symbolic cylinders cover at most {bound:,} inconclusive h values.')
    print(f'Every accepted state first returns inside the scale21 halting basin within {MAX_CALLS} calls.')


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run without -O for verification.')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--replay-shadow',action='store_true')
    args = parser.parse_args()
    verify(args.replay_shadow)
