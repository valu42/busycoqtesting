"""Integer checks for the post-bulk exclusion theorem in BULK_TERMINAL_SIEVE_758.md."""
from fractions import Fraction

from check_bb33 import champion_step
from power_boundary_758 import cut, departure
from power_gates_758 import gate_exits


def safe_depth(m, upper):
    """Minimum ordinary suffix length with delta-1 strictly below upper."""
    k = 0
    a = b = 1
    while 3*a <= upper*2*b:
        a *= 3
        b *= 2
        k += 1
    return max(0, m-1-k)


def interval_audit():
    for alpha in (Fraction(0), Fraction(1, 2)):
        for err in (-13, 2):
            for slope, offset in (((alpha+1)/3, (4*alpha+err-1)/3),
                                  *((2*alpha/3, (2*g*alpha+2*err-eta)/3)
                                    for g, eta in ((5, 7), (9, 13)))):
                assert 0 <= slope <= Fraction(1, 2) and -13 <= offset <= 2


def follow(a, c, margin=None):
    """Follow the literal odd-right counter map to its first R, E or halt."""
    bulks = 0
    while a >= 4*((c+1)//4)+3:
        x = (c+1)//4+3
        pair = champion_step(a, c)
        assert pair == (a-4*x+9, 6*x-13)
        a, c = pair
        assert (c+1)//4+3 == 3*x//2
        bulks += 1
    tail = jumps = 0
    shrink_num = shrink_den = 1
    while True:
        if margin and tail <= margin[0]:
            _, m, left_num, left_den = margin
            if a >= c:
                assert (a-c)*shrink_num > m*shrink_den
            else:
                assert (c-a)*left_den >= (1 << jumps)*left_num
        if a == 1 or (a <= c and a%2 == 0):
            return bulks, tail, 'R'
        if c < a < 4*((c+1)//4)+3:
            return bulks, tail, 'E' if champion_step(a, c) else 'halt'
        if a <= c:
            jumps += 1
        else:
            shrink_num *= 2
        shrink_den *= 3
        a, c = champion_step(a, c)
        tail += 1
        if tail > 10000:
            raise RuntimeError('increase literal orbit budget')


def main():
    interval_audit()
    for m in (20, 35, 292, 1000):
        depth = safe_depth(m, 5*m+11)
        k = 0
        while 3**k < 2*(5*m+12)*2**k:
            k += 1
        margin = m-1-k, m, 3**(m-1), 2**(m-1)
        for multiple in (1, 2):
            offsets = (s-cut(m, multiple) for s in gate_exits(m, multiple))
            rows = [follow(*departure(m, multiple, off), margin) for off in offsets]
            assert all(2*m <= n < 3*m for n, _, _ in rows)
            assert all(end == 'R' or t >= depth for _, t, end in rows)
            totals = {end: sum(e == end for _, _, e in rows)
                      for end in sorted({r[2] for r in rows})}
            print(f'm={m}, gate={multiple}, phases={len(rows)}, depth={depth}, '
                  f'max suffix={max(r[1] for r in rows)}, outcomes={totals}')
    m, distance = 292, 10**30
    upper = Fraction(2*distance + 31*m + 23, 8)
    print(f'm={m}, all odd-reset distances through {distance}: '
          f'depth={safe_depth(m, upper)}')
    for d in (0, 2, 1_934_340, distance//3*2, distance):
        seed = 3**m + d
        a, c = 1, seed
        for _ in range(m):
            a, c = champion_step(a, c)
        assert (a, c) == (2*3**m-1, d+2*m+1)
        n, tail, end = follow(a, c)
        assert m <= n < 3*m
        assert end == 'R' or tail >= safe_depth(m, upper)


if __name__ == '__main__':
    main()
