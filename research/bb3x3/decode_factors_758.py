#!/usr/bin/env python3
"""Recover the central odd/odd state from its mass and two fine ordinary words."""
from check_bb33 import HALTING_TARGET, champion_step
from excursion_power_758 import J, PAIRS, period_data, segments


def coefficients(word):
    # period_data also computes the closed-orbit line, requiring a nonempty word.
    return period_data(word)[:5] if word else (0, 1, 0, 0, 1)


def decode(u, past, future):
    """Yield physical central d values for the given ordinary block history."""
    pv,pq,pa,pc,pm = coefficients(past)
    fv,fq,fa,fc,fm = coefficients(future)
    before_u = u-pv
    if before_u < 1:
        return
    # The past restricts d modulo pq, the future modulo fm.
    left = ((pa*before_u+pc)*pow(pm,-1,pq)) % pq
    right = ((-fa*u-fc)*pow(fq,-1,fm)) % fm
    stride = pq*fm
    residue = (left + pq*((right-left)*pow(pq,-1,fm) % fm)) % stride
    low = max(0, -((fa*u+fc)//fq))
    high = min((u-1)//2, (fm*((u+fv-1)//2)-fa*u-fc)//fq)
    for d in range(low+(residue-low)%stride, high+1, stride):
        before_d, remainder = divmod(pm*d-pa*before_u-pc,pq)
        assert remainder == 0
        a,c = 2*before_u-4*before_d-1, 2*before_d+1
        if min(a,c) < 1:
            continue
        for symbol in (*past,*future):
            if symbol == J:
                if a % 2 != 1 or c % 2 != 1 or a > c:
                    break
                a,c = champion_step(a,c)
            else:
                if (c-1)//2 % 4 != symbol:
                    break
                for _ in range(2):
                    if a < 4*((c+1)//4)+3:
                        break
                    a,c = champion_step(a,c)
                else:
                    continue
                break
        else:
            yield d


def check_launch(seed, size):
    for word, states, _ in segments(seed):
        if sum(1 if symbol == J else 2 for symbol in word) >= size:
            break
    else:
        raise AssertionError("no sufficiently long ordinary segment")
    # Use the shortest suffix with at least the requested number of calls.
    start = len(word)
    calls = 0
    while calls < size:
        start -= 1
        calls += 1 if word[start] == J else 2
    assert 2*3**calls > states[-1][0]
    assert any(symbol != J for symbol in word[start:])
    for split in range(start,len(word)+1):
        u, d = states[split]
        assert list(decode(u,word[start:split],word[split:])) == [d]
    return calls, len(word)-start+1


def forced_code(u, d):
    """One formal block consistent with both infinite inverse representations."""
    assert u >= 8 and -3 <= d and 2*d+1 <= u
    jump = 3*d-u+1
    residue = d%4
    v,b = PAIRS[residue]
    pair = (9*d+b)//4
    allow_jump = jump >= -3
    allow_pair = 2*pair+1 <= u+v
    assert not (allow_jump and allow_pair)
    if allow_jump:
        return J, u+2, jump
    if allow_pair:
        return residue, u+v, pair
    return None


def inverse_obstruction(seed):
    a, c = (1,seed) if seed%2 else champion_step(1,seed)
    u, d = (a+2*c-1)//2,(c-1)//2
    count = 0
    while True:
        move = forced_code(u,d)
        if move is None:
            assert a-c >= 8
            a,c = champion_step(a,c)
            assert a % 2 == 0 and a <= c and champion_step(a,c)[0] == 1
            return count
        symbol,u,d = move
        assert d >= 0  # true on these two actual prefixes
        if symbol == J:
            assert a <= c
            a,c = champion_step(a,c)
        else:
            for _ in range(2):
                assert a >= 4*((c+1)//4)+3
                a,c = champion_step(a,c)
        assert (a,c) == (2*u-4*d-1,2*d+1)
        count += 1


def check_negative_branches():
    results = []
    for d in range(-7,0):
        v,b = PAIRS[d%4]
        results.append((9*d+b)//4)
    assert results == [-7,-7,-4,-4,2,2,5]
    for c in range(3,1000,4):
        a = c+2
        u = (a+2*c-1)//2
        # The smallest E input has u=5; the same direct identity holds there.
        actual = champion_step(a,c)
        for _ in range(2):
            actual = champion_step(*actual)
        formal_u,formal_d = u+2,-1
        v,b = PAIRS[formal_d%4]
        formal_u,formal_d = formal_u+v,(9*formal_d+b)//4
        assert actual == (2*formal_u-4*formal_d-1,2*formal_d+1)


def verify():
    blank = 3_706_040_377_703_662
    scale74 = HALTING_TARGET - 10**10*3**74 + 698
    checked = check_launch(blank,33),check_launch(scale74,292)
    check_negative_branches()
    assert (inverse_obstruction(blank),inverse_obstruction(scale74)) == (72,490)
    for u,k in ((blank+4,40),(scale74,391)):
        assert 21*9**k <= u*4**k and u*4**(k+1) < 21*9**(k+1)
    assert 2*3**292 > HALTING_TARGET
    near = 3_706_040_379_353_000
    for bound, normalized, deviations in ((HALTING_TARGET,792,816),(near,89,113)):
        assert 3**normalized > (bound+14)*2**normalized
        assert 3**deviations > 16_384*(bound+14)*2**deviations
    print("Recovered every split of (calls, cuts) at blank and scale 74:", checked)


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run without -O for verification.")
    verify()
