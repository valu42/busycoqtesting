#!/usr/bin/env python3
"""A mixed ordinary-ancestor certificate and its forward-closure size limit."""
from dataclasses import dataclass

from check_bb33 import champion_step
from coarse_reconstruction_758 import inverse_word
from entry_transport_758 import MAX_H, MIN_MASS, MAX_MASS, accepts
from wider_even_entry_758 import FAR, H, MAX_CALLS, NEAR, TRIM


def state(h, u):
    return 2*h-1, u-h+1


def physical(h, u):
    return isinstance(h, int) and isinstance(u, int) and 1 <= h <= u and (u-h)%2 == 0


def jump_ancestors(h, u, budget):
    """All positive ordinary J ancestors, including the supplied state."""
    for calls in range(budget+1):
        if not physical(h, u) or u < MIN_MASS:
            return
        yield h, u, calls
        if h%3:
            return
        h, u = h//3, u-2


def pair_ancestors(h, u):
    """Exact two-bulk predecessors; siblings share h and differ in u by two."""
    z = 4*h+5*u
    if z%9 == 5:
        previous_h, gains = (z-5)//9, (5, 7)
    elif z%9 == 2:
        previous_h, gains = (z-11)//9, (7, 9)
    else:
        return
    for gain in gains:
        previous_u = u-gain
        if not physical(previous_h, previous_u):
            continue
        current = state(previous_h, previous_u)
        for _ in range(2):
            a, c = current
            if not c%2 or a < 4*((c+1)//4)+3:
                break
            current = champion_step(a, c)
            assert current is not None
        else:
            assert current == state(h, u)
            yield previous_h, previous_u


@dataclass(frozen=True)
class Witness:
    h: int
    u: int
    word: str


def find_entry_ancestor(h, u):
    """Find an accepted source with forward word J^j, or J^j LL J^i.

    None means only that this restricted mixed-ancestor test is inconclusive.
    No assumption about which ancestor blank actually followed is needed.
    """
    if not physical(h, u) or h < 2 or not MIN_MASS <= u <= MAX_MASS+TRIM:
        return None
    for middle_h, middle_u, i in jump_ancestors(h, u, MAX_CALLS):
        if accepts(middle_h, middle_u):
            return Witness(middle_h, middle_u, 'J'*i)
        if middle_h == 1 or i+2 > MAX_CALLS:
            continue
        for previous_h, previous_u in pair_ancestors(middle_h, middle_u):
            for source_h, source_u, j in jump_ancestors(previous_h, previous_u, MAX_CALLS-i-2):
                if accepts(source_h, source_u):
                    return Witness(source_h, source_u, 'J'*j+'LL'+'J'*i)
    return None


def replay(witness, target):
    assert accepts(witness.h, witness.u)
    current = state(witness.h, witness.u)
    for letter in witness.word:
        a, c = current
        assert (a%2 and c%2 and a <= c) if letter == 'J' else (
            c%2 and a >= 4*((c+1)//4)+3)
        current = champion_step(a, c)
        assert current is not None and current[0] != 1
    assert current == state(*target)


def closure_cap():
    """Upper bound at any one odd/odd mass slice, even after later resets."""
    source_masses = TRIM//2+1
    basin_seeds = FAR-NEAR+1
    return source_masses*(MAX_H//2)+basin_seeds


def verify():
    # Check the simplified paired inverse against the independent existing
    # elementary-word inverse, including small guard boundaries.
    checked = 0
    for u in range(1, 100):
        for h in range(1+((u-1)%2), u+1, 2):
            expected = inverse_word(state(h, u), 'LL', physical=True)
            actual = {state(a, b) for a, b in pair_ancestors(h, u)}
            assert actual == expected
            checked += 1

    source_u = MIN_MASS+MIN_MASS%2+1000
    current = state(2, source_u)
    for _ in range(291):
        assert current[0] <= current[1]
        current = champion_step(*current)
    for _ in range(2):
        assert current[0] >= 4*((current[1]+1)//4)+3
        current = champion_step(*current)
    h, u = (current[0]+1)//2, (current[0]+2*current[1]-1)//2
    assert h%2 == 1 and h%3 != 0 and len(str(h)) == 139
    assert h > MAX_H and u-source_u == 589
    witness = find_entry_ancestor(h, u)
    assert witness is not None and witness.word.endswith('LL')
    assert set(witness.word[:-2]) == {'J'}
    replay(witness, (h, u))
    replay(Witness(2, source_u, 'J'*291+'LL'), (h, u))
    for remaining in range(1, MAX_CALLS-len(witness.word)+1):
        current = champion_step(*current)
        assert current is not None
        if current[0] == 1:
            assert H-FAR <= current[1] <= H-NEAR
            break
    else:
        raise AssertionError('witness exceeded its inherited return bound')

    cap = closure_cap()
    assert TRIM == 2488 and TRIM//2+1 == 1245
    assert cap == 43_246_096_003_749_008_708_341_883_613_946_558_761
    assert cap*10**102 < 5*((MIN_MASS+1)//2)
    print(f'Paired inverse agrees at {checked:,} small physical states.')
    print(f'Mixed ancestor certifies a 139-digit primitive h; its remaining return takes {remaining} calls.')
    print(f'Forward descendants occupy at most {cap:,} states at any one slice u >= H-F, '
          'less than 5e-102 of that slice.')


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run without -O for verification.')
    verify()
