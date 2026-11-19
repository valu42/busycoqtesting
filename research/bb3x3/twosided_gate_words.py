"""Check the number-theoretic parameters of the scale-74 two-sided construction."""
from random import Random
from check_bb33 import HALTING_TARGET as H, champion_step
from scale_clauses_758 import BASE


T = H-5*(BASE*3**74)//4
PAST, FUTURE = 48,49


def witness(motifs):
    start = T-7*PAST
    finish = T+7*FUTURE
    word = "".join("BJ" if m == 0 else "JB" for m in motifs)
    # At any backwards stage d=(A*terminal+C)/D.
    a,c,den,u = 1,0,1,finish
    for letter in reversed(word):
        if letter == "J":
            u -= 2
            c += (u-1)*den
            den *= 3
        else:
            u -= 5
            a,c,den = 4*a,4*c-20*den,9*den
    assert u == start and den == 27**(PAST+FUTURE)
    low = (finish+15)//16
    final = low+(-c*pow(a,-1,den)-low)%den
    assert final <= 7*finish//16
    d,rem = divmod(a*final+c,den)
    assert rem == 0
    cut = None
    for i,letter in enumerate(word):
        if i == 2*PAST:
            assert u == T
            cut = d
        state = (2*u-4*d-1,2*d+1)
        assert state[0] > 1 and state[1] > 0
        if letter=="J":
            assert 3*d >= u-1 and 2*d <= u-1
            state = champion_step(*state)
            u,d = u+2,3*d-u+1
        else:
            assert d%4 == 0 and 9*d <= 2*u-12
            middle = champion_step(*state)
            assert middle[0] > middle[1]+1 and middle[1]%4 == 1
            state = champion_step(*middle)
            u,d = u+5,(9*d+20)//4
        assert state == (2*u-4*d-1,2*d+1)
    assert d == final and cut is not None
    return cut


def audit():
    start,finish = T-7*PAST,T+7*FUTURE
    singular = [i for i in range(PAST) if (start+7*i+3)%27 == 0]
    assert singular == [5,32]
    assert (7*finish)//16-(finish+15)//16 >= 27**(PAST+FUTURE)-1
    assert start//(16*3**(2*(PAST+FUTURE))) > 100
    words = [[0]*97,[1]*97,[0,1]*48+[0],[1,0]*48+[1]]
    rng = Random(75874)
    words += [[rng.randrange(2) for _ in range(97)] for _ in range(128)]
    for w in words:
        for index in singular:
            w[index]=0
    assert len(set(witness(w) for w in words)) == len(words)
    assert PAST-len(singular)+FUTURE == 95


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run without -O.")
    audit()
    print("132 representative integer trajectories verified at the scale-74 midpoint.")
