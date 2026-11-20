"""Certificates for the ordering of signed Wily excursion endpoints."""
from wily_dihedral import IDENTITY, forest_children, invariant, raw_label
from wily_integer_map import START, image, inverse
from wily_shell_cone import reference_step


def lift(word, n):
    for letter in reversed(word):
        n = 4*n+6 if letter == "L" else 2*n+(-3 if n%2 else 9)
    return n


def reference_passage(b, coefficient, time, contact_times):
    """Check the finite contact sequence and its uniform validity for j >= 43."""
    for t in range(1,time+1):
        assert 0 <= b < 1 << 40
        b, singular = reference_step(b)
        assert singular == (t in contact_times)
        if singular:
            coefficient = inverse(coefficient)+3
        assert (coefficient > 0) == (t == time)
    assert b < 1 << 40
    return b, coefficient


def main():
    if not __debug__:
        raise SystemExit("Run without -O to enable the checks.")
    # For each j, the two inner inputs are S^j(-8) and S^j(L(S(-8))).
    assert lift("LS",-8) == -22
    assert reference_passage(3,-5,1,{1}) == (18,29)
    assert reference_passage(3,-19,5,{1,5}) == (318,253)

    # Translate those contact computations to a pair of prefixes on the
    # blank's own modular orbit. The -79 coefficient comes from L^2(S(-8)).
    assert lift("LLS",-8) == -82
    w = "SSSSLLSSSSSSSLSLSLLSSLSL"
    v = "LLLLLLLLSLSSLSLLLLLSS"
    assert len(w)+w.count("L") == 32 and len(v)+v.count("L") == 36
    left, right = lift(w,3), lift(v,3)
    assert (left,right) == (25_543_214_355,85_963_243_518)
    pleft, a = reference_passage(left,-79,4209,{1376,2398,2414,4209})
    pright, b = reference_passage(right,-19,4609,{513,4609})
    assert (pleft,a,pright,b) == (12_683_447_586,1009,350_576_705_541,253)

    modulus = 1 << 32
    x = START%modulus
    phases = {}
    while x not in phases:
        phases[x] = len(phases)
        x = image(x if x%3 else x+modulus)%modulus
    assert x == START%modulus and len(phases) == 32768
    assert [phases[n%modulus] for n in (pleft,pright,left,right)] == [
        13702,15513,17911,20122]
    assert invariant(left-(79 << 43)) == invariant(right-(19 << 51)) == IDENTITY
    assert invariant(left-(5 << 44)) == IDENTITY
    assert all(n%3 == 1 for n in (left-(79 << 43),right-(19 << 51),left-(5 << 44)))
    assert reference_passage(left,-5,1376,{1376}) == (44_897_140_755,29)
    state = 1,raw_label(-8)
    short_orbit = set()
    while state not in short_orbit:
        short_orbit.add(state)
        state = forest_children(state)[1]
    assert len(short_orbit) == 12 and state == (1,raw_label(-8))
    print("Verified crossing excursion pairs on the complete 32-bit blank cycle.")


if __name__ == "__main__":
    main()
