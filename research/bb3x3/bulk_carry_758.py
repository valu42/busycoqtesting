#!/usr/bin/env python3
"""Exact carry enclosures and sufficient L^b R passages for #758.

The certificate is conditional: None means that these inequalities did not
decide the passage. Infinite-series claims are proved in RETURN_PREFIX_758.md;
this script uses finite rational enclosures only.
"""
from fractions import Fraction
from itertools import product

from check_bb33 import champion_step


RHO = Fraction(3, 2)


def carry_prefix(e, length):
    """Formal right-counter evolution; no left-counter guard is assumed."""
    assert e >= 1 and length >= 0
    bits = []
    for _ in range(length):
        bit = e % 2
        bits.append(bit)
        e = 3*((e+bit)//2)
    return e, tuple(bits)


def psi_interval(e, precision):
    """Rational lower/upper bounds for the exact bulk-normalizing Psi(e)."""
    end, _ = carry_prefix(e, precision)
    scale = Fraction(2, 3)**precision
    return scale*end, scale*(end+3)


def certify_bulk_return(a, c, bulks, precision=8):
    """Return (seed_low, seed_high, parity) for L^b R to the first subsequent reset.

    At most min(precision, bulks) carry bits are evaluated. The interval
    contains only candidates of the returned parity. None is inconclusive.
    """
    assert a >= 1 and c >= 1 and a % 2 == c % 2 == 1
    assert bulks >= 1 and bulks % 2 == 1 and precision >= 0
    e, mass = (c+7)//2, a+2*c
    depth = min(precision, bulks)
    end, bits = carry_prefix(e, depth)
    carry_count = sum(bits)
    scale = RHO**(bulks-depth)
    lower, upper = scale*end, scale*(end+3)
    if 6*lower < mass+39+9*bulks+4*(carry_count-depth):
        return None
    if 4*upper > mass+14+5*bulks+4*carry_count:
        return None
    seed_low = (mass+5*bulks)//2+2*carry_count+2
    seed_high = seed_low+2*(bulks-depth)
    parity = ((mass+bulks)//2) % 2
    assert seed_low % 2 == seed_high % 2 == parity
    return seed_low, seed_high, parity


def carry_residue(bits):
    modulus = 2**len(bits)
    residue = -sum(bit*2**i*pow(3**i, -1, modulus)
                   for i, bit in enumerate(bits)) % modulus
    return residue, modulus


def valuation_two(value):
    assert value > 0
    return (value & -value).bit_length()-1


def verify_enclosures():
    for e in range(4, 40):
        previous_low, previous_high = psi_interval(e, 0)
        for depth in range(1, 13):
            low, high = psi_interval(e, depth)
            assert previous_low <= low < high <= previous_high
            assert high-low == 3*Fraction(2, 3)**depth
            end, bits = carry_prefix(e, depth)
            prefix = sum((bit*Fraction(2, 3)**i for i, bit in enumerate(bits)),
                         Fraction(0))
            assert low-e == prefix and end >= e
            next_e = 3*((e+e % 2)//2)
            next_bounds = psi_interval(next_e, depth-1)
            assert next_bounds == (RHO*low, RHO*high)
            previous_low, previous_high = low, high

    for length in range(9):
        modulus = 2**length
        residues = set()
        for residue in range(modulus):
            _, bits = carry_prefix(5*modulus+residue, length)
            assert carry_residue(bits) == (residue, modulus)
            residues.add(bits)
        assert len(residues) == modulus

    # Both extremes of the fixed-modulus uncertainty can be approached
    # while keeping the same residue and requiring arbitrarily large inputs.
    for modulus in (3, 8, 12, 40):
        depth = valuation_two(modulus)
        odd_part = modulus//2**depth
        for residue in (0, 1, 2):
            _, fixed_bits = carry_prefix(residue+10*modulus, depth)
            fixed_sum = sum((bit*Fraction(2, 3)**i
                             for i, bit in enumerate(fixed_bits)), Fraction(0))
            for tail_bit in (0, 1):
                bits = fixed_bits+(tail_bit,)*12
                binary_residue, binary_modulus = carry_residue(bits)
                assert (residue-binary_residue) % 2**depth == 0
                shift = (((residue-binary_residue)//2**depth) *
                         pow(binary_modulus//2**depth, -1, odd_part)) % odd_part
                e = binary_residue+binary_modulus*shift
                e += binary_modulus*odd_part*(10**6+1)
                assert e > 10**6 and e % modulus == residue % modulus
                assert carry_prefix(e, len(bits))[1] == bits
                low, high = psi_interval(e, len(bits))
                if tail_bit == 0:
                    assert low-e == fixed_sum
                else:
                    assert high-e == fixed_sum+3*Fraction(2, 3)**depth


def verify_jump_comparison():
    for e in range(4, 49):
        for h in range(1, min(e-3, 12)+1):
            other = e-h+1
            assert other >= 4
            if h == 1:
                assert other == e
                continue
            depth = valuation_two(h-1)
            left_end, left_bits = carry_prefix(e, depth)
            right_end, right_bits = carry_prefix(other, depth)
            assert left_bits == right_bits
            assert left_end-right_end == RHO**depth*(h-1)
            assert left_end % 2 != right_end % 2
            low, high = psi_interval(e, depth+8)
            other_low, other_high = psi_interval(other, depth+8)
            delta_low = other_low-other-(high-e)
            delta_high = other_high-other-(low-e)
            scale = Fraction(2, 3)**depth
            bounds = (-scale, 3*scale) if left_end % 2 == 0 else (-3*scale, scale)
            assert bounds[0] <= delta_low <= delta_high <= bounds[1]


def verify_carry_order():
    def formal(word, changed):
        a, c = Fraction(101), Fraction(11)
        for index, symbol in enumerate(word):
            if symbol == "J":
                a, c = 3*a+2, c-a+1
            else:
                bit = int(index == changed)
                a, c = a-c-2-2*bit, (3*c+7+6*bit)/2
        return a, c

    for word in product("JL", repeat=4):
        low_a, low_c = formal(word, None)
        for index, symbol in enumerate(word):
            if symbol == "L":
                high_a, high_c = formal(word, index)
                da, dc = high_a-low_a, high_c-low_c
                assert da <= -2 and dc >= 3 and da+2*dc == 4


def verify_passages():
    checked = 0
    for bulks in (1, 3, 9, 21, 101, 501):
        for e in (4, 7, 32):
            c = 2*e-7
            depth = min(4, bulks)
            end, bits = carry_prefix(e, depth)
            carries = sum(bits)
            scale = RHO**(bulks-depth)
            minimum = 4*scale*(end+3)-14-5*bulks-4*carries
            maximum = 6*scale*end-39-9*bulks-4*(carries-depth)
            low_mass = max(2*c+1, -((-minimum.numerator)//minimum.denominator))
            low_mass += 1-low_mass % 2
            high_mass = maximum.numerator//maximum.denominator
            high_mass -= 1-high_mass % 2
            if low_mass > high_mass:
                continue
            middle_mass = (low_mass+high_mass)//2
            middle_mass += 1-middle_mass % 2
            for mass in {low_mass, middle_mass, high_mass}:
                a = mass-2*c
                certificate = certify_bulk_return(a, c, bulks, precision=4)
                assert certificate is not None
                left, right = a, c
                for _ in range(bulks):
                    assert left > 1 and right % 2 == 1
                    assert left >= 4*((right+1)//4)+3
                    next_state = champion_step(left, right)
                    assert next_state is not None
                    left, right = next_state
                assert left >= 0 and left % 2 == 0 and left <= right
                final = champion_step(left, right)
                assert final is not None and final[0] == 1
                seed_low, seed_high, parity = certificate
                assert seed_low <= final[1] <= seed_high and final[1] % 2 == parity
                _, all_bits = carry_prefix(e, bulks)
                assert final[1] == (mass+5*bulks)//2+2*sum(all_bits)+2
                checked += 1
            # These are failures of the sufficient certificate, not claims
            # that the neighboring physical starts fail to return.
            if low_mass-2 > 2*c:
                assert certify_bulk_return(low_mass-2-2*c, c, bulks, 4) is None
            assert certify_bulk_return(high_mass+2-2*c, c, bulks, 4) is None
    assert checked >= 30
    return checked


def verify():
    verify_enclosures()
    verify_jump_comparison()
    verify_carry_order()
    checked = verify_passages()
    print("Verified carry congruences, enclosures, jump comparison and opposed extrema.")
    print("Certified first-return passages replayed with the original map:", checked)


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run without -O for verification.")
    verify()
