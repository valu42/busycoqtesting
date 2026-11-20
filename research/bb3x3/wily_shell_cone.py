"""Exact inverse Wily passage near the ordinary integer tail with numerator 3."""
from functools import lru_cache

from wily_integer_map import image, inverse


@lru_cache(None)
def reference_step(b):
    """Inverse on a nonnegative numerator divisible by three, with the zero-tail flag."""
    assert b >= 0 and b % 3 == 0
    if b == 0:
        return 3, True
    if b % 8 in (1, 5):
        return b+(3 if b % 8 == 1 else -21), False
    if b % 4 == 3:
        y, singular = reference_step((b-3)//4)
        return 4*y+6, singular
    y, singular = reference_step(b//2)
    return 2*y+(-3 if b % 4 == 0 else 9), singular


def reference_cycle():
    b = 3
    orbit, contacts = [b], []
    for step in range(1, 8193):
        b, singular = reference_step(b)
        if singular:
            contacts.append(step)
        orbit.append(b)
    assert b == 3 and len(set(orbit[:-1])) == 8192
    assert (min(orbit),max(orbit),len(contacts)) == (0,94_370_751,96)
    return orbit, contacts


def flip(n):
    return n+3*(1-2*(n % 2))


def coordinates(a):
    """Encode an odd numerator as an integer odometer digit track and decorations."""
    assert a % 2 and a % 3
    n = (a-3)//2
    decorations = []
    low = 0
    while n not in (-2,-1):
        bit = n % 2
        low += bit << len(decorations)
        n = (n-3*bit)//2
        if bit:
            n = flip(n)
        zeros = 0
        while n % 2 == 0:
            zeros += 1
            n //= 2
        n = (n-3)//2
        decorations.append(zeros)
    track = low - ((1 << len(decorations)) if n == -1 else 0)
    return track, tuple(decorations)


def dilate_bits(n):
    """The binary digits of a nonnegative integer, read in base four."""
    value = 0
    for digit in format(n, "b"):
        value = 4*value + int(digit)
    return value


def numerator(track, decorations):
    high = track >> len(decorations)
    n = -2-3*dilate_bits(high) if high >= 0 else -1+3*dilate_bits(~high)
    for i in reversed(range(len(decorations))):
        bit = (track >> i) % 2
        n = (3+2*n) << decorations[i]
        n = 3*bit + 2*(flip(n) if bit else n)
    return 3+2*n


def sign_profile(a):
    """Track, essential decorations, and half-length of a finite sign excursion."""
    track, decorations = coordinates(a)
    length = len(decorations)
    while length and decorations[length-1] == 0:
        length -= 1
    decorations = decorations[:length]
    half = 1 << (length-1) if length and decorations[-1] <= 2 else 0
    return track, decorations, half


def forward_sign_escape(a):
    """First positive coefficient under H inverse, or None for perpetual negativity."""
    assert a < 0
    track, _, half = sign_profile(a)
    if track < half:
        return half-track
    return None


def positive_predecessor(a, j, orbit, contacts):
    """First positive inverse iterate of 3 + 2^j*a, for the full verified domain."""
    assert a < 0 and a % 2 and a % 3 and j >= 30
    track, decorations, half = sign_profile(a)
    previous = 2*half-1 if half and track >= 2*half else -1
    steps = track-previous
    cycles, slot = divmod(steps-1,len(contacts))
    time = cycles*8192 + contacts[slot]
    positive = numerator(previous,decorations)
    return time, orbit[contacts[slot]] + (positive << j)


def main():
    if not __debug__:
        raise SystemExit("Run without -O to enable the checks.")
    orbit, contacts = reference_cycle()
    assert [orbit[contacts[k-1]] for k in (1,2,4,8,16,32,64)] == [
        18,318,2595,96462,20988222,90835491,25138494]
    # Test every phase with both signs and both unit residues.
    for t, b in enumerate(orbit[:-1]):
        nxt, singular = reference_step(b)
        for a in (-7,-5,5,7):
            y = b + (a << 30)
            coeff = inverse(a)+3 if singular else a
            assert inverse(y) == nxt + (coeff << 30)
    for a in range(-4001,4002,2):
        if not a % 3:
            continue
        track, decorations = coordinates(a)
        assert numerator(track,decorations) == a
        assert numerator(track-1,decorations) == inverse(a)+3
        assert numerator(track+1,decorations) == image(a-3)
        track, essential, half = sign_profile(a)
        assert numerator(track,essential) == a
        assert (a > 0) == (track < 0 or half <= track < 2*half)
        if a < 0 and image(a-3) > 0:
            assert half and track == half-1
            low_width = 1+sum(2+d for d in essential[:-1])
            positive = numerator(-1,essential)
            assert positive-a == (9 + (1 << (essential[-1]+2))) << low_width
            assert 7*positive > -18*a
    assert coordinates(-7)[0] == 1
    assert forward_sign_escape(-7) is None
    for a in range(-10_001,0,2):
        if a % 3:
            positive_predecessor(a,30,orbit,contacts)
    for a in (-1,-5,-7,-13,-31,-41,-125,-361,-1031):
        assert a % 3
        for j in (30,37):
            target, p = positive_predecessor(a,j,orbit,contacts)
            y = 3+(a << j)
            for _ in range(target):
                assert y < 0
                y = inverse(y)
            assert y == p > 0
    print("Verified the 8,192-step cycle with 96 contacts and exact passage on the punctured cone at 3 mod 2^30.")


if __name__ == "__main__":
    main()
