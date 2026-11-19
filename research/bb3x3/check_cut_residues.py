"""Check the two-sided 98-copy witness at the #758 central mass."""
from check_bb33 import HALTING_TARGET, champion_step


CUT = HALTING_TARGET - 10_000_000


def numerator(u):
    return 92*u - 900


def candidate_scalars(h, j):
    mass = CUT + 7*j
    growth = 27**(h+j)
    low = -(numerator(mass) // growth)
    high = (529*(mass//2) - numerator(mass)) // growth
    residue = -numerator(CUT) * pow(27**h * 4**j, -1, 529) % 529
    return range(low + (residue-low) % 529, high+1, 529)


def audit(h, j, v):
    u = CUT - 7*h
    d, rem = divmod(numerator(u) + 4**(h+j)*v, 529)
    assert rem == 0
    for index in range(h+j):
        if index == h:
            assert u == CUT and 529*d - numerator(u) == 27**h * 4**j * v
        a, c = 2*u - 4*d - 1, 2*d + 1
        for _ in range(2):
            assert a > 1 and c % 4 == 1 and a >= c+2
            a, c = champion_step(a, c)
        assert a > 1 and a <= c and a % 2 == c % 2 == 1
        a, c = champion_step(a, c)
        u, d = u+7, (27*d - 4*u + 44)//4
        assert (a,c) == (2*u - 4*d - 1, 2*d + 1)
    assert 529*d - numerator(u) == 27**(h+j)*v


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run without -O to enable verification.")
    assert 174*(CUT+693)+900 < 27**99
    survivors = [(h, 98-h, v) for h in range(99) for v in candidate_scalars(h, 98-h)]
    assert survivors == [(h, 98-h, 12) for h in (0, 23, 46, 69, 92)]
    for h, j, v in survivors:
        audit(h, j, v)
    print("Checked 5 placements of 98 copies and the bound excluding all 99-copy paths.")
