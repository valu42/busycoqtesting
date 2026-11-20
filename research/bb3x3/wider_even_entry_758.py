#!/usr/bin/env python3
"""Certify the full even-coordinate halting rectangle through exponent 60."""
import argparse
from itertools import combinations
from fractions import Fraction
from math import comb
from pathlib import Path
import subprocess
import re

from scale_clauses_758 import H
from target_basin_758 import GATES_NEW, NEAR, least_tail_margin, read_tails
from target_shadow_758 import D, POWER
from check_bb33 import champion_step
from target_bridge_even_758 import verify as verify_threefold_rectangle

HERE = Path(__file__).resolve().parent
FAR = GATES_NEW[20][1]
PREVIOUS_MAX_H = 2*((H-FAR)//3**248//2)
MAX_H = 2*((H-FAR)//3**247//2)
MAX_CALLS = 553
TRIM = 2488
EXPECTED = {
    (58,29): (248,29,106681061641,544570092,15026,0),
    (59,29): (248,435,1696573012589,8660417440,239568,0),
    (59,30): (248,1,13765298277,70266916,2000,0),
}
EXPECTED_R60 = {
    (60,29): (249,4495,18462706313573,94245716148,2603736,1),
    (60,30): (249,30,440489544851,2248547630,62404,0),
}


def accepts(h,u):
    """Sufficient criterion in odd/odd coordinates, including their parity."""
    return (isinstance(h,int) and isinstance(u,int)
            and h%2==0 and u%2==0 and 2<=h<=MAX_H
            and H-FAR<=u<=H-NEAR-TRIM)


def headers(r,p):
    """Generate the two complete-cut types using combinations of pair slots."""
    for m in (r,r+1):
        blocks=m-p
        fixed={0} if m==r else {0,blocks-1}
        remaining=p-len(fixed)
        available=[i for i in range(blocks) if i not in fixed]
        if not 0<=remaining<=len(available):
            continue
        for chosen in combinations(available,remaining):
            pair_slots=fixed|set(chosen)
            a=0
            four=1
            for i in range(blocks):
                if i in pair_slots:
                    a=9*a+5*four
                    four*=4
                else:
                    a*=3
            assert four==4**p and a%10==5
            yield m,a


def verify(worker=None):
    verify_threefold_rectangle()
    assert PREVIOUS_MAX_H==1_012_257_878_130_399_645_022
    assert MAX_H==3_036_773_634_391_198_935_066
    assert MAX_H==2*(3**60//(2*D))
    assert 3**247*MAX_H<=H-FAR
    assert 2*3**293>H-NEAR-TRIM+2*293
    assert 3**57>D*(FAR+2600)
    # At depth 249 the pulled-back error is <1 at guards 0,1/3,1.
    # At 5/9 it is <3, while 9*N-5*4^p is a nonzero multiple of five.
    assert D*(FAR+2600)<3**57<5*3**56
    assert 61+188==249
    clearance=POWER*least_tail_margin(read_tails(28))/(D*3**61)
    assert clearance>FAR+2600
    assert 307+1+243+2==MAX_CALLS
    assert 9*MAX_CALLS//2==TRIM
    receipt=(HERE/'wider_even_lattice_758.tsv').read_text()
    rows=receipt.splitlines()
    assert rows[0].split()==['r','p','last_guard','cells','eligible','atlas_tests','exact_fallbacks','survivors']
    observed={}
    for row in rows[1:]:
        r,p,*values=map(int,row.split())
        assert (r,p) not in observed
        observed[r,p]=tuple(values)
    assert observed==EXPECTED
    receipt60=(HERE/'wider_even_r60_758.txt').read_text()
    rows60=receipt60.splitlines()
    match=re.fullmatch(r'surviving r=(\d+) m=(\d+) p=(\d+) N=(\d+) A=(\d+)',rows60[0])
    assert match
    r,m,p,n,a=map(int,match.groups())
    assert (r,m,p,n,a)==(60,61,29,247582280329091635,110426321454572863635202307315)
    exception=(m,n,a)
    assert rows60[1]==rows[0]
    observed60={}
    for row in rows60[2:]:
        rr,pp,*values=map(int,row.split())
        assert (rr,pp) not in observed60
        observed60[rr,pp]=tuple(values)
    assert observed60==EXPECTED_R60
    observed.update(observed60)
    total_cells=total_eligible=0
    for (r,p),(guard,cells,eligible,tests,exact,survivors) in observed.items():
        assert guard==(249 if r==60 else 248) and 0<=exact<=tests<=eligible
        assert survivors==int((r,p)==(60,29))
        census=list(headers(r,p))
        assert len(census)==cells==comb(r-p-1,p-1)+comb(r-p-1,p-2)
        independent=0
        for m,a in census:
            step=2*3**(m-r)*D
            first=(-a)%step
            assert first%10==5 and step%10==0 and 0<first<4**p
            independent+=(4**p-1-first)//step+1
        assert independent==eligible
        total_cells+=cells
        total_eligible+=eligible
    assert total_cells==4990
    verify_exception(*exception)
    if worker:
        actual=subprocess.check_output([str(worker.resolve()),'58','59','21','3'],text=True)
        assert actual==receipt
        replay=subprocess.run([str(worker.resolve()),'60','60','21','3','249'],capture_output=True,text=True)
        # The worker reports its one angular-budget survivor. The exact
        # guard-clearance proof in verify_exception settles that survivor.
        assert replay.returncode==1 and replay.stdout==receipt60
    masses=(H-NEAR-TRIM)//2-(H-FAR-1)//2
    states=masses*(MAX_H//2)
    print(f'All {total_cells:,} high-pair cylinders return, including the one resolved long-tail direction.')
    print(f'Exhaustion covers {total_eligible:,} admissible cut directions.')
    print(f'Every even h from 2 through {MAX_H:,} returns inside the halting basin within {MAX_CALLS} calls.')
    print(f'The full rectangle contains {states:,} ordinary states.')
    print(f'Listed lower-pair tails have at least {int(clearance):,} units of guard clearance.')
    if not worker:
        print('Using the archived exhaustive receipt; supply --worker to replay the new enumeration.')


def verify_exception(m,n,a):
    assert (m,a) in set(headers(60,29))
    h,remainder=divmod(a+n,3*D)
    assert remainder==0 and h==2_636_868_592_263_816_134_566 and h%2==0
    assert PREVIOUS_MAX_H<h<=MAX_H
    numerator,denominator,triple=n,4**29,1
    minimum=None
    depth=0
    while True:
        gap=min(9*numerator,3*abs(3*numerator-denominator),
                abs(9*numerator-5*denominator),9*(denominator-numerator))
        assert gap>0
        margin=Fraction(gap,9*triple)
        minimum=margin if minimum is None else min(minimum,margin)
        if 3*numerator<denominator:
            numerator*=3
            triple*=3
            depth+=1
        elif 9*numerator>5*denominator:
            numerator=9*numerator-5*denominator
            denominator*=4
            triple*=9
            depth+=2
        else:
            break
        assert depth<=198
    assert depth==198 and m+depth==259
    clearance=POWER*minimum/(D*3**m)
    assert clearance>FAR+2600
    assert int(clearance)==61235985398907584064538050938048966624970639166467664617671756155191780499747733
    assert 247+m+depth+2==508<=MAX_CALLS
    # These independent physical replays check both mass edges. The
    # exact guard margin above proves every intermediate mass uniformly.
    lower=H-FAR
    lower+=lower%2
    upper=H-NEAR-TRIM
    upper-=upper%2
    for u in (lower,upper):
        left,right=2*h-1,u-h+1
        for call in range(1,MAX_CALLS+1):
            result=champion_step(left,right)
            assert result is not None
            left,right=result
            if left==1:
                assert call==508 and H-FAR<=right<=H-NEAR
                break
        else:
            raise AssertionError('exception did not return')


if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Run without -O for verification.')
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--worker',type=Path)
    args=parser.parse_args()
    verify(args.worker)
