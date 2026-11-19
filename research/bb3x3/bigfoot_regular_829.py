"""Construct halting Bigfoot lengths in a pumped regular language."""
from math import gcd

from check_bb33 import bigfoot_step


def three_order(n):
    assert n > 0
    v = 0
    while n % 3 == 0:
        n //= 3
        v += 1
    return v


def segment(a, x, groups):
    """Replay at most four times groups macro-steps, stopping at the first halt."""
    b, c = 2*x+1, 2
    for steps in range(1, 4*groups+1):
        a, b, c = bigfoot_step(a, b, c)
        if a < 0:
            return steps, None
    assert b % 2 and c == 2
    return None, (a, (b-1)//2)


def halting_cylinder(a, x, precision):
    """A residue inside x mod 3^precision whose entire class halts."""
    n = (precision+3)//4
    early, end = segment(a, x, n)
    if early is not None:
        return x % 81**n, 4*n, early
    height, y = end
    m = height//2+1
    modulus = 81**m
    # Adding 81^n v to x adds 256^n v to y. The loss-by-two
    # branch repeats m times when 175*(y+256^n v)+502 = 0 mod 81^m.
    v = -(175*y+502)*pow(175*256**n, -1, modulus) % modulus
    digits = 4*(n+m)
    residue = (x+81**n*v) % 3**digits
    halt, _ = segment(a, residue, n+m)
    assert halt is not None and (residue-x) % 3**precision == 0
    return residue, digits, halt


def geometric_sum(base, n, modulus):
    """1 + base + ... + base^(n-1), reduced before exponentiation."""
    return (pow(base, n, (base-1)*modulus)-1)//(base-1)


def pump_witness(a, k, prefix, loop_size, loop, suffix_size, suffix):
    """A progression of even loop counts for which prefix loop* suffix halts."""
    assert a >= 0 and k >= 2 and gcd(k, 3) == 1 and prefix >= 1
    assert loop_size >= 1 and suffix_size >= 0
    f, tail = k**loop_size, k**suffix_size
    assert 0 <= loop < f and 0 <= suffix < tail
    x0 = prefix*tail+suffix
    stride = tail*(prefix*(f-1)+loop)*(f+1)
    v = three_order(stride)
    residue, digits, steps = halting_cylinder(a, x0, v)
    mod = 3**(digits-v)
    target = (residue-x0)//3**v * pow(stride//3**v, -1, mod) % mod
    h = 0
    precision = 1
    while precision < mod:
        next_mod = 3*precision
        candidates = [h+t*precision for t in range(3)]
        matches = [j for j in candidates if geometric_sum(f*f,j,next_mod) == target % next_mod]
        assert len(matches) == 1
        h, precision = matches[0], next_mod
    for j in (h, h+mod, h+17*mod):
        x = (x0+stride*geometric_sum(f*f,j,3**digits)) % 3**digits
        assert x == residue and segment(a, x, digits//4)[0] == steps
    return 2*h, 2*mod, steps


def simultaneous(k, completions):
    """Refine one prefix class so every listed (counter,width,suffix) halts."""
    p, t = 1, 0
    witnesses = []
    for a, d, c in completions:
        scale = k**d
        assert 0 <= c < scale
        w = three_order(scale)
        length = scale*p+c
        x, digits, halt = halting_cylinder(a, length, t+w)
        unit = scale//3**w
        new_t = digits-w
        new_p = (x-c)//3**w * pow(unit, -1, 3**new_t) % 3**new_t
        assert (new_p-p) % 3**t == 0
        p, t = new_p, new_t
        witnesses.append((digits, halt))
    for prefix in (p+3**t, p+2*3**t):
        for (a,d,c), (digits,halt) in zip(completions, witnesses):
            assert segment(a, (k**d*prefix+c) % 3**digits, digits//4)[0] == halt
    return p, t


def main():
    if not __debug__:
        raise SystemExit("Run without -O to enable the checks.")
    # 2 is a unit mod 3^8 with 2^4374 = 1 mod 3^8.
    assert pow(2, 4374, 3**8) == 1
    assert segment(2, 128, 2)[0] == 8
    for k in (2, 4, 5, 7, 8, 10, 11, 16):
        for a in (0, 2, 7):
            for w, d in ((0,1), (1,1), (k**2-1,2)):
                pump_witness(a, k, 1, d, w, 2, k+1)
    offsets = []
    for r in range(81):
        _, end = segment(10, r, 1)
        offsets.append(81*end[1]-256*r)
    assert (min(offsets),max(offsets)) == (126,518)
    for k in (2,3,6,9,10):
        simultaneous(k, [(1,1,0),(2,2,k+1),(3,3,k*k+1)])
    example = pump_witness(2, 2, 1, 1, 0, 0, 0)
    print(f'72 pump certificates verified. For x=2^j, j={example[0]} mod {example[1]} halts on macro-step {example[2]}.')
    print('The class j=7 mod 4374 halts on macro-step 8.')
    print('Simultaneous halting prefixes verified in five bases.')


if __name__ == '__main__':
    main()
