"""Upper bound for joint ordinary past and future at the scale-10 mass cut."""
from bisect import bisect_left
from functools import cache

from after_fourth_758 import CHECKPOINT
from check_bb33 import HALTING_TARGET as H, champion_step

NEAR = 543_249_654_390_404
FAR = 905_416_090_650_670
CENTER = H - (FAR+NEAR)//2
PAST = 12
PAIR = ((5,20), (9,35), (7,26), (7,29))
# At a short terminal interval, round the number of consecutive integers up
# to one of these sizes before looking up its maximum allowed population.
SIZES = tuple(range(8,65,4)) + (72,80,96,112,128,160,192,224,256,320,384,
                                  448,512,640,768,896,1024,1280,1536,1792,2048)


@cache
def past_residues(calls, mass, crossing_offset=-1):
    """Projected residue classes after at least 'calls' ordinary elementary calls."""
    if calls < 2:
        assert crossing_offset == -1
    if calls == 0:
        return {0,1,2}
    if calls == 1:
        return {x for x in range(9) if (x+mass)%3 == 0 or x in (2,5)}
    modulus = 3**(calls+1)
    residues = set()
    if 2 > crossing_offset:
        residues.update((3*old-mass+3) % modulus for old in past_residues(calls-1,mass-2))
    inverse = pow(4,-1,modulus)
    for gain,offset in PAIR:
        if gain <= crossing_offset:
            continue
        residues.update(((9*old+offset)*inverse) % modulus
                        for old in past_residues(calls-2,mass-gain))
    return residues


def maximum_hits(residues, modulus, length):
    """Most elements of a periodic set in any 'length' consecutive integers."""
    assert 0 < length < modulus
    twice = residues + [r+modulus for r in residues]
    right = best = 0
    for i,left in enumerate(residues):
        while twice[right] < left+length:
            right += 1
        best = max(best,right-i)
    return best


def upper_bound(mass, maxima):
    # After j jumps and p pairs the interval has diameter at most this rational
    # width plus 7. Hence any such interval contains at most floor(width)+8
    # consecutive integers. Each child extends the predicted future by one block.
    @cache
    def count(jumps,pairs):
        width = (mass*4**pairs) // (2*3**(jumps+2*pairs))
        length = width+8
        if width == 0:
            return maxima[0]
        deeper = count(jumps+1,pairs) + count(jumps,pairs+1)
        idx = bisect_left(SIZES,length)
        return min(maxima[idx],deeper) if idx < len(SIZES) else deeper

    return count(0,0)


def prescribed_history(calls):
    """A word of complete blocks with this total cost fixes d mod 3**calls."""
    modulus = 3**calls
    @cache
    def count(jumps,pairs):
        den = 2*3**(jumps+2*pairs)
        maximum = 1 + ((CENTER+8)*4**pairs+7*den)//(den*modulus)
        if maximum == 1 or jumps+pairs == 399:
            return maximum
        return min(maximum,count(jumps+1,pairs)+count(jumps,pairs+1))
    # This many members of each individual residue class have physical ancestors.
    margin = 100*modulus
    denominator = ((CENTER-1)//2-2*margin+1)//modulus
    return count(0,0),denominator


def audit_backwards():
    # Enumerate literal forward paths, respecting actual guards, and check that
    # every suffix through six elementary calls occurs in the projected classes.
    for initial_mass in range(21,100):
        for initial_d in range((initial_mass-1)//2+1):
            u,d = initial_mass,initial_d
            past = 0
            for _ in range(18):
                a,c = 2*u-4*d-1,2*d+1
                if a <= c:
                    next_state = champion_step(a,c)
                    cost = 1
                else:
                    after = champion_step(a,c)
                    if after is None or after[1] == 1 or after[0] <= after[1]:
                        break
                    next_state = champion_step(*after)
                    cost = 2
                if next_state is None or min(next_state) < 1:
                    break
                a,c = next_state
                if not(a%2 and c%2) or a == 1:
                    break
                u,d = (a+2*c-1)//2,(c-1)//2
                past += cost
                for n in range(1,min(6,past)+1):
                    assert d % 3**(n+1) in past_residues(n,u)


def verify():
    audit_backwards()
    # The unique launch at this mass with 33 ordinary jumps is reached from blank.
    launch = champion_step(1,CHECKPOINT)
    assert launch == (3,CHECKPOINT+3)
    u = CHECKPOINT+4
    assert u%2 == 0 and (u+66)//3**33 == 3
    for _ in range(33):
        a,c = launch
        assert a%2 and c%2 and a <= c
        launch = champion_step(a,c)
    assert launch[0] > launch[1]
    # At most 399 complete future blocks are needed before width < 1 everywhere.
    assert (CENTER+8)*4**399 < 2*9**399
    # The interior includes the whole test and the established E→reset distance.
    assert 2*((FAR-NEAR)//2) > 9*(2*399+PAST+4)+5458
    total_decrement,right = 0,1
    for _ in range(785):
        bulk_q = (right+1)//4
        total_decrement += 4*bulk_q+3
        right = 6*bulk_q+5
    assert total_decrement-6 <= 2*(H-FAR)+1 <= 2*(H-NEAR)+1 <= total_decrement+right-6
    total = physical = with_past = 0
    modulus = 3**(PAST+1)
    margin = 100*3**(PAST+1)
    for offset in range(9):
        u = CENTER+offset
        allowed = sorted(past_residues(PAST,u,offset))
        maxima = [maximum_hits(allowed,modulus,n) for n in SIZES]
        bound = upper_bound(u,maxima)
        total += bound
        physical += (u+1)//2
        # Every compatible residue with both physical margins >= margin has
        # an actual past. Count full periods contained in that interior.
        inside = (u-1)//2-2*margin+1
        with_past += len(allowed)*(inside//modulus)
        print(f'u = CENTER+{offset}: {len(allowed)} classes, upper bound {bound}')
    print(f'Combined upper bound {total} of {physical} integer cut states.')
    print(f'Fraction below {(10**42*total)//physical+1} / 10^42.')
    print(f'At least {with_past} have the required finite physical past.')
    print(f'Fraction among these below {(10**42*total)//with_past+1} / 10^42.')
    assert total*10**42 < 12_826*physical
    assert total*10**42 < 554_393*with_past
    for calls,top,scale in ((0,1581,10**40), (100,4678,10**28),
                            (200,2966,10**15), (250,7032,10**9), (285,256,1000)):
        upper,lower = prescribed_history(calls)
        assert lower > 0 and upper*scale < top*lower
        print(f'{calls} prescribed calls: {upper} possible survivors / '
              f'at least {lower} compatible states.')
    return total,physical,with_past


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run Python with assertions enabled.')
    verify()
