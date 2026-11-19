"""Verify the repeating fourth-candidate terminal and its uniform missed interval."""
from fractions import Fraction as F
from check_bb33 import champion_step, first_return
from terminal_forest_758 import exhaust

BASE = 3**34
ALPHA = F(1043,1000)
BETA = F(5219,5000)
RIGHT = F(104517,100000)


def terminal(m):
    p = 3**m
    numerator = 162*p-1528
    assert numerator%155 == 0
    seed = numerator//155-2*m
    a,c = 4*(p//3)-1,seed-2*(p//3)+2*m+3
    assert c>0 and c%4==3
    assert champion_step(a,c) == champion_step(a,c+2)
    for b in 'CCJB':
        if b == 'J':
            assert a%2 and a<=c
        else:
            assert c%4 == (3 if b=='C' else 1) and a >= 4*((c+1)//4)+3
        a,c=champion_step(a,c)
        assert a!=1
    assert a==c+1 and champion_step(a,c) is None
    return seed,(a,c)


def uniform_guards(odd, lo, hi):
    # omitting bounded branch constants leaves homogeneous affine counters in
    # z/P = (s+2m)/P. Check both endpoints of this real interval for every guard.
    word = 'LLLLLLL' if odd else 'LLJLLJJJL'
    for z in (lo,hi):
        a,c=(F(2),z-1) if odd else (F(4,3),z-F(2,3))
        error=3
        for branch in word+'R':
            assert min(a,c)*BASE > error+2
            gap = a-c if branch=='L' else c-a
            assert gap*BASE > 2*error+5
            if branch=='L':
                a,c=a-c,3*c/2
            elif branch=='J':
                a,c=3*a,c-a
            error=3*error+7


def verify():
    assert pow(3,60,155*16)==1
    # Coefficients of q in the actual fine-word inputs. The constants do
    # not depend on m after substituting the expression for the seed.
    a,c=F(4),F(486,155)-2
    for b in 'CCJB':
        assert min(a,c)>0
        assert (a-c>0) if b!='J' else (c-a>0)
        if b=='J':
            a,c=3*a,c-a
        else:
            a,c=a-c,3*c/2
    assert a==c==F(324,155)
    assert terminal(34)[0]==17_430_344_744_167_562
    uniform_guards(False,ALPHA,BETA)
    uniform_guards(True,ALPHA,RIGHT)
    assert BETA < F(162,155) < RIGHT
    # The even first-return gain is at most 2m+35. At m=34 the room below
    # the candidate already exceeds it. Tripling P grows more than required.
    assert (F(162,155)-BETA)*BASE > 2*34+35+F(1528,155)+2
    # Complete last-reset ancestry for the five family members below H.
    expected=((255,43),(851,109),(1375,159),(1907,233),(2713,288))
    for j in range(5):
        m=34+60*j
        seed, target = terminal(m)
        resets,nodes,longest = exhaust(target,1_000_000)
        assert resets == {seed:m+4,seed+2:m+4}
        assert (nodes,longest)==expected[j]
        print(f"m={m}: exactly two last resets, {nodes:,} inverse states, depth {longest}")

    # A last-reset tree stops when a=1. Older reset ancestors can exist.
    family_seed = terminal(154)[0]
    for distance in (662,664):
        assert first_return(family_seed-distance, batch=False) == family_seed


if __name__=='__main__':
    if not __debug__:
        raise SystemExit("Run without -O to enable the checks.")
    verify()
