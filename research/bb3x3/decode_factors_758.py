#!/usr/bin/env python3
"""Recover the central odd/odd state from its mass and two fine ordinary words."""
from fractions import Fraction
from itertools import product

from check_bb33 import HALTING_TARGET, champion_step
from excursion_power_758 import J, PAIRS, period_data, segments


def coefficients(word):
    # period_data also computes the closed-orbit line, requiring a nonempty word.
    return period_data(word)[:5] if word else (0, 1, 0, 0, 1)


def reset_residue(word, initial_h):
    """Formal integral reset-origin masses; this does not check physical guards."""
    assert initial_h in (1, 2)
    _, q, a, c, m = coefficients(word)
    modulus = 2*m
    denominator = q+2*a
    assert denominator % 2 == 1
    residue = ((initial_h*q-2*c)*pow(denominator, -1, modulus)) % modulus
    return residue, modulus


def check_reset_residues():
    """Finite congruences and fine-lift partitions, with independent rational replay."""
    partitions = {}
    count = 0
    for length in range(5):
        for word in product(range(5), repeat=length):
            v, q, a, c, m = coefficients(word)
            coarse = tuple(symbol == J for symbol in word)
            # Independently sum the finite inverse representation.
            alpha, beta, weight, gain = Fraction(0), Fraction(0), Fraction(1), 0
            for symbol in word:
                if symbol == J:
                    alpha += weight/3
                    beta += weight*(gain-1)/3
                    weight /= 3
                    gain += 2
                else:
                    dv, offset = PAIRS[symbol]
                    beta -= weight*offset/9
                    weight *= Fraction(4, 9)
                    gain += dv
            assert (alpha, beta, weight, gain) == (
                Fraction(-a, q), Fraction(-c, q), Fraction(m, q), v)

            for initial_h in (1, 2):
                residue, modulus = reset_residue(word, initial_h)
                rational_residue = (initial_h+2*beta)/(1-2*alpha)
                assert rational_residue.denominator % 2 == 1
                assert residue == (rational_residue.numerator *
                                   pow(rational_residue.denominator, -1, modulus)) % modulus
                key = coarse, initial_h
                if key not in partitions:
                    partitions[key] = modulus, set()
                previous_modulus, classes = partitions[key]
                assert previous_modulus == modulus and residue not in classes
                classes.add(residue)

                # Include accepted representatives, a period translate, and failures.
                samples = {initial_h, initial_h+12, residue, residue+modulus,
                           residue+1, residue+2}
                for initial_u in samples:
                    u, d = initial_u, Fraction(initial_u-initial_h, 2)
                    all_integral = d.denominator == 1
                    for symbol in word:
                        previous_d = d
                        if symbol == J:
                            u, d = u+2, 3*d-u+1
                        else:
                            dv, offset = PAIRS[symbol]
                            u, d = u+dv, (9*d+offset)/4
                            if all_integral and d.denominator == 1:
                                assert previous_d % 4 == symbol
                        all_integral = all_integral and d.denominator == 1
                    assert u == initial_u+v
                    assert d == Fraction((q+2*a)*initial_u-initial_h*q+2*c, 2*m)
                    assert (d.denominator == 1) == all_integral
                    assert all_integral == (initial_u % modulus == residue)
                count += 1
    for (_, initial_h), (modulus, classes) in partitions.items():
        assert classes == set(range(initial_h % 2, modulus, 2))
    assert count == 2*sum(5**length for length in range(5)) == 1562
    return count, len(partitions)


def check_strategy_obstructions():
    """Audit the exact constants and finite counterexamples in PROOF_STRATEGY."""
    assert (HALTING_TARGET+588)*4**390 < 162*9**390
    assert 293+2*390 == 1073 and (9*1073)//2 == 4828

    def expected_step(a, c, symbol):
        if symbol == "I":
            assert a % 2 == 1 and c % 2 == 0 and a <= c
        elif symbol == "J":
            assert a % 2 == c % 2 == 1 and a <= c
        elif symbol == "L":
            assert c % 2 == 1 and a >= 4*((c+1)//4)+3
        else:
            assert symbol == "R" and a % 2 == 0 and c % 2 == 1 and a <= c
        result = champion_step(a, c)
        assert result is not None
        return result

    word = "I"+"J"*5+"L"*5+"R"
    for seed, end in ((524, 561), (526, 557)):
        a, c = 1, seed
        for index, symbol in enumerate(word):
            a, c = expected_step(a, c, symbol)
            assert (a == 1) == (index == len(word)-1)
        assert c == end

    for k in (6, 7, 8, 20, 36, 291):
        z = 3**(k-4)
        seed = 145*z-2*k
        assert seed > 0 and seed % 2 == 1
        a, c = 1, seed
        for _ in range(k):
            a, c = expected_step(a, c, "J")
            assert a > 1
        assert ((a+1)//2, (a+2*c-1)//2) == (81*z, 145*z)
        assert a > c  # These are exactly the opening jumps.
        assert (c-1)//2 == 32*z and ((c-1)//2) % 4 == 0
        for _ in range(2):
            a, c = expected_step(a, c, "L")
        assert ((a+1)//2, (a+2*c-1)//2) == (z-5, 145*z+5)
        for _ in range(4):
            a, c = expected_step(a, c, "J")
        h, u = (a+1)//2, (a+2*c-1)//2
        assert (h, u) == (81*z-405, 145*z+13)
        assert 145*h-81*u == -59778

    seed = 145*3**32-72  # k=36: verify the first return, not only its prefix.
    a, c = 1, seed
    for count in range(1, 81):
        result = champion_step(a, c)
        assert result is not None
        a, c = result
        assert (a == 1) == (count == 80)
    assert c == seed+182


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
    residues = check_reset_residues()
    check_strategy_obstructions()
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
    print("Checked reset residues and complete fine-lift partitions:", residues)


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run without -O for verification.")
    verify()
