"""Count left coordinates with a mass-uniform physical return test at the target."""
from functools import cache

from check_bb33 import champion_step
from nonreset_entry_758 import FAR, MAX_CALLS, MAX_GAIN, MAX_MASS, MIN_MASS
from target_shadow_758 import D, POWER

MARGIN = FAR+2600
GUARDS = ((0,1),(1,3),(5,9),(1,1))


def predict(h):
    """Return the elementary J/L word before LR, or None for an inconclusive test."""
    n,q,triple = D*h,POWER,1
    j=p=0
    word=[]
    while j+2*p+2 <= MAX_CALLS and 2*j+9*p+7 <= MAX_GAIN:
        if any(abs(z*n-b*q) <= z*triple*D*MARGIN for b,z in GUARDS):
            return None
        if 3*n < q:
            n *= 3
            triple *= 3
            j += 1
            word.append('J')
        elif 9*n > 5*q:
            n,q = 9*n-5*q,4*q
            triple *= 9
            p += 1
            word.append('LL')
        else:
            return ''.join(word)
    return None


@cache
def covering_count(j,p):
    # For integer h = 1,5 (mod 6) an interval of diameter d contains
    # at most floor(d/3)+2 candidates. Its center is immaterial.
    width = (POWER*4**p)//(D*3**(j+2*p))
    coarse = (width+2*MARGIN)//3+2
    if width <= MARGIN or j+2*p+2 > MAX_CALLS or 2*j+9*p+7 > MAX_GAIN:
        return coarse
    return min(coarse,covering_count(j+1,p)+covering_count(j,p+1))


def main():
    size = (MIN_MASS+5)//6 + (MIN_MASS+1)//6
    bad = covering_count(0,0)
    assert 0 < bad*10**35 < 1872*size
    print(f'{bad} possible unresolved odd primitive h out of {size}.')
    print(f'Unresolved fraction <= {bad/size:.9g}.')
    # Probe physical words at both edges of the mass interval. This also
    # checks the direction convention and the allowance for the final LR.
    seen = set()
    for i in range(1,400,2):
        h = (i*MIN_MASS//400)|1
        if h%3==0: continue
        word = predict(h)
        if word is None: continue
        seen.add(len(word))
        for u in (MIN_MASS+(MIN_MASS%2==0),MAX_MASS-(MAX_MASS%2==0)):
            a,c=2*h-1,u-h+1
            for symbol in word+'LR':
                assert a>1 and c>0
                if symbol=='J':
                    assert a%2 and c%2 and a<=c
                elif symbol=='L':
                    assert a>=4*((c+1)//4)+3
                else:
                    assert not a%2 and a<=c
                a,c=champion_step(a,c)
            assert a==1 and 0 < c-u <= MAX_GAIN
    assert len(seen)>=10


if __name__ == '__main__':
    main()
