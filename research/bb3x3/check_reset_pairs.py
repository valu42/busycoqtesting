"""Check the reset-pair identities against check_bb33's original two-counter map."""
from check_bb33 import champion_step, HALTING_TARGET


def odd_pair(a, q):
    assert a % 4 == 1 and q >= 1
    lo, hi = (a, 4*q-1), (a, 4*q+1)
    while lo[0] <= lo[1]:
        lo, hi = champion_step(*lo), champion_step(*hi)
        assert hi == (lo[0], lo[1]+2)
    assert champion_step(*lo) == champion_step(*hi) is not None


def even_pair(seed):
    assert seed % 2 == 0 and seed >= 4
    a, r = champion_step(1, seed)
    n = 0
    while a <= r:
        a, r = champion_step(a, r)
        n += 1
    assert (a,r) == (4*3**n-1, seed+5-2*3**n+2*n)
    if r == 1:
        assert seed == 2*3**n-2*n-4
        return
    delta = -2 if r % 4 == 1 else 2
    sibling = champion_step(1,seed+delta)
    for _ in range(n):
        assert sibling[0] <= sibling[1]
        sibling = champion_step(*sibling)
    assert sibling == (a,r+delta)
    assert champion_step(a,r) == champion_step(*sibling) is not None


def main():
    if not __debug__:
        raise RuntimeError('run with assertions enabled')
    for a in range(1, 260, 4):
        for q in range(1, 260):
            odd_pair(a, q)
    for seed in range(4, 16_386, 2):
        even_pair(seed)
    for k in range(2, 320):
        boundary = 2*3**k - 2*k - 4
        for delta in (-2,0,2):
            if boundary + delta >= 4:
                even_pair(boundary + delta)
    for delta in range(-24,25):
        x = HALTING_TARGET + delta
        if x%2: odd_pair(1, (x+1)//4)
        else: even_pair(x)
    print('Odd cone, even reset siblings, unpaired boundaries and near-H cases passed.')


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit("Run without -O to enable verification.")
    main()
